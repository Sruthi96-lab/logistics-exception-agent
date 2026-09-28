from ollama import chat

from app.memory import HindsightMemory
from app.models import Incident, AgentResponse


class LogisticsExceptionAgent:

    def __init__(self):
        self.memory = HindsightMemory()
        self.model = "llama3.2:3b"

    # =============================================
    # MAIN INCIDENT PROCESSING
    # =============================================

    def process_incident(
        self,
        incident: Incident
    ) -> AgentResponse:

        # -----------------------------------------
        # 1. Recall similar incidents
        # -----------------------------------------

        query = (
            f"Past logistics incidents for exception type "
            f"{incident.exception_type}. "
            f"Description: {incident.description}. "
            f"Location: {incident.location or 'Unknown'}."
        )

        recalled_memories = self.memory.recall_incidents(query)

        # -----------------------------------------
        # 2. Filter relevant memories
        # -----------------------------------------

        similar_incidents = self.filter_memories(
            recalled_memories,
            incident
        )

        # -----------------------------------------
        # 3. Search for successful experiences
        # -----------------------------------------

        success_query = (
            f"Past logistics incidents with documented "
            f"successful resolution and successful outcome "
            f"for {incident.exception_type}. "
            f"Resolution and successful delivery."
        )

        successful_memories = self.memory.recall_incidents(
            success_query
        )

        successful_memories = (
            self.filter_successful_memories(
                successful_memories,
                incident
            )
        )

        # -----------------------------------------
        # 4. Combine memories
        # -----------------------------------------

        combined_memories = []

        for memory in successful_memories:
            if memory not in combined_memories:
                combined_memories.append(memory)

        for memory in similar_incidents:
            if memory not in combined_memories:
                combined_memories.append(memory)

        combined_memories = combined_memories[:5]

        # -----------------------------------------
        # 5. Generate recommendation
        # -----------------------------------------

        llm_result = self.generate_llm_recommendation(
            incident,
            combined_memories,
            successful_memories
        )

        # -----------------------------------------
        # 6. Save current incident + recommendation
        # -----------------------------------------

        incident_text = (
            f"Incident ID: {incident.incident_id} | "
            f"Exception Type: {incident.exception_type} | "
            f"Description: {incident.description} | "
            f"Location: {incident.location or 'Unknown'} | "
            f"Priority: {incident.priority} | "
            f"Status: {incident.status} | "
            f"Resolution: "
            f"{incident.resolution or 'Not resolved yet'} | "
            f"Agent Recommendation: "
            f"{llm_result['recommended_action']}"
        )

        self.memory.save_incident(incident_text)

        # -----------------------------------------
        # 7. Return response
        # -----------------------------------------

        return AgentResponse(
            incident_id=incident.incident_id,
            analysis=llm_result["analysis"],
            recommended_action=llm_result["recommended_action"],
            similar_incidents=combined_memories,
        )

    # =============================================
    # GENERAL MEMORY FILTER
    # =============================================

    @staticmethod
    def filter_memories(
        memories: list[str],
        incident: Incident
    ) -> list[str]:

        filtered = []

        exception_type = incident.exception_type.lower()

        exception_keywords = {

            "vehicle breakdown": [
                "vehicle",
                "breakdown"
            ],

            "address error": [
                "address"
            ],

            "delivery delay": [
                "delay",
                "delayed"
            ],

            "damaged package": [
                "damaged",
                "package"
            ],

            "failed delivery": [
                "failed delivery",
                "delivery attempt",
                "customer unavailability"
            ]
        }

        keywords = exception_keywords.get(
            exception_type,
            []
        )

        for memory in memories:

            text = memory.strip()

            if not text:
                continue

            lower_text = text.lower()

            # -----------------------------------------
            # Never use current incident as past evidence
            # -----------------------------------------

            if incident.incident_id.lower() in lower_text:
                continue

            # -----------------------------------------
            # Same exception category
            # -----------------------------------------

            if keywords:

                if not any(
                    keyword in lower_text
                    for keyword in keywords
                ):
                    continue

            # -----------------------------------------
            # Avoid duplicates
            # -----------------------------------------

            if text in filtered:
                continue

            filtered.append(text)

            if len(filtered) >= 5:
                break

        return filtered

    # =============================================
    # SUCCESSFUL MEMORY FILTER
    # =============================================

    @staticmethod
    def filter_successful_memories(
        memories: list[str],
        incident: Incident
    ) -> list[str]:

        successful = []

        exception_type = incident.exception_type.lower()

        exception_keywords = {

            "vehicle breakdown": [
                "vehicle",
                "breakdown"
            ],

            "address error": [
                "address"
            ],

            "delivery delay": [
                "delay",
                "delayed"
            ],

            "damaged package": [
                "damaged",
                "package"
            ],

            "failed delivery": [
                "failed delivery",
                "customer unavailability",
                "delivery attempt"
            ]
        }

        keywords = exception_keywords.get(
            exception_type,
            []
        )

        for memory in memories:

            text = memory.strip()

            if not text:
                continue

            lower_text = text.lower()

            # -----------------------------------------
            # Never use current incident
            # -----------------------------------------

            if incident.incident_id.lower() in lower_text:
                continue

            # -----------------------------------------
            # Same exception type
            # -----------------------------------------

            if keywords:

                if not any(
                    keyword in lower_text
                    for keyword in keywords
                ):
                    continue

            # -----------------------------------------
            # Detect documented successful experience
            #
            # Hindsight can return memories in two forms:
            #
            # Form 1:
            # Resolution: ...
            # Outcome: ...
            #
            # Form 2:
            # resolved by ...
            # resulting in successful delivery
            # -----------------------------------------

            structured_success = (
                "resolution:" in lower_text
                and
                "outcome:" in lower_text
            )

            summarized_success = (
                "resolved by" in lower_text
                and
                (
                    "successful delivery" in lower_text
                    or
                    "successfully delivered" in lower_text
                    or
                    "successful shipment delivery"
                    in lower_text
                )
            )

            if not (
                structured_success
                or summarized_success
            ):
                continue

            # -----------------------------------------
            # Reject unresolved incidents
            # -----------------------------------------

            if "unresolved" in lower_text:
                continue

            if "remains unresolved" in lower_text:
                continue

            if "not resolved yet" in lower_text:
                continue

            # -----------------------------------------
            # Avoid duplicates
            # -----------------------------------------

            if text in successful:
                continue

            successful.append(text)

            if len(successful) >= 3:
                break

        return successful

    # =============================================
    # LLM RECOMMENDATION
    # =============================================

    def generate_llm_recommendation(
        self,
        incident: Incident,
        memories: list[str],
        successful_memories: list[str]
    ):

        # -----------------------------------------
        # Successful memories
        # -----------------------------------------

        if successful_memories:

            successful_text = "\n".join(
                f"[SUCCESSFUL EXPERIENCE {index + 1}] "
                f"{memory}"
                for index, memory
                in enumerate(
                    successful_memories[:3]
                )
            )

        else:

            successful_text = "NONE"

        # -----------------------------------------
        # Other memories
        # -----------------------------------------

        if memories:

            memories_text = "\n".join(
                f"[PAST INCIDENT {index + 1}] "
                f"{memory}"
                for index, memory
                in enumerate(
                    memories[:5]
                )
            )

        else:

            memories_text = "NONE"

        # -----------------------------------------
        # Evidence-based prompt
        # -----------------------------------------

        prompt = f"""
You are a logistics exception assistant.

CURRENT INCIDENT

Incident ID: {incident.incident_id}
Exception Type: {incident.exception_type}
Description: {incident.description}
Location: {incident.location or "Unknown"}
Priority: {incident.priority}

DOCUMENTED SUCCESSFUL EXPERIENCES

{successful_text}

OTHER RELEVANT PAST INCIDENTS

{memories_text}

IMPORTANT RULES:

1. The CURRENT INCIDENT is new.
   Do not confuse it with any past incident.

2. Only use information explicitly present
   in the provided memories.

3. A successful experience must show evidence
   that the incident was resolved AND resulted
   in successful delivery.

4. Structured memories may contain:
   "Resolution:"
   and
   "Outcome:"

5. Hindsight may summarize memories using wording
   such as:
   "resolved by ..."
   and
   "successful delivery."

6. If a successful experience exists, identify
   the action described as the resolution.

7. Do not copy an Agent Recommendation and call
   it a documented resolution.

8. Never invent a cause.

9. Never invent a resolution.

10. Never invent an outcome.

11. Never mention an incident ID that is not
    present in the evidence.

12. Do not say an action is guaranteed to succeed.

13. If there is no successful experience, say:
    "No documented successful past resolution was found."

14. Keep the response very short.

Return exactly two sections:

ANALYSIS:
State whether a documented successful experience
was found and identify the relevant past incident
if available.

RECOMMENDED ACTION:
If a successful experience exists, give the
resolution/action supported by that experience.

Otherwise say:
"Review the incident through normal logistics procedures."
"""

        try:

            response = chat(
                model=self.model,

                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a strict evidence-based "
                            "logistics assistant. "
                            "Never invent facts. "
                            "Never mix current and past incidents."
                        )
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                options={
                    "temperature": 0.0,
                    "num_predict": 120
                }
            )

            content = (
                response["message"]["content"]
                .strip()
            )

            # -----------------------------------------
            # Extract analysis
            # -----------------------------------------

            analysis = self.extract_section(
                content,
                "ANALYSIS",
                "RECOMMENDED ACTION"
            )

            # -----------------------------------------
            # Extract recommendation
            # -----------------------------------------

            recommended_action = self.extract_section(
                content,
                "RECOMMENDED ACTION",
                None
            )

            return {
                "analysis": analysis.strip(),

                "recommended_action":
                    recommended_action.strip()
            }

        except Exception as error:

            print(
                "LLM Error:",
                error
            )

            return {
                "analysis": (
                    "The local Llama model could not "
                    "complete the analysis."
                ),

                "recommended_action": (
                    "Review the incident through "
                    "normal logistics procedures."
                )
            }

    # =============================================
    # RESPONSE SECTION PARSER
    # =============================================

    @staticmethod
    def extract_section(
        text: str,
        start_marker: str,
        end_marker: str | None
    ) -> str:

        normalized = text.replace(
            "**",
            ""
        )

        start_marker = (
            start_marker
            .replace(":", "")
            .strip()
        )

        normalized = normalized.replace(
            start_marker + ":",
            start_marker
        )

        if start_marker not in normalized:
            return text.strip()

        section = normalized.split(
            start_marker,
            1
        )[1]

        if end_marker:

            end_marker = (
                end_marker
                .replace(":", "")
                .strip()
            )

            if end_marker in section:

                section = section.split(
                    end_marker,
                    1
                )[0]

        return section.strip()

    # =============================================
    # CLOSE
    # =============================================

    def close(self):
        self.memory.close()
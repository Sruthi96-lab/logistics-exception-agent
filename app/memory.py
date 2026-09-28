import os

from dotenv import load_dotenv
from hindsight_client import Hindsight


load_dotenv()


class HindsightMemory:

    def __init__(self):
        self.base_url = os.environ["HINDSIGHT_BASE_URL"]
        self.api_key = os.environ["HINDSIGHT_API_KEY"]
        self.bank_id = os.environ["HINDSIGHT_BANK_ID"]

    def _create_client(self):
        return Hindsight(
            base_url=self.base_url,
            api_key=self.api_key,
        )

    def save_incident(self, incident: str):
        """Save a logistics incident to Hindsight memory."""

        client = self._create_client()

        try:
            client.retain(
                bank_id=self.bank_id,
                content=incident,
            )
        finally:
            client.close()

    def recall_incidents(self, query: str):
        """Retrieve relevant past logistics incidents."""

        client = self._create_client()

        try:
            result = client.recall(
                bank_id=self.bank_id,
                query=query,
            )

            memories = []

            for memory in result.results:

                text = memory.text.strip()

                if not text:
                    continue

                if text not in memories:
                    memories.append(text)

                if len(memories) >= 8:
                    break

            return memories

        finally:
            client.close()

    def close(self):
        """No persistent client to close."""
        pass
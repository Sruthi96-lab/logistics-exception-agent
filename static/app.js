
const form = document.getElementById("incidentForm");

const resultSection = document.getElementById("resultSection");
const analysis = document.getElementById("analysis");
const recommendation = document.getElementById("recommendation");
const memories = document.getElementById("memories");
const loading = document.getElementById("loading");

const resolveButton = document.getElementById("resolveButton");
const resolution = document.getElementById("resolution");
const outcome = document.getElementById("outcome");
const resolveSuccess = document.getElementById("resolveSuccess");

let currentIncidentId = null;
let currentExceptionType = null;


// =========================================
// ANALYZE INCIDENT
// =========================================

form.addEventListener("submit", async function (event) {

    // Prevent normal form submission/page refresh
    event.preventDefault();

    console.log("Analyze button clicked");

    resultSection.classList.add("hidden");
    resolveSuccess.classList.add("hidden");
    loading.classList.remove("hidden");


    const incident = {

        incident_id:
            document.getElementById("incident_id").value.trim(),

        exception_type:
            document.getElementById("exception_type").value,

        description:
            document.getElementById("description").value.trim(),

        location:
            document.getElementById("location").value.trim() || null,

        priority:
            document.getElementById("priority").value,

        status: "Open",

        resolution: null
    };


    // Store current incident information
    currentIncidentId = incident.incident_id;
    currentExceptionType = incident.exception_type;


    try {

        const response = await fetch(
            "/api/incident",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(incident)
            }
        );


        if (!response.ok) {

            const errorText = await response.text();

            throw new Error(
                errorText || "Server returned an error."
            );
        }


        const data = await response.json();


        // -----------------------------------------
        // Show AI analysis
        // -----------------------------------------

        analysis.textContent = data.analysis;


        // -----------------------------------------
        // Show recommendation
        // -----------------------------------------

        recommendation.textContent =
            data.recommended_action;


        // -----------------------------------------
        // Show similar incidents
        // -----------------------------------------

        memories.innerHTML = "";


        if (
            !data.similar_incidents ||
            data.similar_incidents.length === 0
        ) {

            memories.innerHTML =
                "<p>No similar past incidents found.</p>";

        } else {

            data.similar_incidents.forEach(
                function (memory) {

                    const div =
                        document.createElement("div");

                    div.className = "memory-item";

                    div.textContent = memory;

                    memories.appendChild(div);
                }
            );
        }


        // -----------------------------------------
        // Reset resolution fields
        // -----------------------------------------

        resolution.value = "";
        outcome.value = "";

        resolveButton.disabled = false;

        resolveButton.textContent =
            "Save Resolution & Learn";


        // -----------------------------------------
        // Show result section
        // -----------------------------------------

        resultSection.classList.remove("hidden");


    } catch (error) {

        console.error("Analyze error:", error);

        alert(
            "Unable to analyze the incident.\n\n" +
            error.message
        );

    } finally {

        loading.classList.add("hidden");
    }

});


// =========================================
// RESOLVE INCIDENT
// =========================================

resolveButton.addEventListener(
    "click",
    async function () {

        if (!currentIncidentId) {

            alert(
                "Please analyze an incident first."
            );

            return;
        }


        if (!currentExceptionType) {

            alert(
                "Exception type is missing. Please analyze the incident again."
            );

            return;
        }


        const resolutionText =
            resolution.value.trim();

        const outcomeText =
            outcome.value.trim();


        if (!resolutionText) {

            alert(
                "Please enter the resolution."
            );

            return;
        }


        if (!outcomeText) {

            alert(
                "Please enter the outcome."
            );

            return;
        }


        resolveButton.disabled = true;

        resolveButton.textContent =
            "Saving to Hindsight...";


        try {

            const response = await fetch(
                "/api/incident/resolve",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        incident_id:
                            currentIncidentId,

                        exception_type:
                            currentExceptionType,

                        resolution:
                            resolutionText,

                        outcome:
                            outcomeText
                    })
                }
            );


            if (!response.ok) {

                const errorText =
                    await response.text();

                throw new Error(
                    errorText ||
                    "Unable to resolve incident."
                );
            }


            const data =
                await response.json();


            resolveSuccess.textContent =
                "✓ " + data.message;


            resolveSuccess.classList.remove(
                "hidden"
            );


            resolveButton.textContent =
                "Saved to Hindsight ✓";


        } catch (error) {

            console.error(
                "Resolve error:",
                error
            );

            alert(
                "Unable to save resolution.\n\n" +
                error.message
            );


            resolveButton.disabled = false;

            resolveButton.textContent =
                "Save Resolution & Learn";
        }

    }
);


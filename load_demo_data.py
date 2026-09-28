import json
from app.memory import HindsightMemory

def main():
    with open("data/sample_incidents.json", "r", encoding="utf-8") as file:
        incidents = json.load(file)

    memory = HindsightMemory()

    print("\nLoading demo incidents into Hindsight...\n")

    for incident in incidents:
        memory_text = (
            f"Incident {incident['incident_id']}: "
            f"Exception type: {incident['exception_type']}. "
            f"Description: {incident['description']}. "
            f"Location: {incident['location']}. "
            f"Priority: {incident['priority']}. "
            f"Resolution: {incident['resolution']}. "
            f"Outcome: {incident['outcome']}."
        )

        memory.save_incident(memory_text)

        print(
            f"✓ Loaded {incident['incident_id']} "
            f"— {incident['exception_type']}"
        )

    memory.close()

    print("\nAll demo incidents loaded successfully.")
    print("Hindsight is ready for multi-scenario testing.\n")

if __name__ == "__main__":
    main()

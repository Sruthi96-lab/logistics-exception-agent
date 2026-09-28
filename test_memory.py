from app.memory import HindsightMemory


memory = HindsightMemory()

try:
    memory.save_incident(
        "Incident INC-002: A shipment was delayed because the "
        "delivery vehicle broke down. The logistics team assigned "
        "another vehicle and the shipment was delivered successfully."
    )

    print("Incident saved successfully.")

    results = memory.recall_incidents(
        "What happened when a delivery vehicle broke down?"
    )

    print("\nRelevant past incidents:")

    for result in results:
        print("-", result)

finally:
    memory.close()
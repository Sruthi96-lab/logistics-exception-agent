import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

client = Hindsight(
    base_url=os.environ["HINDSIGHT_BASE_URL"],
    api_key=os.environ["HINDSIGHT_API_KEY"],
)

bank_id = os.environ["HINDSIGHT_BANK_ID"]

try:
    # Save one sample delivery incident
    client.retain(
        bank_id=bank_id,
        content=(
            "Incident INC-001: A delivery was delayed because the "
            "customer's house number was incorrect. The support team "
            "contacted the customer, corrected the address, and the "
            "package was delivered successfully."
        ),
    )
    print("Memory saved.")

    # Search for that incident
    result = client.recall(
        bank_id=bank_id,
        query="What resolved the delivery delay caused by an incorrect address?",
    )

    print("\nRetrieved memories:")
    for memory in result.results:
        print("-", memory.text)

finally:
    client.close()
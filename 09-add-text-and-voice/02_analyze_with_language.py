"""
Demo 4: Protect personal data with Azure Language.

- Connects to Azure Language in Foundry Tools with the Text Analytics client
- Uses the Foundry resource endpoint and keyless sign-in
- Redacts personal information (PII) in each ticket
- Labels entities, with a category and confidence score for each
"""
from azure.identity import DefaultAzureCredential
from azure.ai.textanalytics import TextAnalyticsClient

from common import LANGUAGE_ENDPOINT, load_tickets

# 1. Same keyless sign-in, different client. Azure Language uses the
#    resource endpoint, not the project endpoint.
client = TextAnalyticsClient(endpoint=LANGUAGE_ENDPOINT, credential=DefaultAzureCredential())

tickets = load_tickets()

# 2. PII detection: returns the redacted text plus each item it found.
pii_results = client.recognize_pii_entities(tickets)

# 3. Named entity recognition: people, places, products, dates, and more.
entity_results = client.recognize_entities(tickets)

for number, (pii, entities) in enumerate(zip(pii_results, entity_results), start=1):
    print(f"Ticket {number}")
    if pii.is_error or entities.is_error:
        print(f"  Error: {pii.error if pii.is_error else entities.error}\n")
        continue

    print(f"  Redacted: {pii.redacted_text}")
    for item in pii.entities:
        print(f"    PII: {item.text} ({item.category}, {item.confidence_score:.2f})")

    print("  Entities:")
    for item in entities.entities:
        category = item.category + (f"/{item.subcategory}" if item.subcategory else "")
        print(f"    {item.text} ({category}, {item.confidence_score:.2f})")
    print()

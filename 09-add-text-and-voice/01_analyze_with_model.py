"""
Demo 3: Analyze tickets with a model.

- Same connection as the chat app: project client, then the OpenAI client
- Sends each ticket to gpt-5-mini with the Responses API
- Uses structured outputs: a JSON schema the reply has to match
- Prints sentiment, key phrases, category, urgency, and a one-line summary
"""
import json

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

from common import PROJECT_ENDPOINT, CHAT_DEPLOYMENT, load_tickets

# 1. Connect to the project and get the OpenAI-compatible client (keyless).
project = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=DefaultAzureCredential())
openai_client = project.get_openai_client()

INSTRUCTIONS = """You analyze IT helpdesk tickets for Contoso.
Read the ticket and fill in every field of the schema.
Keep key phrases short. Write the summary as one plain sentence."""

# 2. The JSON schema: the fields and types the reply has to match.
#    strict mode means every field is required and no extra fields are allowed.
TICKET_SCHEMA = {
    "type": "object",
    "properties": {
        "sentiment": {"type": "string", "enum": ["positive", "neutral", "negative", "mixed"]},
        "key_phrases": {"type": "array", "items": {"type": "string"}},
        "category": {"type": "string", "enum": ["network", "account", "hardware", "other"]},
        "urgency": {"type": "string", "enum": ["low", "medium", "high"]},
        "summary": {"type": "string"},
    },
    "required": ["sentiment", "key_phrases", "category", "urgency", "summary"],
    "additionalProperties": False,
}

for number, ticket in enumerate(load_tickets(), start=1):
    # 3. Send the ticket. The text format setting turns on structured outputs.
    response = openai_client.responses.create(
        model=CHAT_DEPLOYMENT,
        instructions=INSTRUCTIONS,
        input=ticket,
        text={
            "format": {
                "type": "json_schema",
                "name": "ticket_analysis",
                "schema": TICKET_SCHEMA,
                "strict": True,
            }
        },
    )

    # 4. The reply is JSON, so the code can read each field by name.
    result = json.loads(response.output_text)
    print(f"Ticket {number}")
    print(f"  Sentiment:   {result['sentiment']}")
    print(f"  Key phrases: {', '.join(result['key_phrases'])}")
    print(f"  Category:    {result['category']}")
    print(f"  Urgency:     {result['urgency']}")
    print(f"  Summary:     {result['summary']}\n")

"""
Demo 4: Describe an image in code.

- Same connection as the chat app: project client, then the OpenAI client
- Sends the storm photo and a question to gpt-5-mini with the Responses API
- The user message has two parts: input_text (the question) and input_image (the photo)
- Uses structured outputs, so the damage report comes back as JSON with the same fields every time
"""
import json
import os

from common import CHAT_DEPLOYMENT, IMAGE_DETAIL, PHOTO_FILE, chat_client, photo_data_url

openai_client = chat_client()

INSTRUCTIONS = """You review photos of storm damage to homes for an insurance claims team.
Only report damage you can see in the photo. Keep each entry short.
If the house number isn't readable, set house_number to "not visible"."""

# 1. The JSON schema: the fields and types the damage report has to match.
DAMAGE_SCHEMA = {
    "type": "object",
    "properties": {
        "damage": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": {"type": "string"},
                    "location": {"type": "string"},
                    "severity": {"type": "string", "enum": ["low", "medium", "high"]},
                },
                "required": ["type", "location", "severity"],
                "additionalProperties": False,
            },
        },
        "house_number": {"type": "string"},
        "summary": {"type": "string"},
    },
    "required": ["damage", "house_number", "summary"],
    "additionalProperties": False,
}

# 2. Send the question and the photo in one user message.
#    detail controls how closely the model looks: low, high, or auto.
response = openai_client.responses.create(
    model=CHAT_DEPLOYMENT,
    instructions=INSTRUCTIONS,
    input=[
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "Describe the storm damage in this photo for a repair claim."},
                {"type": "input_image", "image_url": photo_data_url(), "detail": IMAGE_DETAIL},
            ],
        }
    ],
    text={
        "format": {
            "type": "json_schema",
            "name": "damage_report",
            "schema": DAMAGE_SCHEMA,
            "strict": True,
        }
    },
)

# 3. The reply is JSON, so the code can read each field by name.
report = json.loads(response.output_text)
print(f"Photo: {os.path.basename(PHOTO_FILE)} (detail: {IMAGE_DETAIL})\n")
print("Damage found:")
for item in report["damage"]:
    print(f"  - {item['type']} ({item['location']}), severity: {item['severity']}")
print(f"House number: {report['house_number']}")
print(f"Summary:      {report['summary']}")

usage = response.usage
print(f"\nTokens: {usage.input_tokens} in, {usage.output_tokens} out")

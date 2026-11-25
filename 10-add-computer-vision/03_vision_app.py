"""
Demo 6: The repair preview app.

Two models, three steps:
  1. Look:   gpt-5-mini reads the photo and returns a damage report as JSON,
             including a short instruction for an image editor
  2. Create: gpt-image-2.5-flare edits the original photo with that instruction
  3. Label:  the app saves the result as AI-generated and prints a notice
"""
import json
import os

from common import (
    CHAT_DEPLOYMENT,
    IMAGE_DEPLOYMENT,
    IMAGE_DETAIL,
    PHOTO_FILE,
    chat_client,
    image_client,
    photo_data_url,
    save_image,
)

PREVIEW_FILE = "repair-preview-AI-generated.png"

INSTRUCTIONS = """You review photos of storm damage to homes for an insurance claims team.
Only report damage you can see in the photo.
Then write edit_instruction: two or three sentences telling an image editor how to
show this house after the repair and cleanup is finished. Fix the damage you found.
Remove anything left over from the storm or the repair work, such as ladders, tools,
debris, and fallen branches. Remove any people, so only the house and yard remain.
Keep the house design, colors, yard layout, and camera angle the same."""

SCHEMA = {
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
        "summary": {"type": "string"},
        "edit_instruction": {"type": "string"},
    },
    "required": ["damage", "summary", "edit_instruction"],
    "additionalProperties": False,
}

# Step 1, look: gpt-5-mini reads the photo and writes the edit instruction.
response = chat_client().responses.create(
    model=CHAT_DEPLOYMENT,
    instructions=INSTRUCTIONS,
    input=[
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "Review the damage in this photo and plan the repair preview."},
                {"type": "input_image", "image_url": photo_data_url(), "detail": IMAGE_DETAIL},
            ],
        }
    ],
    text={"format": {"type": "json_schema", "name": "repair_plan", "schema": SCHEMA, "strict": True}},
)
plan = json.loads(response.output_text)

print("Step 1, look")
for item in plan["damage"]:
    print(f"  - {item['type']} ({item['location']}), severity: {item['severity']}")
print(f"  Summary: {plan['summary']}")
print(f"  Edit instruction: {plan['edit_instruction']}\n")

# Step 2, create: gpt-image-2.5-flare edits the original photo.
# Editing starts from the real photo, so the house, yard, and angle stay the same.
print("Step 2, create (this can take a few seconds)")
with open(PHOTO_FILE, "rb") as photo:
    result = image_client().images.edit(
        model=IMAGE_DEPLOYMENT,
        image=photo,
        prompt=plan["edit_instruction"],
    )

# Step 3, label: the file name and the notice say this picture is AI-generated.
path = save_image(result.data[0].b64_json, PREVIEW_FILE)
print(f"  Saved {os.path.basename(path)}\n")
print("Step 3, label")
print("  AI-generated preview. Not a record of completed work.")

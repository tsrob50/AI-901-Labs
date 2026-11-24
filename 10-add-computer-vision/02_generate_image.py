"""
Demo 5: Generate an image in code.

- Uses the Images API, not the Responses API
- Sends one text prompt to gpt-image-2.5-flare
- The picture comes back as base64 data, which the script saves to generated.png
"""
from common import IMAGE_DEPLOYMENT, image_client, save_image

openai_client = image_client()

# Change the prompt and run the script again to see a different picture.
PROMPT = (
    "A two-story house with a newly repaired gray shingle roof on a sunny day, "
    "photorealistic."
)

# 1. One prompt in, one image out. model is your image deployment name.
result = openai_client.images.generate(
    model=IMAGE_DEPLOYMENT,
    prompt=PROMPT,
    size="1024x1024",
    n=1,
)

# 2. The image comes back as base64 data. Decode it and save it.
path = save_image(result.data[0].b64_json, "generated.png")
print(f"Prompt: {PROMPT}")
print(f"Image saved to {path}")

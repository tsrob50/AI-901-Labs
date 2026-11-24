"""
Shared settings for the Video 10 demo scripts.

- Reads the .env file
- Creates the two clients:
    chat_client()  -> the OpenAI client from the Foundry project (same as Video 7)
    image_client() -> an OpenAI client for the Images API on the Foundry resource
- Turns a photo into a base64 data URL
- Saves base64 image data to a file
"""
import base64
import mimetypes
import os
from urllib.parse import urlparse

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from openai import OpenAI

# load_dotenv() checks this folder first, then each folder above it, so the
# .env that VS Code for the Web creates at the workspace root is found.
load_dotenv()

PROJECT_ENDPOINT = os.environ["AZURE_EXISTING_AIPROJECT_ENDPOINT"]
CHAT_DEPLOYMENT = os.getenv("AZURE_MODEL_DEPLOYMENT_NAME", "gpt-5-mini")
IMAGE_DEPLOYMENT = os.getenv("IMAGE_DEPLOYMENT_NAME", "gpt-image-2.5-flare")
IMAGE_DETAIL = os.getenv("IMAGE_DETAIL", "high")

HERE = os.path.dirname(os.path.abspath(__file__))
PHOTO_FILE = os.path.join(HERE, os.getenv("PHOTO_FILE", "storm-damage.jpg"))

# The project endpoint looks like this:
#   https://<resource-name>.services.ai.azure.com/api/projects/<project-name>
# The Images API lives on the Foundry resource, at /openai/v1/.
RESOURCE_NAME = urlparse(PROJECT_ENDPOINT).netloc.split(".")[0]
IMAGE_ENDPOINT = os.getenv(
    "IMAGE_ENDPOINT", f"https://{RESOURCE_NAME}.openai.azure.com/openai/v1/"
)

# One keyless sign-in for everything. No API keys anywhere.
credential = DefaultAzureCredential()


def chat_client():
    """The OpenAI client from the Foundry project, same as Video 7."""
    project = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=credential)
    return project.get_openai_client()


def image_client():
    """An OpenAI client for the Images API on the Foundry resource.

    Same sign-in: the token provider turns DefaultAzureCredential into an
    Entra ID token for each request.
    """
    token_provider = get_bearer_token_provider(
        credential, "https://cognitiveservices.azure.com/.default"
    )
    return OpenAI(base_url=IMAGE_ENDPOINT, api_key=token_provider)


def photo_data_url(path=PHOTO_FILE):
    """Read an image file and return it as a base64 data URL.

    Base64 turns the file into plain text characters so it can travel inside
    the JSON request. The data:image/jpeg;base64, prefix says what kind of file it is.
    """
    mime = mimetypes.guess_type(path)[0] or "image/jpeg"
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{encoded}"


def save_image(b64_data, filename):
    """Decode base64 image data from the model and save it in this folder."""
    path = os.path.join(HERE, filename)
    with open(path, "wb") as f:
        f.write(base64.b64decode(b64_data))
    return path

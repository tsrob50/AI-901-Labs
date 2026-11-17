"""
Shared settings for the Video 9 demo scripts.

- Reads the .env file
- Works out the Foundry resource endpoint from the project endpoint
- Loads the sample tickets
"""
import os
from urllib.parse import urlparse

from dotenv import load_dotenv

# load_dotenv() checks this folder first, then each folder above it, so the
# .env that VS Code for the Web creates at the workspace root is found.
load_dotenv()

PROJECT_ENDPOINT = os.environ["AZURE_EXISTING_AIPROJECT_ENDPOINT"]
CHAT_DEPLOYMENT = os.getenv("AZURE_MODEL_DEPLOYMENT_NAME", "gpt-5-mini")
AUDIO_DEPLOYMENT = os.getenv("AUDIO_DEPLOYMENT_NAME", "gpt-audio-1.5")
SPEECH_VOICE = os.getenv("SPEECH_VOICE", "en-US-AvaMultilingualNeural")

HERE = os.path.dirname(os.path.abspath(__file__))

# The project endpoint looks like this:
#   https://<resource-name>.services.ai.azure.com/api/projects/<project-name>
# The resource endpoint is the same address without /api/projects/<project-name>.
_host = urlparse(PROJECT_ENDPOINT).netloc
RESOURCE_NAME = _host.split(".")[0]
RESOURCE_ENDPOINT = f"https://{_host}/"

# Azure Language uses the resource endpoint.
LANGUAGE_ENDPOINT = os.getenv("LANGUAGE_ENDPOINT", RESOURCE_ENDPOINT)

# Keyless sign-in with the Speech SDK needs the resource's custom domain
# endpoint. Same resource name, cognitiveservices.azure.com address.
SPEECH_ENDPOINT = os.getenv(
    "SPEECH_ENDPOINT", f"https://{RESOURCE_NAME}.cognitiveservices.azure.com/"
)


def load_tickets(path=os.path.join(HERE, "tickets.txt")):
    """Return the tickets in tickets.txt. A line with --- separates tickets."""
    with open(path, encoding="utf-8") as f:
        return [t.strip() for t in f.read().split("---") if t.strip()]

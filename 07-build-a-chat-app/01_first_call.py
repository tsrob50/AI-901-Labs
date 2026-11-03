"""
Demo step 1: Connect to a Foundry project and send one prompt.

- Connects to the project endpoint with the Foundry SDK (AIProjectClient)
- Signs in with Microsoft Entra ID (no API key in the code)
- Gets an OpenAI-compatible client from the project
- Sends one prompt with the Responses API and prints the answer and token usage
"""
import os

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Read FOUNDRY_PROJECT_ENDPOINT and MODEL_DEPLOYMENT_NAME from the .env file
load_dotenv()
project_endpoint = os.environ["FOUNDRY_PROJECT_ENDPOINT"]
deployment_name = os.environ["MODEL_DEPLOYMENT_NAME"]

# 1. The project client connects to your Foundry project.
#    DefaultAzureCredential uses the identity you're signed in with (keyless).
project = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(),
)

# 2. Ask the project for an OpenAI-compatible client. This is the client
#    that talks to your deployed model.
openai_client = project.get_openai_client()

# 3. Send one prompt with the Responses API.
#    "model" is your DEPLOYMENT name, not the catalog model name.
response = openai_client.responses.create(
    model=deployment_name,
    input="In two sentences, what does an IT helpdesk do?",
)

print("Model:", response.output_text)

# 4. Every call is billed in tokens. The response tells you how many.
print(
    f"\nTokens - input: {response.usage.input_tokens}, "
    f"output: {response.usage.output_tokens}, "
    f"total: {response.usage.total_tokens}"
)

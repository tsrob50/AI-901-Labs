"""
Demo 6: Connect a client app to an agent.

- Connects to the Foundry project with the Foundry SDK (AIProjectClient)
- Signs in with Microsoft Entra ID (no API key in the code)
- Gets an OpenAI-compatible client from the project
- Sends one question to the agent by name with an agent reference
- Prints the answer and any sources the agent used (file or web citations)

There's no model name and no instructions in this script. The agent you
built in the Foundry portal brings its own model, instructions, and tools.
"""
import os

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Read settings from the .env file. load_dotenv() checks this folder first,
# then each folder above it, so the .env that VS Code for the Web creates
# at the workspace root is found automatically.
# The agent name falls back to it-helpdesk-agent if it isn't set.
load_dotenv()
project_endpoint = os.environ["AZURE_EXISTING_AIPROJECT_ENDPOINT"]
agent_name = os.getenv("AGENT_NAME", "it-helpdesk-agent")

# 1. The project client connects to your Foundry project.
#    DefaultAzureCredential uses the identity you're signed in with (keyless).
project = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(),
)

# 2. Ask the project for an OpenAI-compatible client. Same as the chat app.
openai_client = project.get_openai_client()

# 3. The agent reference tells Foundry which agent should answer.
#    Without a version, Foundry uses the agent's latest version.
agent_reference = {
    "type": "agent_reference",
    "name": agent_name,
    # "version": "2",  # Optional: remove the # to pin a specific version
}

question = "What's the name of the guest Wi-Fi network?"

# 4. Send the question with the Responses API.
#    No model and no instructions: the agent supplies both.
response = openai_client.responses.create(
    input=question,
    extra_body={"agent_reference": agent_reference},
)

print(f"You: {question}")
print(f"{agent_name}: {response.output_text}")

# 5. Show where the answer came from. A file citation means the agent used
#    file search. A URL citation means it used web search. No sources means
#    it answered without a tool.
sources = []
for item in response.output:
    if getattr(item, "type", None) != "message":
        continue
    for part in getattr(item, "content", None) or []:
        for note in getattr(part, "annotations", None) or []:
            if note.type == "file_citation":
                sources.append(f"File: {getattr(note, 'filename', None) or note.file_id}")
            elif note.type == "url_citation":
                sources.append(f"Web: {note.url}")

if sources:
    print("\nSources:")
    for source in dict.fromkeys(sources):  # removes duplicates, keeps order
        print(f"  {source}")
else:
    print("\nSources: none (the agent answered without a tool)")

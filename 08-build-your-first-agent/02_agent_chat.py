"""
Demo 7: Chat with the agent from code.

- Same connection and agent reference as 01_call_agent.py
- Creates one conversation before the chat starts
- Sends only the new message each time, with the conversation ID
- Foundry stores the conversation, so the app keeps no history list
- Shows the sources for each reply (file or web citations)
- Deletes the conversation when you type quit
"""
import os

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Read settings from the .env file (same as 01_call_agent.py).
load_dotenv()
project_endpoint = os.environ["AZURE_EXISTING_AIPROJECT_ENDPOINT"]
agent_name = os.getenv("AGENT_NAME", "it-helpdesk-agent")

project = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(),
)
openai_client = project.get_openai_client()

agent_reference = {"type": "agent_reference", "name": agent_name}


def get_sources(response):
    """Return the file and web sources the agent cited in its reply."""
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
    return list(dict.fromkeys(sources))  # removes duplicates, keeps order


# 1. Create one conversation. Foundry stores every message in it.
#    Compare with the chat app: no history list in the code.
conversation = openai_client.conversations.create()
print(f"Chatting with {agent_name}. Type 'quit' to exit.\n")

try:
    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() == "quit":
            break

        # 2. Send only the new message, plus the conversation ID.
        #    Foundry adds the earlier messages before the agent sees it.
        response = openai_client.responses.create(
            conversation=conversation.id,
            input=user_input,
            extra_body={"agent_reference": agent_reference},
        )

        print(f"{agent_name}: {response.output_text}")
        sources = get_sources(response)
        if sources:
            print("  Sources: " + ", ".join(sources))
        print()
finally:
    # 3. Clean up: delete the conversation when the chat ends.
    openai_client.conversations.delete(conversation_id=conversation.id)
    print("Conversation deleted.")

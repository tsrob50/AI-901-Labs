"""
Demo step 4: Let the service keep the history, and stream the reply.

- Uses previous_response_id so Foundry links each new message to the previous response
  (the app no longer keeps its own history list)
- Streams the reply word by word, like the chat apps you use every day
- Sends the instructions on every call (they aren't carried over
  from the previous response)
"""
import os

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

load_dotenv()
project = AIProjectClient(
    endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
openai_client = project.get_openai_client()
deployment_name = os.environ["MODEL_DEPLOYMENT_NAME"]

INSTRUCTIONS = """You are the IT helpdesk assistant for Contoso employees.
You help with two things only: resetting passwords and connecting to Wi-Fi.
- Keep answers under 100 words, friendly, and in plain language.
- Give steps as a numbered list.
- If a question is about anything else, say you can only help with passwords
  and Wi-Fi, and suggest opening a ticket on the IT portal.
- If you're not sure what the user means, ask one clarifying question.
- Never ask for or accept a user's password."""

previous_response_id = None  # no previous response yet

print("Contoso IT Helpdesk (streaming). Type 'quit' to exit.\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ("quit", "exit"):
        break
    if not user_input:
        continue

    stream = openai_client.responses.create(
        model=deployment_name,
        instructions=INSTRUCTIONS,
        input=user_input,
        previous_response_id=previous_response_id,  # links to the previous response
        stream=True,
    )

    print("Helpdesk: ", end="", flush=True)
    for event in stream:
        if event.type == "response.output_text.delta":
            print(event.delta, end="", flush=True)  # print each chunk as it arrives
        elif event.type == "response.completed":
            previous_response_id = event.response.id  # remember this response for the next message
            usage = event.response.usage
    print(f"\n  [input tokens for this message: {usage.input_tokens}]\n")

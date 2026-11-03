"""
Demo step 3: A chat app that remembers (because the app resends the history).

- Runs a chat loop in the terminal until you type "quit"
- Keeps the conversation in a Python list and sends ALL of it with every new message
- Prints input tokens after every reply so you can watch the history grow
- Set REMEMBER = False to see the model "forget" (only the latest message is sent)
"""
import os

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

load_dotenv()
project = AIProjectClient(
    endpoint=os.environ["AZURE_EXISTING_AIPROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
openai_client = project.get_openai_client()
deployment_name = os.getenv("AZURE_MODEL_DEPLOYMENT_NAME", "gpt-5-mini")

INSTRUCTIONS = """You are the IT helpdesk assistant for Contoso employees.
You help with two things only: resetting passwords and connecting to Wi-Fi.
- Keep answers under 100 words, friendly, and in plain language.
- Give steps as a numbered list.
- If a question is about anything else, say you can only help with passwords
  and Wi-Fi, and suggest opening a ticket on the IT portal.
- If you're not sure what the user means, ask one clarifying question.
- Never ask for or accept a user's password."""

# Change to False, save, and run again to see what happens without history.
REMEMBER = True

# The conversation history: a list of user and assistant messages.
history = []

print("Contoso IT Helpdesk. Type 'quit' to exit.\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ("quit", "exit"):
        break
    if not user_input:
        continue

    # Add the new user message to the history
    history.append({"role": "user", "content": user_input})

    # Send the whole conversation (or only the latest message if REMEMBER is False).
    # Instructions are sent on every call too.
    response = openai_client.responses.create(
        model=deployment_name,
        instructions=INSTRUCTIONS,
        input=history if REMEMBER else [history[-1]],
    )

    reply = response.output_text
    print(f"Helpdesk: {reply}")
    print(f"  [input tokens for this message: {response.usage.input_tokens}]\n")

    # Add the model's reply to the history as an assistant message
    history.append({"role": "assistant", "content": reply})

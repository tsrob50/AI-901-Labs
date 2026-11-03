"""
Demo step 2: Add instructions (the system message).

- Same connection as step 1
- Adds the IT helpdesk instructions from the previous video
- Asks an in-scope question and an out-of-scope question
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

# The instructions parameter is the system message from the playground.
# The end user never sees it.
INSTRUCTIONS = """You are the IT helpdesk assistant for Contoso employees.
You help with two things only: resetting passwords and connecting to Wi-Fi.
- Keep answers under 100 words, friendly, and in plain language.
- Give steps as a numbered list.
- If a question is about anything else, say you can only help with passwords
  and Wi-Fi, and suggest opening a ticket on the IT portal.
- If you're not sure what the user means, ask one clarifying question.
- Never ask for or accept a user's password."""

questions = [
    "My laptop won't connect to the office Wi-Fi.",  # in scope
    "Can you approve my expense report?",             # out of scope
]

for question in questions:
    response = openai_client.responses.create(
        model=deployment_name,
        instructions=INSTRUCTIONS,
        input=question,
    )
    print(f"You: {question}")
    print(f"Helpdesk: {response.output_text}\n")

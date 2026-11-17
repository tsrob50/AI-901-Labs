"""
Demo 5: Answer a spoken question with an audio model.

- Same connection as the other scripts: project client, then the OpenAI client
- Reads question.wav and sends it to an audio model (gpt-audio family)
- Uses the Chat Completions API, because audio models don't support Responses
- Prints the transcript of the reply and saves the spoken reply to reply.wav
"""
import base64
import os

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

from common import PROJECT_ENDPOINT, AUDIO_DEPLOYMENT, HERE

QUESTION_FILE = os.path.join(HERE, "question.wav")
REPLY_FILE = os.path.join(HERE, "reply.wav")

project = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=DefaultAzureCredential())
openai_client = project.get_openai_client()

INSTRUCTIONS = """You are the IT helpdesk assistant for Contoso employees.
Your answers are spoken out loud, so keep them under 60 words, friendly,
and in plain language. Don't use lists or formatting."""

# 1. Read the recording and encode it as base64, which turns the audio into
#    text characters so it can travel in a JSON request.
with open(QUESTION_FILE, "rb") as f:
    question_audio = base64.b64encode(f.read()).decode("utf-8")

# 2. Chat Completions: a list of messages with roles.
#    The user message has a text part and an input_audio part.
completion = openai_client.chat.completions.create(
    model=AUDIO_DEPLOYMENT,
    modalities=["text", "audio"],           # ask for a text and a spoken reply
    audio={"voice": "alloy", "format": "wav"},
    messages=[
        {"role": "system", "content": INSTRUCTIONS},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Answer the question in this recording."},
                {"type": "input_audio", "input_audio": {"data": question_audio, "format": "wav"}},
            ],
        },
    ],
)

# 3. The reply has a transcript (the text of what the model said)
#    and the spoken audio, also base64 encoded.
reply = completion.choices[0].message
print(f"Helpdesk (transcript): {reply.audio.transcript}")

with open(REPLY_FILE, "wb") as f:
    f.write(base64.b64decode(reply.audio.data))
print(f"Spoken reply saved to {os.path.basename(REPLY_FILE)}")

usage = completion.usage
print(f"Tokens: {usage.prompt_tokens} in, {usage.completion_tokens} out")

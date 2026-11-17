"""
Demo 6: Build a speech app with Azure Speech.

The chained pipeline: listen, think, speak.
- Step 1, listen: Azure Speech transcribes question.wav (speech to text)
- Step 2, think: gpt-5-mini answers the question (Responses API)
- Step 3, speak: Azure Speech reads the answer with a neural voice and
  saves it to answer.wav (text to speech)
Keyless sign-in throughout, with the same DefaultAzureCredential.
"""
import os
import sys

import azure.cognitiveservices.speech as speechsdk
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

from common import PROJECT_ENDPOINT, CHAT_DEPLOYMENT, SPEECH_ENDPOINT, SPEECH_VOICE, HERE

QUESTION_FILE = os.path.join(HERE, "question.wav")
ANSWER_FILE = os.path.join(HERE, "answer.wav")

credential = DefaultAzureCredential()

# SpeechConfig: where to connect (the Foundry resource) and how to sign in.
speech_config = speechsdk.SpeechConfig(token_credential=credential, endpoint=SPEECH_ENDPOINT)
speech_config.speech_recognition_language = "en-US"

# Step 1, listen: speech to text from the WAV file.
audio_in = speechsdk.audio.AudioConfig(filename=QUESTION_FILE)
recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_in)
result = recognizer.recognize_once()

if result.reason == speechsdk.ResultReason.RecognizedSpeech:
    question = result.text
    print(f"Step 1, transcript: {question}")
elif result.reason == speechsdk.ResultReason.NoMatch:
    sys.exit("Step 1: no speech could be recognized in the file.")
else:
    details = result.cancellation_details
    sys.exit(f"Step 1 canceled: {details.reason}. {details.error_details}")

# Step 2, think: send the transcript to gpt-5-mini. Same call as the chat app.
project = AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=credential)
openai_client = project.get_openai_client()

INSTRUCTIONS = """You are the IT helpdesk assistant for Contoso employees.
Your answers are spoken out loud, so keep them under 60 words, friendly,
and in plain language. Don't use lists or formatting."""

response = openai_client.responses.create(
    model=CHAT_DEPLOYMENT,
    instructions=INSTRUCTIONS,
    input=question,
)
answer = response.output_text
print(f"Step 2, answer: {answer}")

# Step 3, speak: text to speech with a neural voice, saved to a WAV file.
speech_config.speech_synthesis_voice_name = SPEECH_VOICE
audio_out = speechsdk.audio.AudioOutputConfig(filename=ANSWER_FILE)
synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_out)
spoken = synthesizer.speak_text_async(answer).get()

if spoken.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print(f"Step 3, spoken answer saved to {os.path.basename(ANSWER_FILE)} ({SPEECH_VOICE})")
else:
    details = spoken.cancellation_details
    sys.exit(f"Step 3 canceled: {details.reason}. {details.error_details}")

# Optional: SSML controls pronunciation, rate, and pauses. Replace the
# speak_text_async line above with something like this:
# ssml = f"""<speak version="1.0" xml:lang="en-US">
#   <voice name="{SPEECH_VOICE}"><prosody rate="-10%">{answer}</prosody></voice>
# </speak>"""
# spoken = synthesizer.speak_ssml_async(ssml).get()

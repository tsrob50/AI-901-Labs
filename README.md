# AI-901: Microsoft Azure AI Fundamentals - Course Demos
 
Code and supporting files for the AI-901 video series and course by Travis Roberts. Use this repository to follow along with the hands-on demos as you study for the **Microsoft Certified: Azure AI Fundamentals (AI-901)** exam or start building with **Microsoft Foundry**.
 
If you're studying for the AI-901 certification or just getting started with Microsoft Foundry, this repository is for you.
 
## About the course
 
AI-901 is Microsoft's Azure AI Fundamentals exam. It replaced AI-900 and puts Microsoft Foundry, generative AI, and agents at the center. The exam covers two domains:
 
| Domain | Weight |
|---|---|
| Identify AI concepts and capabilities | 40-45% |
| Implement AI solutions by using Microsoft Foundry | 55-60% |
 
The series starts with concepts (how AI models work, responsible AI, and the main AI workloads) and then moves into hands-on builds in Microsoft Foundry. Each video becomes a module in the full course.
 
- **Watch the videos:** [AI-901 playlist on YouTube](https://www.youtube.com/playlist?list=PLRg-m2DkQG-s)
- **Take the full course:** [My Cloud Coach](https://mycloud.coach) (text lessons, cheat sheets, practice questions, and a study guide)
- **Official exam outline:** [Study guide for Exam AI-901](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ai-901)
## What's in this repository
 
| Module | Topic | Demo files |
|---|---|---|
| 1 | AI-901 Explained | Concepts only |
| 2 | Responsible AI in Azure | Concepts only |
| 3 | Picking the Right AI Model | Concepts only |
| 4 | How AI Reads Text | Concepts only |
| 5 | How AI Sees and Hears | Concepts only |
| 6 | Microsoft Foundry for Beginners | Portal demos, no code |
| 7 | Build a Chat App with the Foundry SDK | [`07-build-a-chat-app`](./07-build-a-chat-app) |
| 8 | Build Your First AI Agent in Microsoft Foundry | [`08-build-your-first-agent`](./08-build-your-first-agent) |
| 9 | Add Text and Voice to Your App with Microsoft Foundry | [`09-add-text-and-voice`](./09-add-text-and-voice) |
| 10 | Add Computer Vision to Your App | [`10-add-computer-vision`](./10-add-computer-vision) |
 
New demo files are added as new videos are released, including information extraction with Azure Content Understanding.
 
## Before you start
 
You need the following to run the demos:
 
- An Azure subscription. A [free account](https://azure.microsoft.com/free/) works.
- A Microsoft Foundry project with a deployed chat model. The demos use `gpt-5-mini`, set up in the Microsoft Foundry for Beginners module.
- The **Foundry User** role (formerly Azure AI User) on the Foundry project or resource. The Owner role alone doesn't let your code call the model.
- A web browser. The demos run in **VS Code for the Web**, opened from the Foundry playground, so you don't need to install anything on your computer.
- A GitHub account, only if you want to keep your work after the session ends.
- For Module 8: an agent built in the Foundry portal. The module steps below walk through it, and the agent needs a model that supports tool calling, like `gpt-5-mini`.
- For Module 9: a separate Foundry project in a region that offers `gpt-audio-1.5`, with two deployments, `gpt-5-mini` and `gpt-audio-1.5`. To create the project, you need the Owner role, or Contributor plus permission to assign roles. The module steps below walk through it.
- For Module 10: a separate Foundry resource and project in a region that offers both `gpt-image-2.5-flare` and `gpt-5-mini`, with a deployment of each. `gpt-image-2.5-flare` is generally available, so no access application is needed. To create the project, you need the Owner role, or Contributor plus permission to assign roles. The module steps below walk through it.
## Module 7: Build a Chat App with the Foundry SDK
 
Four short Python scripts build a terminal chat app step by step with the Microsoft Foundry SDK (`azure-ai-projects`) and the Responses API. The app signs in with Microsoft Entra ID through `DefaultAzureCredential`, so there's no API key in the code.
 
| File | What it shows |
|---|---|
| `requirements.txt` | The packages: `azure-ai-projects`, `azure-identity`, and `python-dotenv` |
| `.env.example` | Settings template for editors other than VS Code for the Web |
| `01_first_call.py` | Connect to the project, send one prompt, and print the reply and token usage |
| `02_instructions.py` | Add helpdesk instructions (the system message) and test an in-scope and out-of-scope question |
| `03_chat_loop.py` | A chat loop that resends the conversation history, with a token counter and a `REMEMBER` switch to watch the model forget |
| `04_chat_streaming.py` | Let Foundry keep the history with `previous_response_id`, and stream replies as they're generated |
 
### Set up and run
 
The scripts read two settings:
 
| Setting | What it is | Required |
|---|---|---|
| `AZURE_EXISTING_AIPROJECT_ENDPOINT` | Your Foundry **project endpoint**, from the project **Home** page. Format: `https://<resource-name>.services.ai.azure.com/api/projects/<project-name>` | Yes |
| `AZURE_MODEL_DEPLOYMENT_NAME` | Your model **deployment name**, from **Build** > **Models** | Only if your deployment isn't named `gpt-5-mini` |
 
Choose the steps for your editor.
 
#### Option 1: VS Code for the Web (recommended)
 
When you open VS Code for the Web from the Foundry playground, Foundry creates a `.env` file at the workspace root with your project endpoint already filled in. The scripts find that file automatically, so there's nothing to copy.
 
1. In the Foundry portal, open your deployment in the playground, select the **Code** tab, choose **Python**, and select **Open in VS Code for the Web**.
2. In the VS Code for the Web terminal, run `az account show` to confirm you're signed in to Azure. If you get an error, run `az login`.
3. Clone this repository into the workspace and move into the module folder:
```bash
git clone https://github.com/tsrob50/AI-901-Labs.git
cd AI-901-Labs/07-build-a-chat-app
```
 
4. Create and activate a virtual environment, then install the packages:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
 
5. If your deployment isn't named `gpt-5-mini`, open the `.env` file at the workspace root (not in the `AI-901-Labs` folder), add the following line with your deployment name, and save the file:
```bash
AZURE_MODEL_DEPLOYMENT_NAME="<your-deployment-name>"
```
 
6. Run the scripts (see [Run the scripts](#run-the-scripts)).
#### Option 2: Another editor (VS Code, PyCharm, or similar)
 
You need Python 3.10 or later and the [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) on your computer.
 
1. Sign in to Azure:
```bash
az login
```
 
2. Clone this repository and move into the module folder:
```bash
git clone https://github.com/tsrob50/AI-901-Labs.git
cd AI-901-Labs/07-build-a-chat-app
```
 
3. Create and activate a virtual environment, then install the packages:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
 
   On macOS and Linux, if you get `command not found: python`, use `python3` instead: `python3 -m venv .venv`. Once the virtual environment is active, `python` works in that terminal, so the rest of the commands stay the same.
 
   On Windows, activate the environment with `.venv\Scripts\activate` instead.
 
4. Copy the settings template:
```bash
cp .env.example .env
```
 
   On Windows, use `copy .env.example .env` instead.
 
5. Open `.env`, replace the placeholder with your **project endpoint**, update the **deployment name** if yours isn't `gpt-5-mini`, and save the file.
### Run the scripts
 
Run the scripts in order from the `07-build-a-chat-app` folder:
 
```bash
python 01_first_call.py
python 02_instructions.py
python 03_chat_loop.py
python 04_chat_streaming.py
```
 
Type `quit` to exit the chat scripts.
 
### Common errors
 
| Error | Likely cause | Fix |
|---|---|---|
| `KeyError: 'AZURE_EXISTING_AIPROJECT_ENDPOINT'` | The scripts can't find a `.env` file with the project endpoint | VS Code for the Web: make sure you cloned the repo inside the workspace. Other editors: create `.env` from `.env.example` in the module folder |
| Deployment not found | Your deployment isn't named `gpt-5-mini`, or `AZURE_MODEL_DEPLOYMENT_NAME` doesn't match | Add or fix `AZURE_MODEL_DEPLOYMENT_NAME` in `.env` using the exact name from **Build** > **Models** |
| Connection or endpoint errors | Wrong endpoint in `.env` | Set `AZURE_EXISTING_AIPROJECT_ENDPOINT` to the **project endpoint** (ends in `/api/projects/<project-name>`), not the Azure OpenAI endpoint |
| `DefaultAzureCredential` failed | No Azure sign-in was found | Run `az login` |
| 401 or 403 permission denied | Signed in, but missing the data plane role | Assign yourself the **Foundry User** role on the project or resource |
 
## Module 8: Build Your First AI Agent in Microsoft Foundry
 
You build an IT helpdesk agent in the Foundry portal, give it knowledge with file search, then call it from Python by name. The agent brings its own model, instructions, and tools, so the script has no model name and no instructions in it. The app signs in with Microsoft Entra ID through `DefaultAzureCredential`. Agents don't support API keys.
 
| File | What it shows |
|---|---|
| `agent-instructions.txt` | The agent instructions (the system message) to paste into the playground |
| `contoso-it-helpdesk-guide.txt` | A sample IT helpdesk guide for file search: Wi-Fi networks, password reset, VPN, loaner laptops, and helpdesk hours. All names and values are fictional |
| `requirements.txt` | The packages: `azure-ai-projects`, `azure-identity`, and `python-dotenv` |
| `.env.example` | Settings template for editors other than VS Code for the Web |
| `01_call_agent.py` | Send one question to the agent with an agent reference, then print the reply and the sources it used (file or web citations) |
| `02_agent_chat.py` | A chat loop that uses a conversation, so Foundry stores the history. It shows the sources for each reply and deletes the conversation when you quit |
 
### Build the agent in the portal
 
The scripts need an agent to call. Create it first:
 
1. Go to [ai.azure.com](https://ai.azure.com), turn on **New Foundry**, and select your project.
2. Go to **Build** > **Models** and select your deployment to open the playground.
3. Paste the text from `agent-instructions.txt` into **Instructions**, then select **Save as agent** and name it `it-helpdesk-agent`. You can also create it from **Build** > **Agents** > **New agent** > **Build an agent**, then pick the model and add the instructions.
4. In the agent playground, go to **Tools** > **Add** and upload `contoso-it-helpdesk-guide.txt` for file search. Keep the default index name.
5. Check that **Web search** is listed under **Tools**. It's turned on by default for new agents. If it isn't there, add it under **Tools** > **Add**.
6. Select **Save**. Every save creates a new version of the agent.
Portal labels change often. If a label doesn't match, check the current [Foundry Agent Service documentation](https://learn.microsoft.com/azure/foundry/agents/).
 
### Set up and run
 
The scripts read two settings:
 
| Setting | What it is | Required |
|---|---|---|
| `AZURE_EXISTING_AIPROJECT_ENDPOINT` | Your Foundry **project endpoint**, from the project **Home** page. Format: `https://<resource-name>.services.ai.azure.com/api/projects/<project-name>` | Yes |
| `AGENT_NAME` | Your agent's name, from **Build** > **Agents** | Only if your agent isn't named `it-helpdesk-agent` |
 
Use the same setup steps as Module 7, with the Module 8 folder:
 
- **VS Code for the Web:** follow [Option 1](#option-1-vs-code-for-the-web-recommended). In step 3, run `cd AI-901-Labs/08-build-your-first-agent`. In step 5, add `AGENT_NAME="<your-agent-name>"` to the workspace `.env` file, only if your agent has a different name.
- **Another editor:** follow [Option 2](#option-2-another-editor-vs-code-pycharm-or-similar). In step 2, run `cd AI-901-Labs/08-build-your-first-agent`. In step 5, fill in your project endpoint and agent name in `.env`.
Then run the scripts in order from the `08-build-your-first-agent` folder:
 
```bash
python 01_call_agent.py
python 02_agent_chat.py
```
 
Type `quit` to exit the chat script.
 
`01_call_agent.py` asks for the guest Wi-Fi network name. If the agent has the helpdesk guide, the answer comes from the guide, and the script lists the guide as the source.
 
To pin a version of the agent, open `01_call_agent.py` and remove the `#` in front of the `"version"` line in the agent reference. Without a version, Foundry uses the latest version.
 
### Common errors
 
| Error | Likely cause | Fix |
|---|---|---|
| `404` Agent `<name>` with version not found | `AGENT_NAME` doesn't match an agent in the project | Copy the exact name from **Build** > **Agents**. Agent names can't be changed after you create the agent |
| The answer doesn't use the guide, and no sources are listed | File search isn't attached, or the change wasn't saved | Check the file under **Tools** in the agent playground, select **Save**, and run the script again. Also check that you didn't pin an older version. If the file is attached but the agent still ignores it, raise the model's reasoning effort to medium in the agent playground and save |
| `KeyError: 'AZURE_EXISTING_AIPROJECT_ENDPOINT'` | The scripts can't find a `.env` file with the project endpoint | VS Code for the Web: make sure you cloned the repo inside the workspace. Other editors: create `.env` from `.env.example` in the module folder |
| `DefaultAzureCredential` failed | No Azure sign-in was found | Run `az login` |
| 401 or 403 permission denied | Signed in, but missing the data plane role | Assign yourself the **Foundry User** role on the project or resource |
 
## Module 9: Add Text and Voice to Your App with Microsoft Foundry
 
Four short Python scripts add text analysis and voice to the IT helpdesk app. Two scripts analyze the same three helpdesk tickets, one with a model and one with Azure Language. Two scripts answer the same recorded question, one in a single call to an audio model and one in three steps with Azure Speech. Everything signs in with Microsoft Entra ID through `DefaultAzureCredential`, so there are no API keys in the code.
 
VS Code for the Web runs in the cloud, so it can't use your microphone or speakers. The scripts read a recorded question from `question.wav` and save their spoken answers as WAV files you can download and play.
 
| File | What it shows |
|---|---|
| `requirements.txt` | The packages: `azure-ai-projects`, `azure-identity`, `python-dotenv`, `azure-ai-textanalytics` (Azure Language), and `azure-cognitiveservices-speech` (Azure Speech) |
| `.env.example` | Settings template for editors other than VS Code for the Web |
| `common.py` | Shared settings used by all four scripts. Reads `.env`, works out the Azure Language and Azure Speech endpoints from the project endpoint, and loads the tickets |
| `tickets.txt` | Three sample helpdesk tickets, separated by `---`. All names, phone numbers, and email addresses are fictional |
| `question.wav` | A short recorded question for the speech scripts (16-bit PCM, mono, 16 kHz) |
| `01_analyze_with_model.py` | Send each ticket to `gpt-5-mini` with the Responses API and structured outputs. A JSON schema returns sentiment, key phrases, category, urgency, and a one-line summary |
| `02_analyze_with_language.py` | Redact personal information (PII) and label entities with Azure Language, with a confidence score for each |
| `03_spoken_prompt.py` | Send `question.wav` to `gpt-audio-1.5` with the Chat Completions API, print the reply transcript, and save the spoken reply to `reply.wav` |
| `04_speech_app.py` | A three-step pipeline: Azure Speech transcribes `question.wav`, `gpt-5-mini` answers it, and Azure Speech saves the spoken answer to `answer.wav` with a neural voice |
 
### Create the project and deploy the models
 
`gpt-audio-1.5` is only offered in a few regions, so this module uses its own project. Create it first:
 
1. Go to [ai.azure.com](https://ai.azure.com) and turn on **New Foundry**.
2. Go to **Build** > **Catalog**, select the **Models** tab, set availability to **All models**, and search for `gpt-audio-1.5`. The results aren't sorted by name, so use your browser's find on page if you can't spot it.
3. Open the model card, select **View availability**, and note a supported region. Check the current list in [Region availability for Foundry Models sold by Azure](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure-region-availability).
4. From the project selector in the top left, select **Create new project** and give it a name.
5. Select **Advanced options**. Choose the supported region, confirm the subscription and your existing resource group, and turn off **Set up recommended resources**. Then select **Create**, and select **Let's go** when it finishes.
6. With the new project selected, go to **Build** > **Catalog** > **Models**, open `gpt-audio-1.5`, and select **Deploy** > **Default settings** > **Deploy**.
7. Repeat for `gpt-5-mini`.
8. Go to **Build** > **Models** and check that both deployments show **Succeeded**.
Foundry usually assigns you the **Foundry User** role on the new resource when you create it in the portal. If a script returns 401 or 403, check the role in the Azure portal under the resource's **Access control (IAM)**.
 
Portal labels change often. If a label doesn't match, check the current [Microsoft Foundry documentation](https://learn.microsoft.com/azure/foundry/).
 
### Set up and run
 
The scripts read these settings:
 
| Setting | What it is | Required |
|---|---|---|
| `AZURE_EXISTING_AIPROJECT_ENDPOINT` | The **project endpoint** of the new project, from the project **Home** page | Yes |
| `AZURE_MODEL_DEPLOYMENT_NAME` | Your chat model deployment name | Only if it isn't `gpt-5-mini` |
| `AUDIO_DEPLOYMENT_NAME` | Your audio model deployment name | Only if it isn't `gpt-audio-1.5` |
| `SPEECH_VOICE` | The neural voice for `04_speech_app.py`, from the Voice Gallery | Only to change the default, `en-US-AvaMultilingualNeural` |
| `LANGUAGE_ENDPOINT`, `SPEECH_ENDPOINT` | Endpoint overrides for Azure Language and Azure Speech | Only if the defaults worked out from the project endpoint don't work |
 
Use the same setup steps as Module 7, with the Module 9 folder:
 
- **VS Code for the Web:** follow [Option 1](#option-1-vs-code-for-the-web-recommended), and open VS Code for the Web from the `gpt-5-mini` deployment in the **new** project, so the `.env` file has the new project endpoint. In step 3, run `cd AI-901-Labs/09-add-text-and-voice`. In step 5, add `AUDIO_DEPLOYMENT_NAME` or `AZURE_MODEL_DEPLOYMENT_NAME` to the workspace `.env` file only if your deployments have different names.
- **Another editor:** follow [Option 2](#option-2-another-editor-vs-code-pycharm-or-similar). In step 2, run `cd AI-901-Labs/09-add-text-and-voice`. In step 5, fill in the new project endpoint and any deployment names that differ.
Then run the scripts in order from the `09-add-text-and-voice` folder:
 
```bash
python 01_analyze_with_model.py
python 02_analyze_with_language.py
python 03_spoken_prompt.py
python 04_speech_app.py
```
 
To play `reply.wav` or `answer.wav` in VS Code for the Web, right-click the file in the Explorer and select **Download**, then play it on your computer.
 
To try your own question, record a short WAV file (16-bit PCM, mono, 16 kHz works best), save it over `question.wav`, and run the speech scripts again.
 
### Common errors
 
| Error | Likely cause | Fix |
|---|---|---|
| `gpt-audio-1.5` doesn't show up in the catalog | The availability filter or your project's region | Set availability to **All models**, and use a project in a region that offers the model |
| Deployment not found | `AUDIO_DEPLOYMENT_NAME` or `AZURE_MODEL_DEPLOYMENT_NAME` doesn't match a deployment | Copy the exact name from **Build** > **Models** in the new project |
| The audio request fails with an error about the input | The audio script is pointed at a model that doesn't accept audio, like `gpt-5-mini` | Set `AUDIO_DEPLOYMENT_NAME` to your `gpt-audio-1.5` deployment |
| `Step 1 canceled` or `Step 3 canceled` in `04_speech_app.py` | Azure Speech couldn't connect or sign in | Read the error details. Check `az login` and the Foundry User role. If it's a connection error, set `SPEECH_ENDPOINT` in `.env` to `https://<resource-name>.cognitiveservices.azure.com/` |
| `Step 1: no speech could be recognized` | The recording is silent, too quiet, or in an unsupported format | Use a 16-bit PCM WAV file with clear speech |
| `KeyError: 'AZURE_EXISTING_AIPROJECT_ENDPOINT'` | The scripts can't find a `.env` file with the project endpoint | VS Code for the Web: make sure you cloned the repo inside the workspace. Other editors: create `.env` from `.env.example` in the module folder |
| `DefaultAzureCredential` failed | No Azure sign-in was found | Run `az login` |
| 401 or 403 permission denied | Signed in, but missing the data plane role on the new resource | Assign yourself the **Foundry User** role on the new Foundry resource |
 
### Clean up Module 9
 
When you're done with this module, delete only what it created. Keep your earlier project and the resource group.
 
1. In the [Azure portal](https://portal.azure.com), open the resource group you used for the new project.
2. Select the Foundry resource you created for this module (not your earlier one) and select **Delete**. This also deletes its project and both deployments.
3. Deleted Foundry resources are soft-deleted first. To remove it right away, purge it from **Manage deleted resources** in the Foundry (Azure AI services) area of the Azure portal.
## Module 10: Add Computer Vision to Your App
 
Three short Python scripts add vision to an app. The scenario is an insurance claims team reviewing a photo of a storm-damaged house. One script describes the photo, one generates a new image, and one does both: it reads the damage and turns the photo into a labeled repair preview. Everything signs in with Microsoft Entra ID through `DefaultAzureCredential`, so there are no API keys in the code.
 
Two models do the work. `gpt-5-mini` reads the photo through the Responses API, the same call as Module 7, with the image added to the prompt. `gpt-image-2.5-flare` creates and edits pictures through the Images API. `gpt-image-2.5-flare` is generally available, so you don't need to apply for access. The older `gpt-image-1.5`, `gpt-image-1`, and `gpt-image-1-mini` models need an approved limited-access application.
 
| File | What it shows |
|---|---|
| `requirements.txt` | The packages: `azure-ai-projects`, `azure-identity`, and `python-dotenv`. Same as Module 7 |
| `.env.example` | Settings template for editors other than VS Code for the Web |
| `common.py` | Shared settings used by all three scripts. Reads `.env`, creates the chat client and the image client, turns the photo into a base64 data URL, and saves images the model returns |
| `storm-damage.jpg` | A sample photo of a storm-damaged house for the scripts to read. It's AI-generated, so it isn't a real house or a real claim |
| `01_describe_image.py` | Send the photo and a question to `gpt-5-mini` with the Responses API. A JSON schema returns each damage item with its location and severity, the house number, and a one-line summary |
| `02_generate_image.py` | Send a text prompt to `gpt-image-2.5-flare` with the Images API and save the picture to `generated.png` |
| `03_vision_app.py` | The repair preview app. `gpt-5-mini` reads the photo and writes an edit instruction, `gpt-image-2.5-flare` edits the original photo, and the app saves `repair-preview-AI-generated.png` with a notice that it's a preview, not a record |
 
### Create the project and deploy the models
 
`gpt-image-2.5-flare` is only offered in a few regions, so this module uses its own Foundry resource and project. You don't need anything from earlier modules, and the region doesn't need to be near you.
 
1. Go to [ai.azure.com](https://ai.azure.com) and turn on **New Foundry**.
2. Go to **Build** > **Catalog**, select the **Models** tab, set availability to **All models**, and search for `gpt-image-2.5-flare`.
3. Open the model card and select **View availability**. Pick a region that offers both `gpt-image-2.5-flare` and `gpt-5-mini`. Check the current list in [Region availability for Foundry Models sold by Azure](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure-region-availability).
4. From the project selector in the top left, select **Create new project** and give it a name.
5. Select **Advanced options**. Choose the region from step 3, confirm the subscription, pick a resource group or create a new one, and turn off **Set up recommended resources**. Then select **Create**, and select **Let's go** when it finishes.
6. With the new project selected, go to **Build** > **Catalog** > **Models**, open `gpt-image-2.5-flare`, and select **Deploy** > **Default settings** > **Deploy**.
7. Repeat for `gpt-5-mini`.
8. Go to **Build** > **Models** and check that both deployments show **Succeeded**.
Foundry usually assigns you the **Foundry User** role on the new resource when you create it in the portal. If a script returns 401 or 403, check the role in the Azure portal under the resource's **Access control (IAM)**.
 
Portal labels change often. If a label doesn't match, check the current [Microsoft Foundry documentation](https://learn.microsoft.com/azure/foundry/).
 
### Set up and run
 
The scripts read these settings:
 
| Setting | What it is | Required |
|---|---|---|
| `AZURE_EXISTING_AIPROJECT_ENDPOINT` | The **project endpoint** of the new project, from the project **Home** page | Yes |
| `AZURE_MODEL_DEPLOYMENT_NAME` | Your chat model deployment name | Only if it isn't `gpt-5-mini` |
| `IMAGE_DEPLOYMENT_NAME` | Your image model deployment name | Only if it isn't `gpt-image-2.5-flare` |
| `PHOTO_FILE` | The photo the scripts read, a JPEG or PNG in the module folder | Only to use your own photo instead of `storm-damage.jpg` |
| `IMAGE_DETAIL` | How closely `gpt-5-mini` looks at the photo: `low`, `high`, or `auto` | Only to change the default, `high` |
| `IMAGE_ENDPOINT` | Endpoint override for the Images API | Only if the default worked out from the project endpoint doesn't work |
 
Use the same setup steps as Module 7, with the Module 10 folder:
 
- **VS Code for the Web:** follow [Option 1](#option-1-vs-code-for-the-web-recommended), and open VS Code for the Web from the `gpt-5-mini` deployment in the **new** project, so the `.env` file has the new project endpoint. In step 3, run `cd AI-901-Labs/10-add-computer-vision`. In step 5, add `IMAGE_DEPLOYMENT_NAME` or `AZURE_MODEL_DEPLOYMENT_NAME` to the workspace `.env` file only if your deployments have different names.
- **Another editor:** follow [Option 2](#option-2-another-editor-vs-code-pycharm-or-similar). In step 2, run `cd AI-901-Labs/10-add-computer-vision`. In step 5, fill in the new project endpoint and any deployment names that differ.
Then run the scripts in order from the `10-add-computer-vision` folder:
 
```bash
python 01_describe_image.py
python 02_generate_image.py
python 03_vision_app.py
```
 
Image generation can take a few seconds. To view `generated.png` or `repair-preview-AI-generated.png` in VS Code for the Web, select the file in the Explorer. To keep a copy, right-click it and select **Download**.
 
To compare detail settings, set `IMAGE_DETAIL=low` in `.env` and run `01_describe_image.py` again. Low detail uses fewer input tokens, but it may miss small things like the house number.
 
To try your own photo, put a JPEG or PNG in the module folder and set `PHOTO_FILE` to its file name. Only use photos you have the right to use, and keep customer photos out of public repositories.
 
### Common errors
 
| Error | Likely cause | Fix |
|---|---|---|
| `gpt-image-2.5-flare` doesn't show up in the catalog | The availability filter or your project's region | Set availability to **All models**, and use a project in a region that offers the model |
| Deployment not found | `IMAGE_DEPLOYMENT_NAME` or `AZURE_MODEL_DEPLOYMENT_NAME` doesn't match a deployment | Copy the exact name from **Build** > **Models** in the new project |
| `01_describe_image.py` fails when it's pointed at the image deployment | An image model can't answer a chat prompt | Chat and image input go to `gpt-5-mini`. Set `AZURE_MODEL_DEPLOYMENT_NAME` back to your chat deployment |
| `FileNotFoundError` for the photo | `PHOTO_FILE` doesn't match a file in the module folder | Check the file name and extension, or remove `PHOTO_FILE` to use `storm-damage.jpg` |
| `429` too many requests | Image models have a low per-minute quota | Wait a minute and run the script again |
| The request is blocked by a content filter | The prompt or the generated image was flagged | Reword the prompt. Content filters check both the prompt and the image |
| Connection or endpoint errors from the image scripts | The Images API endpoint worked out from the project endpoint doesn't match your resource | Set `IMAGE_ENDPOINT` in `.env` to `https://<resource-name>.openai.azure.com/openai/v1/` |
| `KeyError: 'AZURE_EXISTING_AIPROJECT_ENDPOINT'` | The scripts can't find a `.env` file with the project endpoint | VS Code for the Web: make sure you cloned the repo inside the workspace. Other editors: create `.env` from `.env.example` in the module folder |
| `DefaultAzureCredential` failed | No Azure sign-in was found | Run `az login` |
| 401 or 403 permission denied | Signed in, but missing the data plane role on the new resource | Assign yourself the **Foundry User** role on the new Foundry resource |
 
### Clean up Module 10
 
When you're done with this module, delete the Foundry resource it created. Nothing else in your subscription changes.
 
1. In the [Azure portal](https://portal.azure.com), open the resource group you used for the new project.
2. Select the Foundry resource you created for this module and select **Delete**. This also deletes its project and both deployments. If you created a resource group just for this module, you can delete the whole resource group instead.
3. Deleted Foundry resources are soft-deleted first. To remove it right away, purge it from **Manage deleted resources** in the Foundry (Azure AI services) area of the Azure portal.
## Costs and cleanup
 
The demos call a deployed model, and every call is billed in tokens. A Global Standard deployment is billed per token, so a few dozen chat messages cost very little, but check current [Azure pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) before you start. In Module 8, file search adds a small storage charge for the index, and web search is billed per call. In Module 9, audio tokens cost more than text tokens, and Azure Language and Azure Speech are billed per use. In Module 10, images add input tokens to `gpt-5-mini` calls, and the image model is billed by tokens too, with image output tokens costing the most. Keep your `.env` file out of source control.
 
When you're done with the series, delete the resource group that holds your Foundry resources to stop all charges.
 
## License
 
This repository uses two licenses:
 
- **Code** (Python scripts, `requirements.txt`, `.env.example`, and any other source or configuration files) is licensed under the [MIT License](./LICENSE-CODE).
- **All other content** (written guides, documentation, and images) is licensed under [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International](./LICENSE) (CC BY-NC-SA 4.0).
You're welcome to use the content for personal study, study groups, and other non-commercial learning, with credit to Travis Roberts / Ciraltos LLC. Commercial use of the course content, such as including it in paid training, requires written permission.
 
Copyright (c) 2026 Ciraltos LLC.
 
## Disclaimer
 
The code is provided as is, without warranty, for learning purposes. It isn't intended for production use. This project isn't affiliated with or endorsed by Microsoft. Microsoft, Azure, and Microsoft Foundry are trademarks of the Microsoft group of companies.
 
## Connect
 
- Blog: [ciraltos.com](https://www.ciraltos.com)
- Course: [My Cloud Coach](https://mycloud.coach)
 

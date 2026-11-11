Claude


Readme · MD
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
 
New demo files are added as new videos are released, including text and speech, computer vision, and information extraction with Azure Content Understanding.
 
## Before you start
 
You need the following to run the demos:
 
- An Azure subscription. A [free account](https://azure.microsoft.com/free/) works.
- A Microsoft Foundry project with a deployed chat model. The demos use `gpt-5-mini`, set up in the Microsoft Foundry for Beginners module.
- The **Foundry User** role (formerly Azure AI User) on the Foundry project or resource. The Owner role alone doesn't let your code call the model.
- A web browser. The demos run in **VS Code for the Web**, opened from the Foundry playground, so you don't need to install anything on your computer.
- A GitHub account, only if you want to keep your work after the session ends.
- For Module 8: an agent built in the Foundry portal. The module steps below walk through it, and the agent needs a model that supports tool calling, like `gpt-5-mini`.
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
| `contoso-it-helpdesk-guide.txt` | A sample IT helpdesk guide for file search: Wi-Fi networks, password reset, VPN, loaner laptops, and helpdesk hours. All names and values are fictional |
| `requirements.txt` | The packages: `azure-ai-projects`, `azure-identity`, and `python-dotenv` |
| `.env.example` | Settings template for editors other than VS Code for the Web |
| `01_call_agent.py` | Send one question to the agent with an agent reference, then print the reply and the sources it used (file or web citations) |
| `02_agent_chat.py` | A chat loop that uses a conversation, so Foundry stores the history. It shows the sources for each reply and deletes the conversation when you quit |
 
### Build the agent in the portal
 
The scripts need an agent to call. Create it first:
 
1. Go to [ai.azure.com](https://ai.azure.com), turn on **New Foundry**, and select your project.
2. Go to **Build** > **Models** and select your deployment to open the playground.
3. Add instructions for an IT helpdesk assistant, then select **Save as agent** and name it `it-helpdesk-agent`. You can also create it from **Build** > **Agents** > **Create agent**.
4. In the agent playground, go to **Tools** > **Add** and upload `contoso-it-helpdesk-guide.txt` for file search. Keep the default index name.
5. Optional: add **Web search** under **Tools** > **Add**.
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
| The answer doesn't use the guide, and no sources are listed | File search isn't attached, or the change wasn't saved | Check the file under **Tools** in the agent playground, select **Save**, and run the script again. Also check that you didn't pin an older version |
| `KeyError: 'AZURE_EXISTING_AIPROJECT_ENDPOINT'` | The scripts can't find a `.env` file with the project endpoint | VS Code for the Web: make sure you cloned the repo inside the workspace. Other editors: create `.env` from `.env.example` in the module folder |
| `DefaultAzureCredential` failed | No Azure sign-in was found | Run `az login` |
| 401 or 403 permission denied | Signed in, but missing the data plane role | Assign yourself the **Foundry User** role on the project or resource |
 
## Costs and cleanup
 
The demos call a deployed model, and every call is billed in tokens. A Global Standard deployment is billed per token, so a few dozen chat messages cost very little, but check current [Azure pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/) before you start. In Module 8, file search adds a small storage charge for the index, and web search is billed per call. Keep your `.env` file out of source control.
 
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
 
Claude finished the response

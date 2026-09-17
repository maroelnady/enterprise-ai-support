# 🤖 Enterprise AI Support

**Enterprise AI Support** is an AI-powered IT support assistant designed to help employees quickly find solutions to common **IT and SharePoint-related problems**.

The system combines **Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), CrewAI multi-agent orchestration, and FastAPI** to provide a practical enterprise support workflow.

Instead of relying on a single chatbot, the system uses **specialized AI agents** to understand the user's request, determine the appropriate support path, retrieve relevant information from the enterprise knowledge base, and handle IT support requests.

---

## ✨ Key Capabilities

* 🤖 **AI-powered IT Support Assistant**
* 🧠 **Multi-Agent Architecture** using CrewAI
* 🔀 **Manager Agent** for intelligent request routing
* 📚 **Enterprise Knowledge Search** using RAG
* 🔎 **Document Retrieval** using vector search
* 🛠️ **Specialized IT Support Agent**
* 🎫 **Automated IT Ticket Creation**
* 💬 **Interactive Web Chat Interface**
* 🚀 **FastAPI REST API**
* 🔐 **Environment-based API Key Management**
* 📦 **GitHub-ready project structure**

---

## 🏗️ System Architecture

```text
                    ┌───────────────────┐
                    │      Employee     │
                    │    / End User     │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │   Manager Agent   │
                    │ Intent & Routing  │
                    └─────────┬─────────┘
                              │
                 ┌────────────┴────────────┐
                 │                         │
                 ▼                         ▼
      ┌──────────────────┐       ┌──────────────────────┐
      │ Knowledge        │       │ IT Support           │
      │ Specialist       │       │ Specialist           │
      └────────┬─────────┘       └──────────┬───────────┘
               │                            │
               ▼                            ├── Knowledge Search
      ┌──────────────────┐                  │
      │ Enterprise       │                  └── Ticket Creation
      │ Knowledge Base   │
      └──────────────────┘
```

### Request Flow

```text
User Request
     │
     ▼
Manager Agent
     │
     ├──────────────► Knowledge Request
     │                      │
     │                      ▼
     │               Knowledge Specialist
     │                      │
     │                      ▼
     │               RAG / Vector Search
     │                      │
     │                      ▼
     │               Grounded Response
     │
     └──────────────► IT Support Request
                            │
                            ▼
                     IT Support Specialist
                            │
                    ┌───────┴────────┐
                    ▼                ▼
             Knowledge Search   Create Ticket
```

---

## 🧠 AI Agent Architecture

The system uses multiple specialized agents instead of a single general-purpose chatbot.

### 1. Manager Agent

Responsible for:

* Understanding the user's intent
* Classifying the request
* Selecting the appropriate specialist
* Routing the request

Possible routing decisions:

```text
knowledge
it_support
```

### 2. Knowledge Specialist

Responsible for:

* Searching the enterprise knowledge base
* Retrieving relevant documents
* Using RAG to ground responses
* Providing accurate, knowledge-based answers

### 3. IT Support Specialist

Responsible for:

* Handling IT support requests
* Searching the knowledge base for troubleshooting information
* Identifying when further support is required
* Creating IT support tickets when necessary

---

## 📚 Enterprise Knowledge Base

The current knowledge base contains IT support documentation covering:

```text
data/raw/
│
├── account/
│   ├── account_lockout_procedure.txt
│   └── password_reset_policy.txt
│
├── email/
│   ├── email_setup_guide.txt
│   └── email_troubleshooting.txt
│
├── security/
│   └── cybersecurity_mfa_policy.txt
│
├── sharepoint/
│   ├── sharepoint_access_policy.txt
│   └── sharepoint_troubleshooting.txt
│
└── vpn/
    ├── vpn_access_policy.txt
    ├── vpn_setup_guide.txt
    └── vpn_troubleshooting.txt
```

This allows the assistant to provide responses based on enterprise-approved information rather than relying only on the LLM's general knowledge.

---

## 🔎 Retrieval-Augmented Generation

The RAG pipeline follows this process:

```text
User Question
      │
      ▼
Query Processing
      │
      ▼
Vector Search
      │
      ▼
Relevant Documents
      │
      ▼
Context Injection
      │
      ▼
LLM
      │
      ▼
Grounded Answer
```

Vector retrieval is implemented using:

* **FAISS**
* **Chroma**
* Embedding models
* Document chunking
* Retrieval routing

---

## 🎫 IT Ticket Management

The system includes an automated ticket creation capability for IT support requests.

Example workflow:

```text
Employee
   │
   ▼
IT Problem
   │
   ▼
IT Support Specialist
   │
   ├── Can solve from Knowledge Base
   │          │
   │          ▼
   │       Solution
   │
   └── Requires Support
              │
              ▼
        Create IT Ticket
```

Tickets are stored locally during the prototype stage.

---

## 🌐 Web Application

The project includes a web-based chat interface that communicates with the FastAPI backend.

```text
┌─────────────────────────────────────┐
│       Enterprise AI Support         │
├─────────────────────────────────────┤
│                                     │
│  👤 How do I request SharePoint     │
│     access?                         │
│                                     │
│  🤖 According to the enterprise     │
│     access policy...                │
│                                     │
├─────────────────────────────────────┤
│  Type your question...        Send  │
└─────────────────────────────────────┘
```

The application is served through FastAPI and provides a simple conversational interface for employees.

---

## 🚀 API

The backend is implemented using **FastAPI**.

### Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "healthy",
  "service": "Enterprise AI Support API"
}
```

### Chat

```http
POST /chat
```

Example request:

```json
{
  "message": "How do I request access to a SharePoint site?"
}
```

Example response:

```json
{
  "response": "..."
}
```

---

## 🛠️ Technology Stack

| Technology                     | Purpose                        |
| ------------------------------ | ------------------------------ |
| 🐍 **Python**                  | Core development               |
| 🤖 **CrewAI**                  | Multi-agent orchestration      |
| ⚡ **Groq**                     | LLM inference                  |
| 🧠 **RAG**                     | Enterprise knowledge retrieval |
| 🔎 **FAISS / Chroma**          | Vector search                  |
| 🚀 **FastAPI**                 | Backend API                    |
| 🌐 **HTML / CSS / JavaScript** | Web chat interface             |
| ✅ **Pydantic**                 | API data validation            |
| 📦 **Git / GitHub**            | Version control                |

---

## 💡 Example Use Cases

The assistant can handle requests such as:

### SharePoint

> "How do I request access to a SharePoint site?"

> "I cannot access my SharePoint site."

### Account

> "How do I reset my password?"

> "My account is locked."

### Email

> "How do I configure my company email?"

> "My email is not working."

### VPN

> "How do I configure the company VPN?"

> "My VPN is not connecting."

### Security

> "How do I enable MFA?"

### IT Support

> "I have an IT problem and need support."

The system determines whether the request can be answered from the **enterprise knowledge base** or requires **IT support and ticket handling**.

---

## 🎯 Project Goal

The goal of this project is to demonstrate how **Agentic AI can be applied to Enterprise IT Support**.

Rather than building a simple chatbot, the project demonstrates an intelligent workflow where specialized AI agents collaborate to:

1. Understand the employee's request
2. Determine the user's intent
3. Route the request to the appropriate specialist
4. Search enterprise knowledge
5. Generate a grounded response
6. Create an IT support ticket when required

This architecture provides a foundation for developing a more intelligent and automated **Enterprise AI Support Platform**.

---

## 📊 Current Status

### 🟢 Functional Prototype

The current system includes:

* ✅ Manager Agent
* ✅ Knowledge Specialist
* ✅ IT Support Specialist
* ✅ RAG knowledge retrieval
* ✅ Vector search
* ✅ Ticket creation
* ✅ Multi-agent orchestration
* ✅ Conversation/API layer
* ✅ FastAPI backend
* ✅ Web-based chat interface
* ✅ GitHub repository

---

## 🔮 Future Improvements

Planned improvements include:

* 🔐 User authentication and authorization
* 🏢 Enterprise system integrations
* 🎫 Integration with real ITSM platforms
* 📊 Monitoring and analytics
* 🧠 Improved conversation memory
* 🛡️ Advanced AI guardrails
* 🚀 Production deployment
* 🔗 SharePoint integration
* 👥 Role-based access control
* 📈 Support analytics and dashboards

---

## 📁 Project Structure

```text
enterprise-ai-support/
│
├── data/
│   ├── raw/
│   │   ├── account/
│   │   ├── email/
│   │   ├── security/
│   │   ├── sharepoint/
│   │   └── vpn/
│   └── tickets.json
│
├── src/
│   ├── agents/
│   │   ├── crewai_manager_agent.py
│   │   ├── crewai_manager_tasks.py
│   │   ├── crewai_knowledge_agent.py
│   │   ├── crewai_knowledge_tasks.py
│   │   ├── crewai_it_support_agent.py
│   │   ├── crewai_it_support_tasks.py
│   │   └── test_crewai_orchestrator.py
│   │
│   ├── embeddings/
│   ├── ingestion/
│   ├── rag/
│   ├── retrieval/
│   ├── tools/
│   └── api.py
│
├── tests/
│
├── web/
│   └── index.html
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

---

## ▶️ Running the Project

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/enterprise-ai-support.git
cd enterprise-ai-support
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file based on `.env.example`:

### 6. Start the application

```powershell
uvicorn src.api:app --host 127.0.0.1 --port 8000
```

### 7. Open the application

```text
http://127.0.0.1:8000
```

---

## 🔐 Security Note

API keys and runtime data should **never be committed to GitHub**.

The project uses:

```text
.env
```

for local secrets, while:

```text
.env.example
```

provides a safe template.

Sensitive files such as `.env`, runtime ticket data, and generated vector stores are excluded through `.gitignore`.

---

## 👩‍💻 Project

**Enterprise AI Support**

An educational and practical implementation of **Agentic AI + RAG for Enterprise IT Support**.

**Status:** 🟢 Functional Prototype

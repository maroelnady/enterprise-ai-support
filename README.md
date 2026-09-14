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

### 2. Knowledg

Enterprise AI Support

Enterprise AI Support is an AI-powered IT support assistant designed to help employees quickly find solutions to common IT and SharePoint-related problems.

The system combines Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), CrewAI multi-agent orchestration, and FastAPI to provide a practical enterprise support workflow.

Instead of relying on a single chatbot, the system uses specialized AI agents to understand the user's request, determine the appropriate support path, retrieve relevant information from the enterprise knowledge base, and handle IT support requests.

Key Capabilities
🤖 AI-powered IT Support Assistant
🧠 Multi-Agent Architecture using CrewAI
🔀 Manager Agent for intelligent request routing
📚 Enterprise Knowledge Search using RAG
🔎 Document retrieval using vector search
🛠️ Specialized IT Support Agent
🎫 Automated IT Ticket Creation
💬 Interactive Web Chat Interface
🚀 FastAPI REST API
🔐 Environment-based API key management
📦 GitHub-ready project structure
Architecture
Employee
   │
   ▼
┌─────────────────────┐
│    Manager Agent    │
│ Intent & Routing    │
└──────────┬──────────┘
           │
     ┌─────┴─────┐
     ▼           ▼
 Knowledge    IT Support
 Specialist   Specialist
     │           │
     ▼           ├── Knowledge Search
 Enterprise KB   │
                 └── Ticket Creation
Technology Stack
Technology	Purpose
Python	Core development
CrewAI	Multi-agent orchestration
Groq	LLM inference
RAG	Enterprise knowledge retrieval
FAISS / Chroma	Vector search
FastAPI	Backend API
HTML / CSS / JavaScript	Chat interface
Pydantic	API data validation
Git / GitHub	Version control
Example Use Cases

The assistant can handle requests such as:

"How do I request access to a SharePoint site?"
"I cannot access my SharePoint site."
"How do I reset my password?"
"How do I configure my company email?"
"My VPN is not working."
"How do I enable MFA?"
"I have an IT problem and need support."

The system determines whether the request can be answered from the enterprise knowledge base or requires IT support and ticket handling.

Project Goal

The goal of this project is to demonstrate how agentic AI can be applied to enterprise IT support, moving beyond a simple chatbot toward an intelligent workflow where specialized AI agents collaborate to understand, retrieve, and act on employee requests.

Current Status

Development Status: Functional Prototype

The current system includes:

Manager Agent
Knowledge Specialist
IT Support Specialist
RAG knowledge retrieval
Ticket creation
Multi-agent orchestration
Conversation/API layer
FastAPI backend
Web-based chat interface

Future work includes authentication, production deployment, enterprise integrations, monitoring, and additional IT automation.

# Study Agent

A powerful AI-powered study assistant that helps you interact with your notes and documents through natural language conversation. Upload your study materials and chat with the agent to get information, explanations, and answers from your documents.

![Study Agent Demo](https://via.placeholder.com/800x400?text=Study+Agent+Demo)

## 🚀 Features

- **Natural Language Conversation**: Chat with an AI assistant about your documents
- **Document Processing**: Upload PDF and DOCX files for analysis
- **Contextual Responses**: Get insights based on your uploaded materials
- **Modern UI**: Clean, responsive interface built with Next.js and Tailwind CSS
- **API Backend**: Robust FastAPI backend with OpenAI integration

## 🛠️ Technology Stack

### Backend

- Python 3.9+
- FastAPI
- LangChain
- OpenAI API
- Chroma Vector Database

### Frontend

- Next.js 14
- TypeScript
- Tailwind CSS
- React 18

## 📋 Requirements

- Python 3.9+
- Node.js 16+
- npm or yarn
- OpenAI API key

## 🔧 Installation

### Clone the repository

```bash
git clone https://github.com/yourusername/study-agent.git
cd study-agent
```

### Backend Setup

1. Create a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add your OpenAI API key

```bash
OPENAI_API_KEY=your_openai_api_key
```

### Frontend Setup

1. Install dependencies

```bash
npm install
```

2. Build the frontend

```bash
npm run build
```

## 🚀 Usage

### Start the backend server

```bash
python main.py
```

The application will be available at [http://localhost:8000](http://localhost:8000).

### Custom Document Directory

To use a custom document directory, set the `documents_dir` in the `.env` file.

```bash
DOCUMENTS_DIR=path/to/your/documents
```

## 📁 Project Structure

```bash
study-agent/
├── api/
├── frontend/
│ └── dist/
├── config/
├── core/
├── knowledge_base/
├── data/
├── memory/
├── document_processor/
├── main.py
├── requirements.txt
├── .env
└── README.md
```

## 🔌 API Endpoints

| Endpoint     | Method | Description                              |
| ------------ | ------ | ---------------------------------------- |
| `/chat`      | POST   | Send a message to the study agent        |
| `/upload`    | POST   | Upload a document (PDF, DOCX)            |
| `/documents` | GET    | List all documents in the knowledge base |
| `/health`    | GET    | Health check endpoint                    |

## 🔐 Environment Variables

| Variable         | Description                    | Default |
| ---------------- | ------------------------------ | ------- |
| `OPENAI_API_KEY` | Your OpenAI API key (required) | None    |

## 🔄 How It Works

1. **Document Processing**: When you upload a document, the system:

   - Processes the document based on its type (PDF, DOCX)
   - Splits it into smaller, manageable chunks
   - Creates vector embeddings for each chunk using OpenAI's embedding model
   - Stores these embeddings in a Chroma vector database

2. **Chat Interaction**:
   - The system searches for relevant content in your documents based on your query
   - It retrieves the most similar chunks to provide context to the AI
   - The AI generates a response using both the retrieved context and conversation history
   - The response is returned to you in the chat interface

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 🙏 Acknowledgements

- [OpenAI](https://openai.com/) for their powerful API
- [LangChain](https://langchain.com/) for the document processing and embedding framework
- [FastAPI](https://fastapi.tiangolo.com/) for the API framework
- [Next.js](https://nextjs.org/) for the frontend framework
- [Tailwind CSS](https://tailwindcss.com/) for the UI design system

---

Built with ❤️ by [Andrés Espejo]

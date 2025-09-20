# RAG-Powered Departmental Knowledge System

This project is a secure, role-based AI assistant designed for internal enterprise use. It leverages a Retrieval-Augmented Generation (RAG) pipeline to answer questions from a private knowledge base, providing accurate and contextually relevant information tailored to a user's specific department (e.g., Finance, HR, Engineering). The application features a user-friendly chat interface built with Streamlit and a robust backend for user authentication and data management.

## Key Features

*   **Role-Based Access Control:** Users can only access information relevant to their designated department, ensuring data security and relevance.
*   **Retrieval-Augmented Generation (RAG):** Provides accurate, context-aware answers from internal documents (PDFs, CSVs, TXT files), minimizing LLM hallucinations and grounding responses in factual data.
*   **Secure User Authentication:** A complete login and signup system using FastAPI and a MySQL database to manage user credentials securely.
*   **Interactive Chat Interface:** A real-time, conversational UI built with Streamlit for seamless user interaction and history management.
*   **Multi-Department Knowledge Base:** The system is designed to ingest and manage documents from various corporate departments, making it a scalable, centralized knowledge hub.

## How It Works

The application follows a modern RAG architecture:

1.  **User Authentication:** A user signs up or logs in via the Streamlit interface. The FastAPI backend authenticates the user against the MySQL database and identifies their departmental role.
2.  **Query Input:** The authenticated user asks a question in the chat interface.
3.  **Context Retrieval:** The system retrieves the relevant departmental knowledge base from the ChromaDB vector store based on the user's role. The user's query is then used to perform a similarity search to find the most relevant document chunks.
4.  **Prompt Augmentation:** The retrieved text chunks (context) are combined with the user's original question into a prompt template.
5.  **LLM Generation:** This augmented prompt is sent to the `Mistral-7B-Instruct-v0.3` model via the Hugging Face API, which generates a response based *only* on the provided context.
6.  **Display Response:** The final, fact-checked answer is displayed to the user in the Streamlit chat window.

## Technology Stack

*   **AI & Machine Learning:**
    *   **Python:** Core programming language.
    *   **LangChain:** For building and orchestrating the RAG pipeline.
    *   **Hugging Face:** For the Mistral-7B LLM and sentence embeddings.
    *   **ChromaDB:** Vector database for efficient document retrieval.
*   **Backend & API:**
    *   **FastAPI:** For user authentication and backend API endpoints.
    *   **MySQL:** Relational database for user and session management.
    *   **Pydantic:** For data validation.
*   **Frontend:**
    *   **Streamlit:** For the interactive web-based chat interface.
*   **Data Handling:**
    *   **Document Loaders:** `PyPDFLoader`, `CSVLoader`, `TextLoader` for data ingestion.
    *   **Cryptography:** For secure credential handling.

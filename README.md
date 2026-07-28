# 🚀 [Tips Hindawi](https://www.tipshindawi.com/) Challenge (June–July) 2026

> 🏆 This repository is my official submission for the [ **Tips Hindawi** ](https://www.tipshindawi.com/) **Challenge (June–July) 2026**.

## 👤 Participant

| Field            | Value                                |
| ---------------- | ------------------------------------ |
| Full Name        | Marcel Azmy Soliman                  |
| Project Name     | Ahkeelak                            |
| GitHub Username  | marcel-azmy                          |
| Challenge Batch  | June–July 2026                       |
| Training Program | Large Language Models (LLMs) Program |
| Organization     | [**Edrak for Ai**](https://edrak4ai.com/en)                         |

---

# 📖 Project Overview

Ahkeelak is an AI-powered storytelling assistant that generates engaging, personalized stories based on the user's preferences. Users can choose the story topic, style, target audience, length, and output language (English, Arabic, or Bilingual).

The application leverages Large Language Models (LLMs), LangGraph, and Retrieval-Augmented Generation (RAG) to produce high-quality stories while supporting both English and Arabic readers.

---

# ✨ Features

* AI-powered story generation
* Supports English, Arabic, and Bilingual output.
* English → Arabic translation pipeline for higher-quality Arabic text
* Multiple storytelling styles (Adventure, Fantasy, Educational, Horror, etc.)
* Story customization based on audience (Children, Teens, Adults)
* Adjustable story length
* Retrieval-Augmented Generation (RAG) for context-aware responses
* LangGraph workflow for structured generation
* Streamlit web interface
---

# 🛠️ Technologies Used

Programming Language
* Python 3.11+

AI & Machine Learning
* Hugging Face Transformers
* PyTorch
* LangChain
* LangGraph
* Sentence Transformers

Retrieval-Augmented Generation (RAG)
* ChromaDB
* Hugging Face Embeddings
* RecursiveCharacterTextSplitter
* Document Loaders
* Pydantic Output Parser

Backend
* FastAPI
* Uvicorn

Frontend
* Streamlit

Deployment
* Google Colab
* ngrok

Other Libraries
* Requests
* Accelerate
* FAISS

---

# ⚙️ Installation

* Clone the repositiry:
	- (git clone https://github.com/marcel-azmy/Ahkeelak.git)
	- (cd Ahkeelak)

* Install dependencies
  pip install -r requirements.txt

* Start the backend
  - Open the Ahkeelak.ipynb on google colab
  - Set the runtime to T4 (GPU)
  - Run the model

* Run the Streamlit application:
  	(python -m streamlit run app.py)


---

# 🚀 Usage

1. Open the Streamlit application.
2. Enter the research paper.
3. Select:
	* Story style
	* Audience
	* Story length
	* Output language
4. Click Generate Story.
5. The application sends a request to the FastAPI backend running on Google Colab.
6. LangGraph processes the request.
7. The generated story is displayed:
	* English only
	* Arabic only
	* English followed by Arabic (Bilingual)

---

# 📸 Demo

Add screenshots, GIFs, or a demo video.

---

# 📈 Results

* Successfully built an end-to-end AI storytelling application
* Integrated LangGraph to orchestrate the generation workflow.
* Implemented multilingual story generation with improved Arabic quality through an English-first translation pipeline.
* Deployed the backend on Google Colab using FastAPI and ngrok.
* Developed an interactive Streamlit interface for a seamless user experience.
* Created a modular and scalable architecture for future enhancements.

---

# 🔮 Future Improvements

* Text-to-Speech narration
* AI-generated illustrations for stories
* Additional storytelling styles and genres
* User authentication and saved story history
* Export stories as PDF or Word documents
* Voice input support
* Cloud deployment (AWS, Azure, or Hugging Face Spaces)
* Mobile-friendly interface
* Translate charts into illustrations for stories
* Translate scientific books into novel and each book chapter into novel chapter.

---

# 📚 About the Challenge

This project was developed as part of the [**Tips Hindawi**](https://www.tipshindawi.com/) **Challenge (June–July) 2026**.

[Tips Hindawi](https://www.tipshindawi.com/) is the internships department of [**Edrak for Ai**](https://edrak4ai.com/en), and the challenge encourages participants to build real-world projects, apply practical skills, and showcase their work through GitHub.

For more information about the challenge, training programs, and upcoming batches, visit the official [Tips Hindawi](https://www.tipshindawi.com/) website.

---

# 📄 License

This project is shared for educational and portfolio purposes.

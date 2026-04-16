# 🤖 Automata-Guided Local Chatbot

A privacy-focused local chatbot that runs entirely on your machine using **Ollama + Mistral**, enhanced with **DFA-based intent classification, CFG-style prompt structuring, and safety filtering** to make responses more efficient, controlled, and reliable.

---

## ✨ Features

- 🧠 **DFA-based Intent Classification**
  Routes queries into:
  - Greeting / Thanks / Goodbye → instant responses  
  - Math → safe evaluator  
  - General → LLM  

- 🧮 **Safe Math Engine (AST-based)**
  Secure expression evaluation without `eval()`

- ⚡ **CFG-style Prompt Builder**
  Structured prompts for better LLM control and reduced hallucinations

- 🤖 **Local LLM (Ollama + Mistral)**
  Fully offline AI chatbot

- 🔐 **Safety Filtering**
  Blocks unsafe inputs and filters harmful outputs

- 💬 **Streaming Responses**
  Real-time token streaming like ChatGPT

- 💾 **Local Chat Storage**
  Chats saved as JSON files (no database)

- 🎛️ **User Controls**
  Toggle automata mode + adjust temperature

---

## 🏗 Tech Stack

- **Frontend:** Streamlit  
- **Backend:** Python  
- **LLM Runtime:** Ollama (Mistral)  
- **Core Ideas:** DFA, CFG-inspired prompts, AST parsing  
- **Storage:** JSON-based local storage  

---

## 🚀 Setup Instructions

- Download and install Ollama: https://ollama.com  
- Run the model:
```bash
ollama run mistral
```
- Install Dependencies
```bash
pip install -r requirements.txt
```
- Run the App
```bash
streamlit run app.py
```
- Open in Browser
Go at : http://localhost:8501

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

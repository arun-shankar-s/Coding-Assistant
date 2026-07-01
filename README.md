# AI Coding Agent

A lightweight AI-powered coding assistant built with Python, Flask, and an Ollama-hosted Large Language Model (LLM). The agent can inspect project files, search code, execute Python scripts, edit files, and maintain a lightweight memory of previous interactions.

---

## Frontend Preview

> **Replace the image below with a screenshot of your application.**

<img width="1904" height="927" alt="image" src="https://github.com/user-attachments/assets/6457c3ef-9fef-48ca-b563-cb3541f192ad" />

---

## Features

* AI-powered coding assistant
* List and read project files
* Create and edit files
* Search files and source code
* Lightweight in-memory knowledge system
* Stores important tool outputs and file summaries for contextual reasoning
* Automatic file summarization
* Execute Python scripts
* Simple Flask-based web interface

---

## Project Structure

```
.
├── app.py
├── agent.py
├── tools.py
├── memory.py
├── config.py
├── bot_config.json
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── script.js
```

---

## Installation

Clone the repository and install the dependencies:

```bash
pip install openai flask
```

---

## Configuration

Create a `bot_config.json` file:

```json
{
  "openai": {
    "api_key": "YOUR_API_KEY",
    "base_url": "YOUR_BASE_URL",
    "model": "YOUR_MODEL_NAME"
  }
}
```

This allows the project to work with any OpenAI-compatible API endpoint.

---

## Run

Start the Flask application:

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

## Available Tools

* List Files
* Read File
* Write File
* Edit File
* Search Files
* Search Code
* Run Python
* Search Memory
* Build Project Knowledge
* Get File Context

---

## Tech Stack

* Python
* Flask
* Ollama
* HTML
* CSS
* JavaScript

---

## License

This project is intended for learning and experimentation with AI agents and tool-calling workflows.

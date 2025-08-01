# AI Powered Writer Assistant

*Generate compelling titles, descriptions, feedback, and visuals for your articles — all with AI.*

---

## Overview

**Writer Assistant** is a lightweight Python web application that leverages AI to help writers create better content. Given a raw article draft, it automatically generates:

- A **catchy, SEO-friendly title**
- A **professional article description**
- A **custom cover image** (via Gemini Image Generation)
- **Constructive feedback** on writing quality and structure

Built with **LangChain**, **Mistral AI**, and **Google Gemini** this tool is perfect for bloggers, technical writers, and developers who want to refine their content with intelligent AI assistance.

> *Goal:* Help writers improve their craft while automating repetitive tasks like brainstorming titles and generating visuals.

---

## Features

| Feature | Powered By |
|-------|------------|
| Article Title Generation | Mistral AI (creative mode) |
| SEO-Friendly Description | Mistral AI (zero temperature) |
| Writing Feedback | Structured output from Mistral AI |
| Cover Image Generation | Google Gemini 2.0 Flash (image generation) |
| Real-time Web Interface | Built-in HTTP server with live updates |
| Responsive UI | Pico CSS framework |

---

## How It Works

1. **User inputs** an article in the web form.
2. The app sends the text to `generate.py`, which uses **LangChain** to orchestrate multiple LLMs.
3. AI generates:
   - Title (creative)
   - Description (accurate)
   - Feedback (structured)
   - Image (via Gemini)
4. All results are saved to the `output/` directory.
5. The web server serves the final output with auto-refresh (every 10 seconds).

> The app refreshes the image every time you visit the page to avoid caching issues.

---

## Project Structure

```bash
writer-assistant/
├── generate.py               # Main AI logic: title, description, image, feedback
├── server.py                 # Simple web server with form handling
├── output/                   # Generated assets (title.txt, description.txt, image.png, feedback.txt)
├── input.txt                 # Temporary input file
├── README.md
```

---

## Prerequisites

- Python 3.10+
- `pip` package manager
- API keys:
  - [Mistral AI](https://console.mistral.ai/) (for `MISTRAL_API_KEY`)
  - [Google AI Studio](https://aistudio.google.com/) (for `GOOGLE_API_KEY`)

> **Important:** Never commit your API keys to version control.

---

## Setup Instructions

### 1. Install Dependencies

Manually install the dependencies:
```bash
pip install langchain mistralai google-generativeai pydantic scikit-image pillow
```

Or install them from the requirements.txt file:
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

```bash
export MISTRAL_API_KEY="your-mistral-api-key-here"
export GOOGLE_API_KEY="your-google-gemini-api-key-here"
```

> Replace with actual keys from your accounts.

### 3. Run the Server

```bash
python3 server.py
```

Open your browser and go to:  
[http://localhost:3050](http://localhost:3050)

---

## Features

- **AI-Powered Article Enhancement**
  - Generates catchy, SEO-friendly titles
  - Creates compelling meta descriptions
  - Suggests improvements for writing quality
- **Dynamic Cover Image Generation**
  - Uses Gemini 2.0 Flash Image Generation for visual appeal
  - Automatically updates on refresh
- **Constructive Feedback**
  - Structured output from LLM to guide improvement
- **Simple Web Interface**
  - Clean, responsive UI using [Pico CSS](https://picocss.com/)
  - Real-time feedback loop

---

## Why This Project?

This project was built as to learn and experiment with:

- **LangChain** – For chaining prompts and handling LLM interactions
- **Prompt Engineering** – Crafting effective system/user messages
- **Structured Output** – Using Pydantic models for reliable responses
- **Image Generation via LLM** – Integrating multimodal AI
- **Web Server Integration** – Connecting backend logic with frontend

---

## Acknowledgements

This project was inspired by tutorials on LangChain and AI-powered content generation. It’s a hands-on learning exercise to understand how to combine LLMs, web servers, and structured output in a practical application.

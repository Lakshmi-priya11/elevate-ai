# Elevate

**Your AI-powered mock interview coach**

A mock interview coach I built that gives you feedback on your answers to behavioral questions.

You type an answer to a question like *"Tell me about a time you improved a process"*, and Elevate checks it for filler words, whether it follows the STAR format (Situation, Task, Action, Result), and how relevant it is to the question. Then it gives you short, specific feedback. It keeps track of every answer during the session, so you can ask how you're doing overall or which question you struggled with most.

📄 [View the app demo (PDF)](Elevate_project_demo.pdf)


## Why I built this

Practicing for behavioral interviews is hard on your own. You never really know if your answer was good or if you rambled. I wanted something that gives honest, structured feedback right away, and it was also a good excuse to learn how LLM agents and tool calling actually work.

## Features

- **Answer evaluation**: every answer goes through three checks:
  - **Filler words**: counts words like "um", "like" and "basically"
  - **STAR structure**: checks which parts of Situation, Task, Action and Result are there and which are missing
  - **Relevance score (0–100)**: the model picks keywords it expects for the question, and the answer is scored on how many it covers
- **Live scorecard**: a table that updates after each answer
- **Ask your coach**: ask things like *"What's my weakest area so far?"* and get an answer based on your whole session, not just the last question
- **Final report**: average relevance score and your weakest question

## How it works

The interesting part is the agent loop in `main.py`.

The scoring functions are plain Python. The LLM doesn't do the counting or the scoring itself. Instead, I describe the three functions to the model as tools. When an answer comes in:

1. The model reads the question and answer and decides which tools to call (and with what arguments, for example the keywords it expects for relevance scoring).
2. My code runs those Python functions and sends the results back to the model.
3. This repeats until the model has everything it needs, then it writes the feedback based on the actual tool results.

I capped the loop at 5 rounds so it can't get stuck calling tools forever.

Every evaluation is saved in `session_history`, which is what the coach and the final report use.

## Tech stack

- **Python**
- **[Groq](https://groq.com/)** API running `openai/gpt-oss-120b`
- **[Gradio](https://www.gradio.app/)** for the web UI
- **python-dotenv** for loading the API key

## Getting started

### 1. Clone the repo

```bash
git clone https://github.com/<your-username>/elevate-ai.git
cd elevate-ai
```

### 2. Set up a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Add your Groq API key

You can get a free key from the [Groq console](https://console.groq.com/keys).

```bash
cp .env.example .env
```

Then open `.env` and paste your key in.

### 4. Run the app

```bash
python app.py
```

Open the local URL it prints (usually http://127.0.0.1:7860).

You can also run the evaluation from the terminal without the UI:

```bash
python main.py
```

## Project structure

```
├── app.py                     # Gradio web interface
├── main.py                    # Agent loop, session memory, coach and final report
├── detect_filler_words.py     # Tool: counts filler words
├── check_star_structure.py    # Tool: checks STAR components
├── score_relevance.py         # Tool: keyword-based relevance score
├── memory_check.py            # Quick check that session memory finds the weakest answer
├── requirements.txt
└── .env.example
```

Each tool file can also be run on its own (`python detect_filler_words.py`) to test it separately.

## Testing

`memory_check.py` evaluates one strong answer and one weak answer, then checks that the final report correctly picks the weak one as the weakest area:

```bash
python memory_check.py
```

## Things I'd like to improve

- The STAR and filler word checks use keyword matching, so they can miss things a person would catch. I'd like to make them smarter.
- Session history is stored in memory, so it resets when the app restarts and is shared if multiple people use the same running app.
- Let users add their own questions, or pick questions for a specific role.
- Add voice input so you can practice answering out loud.

## Notes

This project uses Gradio 4.44.1, the last version that supports Python 3.9. That's why `huggingface_hub` is pinned below 1.0 in `requirements.txt`. If you're on Python 3.10 or newer, you can upgrade Gradio and drop that pin.

## License

[MIT](LICENSE)

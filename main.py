
import os
import json
from dotenv import load_dotenv
from groq import Groq

from detect_filler_words import detect_filler_words
from check_star_structure import check_star_structure
from score_relevance import score_relevance

load_dotenv(override=True)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Map tool names to Python functions
tool_functions = {
    "detect_filler_words": detect_filler_words,
    "check_star_structure": check_star_structure,
    "score_relevance": score_relevance,
}

# Stores evaluations for the current interview session
session_history = []

# Tell Groq which tools are available and their inputs
tools = [
    {
        "type": "function",
        "function": {
            "name": "detect_filler_words",
            "description": "Detect filler words in a candidate's answer.",
            "parameters": {
                "type": "object",
                "properties": {
                    "answer": {"type": "string"}
                },
                "required": ["answer"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_star_structure",
            "description": "Check the STAR components in an answer.",
            "parameters": {
                "type": "object",
                "properties": {
                    "answer": {"type": "string"}
                },
                "required": ["answer"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "score_relevance",
            "description": "Score an answer's relevance from 0 to 100.",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {"type": "string"},
                    "answer": {"type": "string"},
                    "expected_keywords": {
                        "type": "array",
                        "items": {"type": "string"}
                    }
                },
                "required": ["question", "answer", "expected_keywords"]
            }
        }
    }
]


def evaluate_answer(question, answer):
    messages = [
        {
            "role": "system",
            "content": (
                "You are Elevate, an encouraging interview coach. "
                "Use all three evaluation tools. Identify expected keywords "
                "for relevance scoring. Give concise feedback based on results."
            )
        },
        {
            "role": "user",
            "content": f"Question: {question}\nAnswer: {answer}"
        }
    ]

    evaluation_results = {}

    for _ in range(5):
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0
        )

        message = response.choices[0].message
        messages.append(message)

        if not message.tool_calls:
            feedback = message.content or "No feedback generated."

            # Save the complete evaluation in session memory
            session_history.append({
                "question": question,
                "answer": answer,
                "evaluation": evaluation_results.copy(),
                "feedback": feedback
            })

            return feedback

        for tool_call in message.tool_calls:
            name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            if name not in tool_functions:
                result = {"error": "Unknown tool"}
            else:
                result = tool_functions[name](**arguments)

            evaluation_results[name] = result

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

    return "Evaluation could not be completed."



def generate_final_report():
    if not session_history:
        return {"message": "No evaluations available yet."}

    scores = [
        {
            "question": item["question"],
            "score": item["evaluation"].get(
                "score_relevance", {}
            ).get("relevance_score", 0)
        }
        for item in session_history
    ]

    average_score = round(
        sum(item["score"] for item in scores) / len(scores), 2
    )

    weakest = min(scores, key=lambda item: item["score"])

    return {
        "total_questions": len(scores),
        "average_relevance_score": average_score,
        "weakest_area": weakest["question"],
        "lowest_relevance_score": weakest["score"]
    }


def ask_agent(user_question):
    if not session_history:
        return "Let's evaluate an answer first so I can track your progress."

    history = json.dumps(session_history, indent=2)

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Elevate, an encouraging interview coach. "
                    "Answer the candidate using the complete interview "
                    "history provided. Base insights on all evaluations, "
                    "not just the latest answer. Identify the weakest "
                    "question using the lowest relevance score. "
                    "Do not invent scores or evaluations."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Complete interview history:\n{history}\n\n"
                    f"Candidate's question: {user_question}"
                )
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    print(evaluate_answer(
        "Tell me about a time you improved a process.",
        "I automated a report, reducing processing time by 40%."
    ))

    print(evaluate_answer(
        "Describe a challenging project.",
        "It was challenging, and I worked on it."
    ))

    print("\nSession history:")
    for item in session_history:
        print(item["question"])
        print(item["evaluation"].get("score_relevance", {}))


    print("\nFinal Report:")
    print(generate_final_report())

    print("\nMid-session question:")
    print(ask_agent("How am I doing so far?"))


import gradio as gr

from main import (
    evaluate_answer,
    ask_agent,
    generate_final_report,
    session_history,
)

QUESTIONS = [
    "Tell me about a time you improved a process.",
    "Describe a challenging project you worked on.",
    "Tell me about a time you resolved a conflict.",
    "Describe a situation where you used data to make a decision.",
]


def get_scorecard():
    rows = []
    for item in session_history:
        evaluation = item["evaluation"]
        relevance = evaluation.get("score_relevance", {})
        rows.append([
            item["question"],
            relevance.get("relevance_score", 0),
            item["feedback"],
        ])
    return rows


def submit_answer(index, answer):
    if index >= len(QUESTIONS):
        return (
            "Interview complete!",
            "You've answered all sample questions.",
            get_scorecard(),
            index,
            "",
        )

    if not answer or not answer.strip():
        return (
            QUESTIONS[index],
            "Please enter an answer first.",
            get_scorecard(),
            index,
            answer or "",
        )

    question = QUESTIONS[index]
    feedback = evaluate_answer(question, answer)

    next_index = index + 1
    next_question = (
        QUESTIONS[next_index]
        if next_index < len(QUESTIONS)
        else "Interview complete! Generate your final report."
    )

    return (
        next_question,
        feedback,
        get_scorecard(),
        next_index,
        "",
    )


def coach_reply(question):
    if not question.strip():
        return "Please enter a question for your coach."
    return ask_agent(question)


def final_report():
    return generate_final_report()


with gr.Blocks(title="Elevate") as demo:
    gr.Markdown("# Elevate 🎯")
    gr.Markdown("Your AI-powered mock interview coach")

    question_index = gr.State(0)

    current_question = gr.Textbox(
        label="Current Interview Question",
        value=QUESTIONS[0],
        interactive=False,
    )

    answer_box = gr.Textbox(
        label="Your Answer",
        placeholder="Type your interview answer here...",
        lines=5,
    )

    submit_btn = gr.Button("Submit Answer", variant="primary")
    feedback = gr.Markdown(label="Feedback")

    scorecard = gr.Dataframe(
        headers=["Question", "Relevance Score", "Feedback"],
        label="Live Scorecard",
        interactive=False,
    )

    submit_btn.click(
        fn=submit_answer,
        inputs=[question_index, answer_box],
        outputs=[
            current_question,
            feedback,
            scorecard,
            question_index,
            answer_box,
        ],
    )

    gr.Markdown("## Ask Your Interview Coach")

    coach_question = gr.Textbox(
        label="Ask about your progress",
        placeholder="What's my weakest area so far?",
    )
    coach_btn = gr.Button("Ask Coach")
    coach_response = gr.Markdown()

    coach_btn.click(
        fn=coach_reply,
        inputs=coach_question,
        outputs=coach_response,
    )

    gr.Markdown("## Final Interview Report")

    report_btn = gr.Button("Generate Final Report")
    report_output = gr.JSON(label="Aggregated Report")

    report_btn.click(
        fn=final_report,
        outputs=report_output,
    )


if __name__ == "__main__":
    demo.launch()

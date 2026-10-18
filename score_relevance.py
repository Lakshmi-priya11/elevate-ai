
def score_relevance(question: str, answer: str, expected_keywords: list) -> dict:
    """Score an answer based on expected keyword matches."""

    answer_lower = answer.lower()

    matched_keywords = [
        keyword for keyword in expected_keywords
        if keyword.lower() in answer_lower
    ]

    score = (
        round(len(matched_keywords) / len(expected_keywords) * 100)
        if expected_keywords else 0
    )

    return {
        "relevance_score": score,
        "matched_keywords": matched_keywords,
        "missing_keywords": [
            keyword for keyword in expected_keywords
            if keyword not in matched_keywords
        ]
    }


if __name__ == "__main__":
    question = "How have you used Python for data analysis?"
    answer = "I used Python and pandas to clean data and analyse trends."

    expected_keywords = ["Python", "pandas", "data cleaning", "visualisation"]

    print(score_relevance(question, answer, expected_keywords))

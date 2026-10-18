
def check_star_structure(answer: str) -> dict:
    """Check which STAR components appear in an interview answer."""

    keywords = {
        "situation": ["situation", "context", "background", "when"],
        "task": ["task", "responsible for", "goal", "needed to"],
        "action": ["I did", "I implemented", "I created", "I developed"],
        "result": ["result", "achieved", "improved", "increased", "reduced"]
    }

    answer_lower = answer.lower()
    components = {}

    for component, words in keywords.items():
        components[component] = any(
            word.lower() in answer_lower for word in words
        )

    return {
        "star_components": components,
        "components_present": [
            component for component, present in components.items() if present
        ],
        "components_missing": [
            component for component, present in components.items() if not present
        ]
    }


if __name__ == "__main__":
    answer = """
    Our team had a reporting problem. I was responsible for improving
    the process. I developed an automated dashboard, which reduced
    reporting time by 40%.
    """

    print(check_star_structure(answer))

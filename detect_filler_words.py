
import re

def detect_filler_words(answer: str) -> dict:
    """Detect and count common filler words in an interview answer."""

    filler_words = ["um", "like", "basically"]
    answer = answer.lower()

    counts = {}

    for word in filler_words:
        # Match whole words rather than parts of other words
        pattern = rf"\b{re.escape(word)}\b"
        matches = re.findall(pattern, answer)
        counts[word] = len(matches)

    total = sum(counts.values())

    return {
        "filler_words": counts,
        "total_filler_words": total
    }


# Test the function independently
if __name__ == "__main__":
    answer = (
        "Um, I basically worked on a project and, like, "
        "improved the reporting process."
    )

    result = detect_filler_words(answer)
    print(result)

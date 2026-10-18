
from main import evaluate_answer, generate_final_report, session_history

# Evaluate a strong answer
evaluate_answer(
    "Tell me about a time you improved a process.",
    "Our reporting was slow. I automated the workflow using Python, "
    "reducing processing time by 40% and improving accuracy."
)

# Evaluate a deliberately weak answer
evaluate_answer(
    "Describe your experience resolving a conflict.",
    "I don't know. There was a problem, and it got resolved."
)

# Check the aggregated report
report = generate_final_report()

print("\nMemory Check Report:")
print(report)

weakest_question = report.get("weakest_area")
expected_question = "Describe your experience resolving a conflict."

if weakest_question == expected_question:
    print("\nPASS: The weak answer was identified as the weakest area.")
else:
    print("\nFAIL: The weakest question was not identified correctly.")
    print("Expected:", expected_question)
    print("Actual:", weakest_question)

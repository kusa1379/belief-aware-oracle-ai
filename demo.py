from src.wrapper import OracleEpistemicCopilot
import json

print("===== Running Belief-Aware Oracle Payroll Copilot Demo =====")

# Load ontology from your .txt file
with open("src/ontology_workflow.txt") as f:
    ontology_raw = f.read()
print("\nLoaded ontology_workflow.txt")

# Initialize copilot
copilot = OracleEpistemicCopilot()

# Demo input based on your project
user_query = "I am running QuickPay for Emp001 for the month of May, no retro."
actions = [
    {"stage": "SelectPerson", "event": "select", "value": "Emp001"},
    {"stage": "SetPeriod", "event": "set", "value": "Apr"},
    {"stage": "ConfigureRetro", "event": "set", "value": "on"}
]

print("\n=== USER QUERY ===")
print(user_query)

answer, epimsgs = copilot.answer(user_query, actions)

print("\n=== MODEL EXPLANATION ===")
print(answer)

print("\n=== EPISTEMIC MESSAGES ===")
for m in epimsgs:
    print("-", m)

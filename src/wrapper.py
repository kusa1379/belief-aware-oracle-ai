import os
from openai import OpenAI
from typing import List, Dict, Any, Optional
from src.belief_store import (init_belief_state, update_from_elot,
                          update_from_action_log, detect_mismatches,
                          belief_to_epistemic_messages)
from src.epistemic_parser import parse_to_elot

def get_api_key():
    key = os.getenv("OPENAI_API_KEY")

    if key is None or len(key.strip()) < 20:
        print("\n No valid OpenAI API key detected.")
        print("If you want to use the real LLM, please paste your API key now.")
        print("Otherwise, just press ENTER to continue with MOCK LLM.\n")

        user_key = input(" Paste your OpenAI API key (or press Enter to skip): ").strip()

        if len(user_key) < 20:
            print("\n Proceeding with MOCK LLM mode (no API key).\n")
            return None

        # save key for current runtime
        os.environ["OPENAI_API_KEY"] = user_key
        print("\n API key saved. Using REAL OpenAI LLM.\n")
        return user_key

    print ("\n Using previously configured OpenAI API key.")
    return key


API_KEY = get_api_key()
 
# init client (will use the key from Cell 2)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def real_llm(system: str, user: str) -> str:
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ]
    )
    return resp.choices[0].message.content.strip()

class OracleEpistemicCopilot:
    def __init__(self, ontology=None):
        self.belief = init_belief_state()

    def ingest_intention(self, text: str):
        elot = parse_to_elot(text)
        self.belief = update_from_elot(self.belief, elot)
        return elot

    def ingest_actions(self, actions: List[Dict[str, Any]]):
        self.belief = update_from_action_log(self.belief, actions)

    def answer(self, user_text: str, actions: Optional[List[Dict[str, Any]]] = None):
        if actions:
            self.ingest_actions(actions)

        elot = parse_to_elot(user_text)
        self.belief = update_from_elot(self.belief, elot)

        mismatches = detect_mismatches(self.belief)
        epi_msgs = belief_to_epistemic_messages(self.belief, mismatches)

        system_prompt = (
            "You are an Oracle Payroll copilot with epistemic awareness.\n"
            "Consider user's inferred beliefs and point out mismatches with calibrated language.\n"
            f"Epistemic state: {epi_msgs}\n"
        )

        return real_llm(system_prompt, user_text), epi_msgs



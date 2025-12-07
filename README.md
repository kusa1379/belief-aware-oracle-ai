**How to Run and Test the Belief-Aware Oracle Copilot**

This guide explains how to run the project in Google Colab and test the epistemic reasoning pipeline.
It includes instructions for mock LLM mode and real LLM mode via an OpenAI API key prompt.

**1. Run the Project in Google Colab (Recommended)**

You can run the entire system with three commands, no uploads required.

Step 1 — Clone the Repository:
**!git clone https://github.com/kusa1379/belief-aware-oracle-ai.git**
**%cd belief-aware-oracle-ai**

<img width="959" height="368" alt="image" src="https://github.com/user-attachments/assets/74f95234-c93b-42b6-b38e-86cbe544c925" />

you Will see all the Files imported into the colab session.

Step 2 — Install Dependencies
**!pip install -r requirements.txt**

<img width="734" height="344" alt="image" src="https://github.com/user-attachments/assets/4296db66-71e5-4327-aa31-51b70d1ff029" />

Step 3 — Run the Demo

**!python demo.py**

When You run the above command it will ask you for the API Key, Please enter you API key in Suggested Place. and Press Entre.

<img width="1477" height="288" alt="image" src="https://github.com/user-attachments/assets/991662e2-ebc3-4773-8339-1975b8e9f7a0" />

**API Key Prompt Behavior (IMPORTANT)**
Because we implemented interactive API-key handling in wrapper.py, running demo.py will show:

 No valid OpenAI API key detected.
If you want to use the real LLM, please paste your API key now.
Otherwise, just press ENTER to continue with MOCK LLM.

 Paste your OpenAI API key (or press Enter to skip): **PLEASE ENTER YOUR API KEY HERE**

 **2. Testing Custom Inputs**

You can test your own user queries and action logs: Using Below Code ina colab cell

**from src.wrapper import OracleEpistemicCopilot**

**copilot = OracleEpistemicCopilot()**

**user_query = "Run QuickPay for kusa1379 for June, without retro."**
**actions = [
**    {"stage": "SelectPerson", "value": "300145"},
**   {"stage": "SetPeriod", "value": "Apr"},      # mismatch
**    {"stage": "RetroFlag", "value": "On"}        # mismatch
**]**

**answer, epi = copilot.answer(user_query, actions)**
**print(answer)**
**print(epi)**




**For complete Architecture and Code functionality Please Check Project Paper**


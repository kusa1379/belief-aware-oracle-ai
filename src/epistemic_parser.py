import re
from typing import Dict, Any

PERIODS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
PAYROLL_TYPES = ["QuickPay", "Regular", "Batch", "OffCycle"]
RETRO_WORDS_ON = ["retro on", "with retro", "allow retro", "retro should be considered"]
RETRO_WORDS_OFF = ["no retro", "retro off", "disable retro", "retro should not run"]

def _guess_period(text: str):
    for p in PERIODS:
        if p.lower() in text.lower():
            return p
    return None

def _guess_payroll_type(text: str):
    for t in PAYROLL_TYPES:
        if t.lower() in text.lower():
            return t
    if "quick" in text.lower():
        return "QuickPay"
    if "batch" in text.lower():
        return "Batch"
    return None

def _guess_retro(text: str):
    low = text.lower()
    for pat in RETRO_WORDS_OFF:
        if pat in low:
            return "off"
    for pat in RETRO_WORDS_ON:
        if pat in low:
            return "on"
    return None

def _guess_person(text: str):
    m = re.search(r"(Emp\\d{3})", text)
    if m:
        return m.group(1)
    return None

def parse_to_elot(text: str) -> Dict[str, Any]:
    period = _guess_period(text)
    payroll_type = _guess_payroll_type(text)
    retro = _guess_retro(text)
    person = _guess_person(text)

    elot_facts = []

    if period:
        elot_facts.append({"op": "believes","agent": "user","prop": {"slot": "period", "value": period}})
    if payroll_type:
        elot_facts.append({"op": "believes","agent": "user","prop": {"slot": "payroll_type", "value": payroll_type}})
    if retro:
        elot_facts.append({"op": "believes","agent": "user","prop": {"slot": "retro", "value": retro}})
    if person:
        elot_facts.append({"op": "believes","agent": "user","prop": {"slot": "person", "value": person}})

    if not elot_facts:
        elot_facts.append({"op": "might","agent": "user","prop": {"raw": text}})

    return {"elot": elot_facts, "raw": text}

from typing import Dict, Any, List

DEFAULT_THRESHOLDS = {
    "might": 0.20,
    "likely": 0.70,
    "believes": 0.75,
    "must": 0.95
}

def init_belief_state() -> Dict[str, Dict[str, float]]:
    return {
        "period": {},
        "payroll_type": {},
        "retro": {},
        "person": {},
        "stage": {"Navigate": 1.0}
    }

def normalize_slot(slot_dict: Dict[str, float]):
    total = sum(slot_dict.values())
    if total == 0:
        return
    for k in list(slot_dict.keys()):
        slot_dict[k] = slot_dict[k] / total

def update_from_elot(belief: Dict[str, Dict[str, float]], elot_obj: Dict[str, Any],
                     strength: float = 0.9):
    for fact in elot_obj.get("elot", []):
        prop = fact["prop"]
        if "slot" not in prop:
            continue
        slot = prop["slot"]
        val = prop["value"]
        if slot not in belief:
            belief[slot] = {}
        prior = belief[slot].get(val, 0.0)
        belief[slot][val] = max(prior, strength)
        normalize_slot(belief[slot])
    return belief

def update_from_action_log(belief: Dict[str, Dict[str, float]],
                           actions: List[Dict[str, Any]]):
    for act in actions:
        stage = act.get("stage")
        if stage:
            belief["stage"] = {stage: 1.0}
        if stage == "SetPeriod" and act.get("event") == "set":
            actual_period = act.get("value")
            belief["period"][actual_period] = 1.0
            normalize_slot(belief["period"])
        if stage == "ConfigureRetro" and act.get("event") == "set":
            actual_retro = act.get("value")
            belief["retro"][actual_retro] = 1.0
            normalize_slot(belief["retro"])
        if stage == "SelectPerson" and act.get("event") == "select":
            p = act.get("value")
            belief["person"][p] = 1.0
            normalize_slot(belief["person"])
        if stage == "SetPayrollType" and act.get("event") == "set":
            pt = act.get("value")
            belief["payroll_type"][pt] = 1.0
            normalize_slot(belief["payroll_type"])
    return belief

def detect_mismatches(belief: Dict[str, Dict[str, float]],
                      thresholds: Dict[str, float] = DEFAULT_THRESHOLDS):
    mismatches = []
    for slot, dist in belief.items():
        if slot == "stage":
            continue
        if not dist:
            continue
        sorted_vals = sorted(dist.items(), key=lambda x: x[1], reverse=True)
        if len(sorted_vals) >= 2:
            top, top_p = sorted_vals[0]
            second, second_p = sorted_vals[1]
            if top_p >= 0.6 and second_p >= 0.4:
                mismatches.append({
                    "slot": slot,
                    "type": "conflict",
                    "values": [(top, top_p), (second, second_p)]
                })
    return mismatches

def belief_to_epistemic_messages(belief, mismatches,
                                 thresholds: Dict[str, float] = DEFAULT_THRESHOLDS):
    messages = []
    period_dist = belief.get("period", {})
    if period_dist:
        best_period, p = max(period_dist.items(), key=lambda x: x[1])
        if p >= thresholds["must"]:
            messages.append(f"The user must be intending period {best_period}.")
        elif p >= thresholds["believes"]:
            messages.append(f"The user likely intends period {best_period}.")
        elif p >= thresholds["might"]:
            messages.append(f"The user might be intending period {best_period}.")
    retro_dist = belief.get("retro", {})
    if retro_dist:
        best_retro, p = max(retro_dist.items(), key=lambda x: x[1])
        if p >= thresholds["believes"]:
            messages.append(f"The user likely wants retro '{best_retro}'.")
    for m in mismatches:
        slot = m["slot"]
        vals = ", ".join([f"{v} ({p:.2f})" for v, p in m["values"]])
        messages.append(f"Epistemic mismatch in {slot}: {vals}")
    return messages

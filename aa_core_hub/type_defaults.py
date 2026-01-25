TYPE_DEFAULTS = {
    2233:  {"type_name": "Customs Office", "nearest": "PLANET", "has_fit": False, "can_set_reinforcement": False, "jitter_hours": None},
    81080: {"type_name": "Orbital Skyhook", "nearest": "PLANET", "has_fit": False, "can_set_reinforcement": False, "jitter_hours": None},
    35832: {"type_name": "Astrahus", "nearest": "ANYWHERE", "has_fit": True, "can_set_reinforcement": True, "jitter_hours": 1.5},
    35833: {"type_name": "Fortizar", "nearest": "ANYWHERE", "has_fit": True, "can_set_reinforcement": True, "jitter_hours": 3},
    35834: {"type_name": "Keepstar", "nearest": "ANYWHERE", "has_fit": True, "can_set_reinforcement": True, "jitter_hours": 3},
    35825: {"type_name": "Raitaru", "nearest": "ANYWHERE", "has_fit": True, "can_set_reinforcement": True, "jitter_hours": 1.5},
    35826: {"type_name": "Azbel", "nearest": "ANYWHERE", "has_fit": True, "can_set_reinforcement": True, "jitter_hours": 3},
    35827: {"type_name": "Sotiyo", "nearest": "ANYWHERE", "has_fit": True, "can_set_reinforcement": True, "jitter_hours": 3},
    35835: {"type_name": "Athanor", "nearest": "ANYWHERE", "has_fit": True, "can_set_reinforcement": True, "jitter_hours": 1.5},
    35836: {"type_name": "Tatara", "nearest": "ANYWHERE", "has_fit": True, "can_set_reinforcement": True, "jitter_hours": 3},
    35840: {"type_name": "Pharolux Cyno Beacon", "nearest": "ANYWHERE", "has_fit": False, "can_set_reinforcement": True, "jitter_hours": 0.5},
    37534: {"type_name": "Tenebrex Cyno Jammer", "nearest": "ANYWHERE", "has_fit": False, "can_set_reinforcement": True, "jitter_hours": 0.5},
    35841: {"type_name": "Ansiblex Jump Gate", "nearest": "ANYWHERE", "has_fit": False, "can_set_reinforcement": True, "jitter_hours": 0.5},
    81826: {"type_name": "Metenox Moon Drill", "nearest": "MOON", "has_fit": False, "can_set_reinforcement": True, "jitter_hours": 1},
    85230: {"type_name": "Mercenary Den", "nearest": "PLANET", "has_fit": False, "can_set_reinforcement": False, "jitter_hours": 24},
}

def get_defaults(type_id):
    if not type_id:
        return None
    return TYPE_DEFAULTS.get(int(type_id))

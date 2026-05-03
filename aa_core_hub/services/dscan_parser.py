def classify_dscan_type(type_name: str) -> str:
    normalized = (type_name or "").lower()
    if "upwell structure" in normalized:
        return "STRUCTURE"
    if any(term in normalized for term in ("astrahus", "fortizar", "keepstar", "raitaru", "azbel", "sotiyo")):
        return "STRUCTURE"
    if any(term in normalized for term in ("athanor", "tatara", "metenox")):
        return "STRUCTURE"
    if any(term in normalized for term in ("customs office", "orbital skyhook", "mercenary den")):
        return "STRUCTURE"
    if any(term in normalized for term in ("cyno beacon", "cyno jammer", "ansiblex")):
        return "SOV"
    if "scanner probe" in normalized or normalized.endswith(" probe"):
        return "PROBE"
    if any(term in normalized for term in ("wreck", "container", "mobile tractor unit", "deployable")):
        return "DEPLOYABLE"
    if normalized:
        return "SHIP_OR_OBJECT"
    return ""


def parse_dscan_line(line: str):
    columns = [column.strip() for column in line.split("\t")]
    if len(columns) >= 4:
        object_id, name, type_name, distance = columns[:4]
        return {
            "name": name or object_id,
            "type_name": type_name,
            "distance": distance,
            "category": classify_dscan_type(type_name),
        }
    if len(columns) == 3:
        name, type_name, distance = columns
        return {
            "name": name,
            "type_name": type_name,
            "distance": distance,
            "category": classify_dscan_type(type_name),
        }
    return None


def parse_dscan(text: str):
    items = []
    for line in (text or "").splitlines():
        line = line.strip()
        if not line:
            continue
        item = parse_dscan_line(line)
        if not item:
            continue
        items.append(item)
    return items

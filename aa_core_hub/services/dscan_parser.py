import re

_LINE_RE = re.compile(r"^(?P<name>.+?)\t(?P<type>.+?)\t(?P<distance>.+?)$")


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


def parse_dscan(text: str):
    items = []
    for line in (text or "").splitlines():
        line = line.strip()
        if not line:
            continue
        m = _LINE_RE.match(line)
        if not m:
            continue
        type_name = m.group("type").strip()
        items.append(
            {
                "name": m.group("name").strip(),
                "type_name": type_name,
                "distance": m.group("distance").strip(),
                "category": classify_dscan_type(type_name),
            }
        )
    return items

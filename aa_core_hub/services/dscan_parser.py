import re
from typing import List, Dict

_LINE_RE = re.compile(r"^(?P<name>.+?)\t(?P<type>.+?)\t(?P<distance>.+?)$")

def parse_dscan(text: str) -> List[Dict[str, str]]:
    """Very small parser for tab-separated D-Scan exports.
    Child plugins can provide richer parsing and categorization.
    """
    items = []
    for line in (text or "").splitlines():
        line = line.strip()
        if not line:
            continue
        m = _LINE_RE.match(line)
        if not m:
            continue
        items.append({
            "name": m.group("name").strip(),
            "type_name": m.group("type").strip(),
            "distance": m.group("distance").strip(),
        })
    return items

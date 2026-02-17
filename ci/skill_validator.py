#!/usr/bin/env python3
import json
import os
import sys
import re

# Atslēgvārdi, kas norāda uz nedeterministisku uzvedību
FORBIDDEN_KEYWORDS = [
    "ai decide", "llm interpret", "free form", "best guess", 
    "creative", "model should decide", "approximate"
]

# Atļautie datu tipi (JSON Schema stils)
ALLOWED_TYPES = {"string", "number", "integer", "boolean", "object", "array", "null"}

# Obligātie lauki skill.json failā
REQUIRED_FIELDS = {
    "name", "version", "description", "inputs", "outputs"
}

def fail(errors):
    print(json.dumps({
        "status": "fail", 
        "count": len(errors),
        "errors": errors
    }, indent=2))
    sys.exit(1)

def ok():
    print(json.dumps({"status": "ok", "message": "All skills validated successfully."}))
    sys.exit(0)

def validate_schema_node(node, path, errors):
    """Rekursīvi pārbauda tipus ievades/izvades definīcijās."""
    if isinstance(node, str):
        # Vienkāršais gadījums: "field": "string"
        if node not in ALLOWED_TYPES:
             errors.append(f"Invalid type '{node}' at {path}")
    elif isinstance(node, dict):
        # Sarežģītais gadījums: "field": { "type": "string", ... }
        if "type" in node:
            t = node["type"]
            if t not in ALLOWED_TYPES:
                errors.append(f"Invalid type '{t}' at {path}.type")
        # Ja ir nested objekti vai masīvi, šeit varētu pievienot dziļāku pārbaudi
    else:
        errors.append(f"Unknown schema format at {path}")

def validate_skill(skill_dir):
    errors = []
    skill_json_path = os.path.join(skill_dir, "skill.json")
    
    # 1. Vai skill.json eksistē?
    if not os.path.exists(skill_json_path):
        # Ja mapē nav skill.json, varbūt tā nav prasme, bet tikai utilīta.
        # Bet ja tā ir `skills/` apakšmapē, mēs gribam brīdināt vai ignorēt.
        # Šoreiz pieņemam: katrai apakšmapei iekš skills/ jābūt skill.json
        return [{ "file": skill_dir, "error": "skill.json missing in skill directory" }]

    try:
        with open(skill_json_path, 'r', encoding='utf-8') as f:
            skill = json.load(f)
    except Exception as e:
        return [{ "file": skill_json_path, "error": f"Invalid JSON: {str(e)}" }]

    # 2. Obligātie lauki
    missing = REQUIRED_FIELDS - skill.keys()
    if missing:
        errors.append({ "file": skill_json_path, "error": f"Missing required fields: {', '.join(missing)}" })

    # 3. Ievades/Izvades validācija
    for section in ["inputs", "outputs"]:
        if section in skill:
            if not isinstance(skill[section], dict):
                 errors.append({ "file": skill_json_path, "error": f"'{section}' must be an object (map)" })
            else:
                for k, v in skill[section].items():
                    validate_schema_node(v, f"{section}.{k}", errors)

    # 4. Aizliegtie atslēgvārdi (Meklējam visā failā)
    raw_content = json.dumps(skill).lower()
    for word in FORBIDDEN_KEYWORDS:
        if word in raw_content:
            errors.append({ "file": skill_json_path, "error": f"Forbidden keyword detected: '{word}'" })

    return errors

def main():
    all_errors = []
    skills_root = "skills"
    
    if not os.path.exists(skills_root):
        print(json.dumps({"status": "skipped", "message": "skills/ directory not found"}))
        sys.exit(0)

    # Staigājam tikai pa tiešajām apakšmapēm (skills/viena-prasme, skills/otra-prasme)
    # Tas novērš problēmas ar node_modules vai dziļām struktūrām
    for item in os.listdir(skills_root):
        item_path = os.path.join(skills_root, item)
        if os.path.isdir(item_path):
            errs = validate_skill(item_path)
            all_errors.extend(errs)

    if all_errors:
        fail(all_errors)
    else:
        ok()

if __name__ == "__main__":
    main()

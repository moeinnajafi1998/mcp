import os
import sys
import json
import django

# اضافه کردن مسیر پروژه به PYTHONPATH
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

# معرفی settings پروژه Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from mcp.tools import TOOL_REGISTRY


def main():
    for line in sys.stdin:
        if not line.strip():
            continue  # ignore empty lines
        try:
            payload = json.loads(line.strip())
        except json.JSONDecodeError:
            response = {"success": False, "error": "Invalid JSON input"}
            sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
            sys.stdout.flush()
            continue

        try:
            tool_name = payload.get("tool")
            input_data = payload.get("input", {})

            if tool_name not in TOOL_REGISTRY:
                raise ValueError(f"Tool '{tool_name}' not found")

            result = TOOL_REGISTRY[tool_name](**input_data)

            response = {"success": True, "data": result}

        except Exception as e:
            response = {"success": False, "error": str(e)}

        sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()

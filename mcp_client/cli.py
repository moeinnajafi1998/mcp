import subprocess
import json
import sys

# Command to run MCP Server
MCP_COMMAND = [
    sys.executable,
    "mcp\\server.py"  # Windows path
]


def send_to_mcp(payload: dict):
    """Send payload to MCP Server and get response"""
    process = subprocess.Popen(
        MCP_COMMAND,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    process.stdin.write(json.dumps(payload, ensure_ascii=False) + "\n")
    process.stdin.flush()

    output = process.stdout.readline()
    process.terminate()
    return json.loads(output)


def parse_prompt(prompt: str):
    """Convert user prompt to tool + input"""
    prompt = prompt.strip()

    if "list" in prompt.lower():
        return {"tool": "list_tasks", "input": {}}

    if "create" in prompt.lower():
        # Extract title after 'create'
        title = prompt.lower().replace("create", "").strip()
        return {"tool": "create_task", "input": {"title": title}}

    if "status" in prompt.lower():
        # Example: "set status of task 1 to done"
        parts = prompt.split()
        try:
            task_id = int(parts[4])  # "task 1" -> 1
            status = parts[-1]        # last word -> status
            return {"tool": "update_task_status", "input": {"id": task_id, "status": status}}
        except:
            raise ValueError("Cannot parse status command")

    if "delete" in prompt.lower():
        # Example: "delete task 1"
        parts = prompt.split()
        try:
            task_id = int(parts[2])
            return {"tool": "delete_task", "input": {"id": task_id}}
        except:
            raise ValueError("Cannot parse delete command")

    raise ValueError("Command not recognized")


if __name__ == "__main__":
    print("=== MCP Client ===")
    print("Enter your command. Type 'exit' or 'quit' to leave.\n")

    while True:
        try:
            user_input = input(">>> ")
        except KeyboardInterrupt:
            print("\nExiting...")
            break

        if user_input.lower() in ("exit", "quit"):
            print("Exiting...")
            break

        try:
            payload = parse_prompt(user_input)
        except Exception as e:
            print(f"❌ Command parsing error: {e}")
            continue

        try:
            response = send_to_mcp(payload)
            print(json.dumps(response, indent=2, ensure_ascii=False))
        except Exception as e:
            print(f"❌ Error communicating with MCP Server: {e}")

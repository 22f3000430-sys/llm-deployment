import os
import time

BASE_DIR = "generated_apps"

def generate_app(task_data: dict) -> str:
    """
    Generate a minimal app folder from task_data.
    Returns the folder path.
    """
    base_name = task_data["task"]
    unique_name = f"{base_name}-{int(time.time())}"

    folder_path = os.path.join(BASE_DIR, unique_name)
    os.makedirs(folder_path, exist_ok=True)

    # Create a simple index.html
    index_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{task_data['task']}</title>
</head>
<body>
    <h1>{task_data['brief']}</h1>
    <p>Generated at {time.ctime()}</p>
</body>
</html>"""

    with open(os.path.join(folder_path, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)

    # Create a README
    with open(os.path.join(folder_path, "README.md"), "w", encoding="utf-8") as f:
        f.write(f"# {task_data['task']}\n\nGenerated app for task: {task_data['brief']}")

    # Optionally add CSS/JS folder structure
    os.makedirs(os.path.join(folder_path, "assets"), exist_ok=True)
    with open(os.path.join(folder_path, "assets", "style.css"), "w") as f:
        f.write("body { font-family: Arial, sans-serif; }")

    return folder_path

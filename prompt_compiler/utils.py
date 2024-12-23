from pathlib import Path


def load_template(template_path: Path) -> str:
    """Load template file content."""
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path: Path, content: str) -> None:
    """Write content to file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

import json
from pathlib import Path
from typing import Any, Dict, List
from jinja2 import Environment, FileSystemLoader

# Paths
SCENARIOS_DIR: Path = Path("./scenarios")
RENDERED_DIR: Path = Path("./scenarios_rendered")

def find_templates(base_dir: Path) -> List[Path]:
    """ Recursively find all Jinja templates in the directory. """
    return list(base_dir.rglob("*.jinja"))

def load_config(config_path: Path) -> Dict[str, Any]:
    """ Load JSON configuration if available, else return an empty dict. """
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def render_template(template_path: Path, global_values: Dict[str, Any]) -> str:
    """ Render the Jinja template with given global values. """
    env = Environment(loader=FileSystemLoader(template_path.parent))
    template = env.get_template(template_path.name)
    return template.render(global_values)

def process_templates() -> None:
    templates = find_templates(SCENARIOS_DIR)

    for template_path in templates:
        # Determine corresponding JSON config file
        config_path = template_path.with_suffix(".config.json")
        global_values = load_config(config_path)

        if not global_values:
            print(f"Skipping {template_path} (No config found or empty values)")
            continue

        # Render the entire Jinja file using global values
        rendered_content = render_template(template_path, global_values)

        # Determine output path (same directory, but with .json extension)
        relative_path = template_path.relative_to(SCENARIOS_DIR)
        output_path = RENDERED_DIR / relative_path.with_suffix(".json")

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write the rendered content to a JSON file
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(json.loads(rendered_content), f, indent=4)

        print(f"Rendered {template_path} -> {output_path}")

if __name__ == "__main__":
    process_templates()
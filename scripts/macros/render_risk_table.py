import yaml
import os
from scripts.macros.helpers.load_yaml_cached import load_yaml

def render_risk_table(env, data_path):
    risk_file = os.path.join(env.project_dir, 'data', 'risks.yaml')
    full_data = load_yaml(risk_file)

    try:
        data = full_data
        for key in data_path.split('.'):
            data = data[key]
    except (KeyError, AttributeError):
        return f"**ERROR:** Path `{data_path}` not found."

    headers = ["ID", "Description", "Probability", "Impact", "Level", "Mitigation"]

    markdown_lines = []

    header_line = "| " + " | ".join(headers) + " |"
    
    separator_parts = []
    for idx, _ in enumerate(headers):
        if idx == 0:
            separator_parts.append(":---")
        else:
            separator_parts.append(":---:")
    separator_line = "| " + " | ".join(separator_parts) + " |"

    markdown_lines.append(header_line)
    markdown_lines.append(separator_line)

    for row_key, row_data in data.items():
        if not isinstance(row_data, dict):
            continue
            
        row_cells = []
        for col_name in headers:
            if col_name == "ID":
                val = f"**{row_key}**{{: #{row_key} }}"
            else:
                data_key = col_name.lower()
                raw_val = row_data.get(data_key, '-')

                if isinstance(raw_val, list):
                    val = "<br>".join([str(v) for v in raw_val])
                else:
                    val = str(raw_val)
            
            row_cells.append(val)

        markdown_lines.append("| " + " | ".join(row_cells) + " |")

    return "\n".join(markdown_lines)
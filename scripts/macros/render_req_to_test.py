import os
from scripts.macros.helpers.load_yaml_cached import load_yaml

def render_req_to_test(env):
    
    STATUS_COLORS = {
        "Draft": "orange",
        "Pass": "green",
        "Fail": "red",
        "Unknown": "grey",
    }

    tests_file = os.path.join(env.project_dir, 'data', 'tests.yaml')
    if os.path.exists(tests_file):
      raw_test_data = load_yaml(tests_file)
    else:
      return f'!!! danger\n    File **{os.path.relpath(tests_file, env.project_dir)}** not found.'

    md_table = [
        "| Requirement ID | Test ID | Status |",
        "|:-----------------|:----------|:-------|"
    ]

    for test_id in sorted(raw_test_data.keys()):
        if not test_id.startswith('TST_'):
            continue

        test_info = raw_test_data[test_id]
        req_id = test_id.replace('TST', 'REQ')
        
        status = test_info.get('metadata', {}).get('status', 'Unknown')
        status_color = STATUS_COLORS.get(status, STATUS_COLORS["Unknown"])
        if status_color == 'grey':
          status = f'<span style="color:{status_color}; font-weight: bold;">Unknown</span>'
        else:
          status = f'<span style="color:{status_color}; font-weight: bold;">{status}</span>'
          
        req_link = f"[{req_id}](../01_requirements/SRS.md#{req_id})"
        test_link = f"[{test_id}](../03_verification/TST_{test_id.split('_')[1]}.md#{test_id})"

        row = f"| {req_link} | {test_link} | {status} |"
        md_table.append(row)

    return "\n".join(md_table)
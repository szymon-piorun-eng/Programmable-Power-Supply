import os
from scripts.macros.helpers.load_yaml_cached import load_yaml

def get_all_requirements(data):
    req_codes = set()
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'requirement_code':
                if isinstance(value, list):
                    for item in value:
                        req_codes.add(item.split('**')[1]) 
                elif isinstance(value, str) and '**' in value:
                    req_codes.add(value.split('**')[1])
            else:
                req_codes.update(get_all_requirements(value))        
    elif isinstance(data, list):
        for item in data:
            req_codes.update(get_all_requirements(item))
            
    return req_codes

def render_test_header(env, test_id, equipment_list=None):
    STATUS_MAPPING = {
    "Draft": "orange",
    "Pass": "green",
    "Fail": "red",
    "Unknown": "grey",
    }
    req_file = os.path.join(env.project_dir, 'data', 'requirements.yaml')
    tests_file = os.path.join(env.project_dir, 'data', 'tests.yaml')

    if os.path.exists(req_file):
      req_data = load_yaml(req_file)
      known_req_codes = get_all_requirements(req_data)   
    else:
      return f'\n!!! danger\n    File **{os.path.relpath(req_file, env.project_dir)}** not found.'
    
    if os.path.exists(tests_file):
      raw_test_data = load_yaml(tests_file)
      defined_equipment = raw_test_data.get('equipment', {})
      allowed_tools = set(defined_equipment.get('general', []))
    else:
      return f'\n!!! danger\n    File **{os.path.relpath(tests_file, env.project_dir)}** not found.'
    
    if test_id not in raw_test_data:
      return f'\n!!! danger\n    Test **{test_id}** not defined in **{os.path.relpath(tests_file, env.project_dir)}**.'
    
    test_data = raw_test_data[test_id]

    allowed_tools.update(defined_equipment.get(test_data['metadata']['type'].lower(), []))   

    title = f"{test_data['id']}: {test_data['title']}\n"

    req_code = test_id.replace("TST", "REQ")
    metadata = f"!!!info\n    "

    if req_code not in known_req_codes:
      metadata = f"{metadata}!!!warning\n    Requirement {req_code} is not defined in {os.path.relpath(req_file, env.project_dir)}.\n"
    else:
      metadata = f"{metadata}* **Traceability**: [{req_code}](../01_requirements/SRS.md#{req_code})\n"

    metadata = f"{metadata}    * **Type**: {test_data['metadata']['type']}\n"

    current_status = test_data['metadata'].get('status', 'Unknown')
    status_color = STATUS_MAPPING.get(current_status, "grey")
    if status_color == "grey":
      metadata =f"{metadata}    !!!warning\n        Current status of {test_id} is **Unknown**!\n"
    else: 
      metadata = f'{metadata}    * **Status**: <span style="color:{status_color}; font-weight: bold;">{current_status}</span>\n'
    
    test_equipment = f'###Test equipment\n'
    if equipment_list:
       for tool in equipment_list:
          if tool in allowed_tools:
             test_equipment = f"{test_equipment}* {tool}\n"
          else:
             test_equipment = f"{test_equipment}!!!warning\n    Tool **{tool}** not available in **{test_data['metadata']['type']}** type test!\n"
    else:
       test_equipment =f"{test_equipment}!!! danger\n    Equipment for this test was not specified!"
    return f"{title}{metadata}{test_equipment}"

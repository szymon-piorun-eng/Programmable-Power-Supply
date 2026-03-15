import os
from scripts.macros.helpers.load_yaml_cached import load_yaml
from scripts.macros.helpers.build_req_index import build_req_index

def get_req_val(env, req_id, column_name):

  req_file = os.path.join(env.project_dir, 'data', 'requirements.yaml')
  if os.path.exists(req_file):
      raw_data = load_yaml(req_file)
  else:
    return f'\n!!! danger\n    File **{os.path.relpath(req_file, env.project_dir)}** not found.'

  req_index = build_req_index(raw_data)
        
  if req_id not in req_index:
    return f'\n!!! warning\n    Requirement **{req_id}** is not defined in **{os.path.relpath(req_file, env.project_dir)}**.'
            
  entry = req_index[req_id]
  row_data = entry['row_data']
  list_index = entry['list_index']
        
  target_key = column_name.lower().replace(" ", "_")
        
  if target_key not in row_data:
    return f"\n!!! warning\n    Requirement **{req_id}** does not have **{column_name}** parameter."
             
  raw_value = row_data[target_key]
        
  if isinstance(raw_value, list):
    if list_index < len(raw_value):
      return raw_value[list_index]
    else:
      return f"\n!!! warning\n    Value for **{req_id}** not specified correctly."
                
  return raw_value
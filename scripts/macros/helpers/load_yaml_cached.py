import os
import yaml

_YAML_CACHE = {}

def load_yaml(file_path):
    
    global _YAML_CACHE
    
    if not os.path.exists(file_path):
        return None

    current_mtime = os.path.getmtime(file_path)
    
    if file_path not in _YAML_CACHE or current_mtime > _YAML_CACHE[file_path]['mtime']:
        print(f"[Macro] Loading and parsing file into cache: {os.path.basename(file_path)}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                parsed_data = yaml.safe_load(f)
                
            _YAML_CACHE[file_path] = {
                'data': parsed_data,
                'mtime': current_mtime
            }
        except Exception as e:
            print(f"[Macro Error] Error while parsing YAML {file_path}: {e}")
            return None

    return _YAML_CACHE[file_path]['data']
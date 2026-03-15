def clean_req_id(raw_id):
    if isinstance(raw_id, str) and '**' in raw_id:
        return raw_id.split('**')[1]
    return raw_id

def build_req_index(data, current_columns=None, index=None):

    if index is None:
        index = {}
        
    if isinstance(data, dict):
        columns = data.get('columns', current_columns)
        
        if 'requirement_code' in data:
            req_codes = data['requirement_code']
            
            if isinstance(req_codes, str):
                req_codes = [req_codes]
                
            for i, raw_code in enumerate(req_codes):
                c_id = clean_req_id(raw_code)
                if c_id:
                    index[c_id] = {
                        'row_data': data,       
                        'columns': columns,     
                        'list_index': i         
                    }
        
        for key, value in data.items():
            build_req_index(value, columns, index)
            
    elif isinstance(data, list):
        for item in data:
            build_req_index(item, current_columns, index)
            
    return index
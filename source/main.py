from typing import Dict
import json

from CSCHC_Context import Context
        

if __name__ == '__main__':
    filename: str = './data/example.json'
    
    with open(file=filename, mode='r') as file:
        microschc_context: Dict = json.load(file)

    context: Context = Context(json_data=microschc_context)
    context.display_cschc_context()
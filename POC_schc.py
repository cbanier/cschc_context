from typing import Dict
import json

from source.CSCHC_Context import Context
from source.yang_tools import display_cbor, model_to_CORECONF


if __name__ == '__main__':
    print("=> IETF YANG MODEL")
    print(f"Current representation defined by {'./data/yang-model/ietf-schc@2023-03-01.yang'}")
    print(f"   Example associated is {(ietf_example := './data/yang-model/ietf_model.json')}")
    display_cbor(model_to_CORECONF(ietf_sid := './data/yang-model/ietf-schc@2023-03-01.sid', ietf_example))

    print("=> DRAFT YANG MODEL")
    print(f"Draft representation defined by {'./data/yang-model/draft-ietf-schc.yang'}")
    print(f"   Example associated is {(draft_example := './data/yang-model/draft_ietf_schc_model.json')}")
    display_cbor(model_to_CORECONF(draft_sid := './data/yang-model/draft-ietf-schc@unknown.sid', draft_example))

    print("=> CSCHC")
    print(f"   Example Microschc Context defined by {(filename := './data/yang-model/microschc_yang_example.json')}")
    with open(file=filename, mode='r') as file:
        microschc_context: Dict = json.load(file)
    context: Context = Context(json_data=microschc_context, auto_format=True)

    print(f"   CSCHC Context data (hex) : {context.hexadecimal_cschc_context()}")
    print(f"   CSCHC Context data length (bytes) : {len(context.cschc_context)}")
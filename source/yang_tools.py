from typing import List
import cbor2
import pycoreconf


def model_to_CORECONF(sid_filename: str, config_filename: str) -> bytes:
    ccm: pycoreconf.CORECONFModel = pycoreconf.CORECONFModel(sid_filename)
    cbor_data: bytes              = ccm.toCORECONF(config_filename)
    return cbor_data


def list_to_cbor(data: List[int]) -> bytes:
    cbor_data: bytes = cbor2.dumps(data)
    return cbor_data


def display_cbor(cbor_data: bytes) -> None:
    print(f'   CBOR data (hex) : {cbor_data.hex()}')
    print(f'   CBOR data length (bytes) : {len(cbor_data)}\n')
    return
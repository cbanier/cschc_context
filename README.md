<!-- 
Author: Corentin Banier
Date: 2024-08-27
-->

# CSCHC Context

## CSCHC Context Builder

### Overview

`cschc_context` is a tool designed to generate a SCHC Compression Context for the [CSCHC](https://github.com/quentinlampin/cschc) library from a JSON Context produced by [microschc](https://github.com/quentinlampin/microschc).
`main.py` shows an example usage of it.

### Features

- Converts JSON Context from `microschc` to a format compatible with `cschc`, i.e., a list of `uint8_t`.
- Ensures seamless integration between `microschc` and `cschc`.

## POC SCHC Yang Model

### Overview

`POC_schc.py` highlights how the current [SCHC Yang Model](https://datatracker.ietf.org/doc/html/rfc9363) could be improved. This POC demonstrates how we can drastically reduce the amount of data during context generation. This example still needs to be enhanced, but it illustrates the main idea that could be applied in the future.

### Features

* Data:
 
  * [ietf-schc@2023-03-01.yang](./data/yang-model/ietf-schc@2023-03-01.yang) is the current IETF SCHC Yang Model.
 
  * [ietf-schc@2023-03-01.sid](./data/yang-model/ietf-schc@2023-03-01.sid) is an example of SID allocation from `ietf-schc@2023-03-01.yang`. It is generated using pyang (see [requirements.txt](./requirements.txt)).
 
  * [draft-ietf-schc.yang](./data/yang-model/draft-ietf-schc.yang) is a proposal that simplifies the current Yang Model. We introduce the concept of indexes. Instead of defining a whole hierarchy, we try to optimize repetitions. As a Rule Field Descriptor could appear in several Rule Descriptors, and a Target Value could also be associated with various Rule Field Descriptors, we decided to store the index of every object. The winning rate is obvious because we avoid redundancy. This is the same idea used for the CSCHC Context but generalized with Yang.

  * [draft-ietf-schc@unknown.sid](./data/yang-model/draft-ietf-schc@unknown.sid) is an example of SID allocation from `draft-ietf-schc.yang`.

  * [ietf_model.json](./data/yang-model/ietf_model.json) is an example of Context definition in JSON following the `ietf-schc@2023-03-01.yang` paradigm. 

  * [draft_ietf_schc_model.json](./data/yang-model/draft_ietf_schc_model.json) is an example of Context definition in JSON following the `draft-ietf-schc.yang` paradigm.

  * [microschc_yang_example.json](./data/yang-model/microschc_yang_example.json) is an example of Context definition in JSON following the `microschc` paradigm.

_NB: Context examples are, of course, equivalent but are written using different paradigms._

* `POC_schc.py`: This file shows the corresponding CBOR hexadecimal representation and its length in octets. We can observe that for this example, there is a factor of 2 between the current Yang Model and the draft. At the end, the CSCHC representation is also displayed, which is quite more compact than the draft.

### Usage
```zsh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 POC_schc.py
```
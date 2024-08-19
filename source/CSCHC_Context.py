from typing import Dict, List

from CSCHC_maps import *
from microschc_interpreter import extract_informations_from_json
from utils import int_to_2_bytes, byte_length


class Context:
    def __init__(self, json_data: Dict) -> None:
        self.microschc_context: Dict = json_data
        self.cschc_context: List[int] = []
        self.is_formatted: bool = False
        self.rule_descriptors, self.rule_field_descriptors,\
            self.target_values = extract_informations_from_json(json_data)

    
    def compute_cschc_context(self) -> None:
        self.__create_cschc_context()
        self.__update_offset()


    def display_cschc_context(self) -> None:
        if not self.is_formatted:
            self.compute_cschc_context()
        print(self.__string_cschc_context())
        
        return


    def __create_cschc_context(self):
        # CSCHC Context
        self.cschc_context.append(self.microschc_context['id'])
        self.cschc_context.append(card_rd := len(self.rule_descriptors))
        self.cschc_context += ['RD_offset1', 'RD_offset2'] * card_rd
        
        # CSCHC Rule Descriptors
        for i in range(len(self.rule_descriptors)):
            self.rule_descriptors[i]['offset'] = len(self.cschc_context)

            self.cschc_context.append(int(self.rule_descriptors[i]['id']['content'], 16))
            self.cschc_context.append(RuleNature_Map[self.rule_descriptors[i]['nature']])
            
            card_rfd: int = len(self.rule_descriptors[i].get('field_descriptors', []))
            self.cschc_context.append(card_rfd)
            self.cschc_context += ['RDF_offset1', 'RDF_offset2'] * card_rfd
        
        # CSCHC Rule Field Descriptors
        for i in range(len(self.rule_field_descriptors)):
            self.rule_field_descriptors[i]['offset'] = len(self.cschc_context)

            self.cschc_context += int_to_2_bytes(SID_Map[self.rule_field_descriptors[i]['id']])
            self.cschc_context += int_to_2_bytes(self.rule_field_descriptors[i]['length'])
            self.cschc_context += int_to_2_bytes(self.rule_field_descriptors[i]['position'])
            self.cschc_context.append(
                (DirectionIndicator_Map[self.rule_field_descriptors[i]['direction']] << 5) |\
                (MatchingOperator_Map[self.rule_field_descriptors[i]['matching_operator']] << 3) |\
                CompressionDecompressionAction_Map[self.rule_field_descriptors[i]['compression_decompression_action']]
            )   

            if self.rule_field_descriptors[i]['matching_operator'] == 'MSB':
                self.cschc_context \
                    += int_to_2_bytes(
                        self.target_values[self.rule_field_descriptors[i]['target_value'][0]]['length']
                    )

            if self.rule_field_descriptors[i]['matching_operator'] == 'match-mapping':
                card_rfd: int = len(self.rule_field_descriptors[i]['target_value'])
            elif self.rule_field_descriptors[i]['matching_operator'] == 'ignore':
                card_rfd: int = 0
            else:
                card_rfd: int = 1

            self.cschc_context.append(card_rfd)
            self.cschc_context += ['TV_offset1', 'TV_offset2'] * card_rfd 

        # CSCHC Target Values
        for tv in self.target_values:
            tv['offset'] = len(self.cschc_context)
            self.cschc_context \
                += [int(tv['content'][i:i + 2], 16)\
                    for i in range(0, byte_length(tv['length']) * 2, 2)] # convert hex to int

        return
    

    def __update_offset(self):
        rule_descriptor_context_offset: int = 2

        for rule_descriptor in self.rule_descriptors:
            self.cschc_context[rule_descriptor_context_offset],\
                self.cschc_context[rule_descriptor_context_offset + 1]\
                    = int_to_2_bytes(rule_descriptor['offset'])
            
            rule_descriptor_context_offset += 2
            rule_field_descriptor_context_offset: int = rule_descriptor['offset'] + 2

            if self.cschc_context[rule_field_descriptor_context_offset] > 0: # RuleNature is Compression
                
                for i, index_rule_field_descriptor in enumerate(rule_descriptor['field_descriptors'], start=1):
                    self.cschc_context[rule_field_descriptor_context_offset + i * 2 - 1],\
                        self.cschc_context[rule_field_descriptor_context_offset + i * 2]\
                            = int_to_2_bytes(self.rule_field_descriptors[index_rule_field_descriptor]['offset'])
                    
                    target_value_context_offset: int\
                        = self.rule_field_descriptors[index_rule_field_descriptor]['offset'] + 7

                    if self.rule_field_descriptors[index_rule_field_descriptor]['matching_operator'] == 'MSB':
                        target_value_context_offset += 2
                    
                    if self.cschc_context[target_value_context_offset] > 0: # if 0 then no 'target_value' key

                        for j, index_target_value in\
                              enumerate(
                                    self.rule_field_descriptors[index_rule_field_descriptor]['target_value'],\
                                    start=1
                            ):
                            self.cschc_context[target_value_context_offset + j * 2 - 1],\
                                self.cschc_context[target_value_context_offset + j * 2]\
                                    = int_to_2_bytes(self.target_values[index_target_value]['offset'])

        self.is_formatted = True
        
        return


    def __string_cschc_context(self) -> str:
        output: str = '{\n\t// Context\n\t'
        
        # Context
        offset: int  = 0
        card_rd: int = len(self.rule_descriptors)

        while offset < len(self.cschc_context[0 : 2 + card_rd * 2]):
            output += f'{self.cschc_context[offset]}, '
            offset += 1
        
        # Rule Descriptor
        output += '\n\n\t// Rule Descriptors\n'
            
        for i in range(card_rd):
            output += '\t'

            if i == card_rd - 1:
                offset = next_offset
                next_offset: int = self.rule_field_descriptors[0]['offset']
            else:
                offset = self.rule_descriptors[i]['offset']
                next_offset: int = self.rule_descriptors[i + 1]['offset']

            while offset < next_offset:
                output += f'{self.cschc_context[offset]}, '
                offset += 1

            output += f' // Rule Descriptor n° {i}\n'

        # Rule Field Descriptor
        output += '\n\t// Rule Field Descriptors\n'

        card_rfd: int = len(self.rule_field_descriptors)
        
        for i in range(card_rfd):
            output += '\t'

            if i == card_rfd - 1:
                offset = next_offset
                next_offset = self.target_values[0]['offset']
            else:
                offset = self.rule_field_descriptors[i]['offset']
                next_offset = self.rule_field_descriptors[i + 1]['offset']

            while offset < next_offset :
                output += f'{hex(self.cschc_context[offset])}, '
                offset += 1
                    
            output += f' // Rule Field Descriptor n° {i}\n'
              
        # Target Value
        output += '\n\t// Target Values\n\t'
        
        next_offset = len(self.cschc_context)
        while offset < next_offset:
            if offset == next_offset - 1:
                output += f'{hex(self.cschc_context[offset])}'
            else:
                output += f'{hex(self.cschc_context[offset])}, '

            offset += 1            

        output += '\n}'
        
        return output
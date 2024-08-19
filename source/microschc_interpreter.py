from typing import Any, Dict, List, Tuple


def extract_informations_from_json(data: Dict) -> Tuple[List[Dict], List[Dict], List[Dict]]:
    all_rule_descriptor: List[Dict]       = []
    all_rule_field_descriptor: List[Dict] = []
    all_target_value: List[Dict]          = []

    _: List[int] = __extract_rule_descriptor_from_json(
        data['ruleset'], 
        all_rule_descriptor, 
        all_rule_field_descriptor, 
        all_target_value
    )
    return all_rule_descriptor, all_rule_field_descriptor, all_target_value


def __append_item(elements: List, item: Any) -> int:
    if item not in elements:
        elements.append(item)
    return elements.index(item)


def __extract_target_value_from_json(target_values: Any, all_target_value: List[Dict]) -> Any:
    if isinstance(target_values, list):
        target_values = [__append_item(all_target_value, tv['value']) for tv in target_values]
        return target_values
    return [__append_item(all_target_value, target_values)]


def __extract_rule_field_descriptor_from_json(rule_field_descriptors: List[Dict], 
                                              all_rule_field_descriptor: List[Dict], 
                                              all_target_value: List[Dict]) -> List[int]:
    for ind_rule_f_desc in range(len(rule_field_descriptors)):
        if 'target_value' in rule_field_descriptors[ind_rule_f_desc]:
            rule_field_descriptors[ind_rule_f_desc]['target_value'] = __extract_target_value_from_json(
                rule_field_descriptors[ind_rule_f_desc]['target_value'], all_target_value
            )
        rule_field_descriptors[ind_rule_f_desc] = __append_item(
                                                    all_rule_field_descriptor, 
                                                    rule_field_descriptors[ind_rule_f_desc]
                                                )
    return rule_field_descriptors


def __extract_rule_descriptor_from_json(rule_descriptors: List[Dict], 
                                        all_rule_descriptor: List[Dict], 
                                        all_rule_field_descriptor: List[Dict], 
                                        all_target_value: List[Dict]) -> List[int]:
    for rule_desc in rule_descriptors:
        if 'field_descriptors' in rule_desc:
            rule_desc['field_descriptors'] = __extract_rule_field_descriptor_from_json(
                                                rule_desc['field_descriptors'], 
                                                all_rule_field_descriptor, 
                                                all_target_value
                                            )
        rule_desc = __append_item(all_rule_descriptor, rule_desc)
    return rule_descriptors
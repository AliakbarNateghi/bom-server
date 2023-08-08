import json


def compare_instance_with_dict(instance, data_dict):
    # print(f'instance.ID : {instance.ID}')
    for key, value in instance.__dict__.items():
        print(f"key: {key}")
        print(f"\ndata_dict : {data_dict[key]}")
        if key not in data_dict:
            return False
    # The instance and the dictionary have the same values.
    return True


def delete_common_keys_values(json_data, dictionary):
    json_dict = json.loads(json_data)
    common_keys = set(json_dict.keys()) & set(dictionary.keys())
    for key in common_keys:
        del json_dict[key]
    common_values = set(json_dict.values()) & set(dictionary.values())
    for key, value in json_dict.items():
        if value in common_values:
            del json_dict[key]
    modified_json = json.dumps(json_dict)
    return modified_json

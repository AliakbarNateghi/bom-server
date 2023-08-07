def compare_instance_with_dict(instance, data_dict):
    # print(f'instance.ID : {instance.ID}')
    for key, value in instance.__dict__.items():
        print(f'key: {key}')
        print(f'\ndata_dict : {data_dict[key]}')
        if key not in data_dict:
            return False
    # The instance and the dictionary have the same values.
    return True

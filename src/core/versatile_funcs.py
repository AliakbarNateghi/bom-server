def compare_instance_with_dict(instance, data_dict):
    for key, value in data_dict.items():
        if getattr(instance, key) != value:
            # The instance and the dictionary have different values.
            return False
    # The instance and the dictionary have the same values.
    return True

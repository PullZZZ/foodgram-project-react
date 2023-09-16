
def unique_in_list(list_for_check):
    """Проверяет элементы списка на уникальность"""
    counter_dict = {}
    for item in list_for_check:
        if counter_dict.get(item, 0) > 0:
            return False
        counter_dict[item] = 1
    return True

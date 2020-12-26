from app.common.helpers import month_number_to_text


def transform_result_value(key, value):
    """ Transform value from db to be sent to fe"""
    if key == "id":
        return str(value)
    if key == "mes":
        return month_number_to_text(value)
    if key == "puesto":
        return "Oro" if value == 1 else "Plata" if value == 2 else "Bronce" if value == 3 \
            else None if not value else value

    return value


def transform_values(values_dict):
    """ Transform values from fe to be sent to db """
    result = {}
    for key, value in values_dict.items():
        value = value.strip()
        if key == 'puesto':
            mapper = {
                'oro': 1,
                'plata': 2,
                'bronce': 3
            }
            result[key] = mapper.get(value.lower()) or value
        else:
            result[key] = value
    return result

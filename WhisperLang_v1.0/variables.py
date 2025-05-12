variables = {}


def resolve_value(val):
    return variables.get(val, val)
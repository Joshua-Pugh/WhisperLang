def cast(value):
    print(f"[DEBUG] Casting: {value}")
    if isinstance(value, (int, float)):
        return value
    value = value.strip()
    # Handle percentages
    if value.endswith("%"):
        try:
            return float(value[:-1]) / 100
        except ValueError:
            return value
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value     # fallback to string


def format_output(value):
    if isinstance(value, str) and value.isalpha():
        return value.capitalize()
    return value

from variables import variables
from utils import cast
import operator

# Maps human-readable phrases to actual operator symbols
operator_map = {
    "is": "==",
    "equals": "==",
    "is not": "!=",
    "not equal to": "!=",
    "greater than": ">",
    "greater than or equal to": ">=",
    "less than": "<",
    "less than or equal to": "<="
}

# Maps operator symbols to actual functions
safe_ops = {
    "==": operator.eq,
    "!=": operator.ne,
    ">": operator.gt,
    ">=": operator.ge,
    "<": operator.lt,
    "<=": operator.le
}


def evaluate_condition(text):
    print(f"[DEBUG] Evaluating condition: '{text}'")

    if " and " in text:
        parts = text.split(" and ")
        return evaluate_condition(parts[0]) and evaluate_condition(parts[1])
    elif " or " in text:
        parts = text.split(" or ")
        return evaluate_condition(parts[0]) or evaluate_condition(parts[1])

    for op_phrase in sorted(operator_map, key=len, reverse=True):
        if op_phrase in text:
            try:
                var_part, val_part = text.split(op_phrase, 1)
                var_part = var_part.strip()
                val_part = val_part.strip()

                left = cast(variables.get(var_part, var_part))
                right = cast(variables.get(val_part, val_part))  # fallback to literal

                op_symbol = operator_map[op_phrase]
                op_func = safe_ops.get(op_symbol)

                print(f"[DEBUG] Left: {left}, Operator: {op_symbol}, Right: {right}")

                if op_func:
                    return op_func(left, right)
                else:
                    print(f"[error] Unsupported operator: {op_symbol}")
            except Exception as e:
                print(f"[error] Failed to evaluate: {text} ({e})")
            return False

    print(f"[error] No valid operator found in: {text}")
    return False
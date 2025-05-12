from variables import variables, resolve_value
from utils import cast

# -----------------------
# Utility: Shared evaluator for binary operations
# -----------------------


def evaluate_binary_operation(expr, keyword, connector, operation):
    try:
        left, right = expr.replace(keyword, "", 1).split(connector)
        return operation(
            cast(resolve_value(left.strip())),
            cast(resolve_value(right.strip()))
        )
    except Exception as e:
        print(f"[error] failed to evaluate '{expr}': {e}")
        return 0

# -----------------------
# Command Handlers
# -----------------------


def handle_add(line):
    if " to " not in line:
        print("[error] invalid syntax. Use: add X to Y")
        return
    value, var = line.replace("add", "", 1).split(" to ")
    var = var.strip()
    if var in variables:
        variables[var] += evaluate_expression(value.strip())
    else:
        print(f"[error] variable '{var}' not defined")


def handle_subtract(line):
    print(f"[DEBUG] Expression for subtract: {line}")
    if " from " not in line:
        print("[error] invalid syntax. Use: subtract X from Y")
        return
    var, value = line.replace("subtract", "", 1).split(" from ")
    var = var.strip()
    print(f"[DEBUG] Variable is: {var}, Value is: {value}")
    if var in variables:
        variables[var] -= evaluate_expression(value.strip())
    else:
        print(f"[error] variable '{var}' not defined")


def handle_multiply(line):
    if " by " not in line:
        print("[error] invalid syntax. Use: multiply X by Y")
        return
    var, value = line.replace("multiply", "", 1).split(" by ")
    var = var.strip()
    if var in variables:
        variables[var] *= evaluate_expression(value.strip())
    else:
        print(f"[error] variable '{var}' not defined")


def handle_divide(line):
    if " by " not in line:
        print("[error] invalid syntax. Use: divide X by Y")
        return
    var, value = line.replace("divide", "", 1).split(" by ")
    var = var.strip()
    div_val = evaluate_expression(value.strip())
    if var in variables:
        if div_val == 0:
            print("[error] can't divide by zero")
        else:
            variables[var] /= div_val
    else:
        print(f"[error] variable '{var}' not defined")


def handle_round(line):
    parts = line.split()
    var_name = parts[1]
    places = 2
    if "to" in parts:
        index = parts.index("to")
        places = int(parts[index + 1])
    elif len(parts) >= 3 and parts[2].isdigit():
        places = int(parts[2])
    if var_name in variables:
        variables[var_name] = round(variables[var_name], places)


# -----------------------
# Expression Evaluators
# -----------------------

def evaluate_add(expr):
    return evaluate_binary_operation(expr, "add", " to ", lambda a, b: a + b)


def evaluate_subtract(expr):
    return evaluate_binary_operation(expr, "subtract", " from ", lambda a, b: a - b)


def evaluate_multiply(expr):
    return evaluate_binary_operation(expr, "multiply", " by ", lambda a, b: a * b)


def evaluate_divide(expr):
    return evaluate_binary_operation(expr, "divide", " by ", lambda a, b: 0 if b == 0 else a / b)


def evaluate_sum(expr):
    items = expr.replace("sum of", "", 1).split(",")
    return sum(cast(resolve_value(i.strip())) for i in items)


def evaluate_average(expr):
    items = expr.replace("average of", "", 1).split(",")
    values = [cast(resolve_value(i.strip())) for i in items]
    return sum(values) / len(values) if values else 0


def evaluate_max(expr):
    items = expr.replace("max of", "", 1).split(",")
    return max(cast(resolve_value(i.strip())) for i in items)


def evaluate_min(expr):
    items = expr.replace("min of", "", 1).split(",")
    return min(cast(resolve_value(i.strip())) for i in items)


def evaluate_abs(expr):
    val = expr.replace("absolute value of", "", 1).strip()
    return abs(cast(resolve_value(val)))


def evaluate_round(expr):
    parts = expr.split()
    var_name = parts[1]
    places = 2
    if "to" in parts:
        idx = parts.index("to")
        places = int(parts[idx + 1])
    elif len(parts) == 3 and parts[2].isdigit():
        places = int(parts[2])
    val = resolve_value(var_name)
    return round(cast(val), places)

# -----------------------
# Master Router
# -----------------------


def evaluate_expression(expr):
    expr = expr.strip().lower()

    if expr.startswith("sum of"):
        return evaluate_sum(expr)
    if expr.startswith("average of"):
        return evaluate_average(expr)
    if expr.startswith("max of"):
        return evaluate_max(expr)
    if expr.startswith("min of"):
        return evaluate_min(expr)
    if expr.startswith("absolute value of"):
        return evaluate_abs(expr)
    if expr.startswith("add") and " and " in expr:
        return evaluate_add(expr)
    if expr.startswith("subtract") and " from " in expr:
        return evaluate_subtract(expr)
    if expr.startswith("multiply") and " by " in expr:
        return evaluate_multiply(expr)
    if expr.startswith("divide") and " by " in expr:
        return evaluate_divide(expr)
    if expr.startswith("round"):
        return evaluate_round(expr)

    # Fallback to literal or variable
    return cast(resolve_value(expr))
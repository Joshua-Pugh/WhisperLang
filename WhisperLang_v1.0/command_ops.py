from variables import variables
from utils import format_output
from math_ops import evaluate_expression


def handle_say(line):
    _, value = line.split(maxsplit=1)
    words = value.split()
    output = []

    for i, word in enumerate(words):
        if word in variables:
            val = str(variables[word])
            output.append(format_output(val) if i == 0 else val)

        else:
            output.append(word.capitalize() if i == 0 else word)

    print(" ".join(output))


def handle_set(line):
    if " to " not in line:
        print("[error] invalid set syntax: Use: set x to y")
        return
    line = line.replace("set", "", 1).strip()
    var_name, expr = line.split(" to ", 1)
    var_name = var_name.strip()
    expr = expr.strip()
    variables[var_name] = evaluate_expression(expr)
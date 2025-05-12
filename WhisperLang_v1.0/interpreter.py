from math_ops import (handle_add, handle_round, handle_multiply, handle_subtract, handle_divide)
from command_ops import handle_say, handle_set

# WhisperLang Interpreter v0.1
variables = {}
command_map = {
    "add": handle_add,
    "divide": handle_divide,
    "multiply": handle_multiply,
    "print": handle_say,
    "round": handle_round,
    "say": handle_say,
    "set": handle_set,
    "subtract": handle_subtract
}


def interpreter(line):
    line = line.strip().lower()  # Remove extra spaces, ignore case
    for keyword, handler in command_map.items():
        if line.startswith(keyword):
            print(f"[DEBUG] Executing handler: {handler.__name__}")
            handler(line)
            return
    print(f"[error] could not understand: {line}")

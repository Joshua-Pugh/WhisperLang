from interpreter import interpreter
from logic import evaluate_condition
from parser import parse_blocks


def interpret_block(block):
    blocks = parse_blocks(block[1:] if block[0].strip().endswith(":") else block)

    for b_type, b_content in blocks:
        if b_type == "block":
            interpret_block(b_content)
        elif b_type == "normal":
            interpreter(b_content[0])


def interpret_if_else_block(if_block, else_block=None):
    if not if_block:
        return

    condition = if_block[0][3:-1].strip()
    if_lines = if_block[1:]
    if_blocks = parse_blocks(if_lines)

    else_blocks = []
    if else_block:
        else_lines = else_block[1:]
        else_blocks = parse_blocks(else_lines)

    if evaluate_condition(condition):
        for b_type, b_content in if_blocks:
            if b_type == "block":
                interpret_block(b_content)
            elif b_type == "normal":
                interpreter(b_content[0])
    elif else_blocks:
        for b_type, b_content in else_blocks:
            if b_type == "block":
                interpret_block(b_content)
            elif b_type == "normal":
                interpreter(b_content[0])


def interpret_while_block(block):
    if not block:
        return

    first_line = block[0]
    condition = first_line[6:-1].strip()  # remove "while" and ":"
    nested_lines = block[1:]

    inner_blocks = parse_blocks(nested_lines)  # <- This MUST be here

    loop_counter = 0
    while evaluate_condition(condition):
        for b_type, b_content in inner_blocks:
            if b_type == "if":
                next_type = inner_blocks[inner_blocks.index((b_type, b_content)) + 1][0] \
                    if inner_blocks.index((b_type, b_content)) + 1 < len(inner_blocks) else None
                next_block = inner_blocks[inner_blocks.index((b_type, b_content)) + 1][1] \
                    if next_type == "else" else None
                interpret_if_else_block(b_content, next_block)
            elif b_type == "block":
                interpret_block(b_content)
            elif b_type == "normal":
                interpreter(b_content[0])

        loop_counter += 1
        if loop_counter > 1000:
            print("[warning] loop exceeded 1000 iterations - possible infinite loop")
            break


# For loop function (Key Word: repeat loop | Use: repeat x times)
def interpret_repeat_block(block):
    if not block:
        return

    header = block[0].strip().lower()
    if not header.startswith("repeat"):
        print("[error] invalid repeat syntax")
        return

    # Extract the repeat count
    parts = header.replace("repeat", "").replace("times:", "").strip().split()
    try:
        count = int(parts[0])
    except (IndexError, ValueError):
        print(f"[error] invalid repeat count in line: {header}")
        return

    nested_lines = block[1:]
    nested_blocks = parse_blocks(nested_lines)

    for _ in range(count):
        for tag, content in nested_blocks:
            if tag in ("if", "else"):
                # handled as part of "if" interpreter
                continue
            elif tag == "while":
                interpret_while_block(content)
            elif tag == "repeat":
                interpret_repeat_block(content)
            elif tag == "if":
                # manually pair with else if it exists
                idx = nested_blocks.index((tag, content))
                next_block = nested_blocks[idx + 1] if (idx + 1 < len(nested_blocks) and nested_blocks[idx + 1][0] == "else") else None
                interpret_if_else_block(content, next_block[1] if next_block else None)
            elif tag == "normal":
                interpreter(content[0])
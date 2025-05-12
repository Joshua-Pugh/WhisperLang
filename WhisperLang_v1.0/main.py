from parser import parse_blocks
from control_ops import (interpret_block, interpret_if_else_block, interpret_while_block, interpret_repeat_block)

block_type_map = {
    "if": interpret_if_else_block,
    "while": interpret_while_block,
    "repeat": interpret_repeat_block,
    "normal": interpret_block
}


def run_script(script):
    blocks = parse_blocks(script)
    print(blocks)
    i = 0
    while i < len(blocks):
        block_type, block = blocks[i]
        print(f"[DEBUG] Block Type: {block_type}")
        if block_type == "if":
            next_type = blocks[i +1][0] if i + 1 < len(blocks) else None
            next_block = blocks[i +1][1] if next_type == "else" else None
            interpret_if_else_block(block, next_block)
            i += 2 if next_type == "else" else 1

        else:
            handler = block_type_map.get(block_type, interpret_block)
            handler(block)
            print(f"[DEBUG] Executing handler: {handler.__name__}")
            i += 1


script1 = [
    "set a to 5",
    "set b to 8",
    "set c to 3",
    "multiply a by 2",
    "if a greater than b:",
    "    set x to 3",
    "    set y to 6",
    "    add x to y",
    "    subtract a from 5",
    "    say a",
    "    say x",
    "    say y",
    "else:"
]

run_script(script1)
def parse_blocks(lines):
    def get_indent_level(line):
        return len(line) - len(line.lstrip())

    def group_lines_by_indent(start_index, base_indent):
        block = []
        i = start_index

        while i < len(lines):
            line = lines[i]
            if not line.strip():
                i += 1
                continue

            indent = get_indent_level(line)
            is_new_block = line.strip().endswith(":") and indent == base_indent

            if indent < base_indent or (i != start_index and is_new_block):
                break

            block.append(lines[i])
            i += 1

        return block, i

    blocks = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue

        indent = get_indent_level(line)

        if line.strip().endswith(":"):
            group, new_index = group_lines_by_indent(i, indent)
            header_line = group[0].strip().lower()

            # Tag the type of block
            if header_line.startswith("if "):
                tag = "if"
            elif header_line.startswith("while "):
                tag = "while"
            elif header_line.startswith("repeat"):
                tag = "repeat"
            elif header_line.startswith("else:"):
                tag = "else"
            else:
                tag = "block"

            blocks.append((tag, group))
            i = new_index  # use updated index here

        else:
            blocks.append(("normal", [line]))
            i += 1

    return blocks

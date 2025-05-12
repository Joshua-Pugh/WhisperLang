def build_ast(lines):
    ast = []
    i = 0

    def get_indent_level(line):
        return len(line) - len(line.strip())

    def extract_block(start_index):
        block = []
        base_indent = get_indent_level(lines[start_index])
        i = start_index + 1
        while i < len(lines):
            line = lines[i]
            if not line.strip():
                i += 1
                continue

            indent = get_indent_level(line)
            if indent <= base_indent:
                break
            block.append(lines[i][base_indent:])
            i += 1
        return block, i

    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        # --- Assignments ---
        if line.startswith("set") and " to " in line:
            var, expr = line[4:].split(" to ", 1)
            ast.append({
                "type": "assignment",
                "target": var.strip(),
                "value": expr.strip()
            })

        elif " assigned to " in line:
            var, expr = line.split(" assigned to ", 1)
            ast.append({
                "type": "assignment",
                "target": var.strip(),
                "value": expr.strip()
            })

        # --- Output ---
        elif line.startswith("say ") or line.startswith("print "):
            _, value = line.split(" ", 1)
            ast.append({
                "type": "output",
                "value": value.strip()
            })

        # --- Control Flow ---
        elif line.startswith("if ") and line.endswith(":"):
            condition = line[3:-1].strip()
            body, new_i = extract_block(i)
            ast.append({
                "type": "if",
                "condition": condition,
                "body": build_ast(body)
            })

            i = new_i
            continue

        elif line == "else:":
            body, new_i = extract_block(i)
            ast.append({
                "type": "else",
                "body": build_ast(body)
            })

            i = new_i
            continue

        elif line.startswith("while ") and line.endswith(":"):
            condition = line[6: -1].strip()
            body, new_i = extract_block(i)
            ast.append({
                "type": "while",
                "condition": condition,
                "body": build_ast(body)
            })

            i = new_i
            continue

        elif line.startswith("repeat ") and line.endswith("times:"):
            count = line.replace("repeat", "").replace("times:", "").strip()
            body, new_i = extract_block(i)
            ast.append({
                "type": "repeat",
                "count": count,
                "body": build_ast(body)
            })

            i = new_i
            continue

        # --- Math Commands (mutate variables directly) ---
        elif line.startswith("add ") and " to " in line:
            value, target = line.replace("add", "", 1).split(" to ")
            ast.append({
                "type": "operation",
                "command": "add",
                "target": target.strip(),
                "value": value.strip()
            })

        elif line.startswith("subtract ") and " from " in line:
            value, target = line.replace("subtract", "", 1).split(" from ")
            ast.append({
                "type": "operation",
                "command": "subtract",
                "target": target.strip(),
                "value": value.strip()
            })

        elif line.startswith("multiply ") and " by " in line:
            target, value = line.replace("multiply", "", 1).split(" by ")
            ast.append({
                "type": "operation",
                "command": "multiply",
                "target": target.strip(),
                "value": value.strip()
            })

        elif line.startswith("divide ") and " by " in line:
            target, value = line.replace("divide", "", 1).split(" by ")
            ast.append({
                "type": "operation",
                "command": "divide",
                "target": target.strip(),
                "value": value.strip()
            })

        # --- Unknown (fallback) ---
        else:
            ast.append({
                "type": "unknown",
                "content": line
            })

        i += 1

    return ast

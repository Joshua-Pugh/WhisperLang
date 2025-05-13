# 🗣️ WhisperLang (v0.1)

**A plain-English scripting language interpreter built from scratch in Python.**  
WhisperLang executes human-readable commands like `set x to 5`, `if x greater than 3:`, and `repeat 3 times:`—bridging natural language and logic.

---

## ✨ Features

- ✅ **Human-readable syntax**  
  `set x to 5`, `multiply a by 2`, `say x`
- ✅ **Math operations**  
  `add`, `subtract`, `multiply`, `divide`, `round`
- ✅ **Control flow**  
  `if`, `else`, `while`, `repeat x times`
- ✅ **Variable evaluation** and memory management
- ✅ **Modular design**  
  Built with clean separation: parser, interpreter, logic, and math layers
- ✅ **Debug-friendly**  
  Logs steps using `[DEBUG]` output for transparency and troubleshooting

---

## 🛣️ Roadmap

- [ ] Function definitions and return values  
- [ ] List/array support  
- [ ] User-defined commands/macros  
- [ ] Runtime state inspection tools  
- [ ] REPL with command history and error handling  

---

## 🖼️ Demo

### 🧾 Example Script

```plaintext
set a to 5  
set b to 8  
multiply a by 2  

if a greater than b:
    say a
    say "a is greater"
else:
    say "a is not greater"
```

```plaintext
🔍 Debug Output (Console)

[DEBUG] Executing handler: handle_set
[DEBUG] Executing handler: handle_set
[DEBUG] Executing handler: handle_multiply
[DEBUG] Evaluating condition: 'a greater than b'
[DEBUG] Left: 10, Operator: >, Right: 8
[DEBUG] Executing handler: handle_say
[DEBUG] Executing handler: handle_say
```

### 👤 Author
**Joshua Pugh**  
B.S. in Computer Science & Software Engineering  
*Diesel Technician turned Software Developer*

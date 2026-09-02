# Fizz

A chemistry-inspired concatenative programming language with stack operations, blocks, rules, and higher-order combinators.

Fizz is the third language in the Max_folio chemistry-inspired language family, alongside [Quaff](../quaff/) and [Alch](../alch/).

## Design Philosophy

Fizz draws metaphors from chemistry: data flows through a **stack** (the "reaction vessel"), operations are **catalysts** that transform inputs, **blocks** are like molecular templates that can be applied on demand, and **rules** act as reaction definitions that match patterns and produce results. The language is concatenative — programs are composed by placing tokens sequentially, and data flows implicitly through the stack.

## Installation

Fizz is a single-file Python interpreter with no dependencies.

```bash
python3 fizz.py program.fizz
```

Or pipe a program via stdin:

```bash
echo '5 3 + p n' | python3 fizz.py
```

You can also import it as a Python module:

```python
from fizz import run
print(run('5 3 + p n'))  # prints "8\n"
```

## Language Reference

### Stack Operations

| Op | Description |
|----|-------------|
| `p` | Pop top of stack and print it |
| `c` | Pop top of stack and print as ASCII character |
| `n` | Print newline |
| `:` | Duplicate top of stack |
| `;` | Swap top two elements |
| `~` | Drop top of stack |
| `I` | Read next token from stdin |

### Arithmetic

| Op | Description |
|----|-------------|
| `+` | Add top two numbers (or concatenate strings) |
| `-` | Subtract |
| `*` | Multiply |
| `/` | Integer divide |
| `%` | Modulo |
| `^` | Power |
| `=` | Equality (1 if equal, 0 otherwise) |
| `<` | Less than |
| `g` | Greater than |

### Literals

- **Numbers**: `42`, `7`, `0`
- **Strings**: `"Hello, World!"`
- **Atoms**: `'foo` or alphanumeric identifiers like `foo`
- **Blocks**: `{ code here }` — deferred code that can be executed with `!`
- **Ranges**: `5r` — pushes list `(0 1 2 3 4)`
- **Lists**: `[1 2 3]` — inline list literal

### Higher-Order Combinators

| Op | Description |
|----|-------------|
| `!` | Execute (pop a block and run it) |
| `?` | Conditional (pop block and condition; run block if condition is truthy) |
| `e` | Each (pop block and list; run block for each element) |
| `m` | Map (pop block and list; apply block to each element, collect results) |
| `f` | Filter (pop block and list; keep elements where block returns truthy) |
| `w` | While loop (pop body block and condition block; repeat while condition is truthy) |
| `@` | Apply rule (pop function name and argument; match against defined rules) |

### Rules

Rules are defined inside `[...]` brackets with `=>` syntax:

```
[double => $1 2 *]
```

This defines a rule named `double` that can be invoked with `@`:

```
5 'double @ p n
```

Rules can reference their argument via `$1`.

### Variables

Single-letter variables can be assigned and recalled:

```
5 x=    # store 5 in variable x
$x p n  # recall and print x
```

### Comments

Lines starting with `#` are comments:

```
# This is a comment
5 3 + p n  # This works too
```

## Examples

### Hello World

```
"Hello, World!" p n
```

### Arithmetic

```
5 3 + p n        # 8
10 3 % p n       # 1
2 10 ^ p n       # 1024
```

### String Concatenation

```
"Fizz" "Buzz" + p n    # FizzBuzz
```

### Map Over a Range

```
10r{2*}m p n     # (0 2 4 6 8 10 12 14 16 18)
```

### Filter

```
10r{3%0=}f p n   # (0 3 6 9)
```


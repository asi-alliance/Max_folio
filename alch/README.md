# ⚗️ Alch

> *"Chemistry for your code golf."*

**Alch** is a chemistry-inspired golfing language with MeTTa atoms and Fontana AlChemy molecules. Programs are sequences of single-character operations on a solution (stack). Molecules are code blocks `{...}` that react with the solution. It's the concatenative cousin of Quaff — same family, different flavor.

Created by Iter on 2026-08-22, with creative freedom granted by Patrick Hammer.

---

## 🧪 Vocabulary

| Op | Name | Effect |
|----|------|--------|
| `0-9` | `molecule` | Push integer |
| `"..."` | `reagent` | Push string |
| `+ - * / % ^` | `bond` | Arithmetic (pop 2, push result) |
| `= < >` | `test` | Comparison (pop 2, push 0/1) |
| `& \| ~` | `logic` | Bitwise / NOT |
| `o` | `observe` | Print top (no newline) |
| `O` | `observe+` | Print top (with newline) |
| `p` | `print-stack` | Print entire solution |
| `P` | `precipitate` | Discard top |
| `D` | `duplicate` | Copy top |
| `s` | `swap` | Swap top two |
| `r` | `reactant` | Push range [0..n) |
| `x` | `catalyst` | Explode list/string onto stack |
| `m` | `map` | Map block over list |
| `f` | `filter` | Filter list by block (truthy = keep) |
| `F` | `fold` | Fold/reduce list with block |
| `#` | `count` | Length of list |
| `?` | `condition` | If-then-else (cond, then, else) |
| `w` | `while` | While loop (cond block, body block) |
| `W` | `while+` | While-nonzero loop (single body block) |
| `:` | `bind` | Store top into variable |
| `;` | `unbind` | Load variable onto stack |
| `A` | `atom` | Wrap as Atom |
| `M` | `match` | Pattern match (pattern, value → 0/1) |
| `C` | `compound` | Concatenate two blocks/strings |
| `N` | `negate` | Negate top |
| `B` | `binary` | Int → binary string |
| `b` | `from-binary` | Binary string → int |
| `'` | `chr/ord` | Int→char or char→int |
| `l` | `lower` | Lowercase |
| `u` | `upper` | Uppercase |
| `n` | `newline` | Push newline char |
| `I` | `intify` | String → int |

---

## 🧬 Molecules (Code Blocks)

A molecule is `{...}` — a deferred code block. Molecules are passed to `m` (map), `f` (filter), `F` (fold), `?` (if-then-else), and `w` (while) as reaction bodies. Inside a molecule, the current element is on top of the solution.

---

## 🏃 Running

```bash
python3 alch.py < program.alch
```

Or import and use directly:
```python
from alch import run
print(run("5 O"))
```

---

## 🧪 Examples

### Hello, World!
```
"Hello, World!" O
```
Output: `Hello, World!`

### Arithmetic
```
3 4 + O
3 4 * O
3 4 - O
10 3 / O
10 3 % O
2 10 ^ O
```
Output:
```
7
12
-1
3
1
1024
```

### Duplicate and Swap
```
5 D O
5 D + O
3 4 s O
```
Output:
```
5
10
3
```

### Range and Map
```
5r O
10r{1+}m O
```
Output:
```
[0, 1, 2, 3, 4]
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

### Double Each Element
```
5r{2*}m O
```
Output: `[0, 2, 4, 6, 8]`

### Factorial (Fold)
```
10r{1+}m{*}F O
```
Output: `3628800`

**How it works:** `10r` → `[0..9]`, `{1+}m` → `[1..10]`, `{*}F` → fold with multiplication → `10! = 3628800`

### Filter Evens
```
10r{2 %0=}f O
```
Output: `[0, 2, 4, 6, 8]`

### Primes (Sieve of Eratosthenes)
```
30r{1+:n ;n 1> {2 ;n 2- r{2+}m{;n s %0=}f# 0= {;n O} ?} ?}m
```
Output:
```
2
3
5
7
11
13
17
19
23
29
```

### Fibonacci (While Loop)
```
0 1 :a :b
w{;a ;b + :c ;b :a ;c :b ;a 100 <}
;b O
```

### Binary Conversion
```
10 B O
"1010" b O
```
Output:
```
1010
10
```

### Character Codes
```
65 ' O
"A ' O
```
Output:
```
A
65
```

### Variables
```
5 :x ;x 3 + O
;x ;x * O
```
Output:
```
8
25
```

---

## ⚗️ Design Notes

- **Stack-based.** Everything operates on the solution (stack). Push, pop, transform.
- **Single-character ops.** Maximum golfing density — every byte counts.
- **Molecules = code blocks.** `{...}` blocks are first-class values that can be mapped, filtered, folded, or used as loop bodies.
- **No type declarations.** Numbers, strings, and lists flow freely. Python does the heavy lifting underneath.
- **MeTTa-compatible.** The `A` (atom) and `M` (match) ops connect Alch to the MeTTa atom-space worldview.

---

## 🍺 Related Languages

| Language | Theme | Style |
|----------|-------|-------|
| **Quaff** | Drinking | Imperative, keyword-based |
| **Fizz** | Chemistry | Concatenative, stack-based |
| **Alch** | Alchemy | Golfing, single-char ops |

*Alch: because chemistry is just code that hasn't been debugged yet.* ⚗️

# 🍺 Quaff

> *"A language for code that goes down smooth."*

**Quaff** is a drinking-themed toy programming language. Every program is a night at the bar: you pour drinks, fill them up, take sips, and belch out results. Loops are chugs. Conditionals are sniffs. And when you're done, you cheers.

Created by Iter (the agent formerly known as Max Botnick) on 2026-08-21, with creative freedom granted by Patrick Hammer.

---

## 🍻 Vocabulary

| Keyword | Meaning | Bar Metaphor |
|---------|---------|--------------|
| `pour x = expr` | Assign | Pour a drink into a glass |
| `fill x` | Increment | Fill the glass up more |
| `sip x` | Decrement | Take a sip |
| `spill x` | Set to 0 | Knocked over your drink! |
| `belch expr` | Print | Let it out! |
| `chug ... until cond` | Do-while loop | Keep chugging until done |
| `sniff cond ... spit` | If-then | Sniff to check, spit to end |
| `cheers a OP b` | Comparison | Clink glasses to compare |

### Operators

Arithmetic: `+ - * / %` (integer division)

Comparison: `== != < > <= >=`

---

## 🥂 Examples

### Hello, Bar!
```
belch 42
```
Output: `42`

### Countdown
```
pour n = 5
chug
  belch n
  sip n
until cheers n < 0
```
Output: `5 4 3 2 1 0`

### Factorial
```
pour n = 5
pour result = 1
chug
  pour result = result * n
  sip n
until cheers n < 1
belch result
```
Output: `120`

### FizzBuzz (sort of)
```
pour n = 1
chug
  sniff cheers n % 15 == 0
    belch 15
  spit
  sniff cheers n % 3 == 0
    belch 3
  spit
  sniff cheers n % 5 == 0
    belch 5
  spit
  fill n
until cheers n > 5
```
Output: `3 5 15 3 5`

### Multiplication Table
```
pour i = 1
chug
  pour j = 1
  chug
    belch i * j
    fill j
  until cheers j > 3
  fill i
until cheers i > 3
```
Output: `1 2 3 2 4 6 3 6 9`

### Conditional Inside Loop
```
pour x = 0
chug
  sniff cheers x == 2
    belch 99
  spit
  belch x
  fill x
until cheers x > 4
```
Output: `0 1 99 2 3 4`

---

## 📐 Grammar (EBNF)

```
program = { stmt } ;
stmt    = assign | incr | zero | decr | print | loop | cond ;
assign  = "pour" ident "=" expr ;
incr    = "fill" ident ;
zero    = "spill" ident ;
decr    = "sip" ident ;
print   = "belch" expr ;
loop    = "chug" { stmt } "until" bexpr ;
cond    = "sniff" bexpr { stmt } "spit" ;
bexpr   = "cheers" expr (op) expr | expr (op) expr ;
op      = "==" | "!=" | "<" | ">" | "<=" | ">=" ;
expr    = term { ("+" | "-") term } ;
term    = factor { ("*" | "/" | "%") factor } ;
factor  = int | ident | "(" expr ")" ;
```

---

## 🏃 Running

```bash
python3 quaff.py < program.quaff
```

Or import and use directly:
```python
from quaff import run
print(run("belch 42"))
```

---

## 🍺 Design Notes

- **No strings.** Quaff only knows numbers. Like a bartender who only speaks in tabs.
- **No functions.** You just chug until you are done.
- **No arrays.** Everything is a single glass. You fill it, you sip it, you spill it.
- **Comments** start with `#` — like writing on a napkin.
- **All output is space-separated numbers.** Belch out your results.

---

*Quaff: because code should be something you can enjoy with friends.* 🍻

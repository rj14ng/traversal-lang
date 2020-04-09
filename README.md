# Traversal
Repository for Rocco Jiang's Extended Project Qualification. Traversal is a simple text-based programming language specifically aimed at teaching young students basic programming concepts, with an intention to bridge the gap between visual block-based languages (e.g. Scratch) and text-based languages (e.g. Python).

## Requirements
The parser requires RPly.

Install using `pip3 install rply`.

## Guide
To run: `python3 main.py`.

Test code should be placed in the `test.trv` file.

## Features
- Dynamic typing
- Basic data types
- Loops
- Conditional statements
- Rudimentary string concatenation and 'multiplication'

## Data types
- Integers (`integer`)
- Floats (`decimal`)
- Strings (`text`)
- Booleans (`condition`)

## Grammar
- Comments indicated by `//`
- Typical arithmetic operators `+`, `-`, `*`, `/` (only true division)
- Print to stdout using `output` or `print`
- Assignment operator using `=`
- Loops indicated by `repeat` followed by the integer number of times to repeat (e.g. `repeat 3` loops over 3 times)
- Conditional values are case insensitive (`True`, `TRUE`, `false`, `fALsE` are all acceptable)
- Comparison operators are `=`, `not=`, `<`, `<=`, `>`, `>=`
- Logical operators are `and`, `or`, `not`
- Loops
  - `repeat` to loop for an integer number of items (e.g. `repeat 3`)
  - `repeat until` to loop until a condition is satisfied (e.g. `repeat until x > 10`)
  - No colon (`:`) needed at the end of the line
- Conditional statements
  - `if`, `else if`, and `else`
  - No colon (`:` needed at the end of the line)
- Indentations using `TAB` for code blocks within loops and conditional statements
- Nested loops and conditional statements
- String concatenation can be done with any data type
- String multiplication by integers (just like Python!)
- Booleans are not integers
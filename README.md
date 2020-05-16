# Traversal
[![Python version](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Repository for Rocco Jiang's Extended Project Qualification. Traversal is a simple text-based programming language specifically aimed at teaching young students basic programming concepts, with an intention to bridge the gap between visual block-based languages (e.g. Scratch) and text-based languages (e.g. Python).

## Requirements
The parser requires [RPly](https://github.com/alex/rply).

Install using `pip3 install rply`.

## Guide
Traversal comes with a `test.trv` file by default, which is run if no other files are provided:

`python3 run.py`

A file can be provided and run using:

`python3 run.py filename.trv`

Traversal programs can also be timed, by adding a `-t` flag:

`python3 -t run.py filename.trv`

## Features
- Dynamic typing
- Somewhat weak typing (implicit conversions made where they make logical sense, e.g. string concatenation)
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
- Arithmetic operators
  - Addition (`+`)
  - Subtraction (`-`)
  - Multiplication (`*`)
  - True division (`/`)
  - Exponentiation/powers (`^`)
  - Modulo (`mod`)
- Print to stdout using `output`, `print`, or `say`
- Assignment operator using `=`
- Conditional values are case insensitive (`True`, `TRUE`, `false`, `fALsE` are all acceptable)
- Comparison operators are `=`, `not=`, `<`, `<=`, `>`, `>=`
- Logical operators are `and`, `or`, `not`
- Loops
  - `repeat` to loop for an integer number of items (e.g. `repeat 3`)
  - `repeat until` to loop until a condition is satisfied (e.g. `repeat until x > 10`)
  - No colon (`:`) needed at the end of the line
- Conditional statements (including synonyms for the typical `if`, `else if`, `else` syntax)
  - `if`
  - `else if` / `but if` / `otherwise if`
  - `else` / `otherwise`
  - No colon (`:`) needed at the end of the line
- Indentations using `TAB` for code blocks within loops and conditional statements
- Nested loops and conditional statements
- String concatenation can be done with any data type without need for casting
- String multiplication by integers (just like Python!)
- Booleans are not integers
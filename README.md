# Traversal
Repository for Rocco Jiang's Extended Project Qualification. Traversal is a simple text-based programming language specifically aimed at teaching young students basic CS concepts, with an intention to bridge the gap between visual block-based languages (e.g. Scratch) and text-based languages (e.g. Python).

## Requirements
The parser requires RPly.

Install using `pip3 install rply`.

## Guide
To run: `python3 main.py`.

Test code should be placed in the `test.trv` file.

## Features
- Dynamic typing

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
- Conditional values are case insensitive (`True`, `TRUE`, `false`, `fALsE` are all acceptable)
- Comparison operators are `=`, `not=`, `<`, `<=`, `>`, `>=`
- Logical operators are `and`, `or`, `not`
- String multiplication by integers (just like Python!)
- String concatenation can be done with any data type
- Booleans are not integers
# Natural_Logic_Interpreter

<p align="center">
<img src="logo.png">
</p>

## Description
NLI automatically interprets and validates nested natural logical arguments 
(logical arguments expressed in natural language) based
on rules of inference and propositional logic. The program uses "divide and conquer" algorithms
implemented by recursive functions to go through nested logical arguments and to be able to define
and validate them accordingly.

## Inspiration
"Translating sentences in English (or other natural languages) into logical expressions is a crucial
task in mathematics, logic programming, artificial intelligence, software engineering, and many
other disciplines."

I came across this paragraph while studying "Discrete Mathematics and It's Applications"; therefore, I got inspired
to automate this task using computers.

## Examples
**We can establish these logical arguments:**

`(I go to school) AND ((I study) AND (I exercise))`

`IF (I exercise) THEN (I'm healthy)`

`IF (I'm healthy) THEN (NOT I'm sick)`

`(I study) OR (I'm sick)`

`(NOT it rains today)`

`(I study) AND ((I go to gym) OR (I drink a coffee))`

`(it rains today) OR ((I exercise) AND (I study))`

`IF (I'm healthy) THEN (I'm happy) OR (I'm fit)`

**Then we can validate any proposition we want based on them:**

(I'm sick) -----> `False`

IF (I exercise) THEN (I'm healthy) -----> `True`

(it rains today) OR ((I exercise) AND (I study)) -----> `True`

(It rains today) OR (I'm healthy) -----> `True`

(I drink a coffee) AND ((I'm happy) OR (I'm fit)) -----> `None`

## Dependencies

Python 3.5

## Usage

Download or clone the repo and click on the executable file in the folder called "NLI" to enter an interactive command line interface.

## Syntax Conventions

This is how various expressions should be entered in this program:

Simple expressions: `(expression)`

AND arguments: `(expression1) AND (expression2)`

OR arguments: `(expression1) OR (expression2)`

NOT arguments: `(NOT expression)`

Conditional arguments: `IF (expression1) THEN (expression2)`

## Current Known Bugs and Limitations

The regex that is written to recognize the type of arguments sometimes fails to do so when the depth or length of main
logical arguments becomes large. However, there has not been any known issues when working with arguments similar to the ones seen in the
**Examples** section.

In addition, NOT operation for now cannot be used in the following ways:

*These need to be implemented using De Morgan's Law*

NOT (expression1) AND (expression2)

NOT (Expression1) OR (expression2)


 
The author is working on these issues.

## Contributing

This field of study is huge and this program is not complete by any means. There is a lot
that can be done to add on its capabilities. Please feel free to contribute and build on top
of it. Should you have any questions in order to start email me at: ppourdavood@gmail.com.

## Author

[Parham Pourdavood](https://github.com/ParhamP "Author")


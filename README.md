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
We can establish these logical arguments:

`(I go to school) AND ((I study) AND (I exercise))`

`IF (I exercise) THEN (I'm healthy)`

`(I study) OR (I'm healthy)`

`(NOT it rains today)`

`(I become sick) OR (IF (I exercise) THEN (I'm healthy))`

`(it rains today) OR (I exercise)`

`IF (I'm healthy) THEN ((I'm happy) OR (I'm fit))`

Now we can validate them:
(I go to school) -----> `True`
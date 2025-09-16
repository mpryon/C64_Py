# Commodore 64 BASIC Interpreter

A Python implementation that mimics the classic Commodore 64 BASIC environment, complete with the iconic startup banner and core BASIC commands.

## Features

### Core BASIC Commands
- **PRINT** - Output text and variables
- **INPUT** - Get user input
- **LET** - Variable assignment (LET keyword optional)
- **IF-THEN** - Conditional statements
- **FOR-NEXT** - Loops with STEP support
- **GOTO** - Unconditional branching
- **GOSUB-RETURN** - Subroutine calls
- **REM** - Comments
- **CLS** - Clear screen
- **LIST** - Display program
- **RUN** - Execute program
- **NEW** - Clear program and variables
- **END** - End program execution
- **WAIT** - Simple delay
- **LOAD** - Load program from file
- **SAVE** - Save program to file
- **COLOR** - Set text and background colors (C64-style)
- **SCREEN** - Set background color

### Built-in Functions
- **ABS** - Absolute value
- **SQR** - Square root
- **SIN, COS, TAN** - Trigonometric functions
- **LOG, EXP** - Logarithmic and exponential
- **INT** - Integer conversion
- **RND** - Random number (0-1)
- **LEN** - String length
- **CHR$** - Character from ASCII code
- **ASC** - ASCII code from character
- **STR$** - String conversion
- **VAL** - Numeric conversion

### Variables
- Numeric variables (A, B, X, etc.)
- String variables (A$, B$, etc.)
- System variables (TI, TI$)

## Installation and Usage

1. Make sure you have Python 3.6+ installed
2. Run the interpreter:
   ```bash
   python3 c64_basic.py
   ```
3. Type `BYE` to exit

## Examples

### Hello World
```
PRINT "HELLO, WORLD!"
```

### Simple Calculator
```
10 INPUT "ENTER FIRST NUMBER: ", A
20 INPUT "ENTER SECOND NUMBER: ", B
30 PRINT "SUM: "; A + B
40 PRINT "DIFFERENCE: "; A - B
50 PRINT "PRODUCT: "; A * B
60 PRINT "QUOTIENT: "; A / B
RUN
```

### Countdown Loop
```
10 FOR I = 10 TO 1 STEP -1
20 PRINT I
30 NEXT I
40 PRINT "BLAST OFF!"
RUN
```

### Number Guessing Game
```
10 R = INT(RND(1) * 100) + 1
20 INPUT "GUESS THE NUMBER (1-100): ", G
30 IF G = R THEN PRINT "CORRECT!" : GOTO 60
40 IF G < R THEN PRINT "TOO LOW!"
50 IF G > R THEN PRINT "TOO HIGH!"
60 GOTO 20
RUN
```

### String Manipulation
```
10 A$ = "HELLO"
20 B$ = "WORLD"
30 PRINT A$ + " " + B$
40 PRINT "LENGTH OF A$: "; LEN(A$)
50 PRINT "ASCII CODE OF H: "; ASC("H")
RUN
```

### Color Demo
```
10 COLOR 1,6
20 PRINT "WHITE ON BLUE (C64 DEFAULT)"
30 COLOR 2,6
40 PRINT "RED ON BLUE"
50 COLOR 1,2
60 PRINT "WHITE ON RED"
70 COLOR 1,6
80 PRINT "BACK TO DEFAULT"
RUN
```

### Subroutine Example
```
10 PRINT "MAIN PROGRAM"
20 GOSUB 100
30 PRINT "BACK TO MAIN"
40 END
100 PRINT "IN SUBROUTINE"
110 RETURN
RUN
```

### File Operations
```
10 PRINT "HELLO WORLD"
20 SAVE "MYPROG"
30 NEW
40 LOAD "MYPROG"
50 RUN
```

## Program Mode vs Immediate Mode

### Program Mode
Lines with numbers are stored as part of a program:
```
10 PRINT "HELLO"
20 PRINT "WORLD"
RUN
```

### Immediate Mode
Lines without numbers execute immediately:
```
PRINT "HELLO"
A = 5
PRINT A
```

## Syntax Notes

- Line numbers are required for program mode
- Variable names can be 1-2 characters (A, B, A$, B$, etc.)
- String literals must be in quotes
- Operators: +, -, *, /, =, <>, <, >, <=, >=
- Commas in PRINT create tab separators
- Semicolons in PRINT create no separators

## Limitations

This is a simplified implementation and doesn't include:
- Graphics commands (PLOT, DRAW, etc.)
- Sound commands (SOUND, PLAY, etc.)
- Advanced memory management
- Machine language integration

## Classic C64 Feel

The interpreter includes:
- Authentic startup banner with C64 colors
- "READY." prompt in classic style
- Classic error messages in red
- BREAK handling (Ctrl+C)
- Tab-separated PRINT output
- **C64-style colors**: Blue background, white text by default
- **Color commands**: COLOR and SCREEN for authentic C64 color control
- **16-color palette**: Approximates the original C64 color scheme

Enjoy your nostalgic BASIC programming experience! # C64_Py
# C64_Py

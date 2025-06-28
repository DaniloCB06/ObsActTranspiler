# ObsActTranspiler

ObsActTranspiler is a command-line tool that parses programs written in the ObsAct domain-specific language and translates them into equivalent C code. It implements a lexer and parser using PLY (Python Lex-Yacc) to transform device and observation declarations, conditional statements, and alert/broadcast actions into C function calls.

## Objective

The objective of this project is to demonstrate the implementation of a compiler front-end for a simple DSL (ObsAct) in Python. Key goals include:

* Designing and implementing a grammar for devices, observations, conditions, and actions.
* Building a lexer and LALR parser with PLY.
* Generating readable, idiomatic C code that reflects the ObsAct semantics.
* Showcasing code generation techniques for function calls (`ligar`, `desligar`, `alerta`, `alerta_var`).

## Prerequisites

* Python 3.6 or higher
* [PLY library](https://www.dabeaz.com/ply/)

Install dependencies:

```bash
pip install ply
```

## Usage Tutorial

1. **Clone the repository**

   ```bash
   https://github.com/DaniloCB06/ObsActTranspiler.git
   ```

2. **(Optional) Create and activate a virtual environment**

   ````bash
   python -m venv venv    # create
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate    # Windows
   pip install -r req.txt
   ````

3. **Run the transpiler**

   python main.py \<input\_file.obsact> \<output\_file.c>


      ````bash
      - `<input_file.obsact>`: path to your ObsAct source file.  
      - `<output_file.c>`: target C file to generate.

      **Example:**

      python main.py tests/ex1.obsact output/ex1.c
      ````

4. **Compile and execute the generated C code**

   ````bash
   gcc output/ex1.c -o ex1     # compile
   ./ex1                     # run
   ````

## Final grammar

````bash
   1. program → devices cmds
   2. devices → device
   3. devices → devices device
   4. device → DISPOSITIVO LBRACE NAME RBRACE
   5. device → DISPOSITIVO LBRACE NAME COMMA NAME RBRACE
   6. device → DISPOSITIVO COLON LBRACE NAME RBRACE
   7. device → DISPOSITIVO COLON LBRACE NAME COMMA NAME RBRACE
   8. cmds → cmd DOT
   9. cmds → cmds cmd DOT
   10. cmd → attrib
   11. cmd → obsact
   12. cmd → act
   13. cmd → broadcast
   14. attrib → SET NAME EQUAL var
   15. var → NUMBER
   16. var → BOOL
   17. var → NAME
   18. obsact → SE condition ENTAO
   19. obsact → SE condition ENTAO act
   20. obsact → SE condition ENTAO act SENAO act
   21. condition → expression
   22. expression → NAME OPLOGIC var
   23. expression → expression AND expression
   24. act → LIGAR NAME
   25. act → DESLIGAR NAME
   26. act → ENVIAR ALERTA LPAREN MSG RPAREN PARA NAME
   27. act → ENVIAR ALERTA LPAREN MSG COMMA NAME RPAREN PARA NAME
   28. act → ENVIAR ALERTA LPAREN MSG RPAREN NAME
   29. act → ENVIAR ALERTA LPAREN MSG COMMA NAME RPAREN NAME
   30. broadcast → ENVIAR ALERTA LPAREN MSG RPAREN PARA TODOS COLON name_list
   31. broadcast → ENVIAR ALERTA LPAREN MSG COMMA NAME RPAREN PARA TODOS COLON name_list
   32. name_list → NAME
   33. name_list → name_list COMMA NAME
````

## Grammar Overview

The ObsAct parser grammar is organized into five main sections, each reflecting one aspect of the language:

1. **Program Structure**
   A complete program consists of two parts, in this exact order:

   ```
   program → devices cmds  
   ```

   First you declare all devices, then you write all commands.

2. **Device Declarations**
   Each device declaration begins with the keyword `dispositivo`, optionally a colon, then a pair of braces containing the device name and (optionally) an observation name:

   * **Without observation**

     ```obsact
     dispositivo { lampada }
     dispositivo : { Monitor }
     ```

   * **With observation**

     ```obsact
     dispositivo { sensor, temperatura }
     dispositivo : { celular, movimento }
     ```

3. **Assignments**
   Assign a value to a variable (an observation) using the `set` keyword, an equals sign, and a terminating dot:

   ```obsact
   set NAME = VAR .
   ```

   Here, `VAR` can be:

   * a **NUMBER** (e.g. `42`)
   * a **BOOL** (`True` or `False`)
   * another **NAME** (variable reference)

4. **Conditionals**
   Conditional execution follows the form:

   ```obsact
   se <condition> entao <action> [senao <action>] .
   ```

   where `<condition>` is one comparison of the form `NAME OPLOGIC VAR` (e.g. `temperatura > 30`), and you can chain comparisons with `&&` (logical AND).

5. **Actions & Broadcasts**

   * **Simple actions**

     ```obsact
     ligar NAME .
     desligar NAME .
     ```
   * **Alerts (single target)**

     ```obsact
     enviar alerta ("msg") para NAME .
     enviar alerta ("msg", VAR) para NAME .
     ```
   * **Broadcast alerts (all targets)**

     ```obsact
     enviar alerta ("msg") para todos :
         NAME, NAME, … .
     ```

---

## Application to Examples

Below are four sample programs demonstrating every feature of the grammar.

### ex1.obsact

```obsact
dispositivo { monitor }
dispositivo : { celular }

se temperatura > 30 entao .

enviar alerta (" Temperatura em ", temperatura) para todos :
    monitor, celular .
```

* Declares two devices (`monitor`, `celular`).
* Uses an *empty* conditional to “store” `temperatura > 30` before the broadcast.
* Sends a broadcast alert to both devices.

### ex3.obsact

```obsact
dispositivo : { celular, movimento }
dispositivo : { higrmetro, umidade }
dispositivo : { lampada, potencia }
dispositivo : { Monitor }

set potencia = 100 .

se umidade < 40 entao enviar alerta ("Ar seco detectado") para Monitor .
se movimento == True entao ligar lampada senao desligar lampada .
```

* Declares devices each with an associated observation.
* Assigns `100` to `potencia`.
* Shows both a simple conditional alert and a conditional with `senao`.

### ex5.obsact

```obsact
dispositivo : { lampada, potencia }

set potencia = 100 .
ligar lampada .
```

* Single device with observation.
* Assignment followed by a simple action.

### ex9.obsact

```obsact
dispositivo { termostato }
dispositivo : { janela, abertura }
dispositivo : { sirene, alarme }

set abertura = False .
set alarme = 0 .

se abertura == True entao enviar alerta ("Janela aberta!") para janela .
se alarme >= 1 entao ligar sirene senao desligar sirene .

enviar alerta ("Status geral", alarme) para todos :
    termostato, janela, sirene .
```

* Declares three devices (one without, two with observations).
* Assigns a boolean and a number.
* Demonstrates a conditional alert, a conditional with `senao`, and a broadcast alert.

---


## Project Structure



ObsActTranspiler/<br>
├── main.py                    # Entry point and command-line interface<br>
├── parser/                    # Lexer and parser modules<br>
│   ├── obsact\_lexer.py        # Token definitions<br>
│   └── obsact\_parser.py       # Grammar and code generation<br>
├── tests/                     # Sample .obsact programs<br>
│   ├── ex1.obsact             # Example 1<br>
│   └── ex2.obsact             # Example 2<br>
└── README.md                  # This file<br>



## License

This project is released under the MIT License. Feel free to use, modify, and distribute.|


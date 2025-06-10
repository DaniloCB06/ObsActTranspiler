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



## Project Structure



ObsActTranspiler/
├── main.py                    # Entry point and command-line interface
├── parser/                    # Lexer and parser modules
│   ├── obsact\_lexer.py        # Token definitions
│   └── obsact\_parser.py       # Grammar and code generation
├── tests/                     # Sample .obsact programs
│   ├── ex1.obsact             # Example 1
│   └── ex2.obsact             # Example 2
└── README.md                  # This file



## License

This project is released under the MIT License. Feel free to use, modify, and distribute.|


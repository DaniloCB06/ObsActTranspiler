import sys
from lexico.obsact_lexer import lexer
from parser.obsact_parser import parser

def main():
    if len(sys.argv) != 3:
        print("Uso: python main.py entrada.obsact saida.c")
        sys.exit(1)
    entrada, saida = sys.argv[1], sys.argv[2]
    data = open(entrada).read()
    c_code = parser.parse(data, lexer=lexer)
    with open(saida, 'w') as f:
        f.write(c_code)
    print(f"Arquivo C gerado: {saida}")

if __name__ == '__main__':
    main()

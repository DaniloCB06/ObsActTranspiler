import ply.yacc as yacc
from lexico.obsact_lexer import tokens

# listas globais para coletar nomes
device_list    = []
observation_list = []

# coleção de trechos C gerados
c_statements = []

# --- PRODUÇÕES ---

def p_program(p):
    'program : devices cmds'
    # cabeçalho e defaults
    header = [
        '#include <stdio.h>',
        '',
        '// protótipos das funções ObsAct → C',
        'void ligar(const char* dev);',
        'void desligar(const char* dev);',
        'void alerta(const char* dev, const char* msg);',
        'void alerta_var(const char* dev, const char* msg, int var);',
        '',
        'int main() {'
    ]
    # inic defaults de observations
    for obs in observation_list:
        header.append(f'    int {obs} = 0;')
    header.append('')

    # corpo de comandos
    body = ['    ' + stmt for stmt in c_statements]
    footer = [
        '    return 0;',
        '}',
        '',
        '// definições das funções',
        'void ligar(const char* dev) { printf("%s ligado !\\n", dev); }',
        'void desligar(const char* dev) { printf("%s desligado !\\n", dev); }',
        'void alerta(const char* dev, const char* msg) {',
        '    printf("%s recebeu o alerta :\\n", dev);',
        '    printf("%s\\n", msg);',
        '}',
        'void alerta_var(const char* dev, const char* msg, int var) {',
        '    printf("%s recebeu o alerta :\\n", dev);',
        '    printf("%s %d\\n", msg, var);',
        '}',
    ]

    p[0] = '\n'.join(header + body + footer)


def p_devices_single(p):
    'devices : DISPOSITIVO COLON LBRACE NAME RBRACE'
    device_list.append(p[4])
    p[0] = None

def p_devices_obs(p):
    'devices : DISPOSITIVO COLON LBRACE NAME COMMA NAME RBRACE'
    device_list.append(p[4])
    observation_list.append(p[6])
    p[0] = None

def p_devices_rec(p):
    'devices : devices devices'
    p[0] = None

# AQUI você vai adicionar as produções para CMD, ATTRIB, OBSACT e ACT
# Exemplo de atribuição:
def p_cmd_attrib(p):
    'cmds : SET NAME OPLOGIC expr DOT cmds'
    # mas na gramática VAR → NUMBER | BOOL | NAME, e para usarmos 'set obs = VAR .'
    # depois você deve ajustar para VAR e parser independente de expr
    stmt = f'{p[2]} = {p[4]};'
    c_statements.append(stmt)
    p[0] = p[6]

# e assim por diante para as outras regras...

# A produção de erro
def p_error(p):
    print(f"Syntax error perto de {p.value!r}")

parser = yacc.yacc()

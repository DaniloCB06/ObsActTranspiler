import ply.yacc as yacc
from lexico.obsact_lexer import tokens

# globais que acumulam cada parse
device_list      = []
observation_list = []
c_statements     = []

# --- PRODUÇÕES ---

def p_program(p):
    'program : devices cmds'
    # monta o C final
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
    # inicializa observations
    for obs in observation_list:
        header.append(f'    int {obs} = 0;')
    header.append('')

    body = ['    ' + stmt for stmt in c_statements]
    footer = [
        '',
        '    return 0;',
        '}',
        '',
        '// implementações das funções',
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

# --- dispositivos ---
def p_devices(p):
    '''devices : device
               | devices device'''
    # nada a retornar

def p_device_simple(p):
    'device : DISPOSITIVO COLON LBRACE NAME RBRACE'
    device_list.append(p[4])

def p_device_obs(p):
    'device : DISPOSITIVO COLON LBRACE NAME COMMA NAME RBRACE'
    device_list.append(p[4])
    observation_list.append(p[6])

# --- comandos ---
def p_cmds(p):
    '''cmds : cmd DOT
            | cmds cmd DOT'''
    # p[2] ou p[3] já adicionam o stmt

def p_cmd(p):
    '''cmd : attrib
           | obsact
           | act
           | broadcast'''
    # cada uma das sub-produções já faz c_statements.append()

# atribuição
def p_attrib(p):
    'attrib : SET NAME EQUAL var'
    c_statements.append(f'{p[2]} = {p[4]};')

# variável (número, bool, nome)
def p_var_number(p):
    'var : NUMBER'
    p[0] = str(p[1])

def p_var_bool(p):
    'var : BOOL'
    p[0] = '1' if p[1] else '0'

def p_var_name(p):
    'var : NAME'
    p[0] = p[1]

# se … então … [senao …]
def p_obsact(p):
    '''obsact : SE condition ENTAO act
              | SE condition ENTAO act SENAO act'''
    cond = p[2]
    then_code = p[4]
    if len(p) == 6:
        c_statements.append(f'if ({cond}) {{ {then_code} }}')
    else:
        else_code = p[6]
        c_statements.append(f'if ({cond}) {{ {then_code} }} else {{ {else_code} }}')

# condição com && e operadores lógicos
def p_condition_expr(p):
    'condition : expression'
    p[0] = p[1]

def p_expression_cmp(p):
    'expression : NAME OPLOGIC var'
    p[0] = f'{p[1]} {p[2]} {p[3]}'

def p_expression_and(p):
    'expression : expression AND expression'
    p[0] = f'({p[1]}) && ({p[3]})'

# ações simples: ligar, desligar
def p_act_ligar(p):
    'act : LIGAR NAME'
    p[0] = f'ligar("{p[2]}");'

def p_act_desligar(p):
    'act : DESLIGAR NAME'
    p[0] = f'desligar("{p[2]}");'

# enviar alerta simples ou com var
def p_act_alerta_var(p):
    'act : ENVIAR ALERTA LPAREN MSG COMMA NAME RPAREN NAME'
    msg, var, dev = p[5], p[7], p[9]
    p[0] = f'alerta_var("{dev}", "{msg}", {var});'

def p_act_alerta(p):
    'act : ENVIAR ALERTA LPAREN MSG RPAREN NAME'
    msg, dev = p[5], p[7]
    p[0] = f'alerta("{dev}", "{msg}");'

# broadcast
def p_broadcast(p):
    'broadcast : ENVIAR ALERTA LPAREN MSG RPAREN PARA TODOS COLON name_list'
    msg = p[5]
    for dev in p[10]:
        c_statements.append(f'alerta("{dev}", "{msg}");')

def p_name_list_single(p):
    'name_list : NAME'
    p[0] = [p[1]]

def p_name_list_rec(p):
    'name_list : name_list COMMA NAME'
    p[0] = p[1] + [p[3]]

# erro de sintaxe
def p_error(p):
    if p:
        print(f"Syntax error perto de {p.value!r}")
    else:
        print("Syntax error no fim de arquivo")

parser = yacc.yacc()

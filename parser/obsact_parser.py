import ply.yacc as yacc
from lexico.obsact_lexer import tokens

# globais que acumulam cada parse
device_list      = []
observation_list = []
c_statements     = []
last_condition   = None

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
    # Especificação:
    #   Gramática: devices -> device | devices device
    #   Parâmetros:
    #     p[1]/p[2]: dispositivo(s) analisado(s)
    #   Efeitos: dispositivos acumulados em device_list
    '''devices : device
               | devices device'''
    pass

def p_device_simple_nc(p):
    # Especificação:
    #   - Gramática: device -> DISPOSITIVO LBRACE NAME RBRACE
    #   - p[3]: token NAME do dispositivo
    #   - Efeito: adiciona p[3] a device_list
    'device : DISPOSITIVO LBRACE NAME RBRACE'
    device_list.append(p[3])

def p_device_obs_nc(p):
    # Especificação:
    #   - Gramática: device -> DISPOSITIVO LBRACE NAME COMMA NAME RBRACE
    #   - p[3]: dispositivo, p[5]: observação
    #   - Efeito: adiciona dispositivo e observação nas listas
    'device : DISPOSITIVO LBRACE NAME COMMA NAME RBRACE'
    device_list.append(p[3])
    observation_list.append(p[5])


def p_device_simple(p):
    # Especificação:
    #   - Gramática: device -> DISPOSITIVO COLON LBRACE NAME RBRACE
    #   - p[4]: token NAME do dispositivo
    #   - Efeito: adiciona dispositivo a device_list
    'device : DISPOSITIVO COLON LBRACE NAME RBRACE'
    device_list.append(p[4])

def p_device_obs(p):
    # Especificação:
    #   - Gramática: device -> DISPOSITIVO COLON LBRACE NAME COMMA NAME RBRACE
    #   - p[4]: dispositivo, p[6]: observação
    #   - Efeito: adiciona ambos às listas
    'device : DISPOSITIVO COLON LBRACE NAME COMMA NAME RBRACE'
    device_list.append(p[4])
    observation_list.append(p[6])

# --- comandos ---
def p_cmds(p):
    # Especificação:
    #   - Gramática: cmds -> cmd DOT | cmds cmd DOT
    #   - Gatilho: cada cmd adiciona instrução em c_statements
    '''cmds : cmd DOT
            | cmds cmd DOT'''
    # p[2] ou p[3] já adicionam o stmt

def p_cmd(p):
    '''cmd : attrib
           | obsact
           | act
           | broadcast'''
    # p[1] vem de:
    #  - attrib: já fez c_statements.append() e retorna None
    #  - obsact: idem
    #  - broadcast: idem
    #  - act: retorna a string da chamada C mas não appendou
    if p[1]:
        c_statements.append(p[1])

# atribuição
def p_attrib(p):
    # Especificação:
    #   - Gramática: attrib -> SET NAME EQUAL var
    #   - p[2]: variável, p[4]: valor string
    #   - Efeito: adiciona "var = valor;" a c_statements
    'attrib : SET NAME EQUAL var'
    c_statements.append(f'{p[2]} = {p[4]};')

# variável (número, bool, nome)
def p_var_number(p):
     # Especificação:
    #   - Gramática: var -> NUMBER
    #   - p[1]: valor inteiro
    #   - Retorno: p[0] = str(p[1])
    'var : NUMBER'
    p[0] = str(p[1])

def p_var_bool(p):
    # Especificação:
    #   - Gramática: var -> BOOL
    #   - p[1]: True/False
    #   - Retorno: '1' ou '0'
    'var : BOOL'
    p[0] = '1' if p[1] else '0'

def p_var_name(p):
    # Especificação:
    #   - Gramática: var -> NAME
    #   - p[1]: identificador
    #   - Retorno: p[0] = p[1]
    'var : NAME'
    p[0] = p[1]

def p_obsact_empty(p):
    # Especificação:
    #   - Gramática: obsact -> SE condition ENTAO
    #   - p[2]: condição
    #   - Efeito: armazena condição em last_condition
    'obsact : SE condition ENTAO'
    global last_condition
    last_condition = p[2]


# se … então … [senao …]
def p_obsact(p):
    # Especificação:
    #   - Gramática: obsact -> SE condition ENTAO act [SENAO act]
    #   - p[2]: condição, p[4]: then, p[6]: else
    #   - Efeito: adiciona if/else em c_statements
    '''obsact : SE condition ENTAO act
              | SE condition ENTAO act SENAO act'''
    cond       = p[2]
    then_code  = p[4]
    # sem 'senao', len(p)==5 (p[0]..p[4])
    if len(p) == 5:
        c_statements.append(f'if ({cond}) {{ {then_code} }}')
    else:
        else_code = p[6]
        c_statements.append(f'if ({cond}) {{ {then_code} }} else {{ {else_code} }}')

# condição com && e operadores lógicos
def p_condition_expr(p):
    # Especificação:
      #   - Gramática: condition -> expression
      #   - Retorno: p[0] = p[1]
    'condition : expression'
    p[0] = p[1]

def p_expression_cmp(p):
    # Especificação:
    #   - Gramática: expression -> NAME OPLOGIC var
    #   - p[1]: variável, p[2]: operador, p[3]: valor
    #   - Retorno: string '<var> <op> <value>'
    'expression : NAME OPLOGIC var'
    p[0] = f'{p[1]} {p[2]} {p[3]}'

def p_expression_and(p):
    # Especificação:
    #   - Gramática: expression -> expression AND expression
    #   - p[1], p[3]: subexpressões
    #   - Retorno: string '(expr1) && (expr2)'
    'expression : expression AND expression'
    p[0] = f'({p[1]}) && ({p[3]})'

# ações simples: ligar, desligar
def p_act_ligar(p):
    # Especificação:
    #   - Gramática: act -> LIGAR NAME
    #   - p[2]: dispositivo
    #   - Retorno: p[0] = 'ligar("dev");'
    'act : LIGAR NAME'
    p[0] = f'ligar("{p[2]}");'
    

def p_act_desligar(p):
    # Especificação:
    #   - Gramática: act -> DESLIGAR NAME
    #   - p[2]: dispositivo
    #   - Retorno: p[0] = 'desligar("dev");'
    'act : DESLIGAR NAME'
    p[0] = f'desligar("{p[2]}");'

# enviar alerta simples ou com var
def p_act_alerta_var(p):
    # Especificação:
    #   - Gramática: act -> ENVIAR ALERTA LPAREN MSG COMMA NAME RPAREN PARA NAME
    #   - p[4]: mensagem, p[6]: variável, p[9]: dispositivo
    #   - Retorno: p[0] = 'alerta_var(dev, msg, var);'
    'act : ENVIAR ALERTA LPAREN MSG COMMA NAME RPAREN PARA NAME'
    msg, var, dev = p[4], p[6], p[9]
    p[0] = f'alerta_var("{dev}", "{msg}", {var});'

def p_act_alerta(p):
    # Especificação:
    #   - Gramática: act -> ENVIAR ALERTA LPAREN MSG RPAREN PARA NAME
    #   - p[4]: mensagem, p[7]: dispositivo
    #   - Retorno: p[0] = 'alerta(dev, msg);'
    'act : ENVIAR ALERTA LPAREN MSG RPAREN PARA NAME'
    msg, dev = p[4], p[7]
    p[0] = f'alerta("{dev}", "{msg}");'

# broadcast
def p_broadcast(p):
    # Especificação:
      #   - Gramática: broadcast -> ENVIAR ALERTA LPAREN MSG RPAREN PARA TODOS COLON name_list
      #   - p[5]: mensagem, p[10]: lista de dispositivos
      #   - Efeitos:
      #       Se last_condition, envolve em if e reseta;
      #       Senão, emite alertas diretos.
    'broadcast : ENVIAR ALERTA LPAREN MSG RPAREN PARA TODOS COLON name_list'
    msg = p[5]
    global last_condition
    if last_condition:
        # cria um bloco if(...) { … }
        c_statements.append(f'if ({last_condition}) {{')
        for dev in p[10]:
            c_statements.append(f'    alerta("{dev}", "{msg}");')
        c_statements.append('}')
        last_condition = None
    else:
        for dev in p[10]:
            c_statements.append(f'alerta("{dev}", "{msg}");')

def p_broadcast_var(p):
    # Especificação semelhante a p_broadcast, mas chama alerta_var
    'broadcast : ENVIAR ALERTA LPAREN MSG COMMA NAME RPAREN PARA TODOS COLON name_list'
    msg, var = p[4], p[6]
    global last_condition
    if last_condition:
        c_statements.append(f'if ({last_condition}) {{')
        for dev in p[11]:
            c_statements.append(f'    alerta_var("{dev}", "{msg}", {var});')
        c_statements.append('}')
        last_condition = None
    else:
        for dev in p[11]:
            c_statements.append(f'alerta_var("{dev}", "{msg}", {var});')

def p_name_list_single(p):
    # Especificação:
    #   - Gramática: name_list -> NAME
    #   - p[1]: dispositivo
    #   - Retorno: p[0] = [p[1]]
    'name_list : NAME'
    p[0] = [p[1]]

def p_name_list_rec(p):
    # Especificação:
    #   - Gramática: name_list -> name_list COMMA NAME
    #   - p[1]: lista atual, p[3]: próximo dispositivo
    #   - Retorno: p[0] = p[1] + [p[3]]
    'name_list : name_list COMMA NAME'
    p[0] = p[1] + [p[3]]
    
def p_act_alerta_no_para(p):
    # Especificação:
    #   - Gramática: name_list -> NAME
    #   - p[1]: nome
    #   - Retorno: p[0] = [p[1]]
    'act : ENVIAR ALERTA LPAREN MSG RPAREN NAME'
    msg, dev = p[4], p[6]
    p[0] = f'alerta("{dev}", "{msg}");'

def p_act_alerta_var_no_para(p):
    # Especificação:
    #   - Gramática: name_list -> name_list COMMA NAME
    #   - p[1]: lista atual, p[3]: próximo dispositivo
    #   - Retorno: p[0] = p[1] + [p[3]]
    'act : ENVIAR ALERTA LPAREN MSG COMMA NAME RPAREN NAME'
    msg, var, dev = p[4], p[6], p[8]
    p[0] = f'alerta_var("{dev}", "{msg}", {var});'

# erro de sintaxe
def p_error(p):
    # Especificação:
    #   - Chamado em erro de sintaxe
    #   - p: token que causou o erro ou None no EOF
    #   - Efeito: imprime mensagem de erro
    if p:
        print(f"Syntax error detectado perto de {p.value!r} (erro presente antes ou depois)")
        print(f"Reavalie o arquivo e tente detectar alguma regra faltante ou alguma syntaxe mal definida")
    else:
        print("Syntax error no fim de arquivo")

parser = yacc.yacc()

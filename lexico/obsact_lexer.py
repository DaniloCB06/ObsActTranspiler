import ply.lex as lex

# --------------------------------------------------
# 1) lista de nomes de tokens
#    inclua aqui TODOS os tokens, exceto os keywords
tokens = (
    'DISPOSITIVO','SET','SE','ENTAO','SENAO','ENVIAR','ALERTA',
    'PARA','TODOS',
    'LIGAR','DESLIGAR',

    'COLON',
    'LBRACE','RBRACE','LPAREN','RPAREN','COMMA','DOT',

    'AND','OPLOGIC','EQUAL',

    'NUMBER','BOOL','MSG','NAME',
)
# --------------------------------------------------

# --------------------------------------------------
# 2) dicionário de palavras-reservadas
reserved = {
    'dispositivo': 'DISPOSITIVO',
    'set'        : 'SET',
    'se'         : 'SE',
    'entao'      : 'ENTAO',
    'senao'      : 'SENAO',
    'enviar'     : 'ENVIAR',
    'alerta'     : 'ALERTA',
    'para'       : 'PARA',
    'todos'      : 'TODOS',
    'ligar'      : 'LIGAR',
    'desligar'   : 'DESLIGAR',
}
# --------------------------------------------------

# --------------------------------------------------
# 3) regex para literais e símbolos
t_LBRACE   = r'\{'
t_RBRACE   = r'\}'
t_LPAREN   = r'\('
t_RPAREN   = r'\)'
t_COMMA    = r','
t_DOT      = r'\.'
t_COLON    = r':'
t_AND      = r'&&'
t_OPLOGIC  = r'<=|>=|==|!=|<|>'
t_EQUAL    = r'='
# --------------------------------------------------

# --------------------------------------------------
# 4) tokens compostos com função (para poder dar t.type dinâmico)
def t_MSG(t):
    r'"([^"]*)"'
    t.value = t.value[1:-1]
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_BOOL(t):
    r'True|False'
    t.value = (t.value == 'True')
    return t

def t_NAME(t):
    r'[A-Za-z][A-Za-z0-9]*'
    # se for palavra-reservada, sobrescreve o tipo
    t.type = reserved.get(t.value, 'NAME')
    return t
# --------------------------------------------------

# --------------------------------------------------
# 5) ignorar espaços e quebras de linha
t_ignore = ' \t\r\n'

def t_error(t):
    print(f"Lex error em '{t.value[0]}'")
    t.lexer.skip(1)
# --------------------------------------------------

lexer = lex.lex()

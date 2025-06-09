import ply.lex as lex

# 1) lista de nomes de tokens
tokens = (
    'DISPOSITIVO','SET','SE','ENTAO','SENAO','ENVIAR','ALERTA',
    'PARA','TODOS',
    'LBRACE','RBRACE','LPAREN','RPAREN','COMMA','DOT',
    'AND','OPLOGIC',
    'NUMBER','BOOL','MSG','NAME'
)

# 2) regex para tokens fixos / literais
t_DISPOSITIVO = r'dispositivo'
t_SET         = r'set'
t_SE          = r'se'
t_ENTAO       = r'entao'
t_SENAO       = r'senao'
t_ENVIAR      = r'enviar'
t_ALERTA      = r'alerta'
t_PARA        = r'para'
t_TODOS       = r'todos'
t_LBRACE      = r'\{'
t_RBRACE      = r'\}'
t_LPAREN      = r'\('
t_RPAREN      = r'\)'
t_COMMA       = r','
t_DOT         = r'\.'
t_AND         = r'&&'
t_OPLOGIC     = r'<=|>=|==|!=|<|>'

# 3) tokens com algum processamento
def t_MSG(t):
    r'\"([^"]*)\"'
    t.value = t.value[1:-1]  # retira as aspas
    return t

def t_BOOL(t):
    r'True|False'
    t.value = (t.value == 'True')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_NAME(t):
    r'[A-Za-z][A-Za-z0-9]*'
    return t

# 4) ignorar espaços em branco e quebras
t_ignore = ' \t\r\n'

# 5) erro de lex
def t_error(t):
    print(f"Lex error em '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

import ply.lex as lex
import sys

tokens = ['OBJETO', 'AOT', 'COMENTARIO', 'ATRIBUTO', 'STR', 'LITSTR', 'INT', 'FLOAT', 'NOTACIEN', 'INFNAN', 'SC', 'DATA', 'TEMPO', 'BOOLEANO']

literals = '{=[],}'

def t_COMENTARIO(t):
    r'\#.*'
    return t

def t_ATRIBUTO(t):
    r'[\w\-]+(\s*\.\s*[\w\-]+)*(?=\s*=)'
    return t

def t_STR(t):
    r'".*?"'
    return t

def t_LITSTR(t):
    r"'.*?'"
    return t 

def t_DATA(t):
    r'\d+\-\d+\-\d+((T| )\d+:\d+:\d+(\.\d+)?(Z|[+\-]\d+:\d+)?)?'
    return t

def t_TEMPO(t):
    r'\d+:\d+:\d+(\.\d+)?'
    return t

# Binário, octal e hexadecimal
def t_SC(t):
    r'(0b[01]+|0o[0-7]+|0x([0-9]|[A-F]|[a-f])+)'
    return t

def t_INFNAN(t):
    r'[+\-]?(inf|nan)'
    return t 

def t_NOTACIEN(t):
    r'[+\-]?\d+(\.\d+)?(e|E)[+\-]?\d+'
    return t

def t_FLOAT(t):
    r'[+\-]?\d+\.\d+'
    return t

def t_INT(t):
    r'[+\-]?\d+'
    return t

def t_BOOLEANO(t):
    r'(true|false)'
    return t

def t_AOT(t):
    r'\[\[\S*\s*\]\]'
    t.value = t.value[2:-2]
    return t 

def t_OBJETO(t):
    r'(?<=\[)\S*\s*(?=\])'
    return t

t_ignore = ' \t\n'

def t_error(t):
    # Se houver um erro na análise léxica essa informação é enviada para o servidor
    print("Caracter ilegal: " + t.value[0])
    sys.stdout.flush()
    t.lexer.skip(1)

lexer = lex.lex()

with open(sys.argv[1], "r") as f:
    data = f.read()

def lexer_debugger(d):
    lexer.input(d)
    while True:
        tok = lexer.token()
        if not tok: 
            break      # No more input
        print(tok)

def main():
    # Debug
    lexer_debugger(data)

if __name__ == "__main__":
    main()

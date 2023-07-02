import ply.yacc as yacc
from anaLexTOML import lexer_debugger, tokens, data
import re
import sys

# Recebo uma lista de tuplos que representam o dicionário
def constroiDict(lista):
    obj = dict()

    for i in lista:
        if i is not None:
            c, v = i
            l = re.split(r'\.', c)
            if len(l) > 1 and l[0] in obj.keys():
                o = obj
                i = 0
                while i < len(l)-1:
                    if l[i] not in o.keys():
                        o[l[i]] = dict()
                    o = o[l[i]]
                    i += 1
                o[l[i]] = v
            else:
                if len(l) > 1:
                    o = obj
                    i = 0
                    while i < len(l)-1:
                        o[l[i]] = dict()
                        o = o[l[i]]
                        i += 1
                    o[l[i]] = v
                else:
                    obj[c] = v

    return obj


toml = dict()

def p_toml0(p):
    "toml : linha toml"

def p_toml1(p):
    "toml : "

# Comentário é ignorado -> não existem comentários em JSON
def p_linha0(p):
    "linha : COMENTARIO"

def p_linha1(p):
    "linha : chaveValor"
    c, v = p[1]

    l = re.split(r'\.', c)
    if len(l) > 1 and l[0] in toml.keys():
        o = toml
        i = 0
        while i < len(l)-1:
            o = o[l[i]]
            i += 1
        o[l[i]] = v   
    else:
        if len(l) > 1:
            o = toml
            i = 0
            while i < len(l)-1:
                o[l[i]] = dict()
                o = o[l[i]]
                i += 1
            o[l[i]] = v
        else:
            toml[c] = v

def p_linha2(p):
    "linha : obj"

def p_linha3(p):
    "linha : aot"

def p_obj0(p):
    "obj : '[' OBJETO ']' contObj"
    global toml

    if p[4]:
        obj = constroiDict(p[4])
    else:
        obj = dict()

    # Preencher com o conteúdo do objeto
    l = re.split(r"\.", p[2])
    o = toml
    i = 0
    while i < len(l) - 1:
        if l[i] not in o.keys():
            o[l[i]] = dict()
        o = o[l[i]]
        i += 1

    o[l[-1]] = obj

def p_contObj0(p):
    "contObj : contOb"
    p[0] = p[1]

def p_contOb0(p):
    "contOb : COMENTARIO contOb"
    p[0] = p[2]

def p_contOb1(p):
    "contOb : chaveValor contOb"
    if p[2]:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]] + []

def p_contOb2(p):
    "contOb : "
    p[0] = None

def p_aot(p):
    "aot : AOT arrayCont"
    if p[1] not in toml.keys():
        toml[p[1]] = [constroiDict(p[2])]
    else:
        if len(p[2]) == 0: # AOT vazio
            toml[p[1]].append(dict())
        else:
            toml[p[1]].append(constroiDict(p[2]))

def p_arrayCont0(p):
    "arrayCont : elem arrayCont"
    p[0] = [p[1]] + p[2]

def p_arrayCont1(p):
    "arrayCont : "
    p[0] = []

def p_elem0(p):
    "elem : chaveValor"
    p[0] = p[1]

def p_elem1(p):
    "elem : COMENTARIO"

def p_chaveValor(p):
    "chaveValor : ATRIBUTO '=' val"
    p[0] = (p[1], p[3])

def p_val0(p):
    "val : STR"
    p[0] = p[1][1:-1]

def p_val1(p):
    "val : LITSTR"
    p[0] = p[1][1:-1]

def p_val2(p):
    "val : INT"
    p[0] = int(p[1])

def p_val3(p):
    "val : FLOAT"
    p[0] = float(p[1])

def p_val4(p):
    "val : NOTACIEN"

    if '.' in p[1]: # decimal
        p[0] = float(format(float(p[1]), "e"))
    else: # inteiro
        p[0] = int(float(format(float(p[1]), "e")))

def p_val5(p):
    "val : SC"

    if p[1][:2] == "0b":
        num = p[1][2:]
        p[0] = int(num,2)
    elif p[1][:2] == "0o":
        num = p[1][2:]
        p[0] = int(num,8)
    if p[1][:2] == "0x":
        num = p[1][2:]
        p[0] = int(num,16)

def p_val6(p):
    "val : INFNAN"
    p[0] = str(p[1])

def p_val7(p):
    "val : DATA"
    p[0] = p[1]

def p_val8(p):
    "val : TEMPO"
    p[0] = p[1]

def p_val9(p):
    "val : BOOLEANO"
    if p[1] == "false":
        p[0] = False 
    elif p[1] == "true":
        p[0] = True 

def p_val10(p):
    "val : '{' contDict '}'"
    p[0] = dict(p[2])

def p_val11(p):
    "val : '{' '}'"
    p[0] = dict()

def p_contDict0(p):
    "contDict : chaveValor ',' contDict"
    p[0] = [p[1]] + p[3]

def p_contDict1(p):
    "contDict : chaveValor"
    p[0] = [p[1]]

def p_val12(p):
    "val : lista"
    p[0] = p[1]

def p_lista0(p):
    "lista : '[' ']'"
    p[0] = []

def p_lista1(p):
    "lista : '[' cont ']'"
    p[0] = p[2]

def p_cont0(p):
    "cont : val"
    p[0] = [p[1]]

def p_cont1(p):
    "cont : val ',' cont"
    p[0] = [p[1]] + p[3]

# Tratamento de Erros
def p_error(p):
    # Se houver um erro na compilação essa informação é enviada para servidor
    print(f"Sintax error: {p.value}")
    sys.stdout.flush()

parser = yacc.yacc()
parsed = parser.parse(data)

# YAML
def listToYAML(l, s, iden):
    i = 0
    while i < len(l):
        s += "- "
        if type(l[i]) is list:
            iden += '\t'
            s = listToYAML(l[i], s, iden)
        else:
            if type(l[i]) is dict:
                iden += '  \t'
                s = dicToYAML(l[i], s, iden)
                iden = iden[:-3]
            else:
                s += str(l[i]) + "\n\t" + iden
        i += 1 

    return s

# Converte o dicionário construido no parsing para YAML
def dicToYAML(obj, s, iden = '\t'):
    o = obj
    for key in o.keys():
        if type(o[key]) is dict:
            s += f'{iden}{str(key)}:\n'
            iden += '\t'
            s = dicToYAML(o[key], s, iden)
            iden = iden[:-1]
        elif type(o[key]) is list:
            s += f'{iden}{str(key)}:\n\t{iden}'
            s = listToYAML(o[key], s, iden)
            iden = iden[:-1]
        else:
            s += f'{iden}{str(key)}: {str(o[key])}\n'
    
    return s

# JSON
# Converte o dicionário construido no parsing para JSON
def dicToJSON(toml, s, f, iden = '\t'):
    # Esta linha converte para JSON de forma automática
    # json.dump(toml, f, ensure_ascii=False)
    o = toml
    entrou = False

    for key in o.keys():
        entrou = True
        if type(o[key]) is dict:
            s += f'{iden}"{key}":' + '{\n'
            iden += '\t'
            s = dicToJSON(o[key], s, f, iden)
            iden = iden[:-1]
            s += iden + '},\n'
        else:
            s += f'{iden}"{key}": '
            if type(o[key]) is str:
                s += f'"{o[key]}",\n'
            elif type(o[key]) is bool:  
                if o[key] is True:
                    s += f'true,\n'
                else:
                    s += f'false,\n'
            elif type(o[key]) is list:
                s += f'[\n'
                for i in o[key]:
                    s += f'\t{iden}{str(i)},\n'
                s = s[:-2] + s[-1:]
                s += f'{iden}],\n'
            else:
                s += f'{str(o[key])},\n'

    if entrou: return s[:-2] + s[-1:] # remove a última vírgula
    else: return s

# XML
def listToXML(l, s, iden):
    s += f'{iden}<lista>\n'
    iden += '\t'

    for i in l: 
        if type(i) == list:
            s += f'{iden}<item>\n'
            iden += '\t'
            s = listToXML(i, s, iden)
            iden = iden[:-1]
            s += f'{iden}</item>\n'
        elif type(i) is dict:
            s += f'{iden}<item>\n'
            iden += '\t'
            s = dicToXML(i, s, iden)
            iden = iden[:-1]
            s += f'{iden}</item>\n'
        else:
            s += f'{iden}<item>{i}</item>\n'

    iden = iden[:-1]
    s += f'{iden}</lista>\n'
    return s

def dicToXML(toml, s, iden = '\t'):
    o = toml

    for key in o.keys():
        if type(o[key]) is dict:
            s += f'{iden}<{key}>\n'
            iden += '\t'
            s = dicToXML(o[key], s, iden)
            iden = iden[:-1]
            s += f'{iden}</{key}>\n'
        elif type(o[key]) is list:
            s += f'{iden}<{key}>\n'
            iden += '\t'
            s = listToXML(o[key], s, iden)
            iden = iden[:-1]
            s += f'{iden}</{key}>\n'
        else:
            s += f'{iden}<{key}>\n'
            iden += '\t'
            s += f'{iden}{o[key]}\n'
            iden = iden[:-1] 
            s += f'{iden}</{key}>\n'

    return s

if sys.argv[2] == "JSON":
    with open("out.json", "w") as f:
        s = '{\n'
        s = dicToJSON(toml, s, f)
        s += '}'
        s = re.sub(r"'", r'"', s)
        f.write(s)
elif sys.argv[2] == "YAML":
    with open("out.yaml", "w") as f:
        s = 'toml:\n' 
        s = dicToYAML(toml, s)
        f.write(s)
elif sys.argv[2] == "XML":
    with open("out.xml", "w") as f:
        s = '<toml>\n'
        s = dicToXML(toml, s)
        s += '</toml>'
        f.write(s)

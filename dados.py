import json

FILE = "bd.json"

def _pegaDict():
    try:
        with open(FILE, 'r') as arq:
            return json.load(arq), open(FILE, 'w')
    except FileNotFoundError:
        return {}, open(FILE, 'w')

def search(key):
    with open(FILE, 'r') as arq:
        return json.load(arq)[key]

def insert(key, val):  
    dict, arq = _pegaDict()
    dict.setdefault(key,[]).append(val) # cria uma lista caso nao exista e adiciona o valor a lista
    json.dump(dict, arq)

def remove(key):
    dict, arq = _pegaDict()
    val = dict.pop(key, None) # remove todos os valores da chave sem levantar erro caso não exista
    json.dump(dict, arq)
    return val

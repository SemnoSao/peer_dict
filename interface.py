import socket

PORT = 10001 # porta que o servidor esta escutando

def utf8len(s):
        return len(s.encode('utf-8'))

def iniciaConexao(host):
    '''Cria um socket de cliente e conecta-se ao servidor.
    Saida: socket criado'''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cria socket [Internet (IPv4 + TCP) ]
    try:
        sock.connect((host, PORT)) # conecta-se com o servidor
    except:
        return None
	
    return sock

def fazRequisicoes(sock, msg):
    '''Faz requisicoes ao servidor e exibe o resultado.
    Entrada: socket conectado ao servidor
    Saida: mensagem de retorno do servidor'''

    sock.send(msg.encode('utf-8')) # envia a mensagem do usuario para o servidor
    r = sock.recv(1024) # espera a resposta do servidor
    finalizaConexao(sock)
    return str(r, encoding='utf-8') # retorna a mensagem recebida

def finalizaConexao(sock):
    '''Fecha o socket do cliente.
    Entrada: socket conectado ao servidor'''
    sock.close() # encerra o socket

def conecta(host):
    sock = iniciaConexao(host) 
    if sock is None: # caso não exista o servidor, encerra o cliente
        print('Servidor offline :(')
        print('Tente novamente mais tarde ou entre em contato com um administrador.')

    return sock

# main

host = input('informe o host da requisição (localhost): ') or 'localhost' # endereço do servidor
while True:
    sock = conecta(host) # testa conexao
    if sock is not None: break
    host = input('informe o host da requisição (localhost): ') or 'localhost' # endereço do servidor
finalizaConexao(sock)
print('Servidor Online :)')

print('''
Boas Vindas ao Dicionário distribuído!
    1 - Consultar
    2 - Inserir
    3 - Remover
    4 - Sair
''')

while True:
    op = input('Informe a opção desejada: ')
    match op: # primeira vez q o switch do c faria diferença na minha vida, daria pra escreve pra abrir e fechar a conexao menos vezes
        case '1':
            sock = conecta(host)
            if sock is None: continue
            msg = 'search '
            msg += input('Informe a chave a ser consultada: ')
            msg += ' 0'
            res = fazRequisicoes(sock, msg)
            finalizaConexao(sock)
            print(res)
        case '2':
            sock = conecta(host)
            if sock is None: continue
            msg = 'insert ' 
            msg += input('Informe a chave a ser inserida: ')
            val = input('Informe o valor a ser inserido: ')
            msg += ' '+str(utf8len(val))
            msg += '\n'+val
            res = fazRequisicoes(sock, msg)
            finalizaConexao(sock)
            print(res)
        case '3':
            sock = conecta(host)
            if sock is None: continue
            msg = 'insert ' 
            msg += input('Informe a chave a ser removida: ')
            val = input('Informe a senha de administrador: ')
            msg += ' '+str(utf8len(val))
            msg += '\n'+val
            res = fazRequisicoes(sock, msg)
            finalizaConexao(sock)
            print(res)
        case '4':
            print('Tchau! Até a próxima!')
            exit()
        case _:
            print('Opção inválida')
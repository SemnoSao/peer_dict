import signal
import socket
import threading
from selectors import DefaultSelector, EVENT_READ # biblioteca para multiplexação de I/O de alto nível, construida em cima das primitivas de select

interrupt_read, interrupt_write = socket.socketpair() # Cria um par de sockets conectados entre si de maneira full-duplex
SENHA = input('crie a senha de administrador(admin): ') or 'admin'

def interrupt_handler(signum, frame):
    print('\rSinal de interrupção recebido')
    interrupt_write.send(b'\0')
## a segunte linha inscreve o sinal de interrupção para ser 
## tratado pela função handler e impedir que o servidor seja 
## finalizado com CTRL+C bruscamente, achei uma ideia muito elegante
signal.signal(signal.SIGINT, interrupt_handler)

def iniciaServidor():
	'''Cria um socket de servidor e o coloca em modo de espera por conexoes
	Saida: o socket criado'''
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cria o socket [Internet( IPv4 + TCP)]
	sock.bind((HOST, PORT)) # vincula a localizacao do servidor
	sock.listen(5) # coloca-se em modo de espera por conexoes
	sock.setblocking(False) # configura o socket para o modo nao-bloqueante

	return sock

def serve(sock):

    def aceitaConexao(sock):
        '''Aceita o pedido de conexao de um cliente
        Entrada: o socket do servidor
        Saida: o novo socket da conexao e o endereco do cliente'''
        clisock, endr = sock.accept() # estabelece conexao com o proximo cliente

        return clisock, endr
  
    clientes = [] # objeto que armazena a referencia das threads criadas
    sel = DefaultSelector() # cria um seletor com a implementação mais eficiente para dada plataforma
    sel.register(interrupt_read, EVENT_READ)
    sel.register(sock, EVENT_READ)

    while True:
        for key, _ in sel.select():
            if key.fileobj == interrupt_read:
                interrupt_read.recv(1)
                return clientes
            if key.fileobj == sock:
                clisock, endr = aceitaConexao(sock)
                print ('Conectado com: ', endr)
                cliente = threading.Thread(target=atendeRequisicoes, args=(clisock,endr)) # cria nova thread para atender o cliente
                cliente.start()
                clientes.append(cliente) # armazena a referencia da thread para usar com join()
                
def finalizaServidor(clientes):
    for c in clientes: # aguarda todas as threads terminarem
        c.join()
        sock.close()
    interrupt_read.close()
    interrupt_write.close()

def atendeRequisicoes(clisock, endr):
    '''Recebe mensagens e chama as funcoes apropriadas para processar os comandos recebidos
    Entrada: socket da conexao e endereco do cliente
    Saida: '''

    def utf8len(s):
        return len(s.encode('utf-8'))

    while True:
        #recebe dados do cliente
        data = clisock.recv(1024) 
        if not data: # dados vazios: cliente encerrou
            print(str(endr) + ' -> desconectou')
            clisock.close() # encerra a conexao com o cliente
            return 
        header, *msg = data.decode('utf-8').split('\n') # pega o cabeçalho e a mensagem caso exista
        print(str(endr) + ': ' + header) # log
        msg = '\n'.join(msg) # junta a mensagem caso ela tenha sido separada
        cmd, key, tmh = header.split(' ') # separa o cabeçalho em comando, chave e tamanho da mensagem
        if (utf8len(header)+1)+int(tmh) > 1024: # caso o tamanho total da mensagem seja maior que 1024, continue recebendo a mensagem
            print('Mensagem muito grande, recebendo o restante...')
            print('Tamanho restante: '+str(int(tmh) - utf8len(msg)))
            restante = int(tmh) - utf8len(msg)
            msg += clisock.recv(restante).decode('utf-8')
            print('Mensagem recebida')
        
        match cmd: # verifica qual comando deve ser executado
            case 'insert':
                res = 'insert'
            case 'search':
                res = 'search'
            case 'remove':
                res = 'remove'
        
        clisock.send(res.encode('utf-8')) # envia a resposta para o cliente

# main thread

print("Servindo na porta 10001")
## define a localizacao do servidor
HOST = '' # vazio indica que podera receber requisicoes a partir de qq interface de rede da maquina
PORT = 10001 # porta de acesso
sock = iniciaServidor()
clientes = serve(sock) # inicia o servidor e ao finalizar, retorna as conexoes abertas para q sejam fechadas
print("Finalizando graciosamente, esperando fim das conexões abertas...")
finalizaServidor(clientes)
print("Até a próxima!")
from socket import *
import _thread

apelido = input("Escolha seu apelido: ")
serverIp = gethostname()
serverPort = 5555
cliente = socket(AF_INET, SOCK_STREAM)   #cria um socket tcp cliente
cliente.connect((serverIp, serverPort))  #se conecta a um  socket tcp servidor

def recebeMensagens():                                      #Funcao que recebe mensagens do servidor e printa elas
    while (1):
        mensagem = cliente.recv(1024).decode('ascii')   #Tenta receber uma mensagem do servidor(trava o programa aqui)
        if (mensagem == 'Apelido'):                     #Caso nao seja uma mensagem pedindo um Nick, printa a mensagem
            cliente.send(apelido.encode('ascii'))
        elif mensagem == 'close':                       #encerrar a conexao quando receber do server o sinal e sair da thread
            print("saindo desse chat maravigold")
            cliente.close()  
            _thread.exit()
            break
        else:
            print(mensagem)

recebe_thread = _thread.start_new_thread(recebeMensagens, ())   #inicia thread de recebimento de mensagem

while (1):
    mensagem = input()                 #Recebe input e concatena seu apelido + input
    if mensagem[0:9] == "send -all":
        cliente.send(mensagem.encode('ascii'))
    if mensagem == 'bye':
        cliente.send(mensagem.encode('ascii'))
        break
    if mensagem == 'list':
        cliente.send(mensagem.encode('ascii'))
    if mensagem[0:10] == 'send -user':
        cliente.send(mensagem.encode('ascii'))

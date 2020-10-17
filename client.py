from socket import *
import threading

apelido = input("Escolha seu apelido: ")
serverIp = '192.168.0.100'
serverPort = 5555
cliente = socket(AF_INET, SOCK_STREAM)   #cria um socket tcp cliente
cliente.connect((serverIp, serverPort))  #se conecta a um  socket tcp servidor

def recebeMensagens():                                      #Funcao que recebe mensagens do servidor e printa elas
    while (1):
        try:
            mensagem = cliente.recv(1024).decode('ascii')   #Tenta receber uma mensagem do servidor(trava o programa aqui)
            if (mensagem == 'Apelido'):                     #Caso nao seja uma mensagem pedindo um Nick, printa a mensagem
                cliente.send(apelido.encode('ascii'))
            else:
                print(mensagem)
        except:
            print("Ocorreu um erro")                        #Caso ocorra um erro, ele fecha o cliente e printa erro
            cliente.close()
            break

def escreve():                                              #funcao que que fica vendo se voce escreveu alguma coisa
    while (1):
        mensagem = apelido + ": " +  input()                 #Recebe input e concatena seu apelido + input
        cliente.send(mensagem.encode('ascii'))               #Envia mensagem para servidor

recebe_thread = threading.Thread(target= recebeMensagens)   #inicia thread de recebimento de mensagem
recebe_thread.start()

escreve_thread = threading.Thread(target= escreve)          #inicia thread de envio de mensagem
escreve_thread.start()
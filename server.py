from socket import *
import _thread
from datetime import datetime

serverName = "0.0.0.0" #local host
serverPort = 5555  

serverSocket = socket(AF_INET, SOCK_STREAM) #CRIA SOCKET TCP DO SERVER
serverSocket.bind((serverName,serverPort)) #Associa um ip e um numero de porta ao socket do server 
serverSocket.listen()                       #Fica ouvindo a porta e espera algum cliente se conectar, se colocar um numero no parametro, ele espera esse numero de clientes

clientes = []
apelidos = []
enderecos = []

def formataMensagem(cliente, mensagem): #FORMATA A MENSAGEM PARA DIZER O IP,PORTA, E APELIDO E DPS MENSAGEM
    index = clientes.index(cliente)
    data_e_hora_atuais = datetime.now()
    data_e_hora_em_texto = data_e_hora_atuais.strftime(" %Hh%M %d/%m/%Y")
    mensagemFinal = str(enderecos[index][0]) + ":" + str(enderecos[index][1]) + "/~" + str(apelidos[index]) + ": " + mensagem + data_e_hora_em_texto
    return mensagemFinal

def formataMensagemPrivada(cliente, mensagem, destino): #FORMATA A MENSAGEM PARA DIZER O IP,PORTA, E APELIDO E DPS MENSAGEM
    index = clientes.index(cliente)
    data_e_hora_atuais = datetime.now()
    data_e_hora_em_texto = data_e_hora_atuais.strftime(" %Hh%M %d/%m/%Y")
    mensagemFinal = str(enderecos[index][0]) + ":" + str(enderecos[index][1]) + "/~" + str(apelidos[index])  + ": "+ "(PM to "+ destino +") "+ mensagem + data_e_hora_em_texto
    return mensagemFinal
def formataMensagemPrivadaDest(cliente, mensagem, destino): #FORMATA A MENSAGEM PARA DIZER O IP,PORTA, E APELIDO E DPS MENSAGEM
    index = clientes.index(cliente)
    data_e_hora_atuais = datetime.now()
    data_e_hora_em_texto = data_e_hora_atuais.strftime(" %Hh%M %d/%m/%Y")
    mensagemFinal = str(enderecos[index][0]) + ":" + str(enderecos[index][1]) + "/~" + str(apelidos[index])  + ": "+ "(PM to you) "+ mensagem + data_e_hora_em_texto
    return mensagemFinal

def formataLista(apelidos): #enviar lista de users como uma string so
    msg = ""
    for user in apelidos:
        msg = msg + user + ", "
    msg = msg[:-2]
    return "Usuarios: " + msg


def broadcast(mensagem):                    #Funcao que envia uma mensagem para todos os clientes conectados!
    for cliente in clientes:                #Percorre vetor que contem todos os clientes
        cliente.send(mensagem)               #Manda mensagem para determinado cliente

def handle(cliente):                                        #Funcao que fica ouvindo se o cliente enviou uma mensagem
    while (1):                                           #tenta receber uma mensagem
        try:
            mensagem = cliente.recv(1024)               #Tenta receber mensagem do client
            mensagem = mensagem.decode('ascii')
        except:
            print("Cliente fechou a janela")
            index = clientes.index(cliente)
            apelido = apelidos[index]                   
            endereco = enderecos[index]        #envia a todos que um user saiu do chat
            apelidos.remove(apelido)                      #Tira o Apelido do vetor de apelidos
            enderecos.remove(endereco)                  #tira endereço do vetor de endereços
            clientes.remove(cliente)                    #retira o cliente do vetor de clientes
            desconectado = apelido + " saiu do chat"
            print(desconectado)
            broadcast(desconectado.encode('ascii'))
            cliente.close()                             #fecha conexão do cliente
            _thread.exit()
        if mensagem == 'bye':
            cliente.send('close'.encode('ascii'))       #envia sinal para o cliente fechar seu lado da conexão
            index = clientes.index(cliente)
            apelido = apelidos[index]                   
            endereco = enderecos[index]
            desconectado = apelido + " saiu do chat"
            print(desconectado)
            broadcast(desconectado.encode('ascii'))        #envia a todos que um user saiu do chat
            apelidos.remove(apelido)                      #Tira o Apelido do vetor de apelidos
            enderecos.remove(endereco)                  #tira endereço do vetor de endereços
            clientes.remove(cliente)                    #retira o cliente do vetor de clientes
            cliente.close()                             #fecha conexão do cliente
            _thread.exit()                              #fecha a thread do cliente
        elif mensagem == 'list':                            
            msg = formataLista(apelidos)                   #envia lista formatada para o cliente que a solicitou
            cliente.send(msg.encode('ascii'))
        elif mensagem[0:9] == "send -all":                  #faz broadcast das mensagens publicas
            mensagem = formataMensagem(cliente, mensagem[10:])
            broadcast(mensagem.encode('ascii'))
       
        elif mensagem[0:10] == "send -user":                #envia para o user (que existe) a mensagem privada
            lista = mensagem.split(' ')
            if lista[2] in apelidos:
                index = apelidos.index(lista[2])
                clienteDestino = clientes[index]
                cliente.send(formataMensagemPrivada(cliente," ".join(lista[3:]),lista[2]).encode('ascii'))
                clienteDestino.send(formataMensagemPrivadaDest(cliente," ".join(lista[3:]),lista[2]).encode('ascii'))
            else:                   
                #caso user nao exista, apenas retorna um erro para o cliente que a solicitou
                cliente.send("Usuario nao existe".encode('ascii'))
        

def conexoes():                                         #Funcao que aceita conexoes novas
    while (1):                                          #CUIDADO, SE VC RODAR O SERVER, TERA QUE FECHAR PROCESSO PYTHON NO GERENCIADOR DE TAREFAS
        cliente, endereco = serverSocket.accept()       #Trava o programa ate encontrar uma conexao e recebe tupla (cliente,endereco)
        palavra = "conectado endereco: " + (str(endereco))
        print(palavra)

        cliente.send('Apelido'.encode('ascii'))         #Pergunta ao cliente qual seu Apelido
        try:
            apelido = cliente.recv(1024).decode('ascii')       #recebe o apelido do cliente
            while apelido in apelidos:
                cliente.send('Apelido2'.encode('ascii'))         #Pergunta ao cliente qual seu Apelido
                apelido = cliente.recv(1024).decode('ascii')
            cliente.send('ok'.encode('ascii')) 
            apelidos.append(apelido)                        #Salva o apelido na lista de apelidos
            clientes.append(cliente)                        #Salva cliente na lista de clientes
            enderecos.append(endereco)
            
            menConexao = "O apelido do cliente eh: " + apelido          
            print(menConexao)                                          #Printa o apelido do cliente recebido no servidor

            menConexao = apelido + " entrou no chat"                    
            broadcast(menConexao.encode('ascii'))                      #Envia para todos os cliente que um novo usuario se conectou

            _thread.start_new_thread(handle, (cliente,))  #Cria uma thread para ficar ouvindo as mensagens desse cliente                                         #starta a Thread
        except:
            print("Tentativa de conexao falhou")
print("Server iniciado!")
conexoes()

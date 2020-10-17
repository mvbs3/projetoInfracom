from socket import *
import threading

serverName = '192.168.0.100' #local host
serverPort = 5555  

serverSocket = socket(AF_INET, SOCK_STREAM) #CRIA SOCKET TCP DO SERVER
serverSocket.bind((serverName, serverPort)) #Associa um ip e um numero de porta ao socket do server 
serverSocket.listen()                       #Fica ouvindo a porta e espera algum cliente se conectar, se colocar um numero no parametro, ele espera esse numero de clientes

clientes = []
apelidos = []
enderecos = []

def formataMensagem(cliente, mensagem): #FORMATA A MENSAGEM PARA DIZER O IP,PORTA, E APELIDO E DPS MENSAGEM
    index = clientes.index(cliente)
    mensagemFinal = str(enderecos[index][0])+":"+str(enderecos[index][1])+"\~"+str(apelidos[index])+": "+mensagem
    return mensagemFinal

def broadcast(mensagem):                    #Funcao que envia uma mensagem para todos os clientes conectados!
    for cliente in clientes:                #Percorre vetor que contem todos os clientes
        cliente.send(mensagem)               #Manda mensagem para determinado cliente

def handle(cliente):                                        #Funcao que fica ouvindo se o cliente enviou uma mensagem
    while (1):                                              #Loop infinito para ficar ouvindo o client
            try:                                            #tenta receber uma mensagem
                mensagem = cliente.recv(1024)               #Tenta receber mensagem do client
                mensagem = formataMensagem(cliente,mensagem.decode('ascii'))
                broadcast(mensagem.encode('ascii'))
            except:                                         #Caso nao consiga receber uma mensagem, faz algo
                index =clientes.index(cliente)              #Se der erro no recebimento da mensagem, desconecta o cliente, recebe o indice do cliente q bugou
                clientes.remove(cliente)                    #retira o cliente do vetor de clientes
                cliente.close()                             #desconecta cliente
                apelido = apelidos[index]                   #recebe o nome de quem saiu, para printar para todos que ele saiu
                endereco = enderecos[index]
                desconectado = apelido + " saiu do chat"
                broadcast(desconectado.encode('ascii'))
                apelidos.remove(apelido)                      #Tira o Apelido do vetor de apelidos
                enderecos.remove(endereco)
                break                                       #Quebra o loop

def conexoes():                                         #Funcao que aceita conexoes novas
    while (1):                                          #CUIDADO, SE VC RODAR O SERVER, TERA QUE FECHAR PROCESSO PYTHON NO GERENCIADOR DE TAREFAS
        cliente, endereco = serverSocket.accept()       #Trava o programa ate encontrar uma conexao e recebe tupla (cliente,endereco)
        palavra="conectado endereco: "+ (str(endereco))
        print(palavra)
        #print(str(endereco))

        cliente.send('Apelido'.encode('ascii'))         #Pergunta ao cliente qual seu Apelido
        apelido=cliente.recv(1024).decode('ascii')       #recebe o apelido do cliente
        apelidos.append(apelido)                        #Salva o apelido na lista de apelidos
        clientes.append(cliente)                        #Salva cliente na lista de clientes
        enderecos.append(endereco)
        
        menConexao = "O apelido do cliente eh: " + apelido          
        print(menConexao)                                          #Printa o apelido do cliente recebido no servidor
        menConexao = apelido + " entrou no chat"                    
        broadcast(menConexao.encode('ascii'))                      #Envia para todos os cliente que um novo usuario se conectou
        cliente.send("Voce se conectou no chat!".encode('ascii'))  #Envia o feedback para o cliente

        thread = threading.Thread(target=handle, args=(cliente,)) #Cria uma thread para ficar ouvindo as mensagens desse cliente
        thread.start()                                             #starta a Thread

print("Server iniciado!")
conexoes()
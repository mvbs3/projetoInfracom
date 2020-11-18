from socket import *
import PySimpleGUI as sg
import _thread

sg.theme('BluePurple')
serverPort = 5555
cliente = socket(AF_INET, SOCK_STREAM)   #cria um socket tcp cliente

#Cria uma caixa onde cada linha faz:
#Pede username
#pede IP do server
#botoes de OK e Cancelar
event, values = sg.Window('Login',
                  [[sg.T('Digite seu apelido:   '), sg.In(key='-ID-')],
                  [sg.T('Digite IP do servidor:'), sg.In(key='-IP-')],
                  [sg.B('OK', bind_return_key=True), sg.B('Cancel') ]]).read(close=True)
#caso vc clique no botao de sair, vc fecha o programa
if (event == "Cancel"): 
    quit()
#pega o apelido e o ip q vc inseriu
apelido = values['-ID-']
serverIp = values['-IP-']
mensagem = ""

#Caso o Username que vc insira tenha Espacos em branco, vc sera obrigado a colocar um nome que nao tenha espacos em branco
while ' ' in apelido:
    event, values = sg.Window('Login',
                  [[sg.T('Digite seu apelido sem espaço', key='-TEXTO-'), sg.In(key='-ID-')],
                  [sg.B('OK',bind_return_key=True), sg.B('Cancel') ]]).read(close=True)
    apelido = values['-ID-']
    if (event == "Cancel"):
        quit()

#AQUI VC VAI SE CONECTAR!!!!!!!!!!!!!!!!!!!!!!!!!!!!
cliente.connect((serverIp, serverPort))  #se conecta a um  socket tcp servidor

#RECEBE AAS MENSAGENS E PRINTA AS MENSAGENS NA TELA
def recebeMensagens():  
    global apelido                                    #Funcao que recebe mensagens do servidor e printa elas
    while (1):
        mensagem = cliente.recv(1024).decode('ascii')   #Tenta receber uma mensagem do servidor(trava o programa aqui)
        if mensagem == 'close':                       #encerrar a conexao quando receber do server o sinal e sair da thread
            print("Saindo desse chat")
            cliente.close()  
            _thread.exit()
            break
        else:
            print(mensagem)

#FUNCAO QUE SERVE PARA CHECAR SE O APELIDO Q VC ESCOLHEU JA FOI ESCOLHIDO
while mensagem != 'ok':
    mensagem = cliente.recv(1024).decode('ascii')   #Tenta receber uma mensagem do servidor(trava o programa aqui)
    if mensagem == 'Apelido':
        cliente.send(apelido.encode('ascii'))
    if mensagem == 'Apelido2':
        event, values = sg.Window('Login',
                  [[sg.T('Apelido ja escolhido, escolha outro.'), sg.In(key='-ID-')],
                  [sg.B('OK',bind_return_key=True), sg.B('Cancel') ]]).read(close=True)
        if (event == "Cancel"):
            quit()
        apelido = values['-ID-']
        while ' ' in apelido:
            event, values = sg.Window('Login',
                  [[sg.T('Digite seu apelido sem espaço', key='-TEXTO-'), sg.In(key='-ID-')],
                  [sg.B('OK',bind_return_key=True), sg.B('Cancel') ]]).read(close=True)
            apelido = values['-ID-']
            if (event == "Cancel"):
                quit()
        cliente.send(apelido.encode('ascii'))

#Define o layout do chat linhas sao:
#Usuario: apelido
#Define uma caixa de texto de saida, mostra todas as mensagens do chat
#Um input para vc escrever suas mensagens
#botoes de Enviar, limpar tela e Sair
layout = [[sg.Text("Usuario: " + apelido)],
          [sg.Output(size=(100,20), key='-OUTPUT-')],
          [sg.Input(key='-MSG-')],
          [sg.Button('Enviar', bind_return_key=True), sg.Button('Clear'), sg.Button('Sair')]]

#Inicia o chat
window = sg.Window('Chat', layout)

recebe_thread = _thread.start_new_thread(recebeMensagens, ())   #inicia thread de recebimento de mensagem

#LOOP que envia as suas entradas para o servidor
while True:  # Event Loop
    event, values = window.read() #lendo entrada
    window['-MSG-'].update("") 
    mensagem = values['-MSG-']
    if event == 'Clear':
        window['-OUTPUT-'].update("")
    if mensagem[0:9] == "send -all" or (event == 'Enviar' and  mensagem[0:9] == "send -all"):
        cliente.send(mensagem.encode('ascii'))
        window['-MSG-'].update("")
    if event == sg.WIN_CLOSED or mensagem == 'bye' or event == 'Sair':
        mensagem = 'bye'
        cliente.send(mensagem.encode('ascii'))
        break
    if mensagem == 'list':
        cliente.send(mensagem.encode('ascii'))
        window['-MSG-'].update("")
    if mensagem[0:10] == 'send -user'or (event == 'Enviar' and  mensagem[0:10] == "send -user"):
        window['-MSG-'].update("")
        cliente.send(mensagem.encode('ascii'))



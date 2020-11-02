from socket import *
import PySimpleGUI as sg
import _thread

sg.theme('BluePurple')

serverIp = gethostname()
serverPort = 5555
cliente = socket(AF_INET, SOCK_STREAM)   #cria um socket tcp cliente
cliente.connect((serverIp, serverPort))  #se conecta a um  socket tcp servidor

event, values = sg.Window('Login',
                  [[sg.T('Digite seu apelido'), sg.In(key='-ID-')],
                  [sg.B('OK', bind_return_key=True), sg.B('Cancel') ]]).read(close=True)

apelido = values['-ID-']

mensagem = ""
#apelido = input("Escolha seu apelido: ")
while ' ' in apelido:
    event, values = sg.Window('Login',
                  [[sg.T('Digite seu apelido sem espaco', key='-TEXTO-'), sg.In(key='-ID-')],
                  [sg.B('OK'), sg.B('Cancel') ]]).read(close=True)
    apelido = values['-ID-']
    #print("escolha um apelido sem espaco")
    #apelido = input("Escolha seu apelido: ")

layout = [[sg.Text("Usuário: " + apelido)],
          [sg.Output(size=(50,10), key='-OUTPUT-')],
          [sg.Input(key='-MSG-')],
          [sg.Button('Enviar', bind_return_key=True), sg.Button('Clear'), sg.Button('Sair')]]

window = sg.Window('Chat Maravigold', layout)

def recebeMensagens():  
    global apelido                                    #Funcao que recebe mensagens do servidor e printa elas
    while (1):
        mensagem = cliente.recv(1024).decode('ascii')   #Tenta receber uma mensagem do servidor(trava o programa aqui)
        if mensagem == 'close':                       #encerrar a conexao quando receber do server o sinal e sair da thread
            print("saindo desse chat maravigold")
            cliente.close()  
            _thread.exit()
            break
        else:
            print(mensagem)

while mensagem != 'ok':
    mensagem = cliente.recv(1024).decode('ascii')   #Tenta receber uma mensagem do servidor(trava o programa aqui)
    if mensagem == 'Apelido':
        cliente.send(apelido.encode('ascii'))
    if mensagem == 'Apelido2':
        event, values = sg.Window('Login',
                  [[sg.T('Apelido ja escolhido, escolha outro.'), sg.In(key='-ID-')],
                  [sg.B('OK'), sg.B('Cancel') ]]).read(close=True)
        apelido = values['-ID-']
        #apelido = input("Apelido ja escolhido, escolha outro: ") 
        cliente.send(apelido.encode('ascii'))

recebe_thread = _thread.start_new_thread(recebeMensagens, ())   #inicia thread de recebimento de mensagem

while True:  # Event Loop
    event, values = window.read()
    mensagem = values['-MSG-']
    if event == 'Clear':
        window['-OUTPUT-'].update("")
    if mensagem[0:9] == "send -all" or (event == 'Enviar' and  mensagem[0:9] == "send -all"):
        cliente.send(mensagem.encode('ascii'))
        #print(mensagem[10:])
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



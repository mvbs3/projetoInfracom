import PySimpleGUI as sg

sg.theme('BluePurple')


event, values = sg.Window('Login',
                  [[sg.T('Digite seu apelido'), sg.In(key='-ID-')],
                  [sg.B('OK', bind_return_key = True), sg.B('Cancel') ]]).read(close=True)

login_id = values['-ID-']

layout = [[sg.Output(size=(50,10), key='-OUTPUT-')],
          [sg.Input(key='-MSG-', enable_events=True)],
          [sg.Button('Enviar', bind_return_key=True), sg.Button('Clear'), sg.Button('Sair')]]

window = sg.Window('Chat Maravigold', layout)

while True:  # Event Loop
    event, values = window.read()
    if event == sg.WIN_CLOSED or values['-MSG-'] == 'bye' or event == 'Sair':
        break
    if event == 'Enviar':
        print(values['-MSG-'])
        # Update the "OUTPUTput" text element to be the value of "input" element
        window['-MSG-'].update("")
    if event == 'Clear':
        window['-OUTPUT-'].update("")

window.close()
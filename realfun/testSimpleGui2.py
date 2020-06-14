import PySimpleGUI as sg

choices = ('Red', 'Green', 'Blue', 'Yellow', 'Orange', 'Purple', 'Chartreuse')
framerates_ch = ('5','10', '15', '20', '25', '30')
layout = [  [sg.Text('What is your favorite color?')],
            [sg.Listbox(choices, size=(15, len(choices)), key='-COLOR-', enable_events=True)],
            [sg.Text('framerate [fps]')], 
            [sg.Listbox(framerates_ch, size=(15, len(framerates_ch)), key='-FRAMERATE-', enable_events=True)],

          ]

window = sg.Window('Pick a color', layout)

while True:                  # the event loop
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if values['-COLOR-']:    # if something is highlighted in the list
        sg.popup(f"Your favorite color is {values['-COLOR-'][0]}")
   #"""  if event == 'Ok':
   #     if values['-COLOR-']:    # if something is highlighted in the list
   #         sg.popup(f"Your favorite color is {values['-COLOR-'][0]}") """
window.close()
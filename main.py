from psychopy import visual, event
from datetime import datetime
from Env_variables import *
import time
import random

win = visual.Window(fullscr=True)
mouse = event.Mouse()

test_score = []
proper_score = []
score_table = []


def text(text_to_print, color='white', height=0.1, pos=(0, 0)):
    return visual.TextStim(win, text=text_to_print, color=color, height=height, pos=pos)


def single_session():
    mouseIsDown = False
    time.sleep(0.5)
    squares_table = []
    times = []
    level = 0
    game_flag = True
    for square in squares:
        square.setAutoDraw(not square.autoDraw)
    while game_flag:
        level += 1
        level_text = text(f'Poziom: {level}', pos=(0, 0.8))
        level_text.draw()
        win.flip()
        square = random.randrange(0, 9)
        squares_table.append(square)
        time.sleep(0.5)
        for i in range(0, len(squares_table)):
            win.mouseVisible = False
            squares[squares_table[i]].fillColor = square_click_color
            level_text.draw()
            win.flip(clearBuffer=False)
            time.sleep(0.5)
            squares[squares_table[i]].fillColor = square_basic_color
            level_text.draw()
            win.flip(clearBuffer=False)
        win.mouseVisible = True
        # Początek mierzenia czasu
        start = time.time()

        for i in range(0, len(squares_table)):
            while True:
                if mouse.getPressed()[0] == 1 and mouseIsDown == False:
                    mouseIsDown = True

                if mouse.getPressed()[0] == 0 and mouseIsDown:
                    if squares[squares_table[i]].contains(mouse):
                        squares[squares_table[i]].fillColor = square_click_color
                        level_text.draw()
                        win.flip()
                        time.sleep(0.2)
                        squares[squares_table[i]].fillColor = square_basic_color
                        level_text.draw()
                        win.flip()
                        mouseIsDown = False
                        break
                    else:

                        game_flag = False
                        for square in squares:
                            square.setAutoDraw(False)
                        win.flip()
                        break
        end = time.time()
        times.append(round(end - start, 3))
    return [level - 1, times[ : -1], squares_table]


# Create a text stimulus
text1 = visual.TextStim(win, text='Witaj w eksperymencie badającym Twoją pamięć sekwencyjną. Celem tego testu jest '
                                  'ocena Twoich umiejętności zapamiętywania kolejnych elementów w sekwencji. Prosimy o '
                                  'dokładne zapoznanie się z poniższymi instrukcjami i postępowanie zgodnie z nimi. '
                                  , color='white', height=0.06, pos=(0, 0.6))
text2 = visual.TextStim(win, text='1.Test składa się z pojedynczych etapów, na każdym z nich będzie widoczna '
                                  'siatka dziewięciu kwadratów ułożonych w formie 3x3. \n2.Na każdym etapie pewna ilość '
                                  'kwadratów zostanie podświetlonych w konkretnej kolejności. \n3.Po wyświetleniu '
                                  'sekwencji, Twoim zadaniem jest kliknięcie tych samych kwadratów, w tej samej '
                                  'kolejności \n4.Każdy kolejny etap wyświetli tę samą sekwencję kwadratów z jednym '
                                  'dodatkowym podświetleniem na końcu sekwencji. \n5.Pierwszy etap będzie się składał '
                                  'tylko z jednego podświetlenia. \n6.Zanim przystąpisz do sesji eksperymentalnych, '
                                  'najpierw przejdziesz sesje testowe składające się z ' + str(
    NUMBER_OF_TRAINING_SESSIONS) + ' osobnych prób aby zapoznać '
                                   'się z przebiegiem zadania. Jeżeli jesteś gotowy_a, naciśnij spację aby rozpocząć '
                                   'sesje testowe. Powodzenia!', color='white', height=0.06, pos=(0, -0.3), alignText='left')

text1.draw()
text2.draw()
win.flip()

# Creating square grid
squares = []
square_size = 0.35  # Size of each square
grid_size = 3  # Number of squares per row/column in the grid
gap = 0.1  # Gap between squares

grid_width = (grid_size * square_size) + ((grid_size - 1) * gap)
start_x = -grid_width / 3
start_y = grid_width / 3

for row in range(grid_size):
    for col in range(grid_size):
        x = start_x + (col * (square_size + gap))
        y = start_y - (row * (square_size + gap))
        square = visual.Rect(
            win,
            width=square_size,
            height=square_size,
            fillColor=square_basic_color,
            pos=(x, y)
        )
        squares.append(square)

mouseIsDown = False
# Main event loop
while True:
    # Check for keyboard events
    keys = event.getKeys()
    if 'space' in keys:
        # Toggle the visibility of all squares
        for i in range(0, NUMBER_OF_TRAINING_SESSIONS):
            wynik = single_session()
            score_table.append(wynik)
            test_score.append(wynik[0])
            between_text = text(f'Ukończyłeś/aś {i + 1} sesję treningową z wynikiem: {wynik[0]}', pos=(0, 0.8))
            if i < NUMBER_OF_TRAINING_SESSIONS - 1:
                between_text2 = text(
                    f'Do rozegrania zostało jeszcze {NUMBER_OF_TRAINING_SESSIONS - i - 1} sesji testowych, naciśnij spację aby rozpocząć.',
                    pos=(0, 0.3))
                between_text.draw()
                between_text2.draw()
                win.flip()
                while True:
                    keys = event.getKeys()
                    if 'space' in keys:
                        break
            else:
                between_text3 = text(
                    f'Jeżeli jesteś gotowy_a, naciśnij spację aby rozpocząć sesję eksperymentalną. Powodzenia!',
                    pos=(0, 0.3))
                between_text.draw()
                between_text3.draw()
                win.flip()
                while True:
                    keys = event.getKeys()
                    if 'space' in keys:
                        break
        for i in range(0, NUMBER_OF_PROPER_SESSIONS):
            wynik = single_session()
            score_table.append(wynik)
            proper_score.append(wynik[0])
            between_text = text(f'Gratulujemy ukończenia {i + 1} sesji eksperymentalnej. Twój wynik to: {wynik[0]}.',
                                pos=(0, 0.8))
            if i < NUMBER_OF_PROPER_SESSIONS - 1:
                between_text2 = text(
                    f'Do rozegrania zostało jeszcze {NUMBER_OF_PROPER_SESSIONS - i - 1} sesji eksperymentalnych, naciśnij spację aby rozpocząć.',
                    pos=(0, 0.3))
                between_text.draw()
                between_text2.draw()
                win.flip()
                while True:
                    keys = event.getKeys()
                    if 'space' in keys:
                        break
        end_text = text(
            f'Gratulujemy ukończenia eksperymentu. Twój wynik w etapach testowych to: {test_score}.Twój wynik w etapach eksperymentalnym to: {proper_score}. Dziękujemy za wzięcie udziału w badaniu!',
            pos=(0, 0.4))
        end_text.draw()
        win.flip()
        while True:
            keys = event.getKeys()
            if 'space' in keys:
                break
        break
# Close the window
win.close()

# Saving data to file
now = datetime.now()
num_lines = sum(1 for _ in open('../zapis.txt'))
plec = input("Podaj plec osoby: 'm', 'k' lub 'inna': ")
wiek = input("Podaj wiek osoby: ")
with open('../zapis.txt', 'a+') as f:
    f.write(str(num_lines + 1) + ' ' + plec + ' ' + wiek + ' Data ukończenia eksperymentu: ' + str(now) + ' ' + str(score_table) + '\n')

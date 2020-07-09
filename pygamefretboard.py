import pygame
from math import floor
import random
import time
random.seed(time.time())

pygame.init()

screen = pygame.display.set_mode([1300, 900])
pygame.display.set_caption("Fretboard Learning")
black = (0, 0, 0)
grey = (150, 150, 150)
WHITE = (255, 255, 255)
red = (255, 0, 0)
mode = "main menu"
status = ''
running = True
score = 0
objective = 'Choose a game mode (1,2)'
font = pygame.font.Font(pygame.font.get_default_font(), 24)
bigfont = pygame.font.Font(pygame.font.get_default_font(), 32)
smallfont = pygame.font.Font(pygame.font.get_default_font(), 16)
# Setting string height
stringht = []
for i in range(6):
    stringht.extend([575 + 50 * i])
# Setting Fret distances,fretboard is 1200px but displays up to 1 octave/ 12th fret(half string length) so use 2400px as 'string length'.
# Every fret moves up 1/17.817 of the remainign vibrating portion of the string.
fret = [floor(2400 / 17.817)]
for i in range(11):
    fret.extend([floor(fret[i] + (2400 - fret[i]) / 17.817)])

# Defining notes, will use modular arithmetic on list index
Notes = ['E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B', 'C', 'C#/Db', 'D', 'D#/Eb']
# Recall Notes[0] = 'E'
Stringname = ['high E', 'B', 'G', 'D', 'A', 'low E']

# Setting up a gamelog (For debugging and for user instructions)
gamelog = ['Game Log:', '...', '...', '...', '...', '...', '...']

def gamelogtext(text):
    for i in range(1, len(gamelog)-1):
        gamelog[i] = gamelog[i + 1]
    gamelog[6] = text

def gamelogrender():
    for i in range(7):
        screen.blit(smallfont.render(gamelog[i], True, WHITE), (100, 100+20*i))


gamelogtext('initializing...')
gamelogtext('Select game mode: Press 1 or 2')
gamelogtext('Mode 1: Identify highlighted notes')
gamelogtext('Mode 2: Find named note on given string')



# Note buttons
class notebutton():
    def __init__(self, x, y, text=''):
        self.x = x
        self.y = y
        self.text = text

    def draw(self):
        pygame.draw.rect(screen, grey, (self.x, self.y, 75, 50), 0)
        text = font.render(self.text, 1, black)
        screen.blit(text, (self.x + 38 - floor(text.get_width() / 2), self.y + 25 - floor(text.get_height() / 2)))

    def hover(self, pos):
        if self.x < pos[0] < self.x + 75 and pos[1] > self.y and pos[1] < self.y + 50:
            return True
        return False


mynotebuttons = []
for i in range(12):
    mynotebuttons.extend([notebutton(50 + 100 * i, 450, Notes[i])])

# Fretbutton
class fretbutton():
    def __init__(self, x, y, text=''):
        self.x = x
        self.y = y
        self.text = text
    def draw(self):
        pygame.draw.circle(screen, grey, (self.x, self.y), 15)
    def hover(self, pos):
        if ((pos[0]-self.x)**2) * (pos[1]-self.y)**2 < 16:
            return True
        return False
fretbuttonxloc = [floor(50+fret[0]/2)]
fretbuttonxloc.extend([50+floor((fret[i]+fret[i-1])/2) for i in range(1,12)])
fretbuttons = [[fretbutton(fretbuttonxloc[i],stringht[0],Notes[(i+1)%len(Notes)]) for i in range(12)]]
fretbuttons.extend([[fretbutton(fretbuttonxloc[i],stringht[1],Notes[(i+8)%len(Notes)]) for i in range(12)]])
fretbuttons.extend([[fretbutton(fretbuttonxloc[i],stringht[2],Notes[(i+4)%len(Notes)]) for i in range(12)]])
fretbuttons.extend([[fretbutton(fretbuttonxloc[i],stringht[3],Notes[(i+11)%len(Notes)]) for i in range(12)]])
fretbuttons.extend([[fretbutton(fretbuttonxloc[i],stringht[4],Notes[(i+6)%len(Notes)]) for i in range(12)]])
fretbuttons.extend([[fretbutton(fretbuttonxloc[i],stringht[5],Notes[(i+1)%len(Notes)]) for i in range(12)]])
# First index: string, second index= fret

# MAIN GAME LOOP
while running:
    # Everything that needs to be drawn:
    screen.fill(black)
    pygame.draw.rect(screen, (180, 121, 33), [50, 550, 1200, 300])  # Fretboard
    # Frets and strings
    for i in range(12):
        pygame.draw.line(screen, grey, [50 + fret[i], 550], [50 + fret[i], 850], 2)
    for i in range(6):
        pygame.draw.line(screen, grey, [50, stringht[i]], [1250, stringht[i]], floor(2 + i / 2))
    # Note buttons
    for i in range(12):
        mynotebuttons[i].draw()
        for j in range(6):
            fretbuttons[j][i].draw()
    if mode != "main menu" and status == '':
        LFstr = random.randint(0, 5)
        if mode == "1":
            LFfr = random.randint(0,11)
            objective = "Name the note on fret "+ str(LFfr+1) + " of the " + Stringname[LFstr] +" string."
            gamelogtext(objective)
            status = 'waiting'
        if mode == "2":
            LFnote = random.randint(0,11)
            objective = "Find the note "+ Notes[LFnote] + " on the " + Stringname[LFstr] +" string."
            gamelogtext(objective)
            status = 'waiting'
    if mode == "1" and status == 'waiting':
        pygame.draw.circle(screen, (255, 0, 0), (fretbuttons[LFstr][LFfr].x, fretbuttons[LFstr][LFfr].y), 15)
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if mode == "main menu":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    mode = "1"
                    gamelogtext('mode 1 has been selected')
                if event.key == pygame.K_2:
                    mode = "2"
                    gamelogtext('mode 2 has been selected')
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mode == "1":
                for i in range(12):
                    if mynotebuttons[i].hover(pygame.mouse.get_pos()):
                        if mynotebuttons[i].text == fretbuttons[LFstr][LFfr].text:
                            gamelogtext('CORRECT!')
                            score += 10
                            status = ''
                        else:
                            gamelogtext('INCORRECT!')
                            score += -10
                            status = ''

            if mode == "2":
                for i in range(12):
                    if fretbuttons[LFstr][i].hover(pygame.mouse.get_pos()):
                        if fretbuttons[LFstr][i].text == Notes[LFnote]:
                            gamelogtext('CORRECT!')
                            score += 10
                            status = ''
                        else:
                            gamelogtext('INCORRECT!')
                            score += -10
                            status = ''
                print()
    gamemodetext = font.render('The current game mode is: ' + mode, True, WHITE)
    gmtextrect = gamemodetext.get_rect()
    gmtextrect.center = (600, 20)
    screen.blit(gamemodetext, gmtextrect)
    gamelogrender()
    text2 = smallfont.render('Mouse position (for debugging):' + str(pygame.mouse.get_pos()), True, WHITE)
    screen.blit(text2, (900, 50))
    scoretext = smallfont.render('Your score:' + str(score), True, WHITE)
    screen.blit(scoretext, (900, 100))
    objectivetext = bigfont.render(objective, True, WHITE)
    screen.blit(objectivetext, (400, 400))
    #Fret Markers:
    fretfivemarker = font.render('5', True, red)
    screen.blit(fretfivemarker, (fretbuttonxloc[4],520))
    fretsevenmarker = font.render('7', True, red)
    screen.blit(fretsevenmarker, (fretbuttonxloc[6],520))
    fretninemarker = font.render('9', True, red)
    screen.blit(fretninemarker, (fretbuttonxloc[8],520))

    pygame.display.flip()
pygame.quit()

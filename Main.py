from lib2to3.pgen2.token import ATEQUAL
import pygame
from pygame.locals import *
import paho.mqtt.client as mqtt
import time

# MQTT configs

mqttBroker = "labdigi.wiseful.com.br"
mqttPort = 80
client = mqtt.Client("Python_Client_GrupoB1")
client.username_pw_set("grupo1-bancadaB1", "L@Bdygy1B1")
client.connect(mqttBroker, mqttPort)

clientLed1 = mqtt.Client("Python_Client_GrupoB1_Led1")
clientLed1.username_pw_set("grupo1-bancadaB1", "L@Bdygy1B1")
clientLed1.connect(mqttBroker, mqttPort)

clientLed2 = mqtt.Client("Python_Client_GrupoB1_Led2")
clientLed2.username_pw_set("grupo1-bancadaB1", "L@Bdygy1B1")
clientLed2.connect(mqttBroker, mqttPort)

clientLed3 = mqtt.Client("Python_Client_GrupoB1_Led3")
clientLed3.username_pw_set("grupo1-bancadaB1", "L@Bdygy1B1")
clientLed3.connect(mqttBroker, mqttPort)

clientLed4 = mqtt.Client("Python_Client_GrupoB1_Led4")
clientLed4.username_pw_set("grupo1-bancadaB1", "L@Bdygy1B1")
clientLed4.connect(mqttBroker, mqttPort)

b0 = "grupo1-bancadaB1/E3"
b1 = "grupo1-bancadaB1/E4"
b2 = "grupo1-bancadaB1/E5"
b3 = "grupo1-bancadaB1/E6"

l0 = "grupo1-bancadaB1/S4"
l1 = "grupo1-bancadaB1/S5"
l2 = "grupo1-bancadaB1/S6"
l3 = "grupo1-bancadaB1/S7"

# username = 'emqx'
# password = 'public'

# Game interface configs

mainClock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption("Piano Genius")

screenWidth = 550
screenHeight = 700

screen = pygame.display.set_mode((screenWidth,screenHeight))

logo = pygame.image.load("logoNoBorderTransparent.png")
strt = pygame.image.load("start.png")
stat  = pygame.image.load("_stats.png")
rst = pygame.image.load("srest.png")
faixa1 = pygame.image.load("_faixa1.png")
faixa2 = pygame.image.load("_faixa2.png")
faixa3 = pygame.image.load("_faixa3.png")
faixa4 = pygame.image.load("_faixa4.png")
faixa1play = pygame.image.load("_faixa1play.png")
faixa2play = pygame.image.load("_faixa2play.png")
faixa3play = pygame.image.load("_faixa3play.png")
faixa4play = pygame.image.load("_faixa4play.png")

slctTxt = pygame.image.load("_trackSelect.png")
running = True 

game_font = pygame.font.Font("Minecraft.ttf", 55)

totalHits = 0
totalMisses = 0
highScore = 0

def Stats():
    running = True
    click = False
    global totalHits
    global totalMisses
    global highScore
    
    while running:
        _hits = "Total hits: " + str(totalHits)
        _misses = "Total misses: " + str(totalMisses)      
        _high = "Highscore: " + str(highScore)
        screen.fill((151, 204, 187))
        
        title_render = game_font.render("Estatisticas:", True, (59, 115, 103))
        screen.blit(title_render, ((screenWidth-title_render.get_width())/2,70))

        hits_render = game_font.render(_hits, True, (59, 115, 103))
        screen.blit(hits_render,((screenWidth-hits_render.get_width())/2,100+title_render.get_height()))

        misses_render = game_font.render(_misses, True, (59, 115, 103))
        screen.blit(misses_render,((screenWidth-misses_render.get_width())/2,100+title_render.get_height()+70+hits_render.get_height()))

        high_render = game_font.render(_high, True, (59, 115, 103))
        screen.blit(high_render,((screenWidth-high_render.get_width())/2,100+title_render.get_height()+hits_render.get_height()+misses_render.get_height()+70+70))

        

        faixa1btn = pygame.Rect((screenWidth-200)/2,200+title_render.get_height()+hits_render.get_height()+misses_render.get_height()+70+70,200,80)
        

        screen.blit(rst, ((screenWidth-200)/2,200+title_render.get_height()+hits_render.get_height()+misses_render.get_height()+70+70))
        

    
        #Mouse Controller
        mx, my = pygame.mouse.get_pos()
        
        if faixa1btn.collidepoint((mx, my)):
            if click:
                totalHits = 0
                totalMisses = 0
                highScore = 0
    
        click = False
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            if event.type == QUIT:
                pygame.quit()
                
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        mainClock.tick(60)

led1=0
led2=0
led3=0
led4=0
iterador = 0
def decodeLed1(client, userdata, message):
    global led1
    anterior = led1
    led1 = int(message.payload.decode("utf-8"))
    if anterior == 0 and led1 == 1:
        iterador += 1



def decodeLed2(client, userdata, message):
    global led2
    anterior = led2
    led2 = int(message.payload.decode("utf-8"))
    if anterior == 0 and led2 == 1:
        iterador += 1

def decodeLed3(client, userdata, message):
    global led3
    anterior = led3
    led3 = int(message.payload.decode("utf-8"))
    if anterior == 0 and led3 == 1:
        iterador += 1

def decodeLed4(client, userdata, message):
    global led4
    anterior = led4
    led4 = int(message.payload.decode("utf-8"))
    if anterior == 0 and led4 == 1:
        iterador += 1

def Faixa(n, id):
    begin = int(round(time.time()*1000))
    topico = "grupo1-bancadaB1/E" + str(id+2)
    maxnotes = n
    running = True
    click = False
    acertos = 0
    misses = 0
    delay = 240/id
    pontuacao = 0

    global led1
    global led2
    global led3
    global led4

    clientLed1.on_message = decodeLed1
    clientLed1.subscribe("grupo1-bancadaB1/S4")
    
    clientLed2.on_message = decodeLed2
    clientLed2.subscribe("grupo1-bancadaB1/S5")

    clientLed3.on_message = decodeLed3
    clientLed3.subscribe("grupo1-bancadaB1/S6")

    clientLed4.on_message = decodeLed4
    clientLed4.subscribe("grupo1-bancadaB1/S7")

    client.on_message = decodeBit
    client.subscribe([("grupo1-bancadaB1/E3",0),("grupo1-bancadaB1/E4",0),("grupo1-bancadaB1/E5",0),("grupo1-bancadaB1/E6",0)])
    global instr
    global totalHits
    global totalMisses
    global highScore
    first = True
    while running:
        time.sleep(0.2)
        client.loop_start()
        clientLed1.loop_start()
        clientLed2.loop_start()
        clientLed3.loop_start()
        clientLed4.loop_start()
        if(pontuacao>highScore):
            highScore = pontuacao

        if instr != 0:
            print(instr)        
    

        screen.fill((151, 204, 187))
        title_render = game_font.render("Faixa "+str(id), True, (59, 115, 103))
        screen.blit(title_render, ((screenWidth-title_render.get_width())/2,70))

        hits = "Hits: " + str(acertos)
        pont_render = game_font.render(hits, True, (59, 115, 103))
        screen.blit(pont_render,((screenWidth-pont_render.get_width())/2,200))
        
        erros = "Misses: " + str(misses)
        mis_render = game_font.render(erros, True, (59, 115, 103))
        screen.blit(mis_render,((screenWidth-mis_render.get_width())/2,200 + pont_render.get_height()))

        
        pontos = "Score: " + str(pontuacao)
        score_render = game_font.render(pontos, True, (59, 115, 103))
        screen.blit(score_render,((screenWidth-score_render.get_width())/2,200 + pont_render.get_height() + mis_render.get_height()))
        

        if(acertos + misses >= maxnotes):
            end_render = game_font.render("Fim da faixa!", True, (59, 115, 103))
            screen.blit(end_render,((screenWidth-end_render.get_width())/2,200 - pont_render.get_height()))

        #Mouse Controller
        mx, my = pygame.mouse.get_pos()
        
        
        click = False
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            if event.type == QUIT:
                pygame.quit()
                
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    if(delay>0):
                        pontuacao += 100 * delay // (240/id)
                    else:
                        pontuacao += 1
                    delay = 240/id
                    acertos+=1
                    totalHits+=1
                if event.key == K_DOWN:
                    misses+=1
                    totalMisses+=1
                    instr = 0
                    delay = 240/id

                if event.key == K_ESCAPE:
                    running = False

        if (click and acertos + misses >= maxnotes):
            print(topico)
            client.publish(topico, id)
            time.sleep(.1)
            client.publish(topico, 0)
            pygame.time.delay(300)
            running = False
        delay -=1
        pygame.display.update()
        mainClock.tick(60)

        if (instr!=0 and acertos + misses >= maxnotes):
            print(topico)
            client.publish(topico, id)
            client.publish(topico, 0)
            pygame.time.delay(300)
            running = False
        
        if(instr == 1 and led1):
            if(delay>0):
                pontuacao += 100 * delay // (240/id)
            else:
                pontuacao += 1
            delay = 240/id
            acertos+=1
            totalHits+=1
            instr = 0

        elif(instr == 2 and led2):
            if(delay>0):
                pontuacao += 100 * delay // (240/id)
            else:
                pontuacao += 1
            delay = 240/id
            acertos+=1
            totalHits+=1
            instr = 0
        
        elif(instr == 3 and led3):
            if(delay>0):
                pontuacao += 100 * delay // (240/id)
            else:
                pontuacao += 1
            delay = 240/id
            acertos+=1
            totalHits+=1
            instr = 0
        
        elif(instr == 4 and led4):
            if(delay>0):
                pontuacao += 100 * delay // (240/id)
            else:
                pontuacao += 1
            delay = 240/id
            acertos+=1
            totalHits+=1
            instr = 0

        elif((instr!=0 and not first and (int(round(time.time()*1000)) - begin > 1500))):
            misses+=1
            totalMisses+=1
            instr = 0
            delay = 240/id
        print(delay)
        first = False
        
        
instr = 0

def decodeBit(client, userdata, message):
    global instr
    instr = int(message.payload.decode("utf-8"))
    
     

# Game Screen
def GameSelect():
    global instr
    client.on_message = decodeBit
    client.subscribe([("grupo1-bancadaB1/E3",0),("grupo1-bancadaB1/E4",0),("grupo1-bancadaB1/E5",0),("grupo1-bancadaB1/E6",0)])
    running = True
    click = False

    while running:
        if instr != 0:
            print(instr)        
        client.loop_start()
        screen.fill((151, 204, 187))
        screen.blit(slctTxt, ((screenWidth-400)/2,30))

        faixa1btn = pygame.Rect((screenWidth-200)/2,30+80+120,200,80)
        faixa2btn = pygame.Rect((screenWidth-200)/2,30+80+120+80+30,200,80)
        faixa3btn = pygame.Rect((screenWidth-200)/2,30+80+120+30+80+80+30,200,80)
        faixa4btn = pygame.Rect((screenWidth-200)/2,30+80+120+30+30+80+80+80+30,200,80)

        screen.blit(faixa1, ((screenWidth-200)/2,30+80+120))
        screen.blit(faixa2, ((screenWidth-200)/2,30+80+120+80+30))
        screen.blit(faixa3, ((screenWidth-200)/2,30+80+120+30+80+80+30))
        screen.blit(faixa4, ((screenWidth-200)/2,30+80+120+30+30+80+80+80+30))

    
        #Mouse Controller
        mx, my = pygame.mouse.get_pos()
        
        if faixa1btn.collidepoint((mx, my)) or instr == 1:
            if click or instr == 1:
                client.publish(b0, 1)
                time.sleep(0.1)
                client.publish(b0, 0)
                time.sleep(0.1)
                Faixa(30, 1)
        if faixa2btn.collidepoint((mx, my)) or instr == 2:
            if click or instr == 2:
                client.publish(b1, 1)
                time.sleep(0.1)
                client.publish(b1, 0)
                time.sleep(0.1)
                Faixa(30,2)
        if faixa3btn.collidepoint((mx, my)) or instr == 3:
            if click or instr == 3:
                client.publish(b2, 1)
                time.sleep(0.1)
                client.publish(b2, 0)
                time.sleep(0.1)
                Faixa(30, 3)
        if faixa4btn.collidepoint((mx, my)) or instr == 4:
            if click or instr == 4:
                client.publish(b3, 1)
                time.sleep(0.1)
                client.publish(b3, 0)
                time.sleep(0.1)
                Faixa(30, 4)

        click = False
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

            if event.type == QUIT:
                pygame.quit()
                
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        
        pygame.display.update()
        mainClock.tick(60)
    


# Main menu screen

click = False
while running:
    screen.fill((151, 204, 187))
    screen.blit(logo, ((screenWidth-332)/2,15))

    startButton = pygame.Rect((screenWidth-200)/2,398,200,80)
    resetButton = pygame.Rect((screenWidth-200)/2,398+80+63,200,80)    
 
    screen.blit(strt, ((screenWidth-200)/2,398))
    screen.blit(stat, ((screenWidth-200)/2,398+80+63))
    
    #Mouse Controller
    mx, my = pygame.mouse.get_pos()

    if startButton.collidepoint((mx, my)):
        if click:
            GameSelect()
    if resetButton.collidepoint((mx, my)):
        if click:
            print('reset')
            Stats()

    click = False
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True


    for event in pygame.event.get():    
        if event.type == pygame.QUIT:
            running = False
        if event.type == KEYDOWN:
            # If the Backspace key has been pressed set
            # running to false to exit the main loop
            if event.key == K_BACKSPACE or event.key == K_ESCAPE:
                running = False
    pygame.display.update()
    mainClock.tick(60)
                


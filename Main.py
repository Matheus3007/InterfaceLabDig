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

btns_topics = ["grupo1-bancadaB1/E0", "grupo1-bancadaB1/E1", "grupo1-bancadaB1/E2", "grupo1-bancadaB1/E3"]
leds_topics = ["grupo1-bancadaB1/S0", "grupo1-bancadaB1/S1", "grupo1-bancadaB1/S2", "grupo1-bancadaB1/S3"]

# Game interface configs

mainClock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption("Piano Genius")

screenWidth = 550
screenHeight = 700

screen = pygame.display.set_mode((screenWidth,screenHeight))

logo = pygame.image.load("logoNoBorderTransparent.png")
strt = pygame.image.load("start.png")
stat  = pygame.image.load("stats.png")
rst = pygame.image.load("srest.png")
faixa1 = pygame.image.load("faixa1.png")
faixa2 = pygame.image.load("faixa2.png")
faixa3 = pygame.image.load("faixa3.png")
faixa4 = pygame.image.load("faixa4.png")
faixa1play = pygame.image.load("faixa1play.png")
faixa2play = pygame.image.load("faixa2play.png")
faixa3play = pygame.image.load("faixa3play.png")
faixa4play = pygame.image.load("faixa4play.png")

slctTxt = pygame.image.load("trackSelect.png")
running = True 

game_font = pygame.font.Font("Minecraft.ttf", 55)

totalHits = 0
totalMisses = 0
highScore = 0
led_recieved = 0
btn_recieved = 0
misses = 0
id = 0
delay = 0
pontuacao = 0
acertos = 0

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

iterator = 0

def callback(client, userdata, message):
    global led_recieved
    global btn_recieved
    global iterator
    global misses
    global totalMisses
    global id
    global acertos
    global totalHits
    global delay
    global pontuacao

    print("AAAAAAAAAA")

    for i in range(4):
        if message.topic == leds_topics[i]:
            if int(message.payload.decode("utf-8")) == 1:
                led_recieved = i + 1
            else:     
                iterator += 1
                led_recieved = 0
                
                if btn_recieved == 0:
                    misses += 1
                    totalMisses += 1
                    delay = 60 * (6 - id)

            btn_recieved = 0


    for i in range(4):
        if message.topic == btns_topics[i]:
            if int(message.payload.decode("utf-8")) == 1:
                if btn_recieved == 0:
                    btn_recieved = i + 1

                    if iterator >= 30:
                        return

                    if led_recieved == btn_recieved:
                        if(delay > 0):
                            pontuacao += 100 * delay // (240 / id)
                        else:
                            pontuacao += 1
                        acertos += 1
                        totalHits += 1
                    else:
                        misses += 1
                        totalMisses += 1

                    delay = 60 * (6 - id)


def Faixa(n):
    global id
    global misses
    global delay
    global pontuacao
    global acertos
    global iterator

    begin = int(round(time.time()*1000))
    topico = "grupo1-bancadaB1/E" + str(id+2)
    maxnotes = n
    running = True
    click = False
    acertos = 0
    delay = 240/id
    pontuacao = 0
    misses = 0
    iterator = 0

    client.on_message = callback

    for topic in leds_topics:
        client.subscribe(topic)

    for topic in btns_topics:
        client.subscribe(topic)

    global btn_recieved
    global totalHits
    global totalMisses
    global highScore

    btn_recieved = 0

    first = True
    while running:
        time.sleep(0.2)
        client.loop_start()

        if(pontuacao>highScore):
            highScore = pontuacao

        if btn_recieved != 0:
            print(btn_recieved)        
    

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
        

        if(iterator >= maxnotes):
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
                    if(delay > 0):
                        pontuacao += 100 * delay // (240/id)
                    else:
                        pontuacao += 1
                    delay = 240/id
                    acertos += 1
                    totalHits += 1
                if event.key == K_DOWN:
                    misses += 1
                    totalMisses += 1
                    btn_recieved = 0
                    delay = 240/id

                if event.key == K_ESCAPE:
                    running = False

        if (click and iterator >= maxnotes):
            print(topico)
            client.publish(topico, id)
            time.sleep(.1)
            client.publish(topico, 0)
            pygame.time.delay(300)
            running = False
        delay -=1
        pygame.display.update()
        mainClock.tick(60)

        if (btn_recieved!=0 and iterator >= maxnotes):
            print(topico)
            client.publish(topico, id)
            client.publish(topico, 0)
            pygame.time.delay(300)
            running = False

        # print(delay)
        first = False

# Game Screen
def GameSelect():
    global btn_recieved
    global id
    
    client.on_message = callback

    for topic in leds_topics:
        client.subscribe(topic)

    for topic in btns_topics:
        client.subscribe(topic)

    running = True
    click = False

    while running:
        if btn_recieved != 0:
            print(btn_recieved)        
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
        
        if faixa1btn.collidepoint((mx, my)) or btn_recieved == 1:
            if click or btn_recieved == 1:
                client.publish(btns_topics[0], 1)
                time.sleep(0.1)
                client.publish(btns_topics[0], 0)
                time.sleep(0.1)
                id = 1
                Faixa(30)
        if faixa2btn.collidepoint((mx, my)) or btn_recieved == 2:
            if click or btn_recieved == 2:
                client.publish(btns_topics[1], 1)
                time.sleep(0.1)
                client.publish(btns_topics[1], 0)
                time.sleep(0.1)
                id = 2
                Faixa(30)
        if faixa3btn.collidepoint((mx, my)) or btn_recieved == 3:
            if click or btn_recieved == 3:
                client.publish(btns_topics[2], 1)
                time.sleep(0.1)
                client.publish(btns_topics[2], 0)
                time.sleep(0.1)
                id = 3
                Faixa(30)
        if faixa4btn.collidepoint((mx, my)) or btn_recieved == 4:
            if click or btn_recieved == 4:
                client.publish(btns_topics[3], 1)
                time.sleep(0.1)
                client.publish(btns_topics[3], 0)
                time.sleep(0.1)
                id = 4
                Faixa(30)

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
                


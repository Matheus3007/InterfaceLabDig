import pygame
from pygame.locals import *


mainClock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption("Piano Genius")

screenWidth = 550
screenHeight = 700

screen = pygame.display.set_mode((screenWidth,screenHeight))

logo = pygame.image.load("Pynterface\logoNoBorderTransparent.png")
strt = pygame.image.load("Pynterface\start.png")
stat  = pygame.image.load("Pynterface\_stats.png")
rst = pygame.image.load("Pynterface\srest.png")
faixa1 = pygame.image.load("Pynterface\_faixa1.png")
faixa2 = pygame.image.load("Pynterface\_faixa2.png")
faixa3 = pygame.image.load("Pynterface\_faixa3.png")
faixa4 = pygame.image.load("Pynterface\_faixa4.png")
faixa1play = pygame.image.load("Pynterface\_faixa1play.png")
faixa2play = pygame.image.load("Pynterface\_faixa2play.png")
faixa3play = pygame.image.load("Pynterface\_faixa3play.png")
faixa4play = pygame.image.load("Pynterface\_faixa4play.png")

slctTxt = pygame.image.load("Pynterface\_trackSelect.png")
running = True 

game_font = pygame.font.Font("Pynterface\Minecraft.ttf", 55)

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



def Faixa(n, id):
    maxnotes = n
    running = True
    click = False
    acertos = 0
    misses = 0
    delay = 240/id
    pontuacao = 0
    global totalHits
    global totalMisses
    global highScore
    while running:
        if(pontuacao>highScore):
            highScore = pontuacao
        print(delay)

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
                        pontuacao += 100 * delay // 240
                    else:
                        pontuacao += 1
                    delay = 240/id
                    acertos+=1
                    totalHits+=1
                    
                if event.key == K_ESCAPE:
                    running = False

        if (click and acertos + misses >= maxnotes):
            pygame.time.delay(300)
            running = False
        delay -=1
        pygame.display.update()
        mainClock.tick(60)

# Game Screen
def GameSelect():
    running = True
    click = False
    while running:
          
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
        
        if faixa1btn.collidepoint((mx, my)):
            if click:
                Faixa(17, 1)
        if faixa2btn.collidepoint((mx, my)):
            if click:
                Faixa(30,2)
        if faixa3btn.collidepoint((mx, my)):
            if click:
                Faixa(30, 3)
        if faixa4btn.collidepoint((mx, my)):
            if click:
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
                


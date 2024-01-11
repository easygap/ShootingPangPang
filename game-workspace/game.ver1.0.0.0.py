import pygame
import sys
from time import sleep


# 1.0 우주선, 미사일, 배경

#게임 기본 화면
BLACK = (0, 0, 0)
padWidth = 480
padHeight = 640


#게임정의
def initGame() :
    global gamePad, clock, background, fighter, missile
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('비행기 슈팅 팡팡')              # 게임 이름
    background = pygame.image.load('object/background.png')    # 배경 그림
    fighter = pygame.image.load('object/fighter.png')          # 전투기 그림
    missile = pygame.image.load('object/missile.png')          # 미사일 그림
    clock = pygame.time.Clock()
    
#게임에 등장하는 객체를 드로잉
def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y))
    
#게임 런 정의
def runGame():
    global gamepad, clock, background, fighter, missile
    
    #전투기 크기
    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]
    
    #전투기 시작 위치 (x,y)
    x = padWidth * 0.45
    y = padHeight * 0.9
    fighterX = 0
    
    #미사일 좌표 리스트
    missileXY = []
        
    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]: #게임 종료
                pygame.quit()
                sys.exit()
            
            #전투기 이동
            if event.type in [pygame.KEYDOWN]:
                if event.key == pygame.K_LEFT:  #비행기 왼쪽 이동
                    fighterX -= 5
                    
                elif event.key == pygame.K_RIGHT: #비행기 오른쪽 이동
                    fighterX +=5
                    
                elif event.key == pygame.K_SPACE:
                    missileX = x + fighterWidth/2
                    missileY = y - fighterHeight
                    missileXY.append([missileX, missileY])
                    
            if event.type in [pygame.KEYUP]:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:  #비행기 멈춤
                    fighterX = 0
            
                
        drawObject(background, 0, 0) #배경화면 다시 그리기
        
        # 전투기 위치 재조정
        x += fighterX
        if x < 0:
            x = 0
        elif x > padWidth - fighterWidth:
            x = padWidth - fighterWidth
        
        drawObject(fighter, x, y) # 비행기를 게임 화면의 (x,y)좌표에 그림
        
        # 미사일 발사 화면에 그리기
        if len(missileXY) != 0:
            for i, bxy in enumerate(missileXY):  # 미사일 요소의 반복
                bxy[1] -= 10                     # 미사일의 y좌표 -10(위로이동)
                missileXY[i][1] = bxy[1]
                
                if bxy[1] <= 0: #미사일이 화면밖으로 벗어나면
                    try:
                        missileXY.remove(bxy)  # 미사일 제거
                    except:
                        pass
        if len(missileXY) != 0:
            for bx, by in missileXY:
                drawObject(missile, bx, by)
            
        pygame.display.update() #게임화면을 다시그림
            
        clock.tick(60)
    pygame.quit()
        
initGame()
runGame()

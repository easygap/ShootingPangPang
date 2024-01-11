# coding: utf-8

#게임 창
import pygame
import sys
from time import sleep
BLACK = (0, 0, 0)
padWidth = 480         # 게임화면 가로크기
padHeight = 640        # 게임화면 세로크기

# 게임에 등장하는 객체를 드로잉
def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y))
    
def initGame():
    global gamePad, clock, background, fighter, missile
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('pyshooting')                                                           #게임 이름
    background = pygame.image.load("./object/background.png")  # 배경 그림
    fighter = pygame.image.load("./object/fighter.png")        # 플레이어 그림
    missile = pygame.image.load("./object/missile.png")        # 미사일 그림
    clock = pygame.time.Clock()

    
def runGame():
    global gamePad, clock, background, fighter, missile
    
    # 플레이어 크기
    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]
    
    # 무기 크기
    missileSize = missile.get_rect().size
    missileWidth = missileSize[0]
    missileHeight = missileSize[1]
    
    # 무기 좌표 리스트
    missileXY = []
    
    # 플레이어 초기 위치 (x,y)
    x = padWidth * 0.45
    y = padHeight * 0.9
    fighterX = 0
    fighterY = 0
    fighterSpeed = 5  # 초기 전투기 속도
    
    # 전투기 미사일에 운석이 맞았을 경우 True
    isShot = False
    shotCount = 0
    rockPassed = 0
    missileSpeed = 5
    missile_num = 1
    
    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:          # 게임 프로그램 종료
                pygame.quit()
                sys.exit()
            
            if event.type in [pygame.KEYDOWN]:
                if event.key == pygame.K_LEFT:     # 전투기 왼쪽으로 이동
                    fighterX -= fighterSpeed

                elif event.key == pygame.K_RIGHT:  # 전투기 오른쪽으로 이동
                    fighterX += fighterSpeed

                elif event.key == pygame.K_UP:     # 전투기 위로 이동
                    fighterY -= fighterSpeed

                elif event.key == pygame.K_DOWN:  # 전투기 아래로 이동
                    fighterY += fighterSpeed
                
                elif event.key == pygame.K_SPACE:  # 미사일 발사
                    #   missileSound.play()        # 미사일 사운드 재생
                    if missile_num == 1:           # 미사일 1개
                        missileX = x + fighterWidth/2 - missileWidth/2
                        missileY = y
                        missileXY.append([missileX, missileY])
                    elif missile_num == 2:         # 미사일 2개
                        missileX = x
                        missileY = y
                        missileXY.append([missileX, missileY])
                        missileX = x + fighterWidth - missileWidth
                        missileXY.append([missileX, missileY])
                    elif missile_num == 3:         # 미사일 3개
                        missileX = x
                        missileY = y
                        missileXY.append([missileX, missileY])
                        missileX = x + fighterWidth - missileWidth
                        missileXY.append([missileX, missileY])
                        missileX = x + fighterWidth/2 - missileWidth/2
                        missileXY.append([missileX, missileY])
            
            if event.type in [pygame.KEYUP]:  # 방향키를 떼면 전투기 멈춤
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighterX = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    fighterY = 0

        
        x += fighterX
        if x < 0:
            x = 0
        elif x > padWidth - fighterWidth:
            x = padWidth - fighterWidth
            
        y += fighterY
        if y < 0:
            y = 0
        elif y > padHeight - fighterHeight:
            y = padHeight - fighterHeight
            
        #print("x", x, " y ", y)  
        
        drawObject(background, 0, 0)                 # 배경 화면 그리기
                           
        drawObject(fighter, x, y)
         
        # 미사일 발사 화면에 그리기
        if len(missileXY) != 0:
            for i, bxy in enumerate(missileXY):  # 미사일 요소에 대해 반복함
                bxy[1] -= missileSpeed           # 총알의 y좌표 (미사일 위로 이동)
                missileXY[i][1] = bxy[1]

                if bxy[1] <= 0:                   # 미사일이 화면 밖을 벗어나면
                    try:
                        missileXY.remove(bxy)
                    except:
                        pass
  
        if len(missileXY) != 0:
            for bx, by in missileXY:
                drawObject(missile, bx, by)
             
        pygame.display.update()                   # 게임화면을 다시그림
        
        clock.tick(60)                            # 프레임
        
    pygame.quit()
    
initGame()
runGame()
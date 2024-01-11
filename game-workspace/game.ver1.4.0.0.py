import pygame
import sys
import random
import os
from time import sleep
from PIL import Image

# 1.0 우주선, 미사일, 배경
# 1.1 운석 생성 및 랜덤 낙하
# 1.2 운석 맞출시 폭발
# 1.3 운석 맞추면 카운트, 3개이상 놓칠 경우 게임오버
# 1.4 사운드 추가

#게임 기본 화면
BLACK = (0, 0, 0)
padWidth = 480
padHeight = 640

# 운석 이미지 불러오기
rockImage = []
image_extesions = ['.png']
folder_path = "rock"
for filename in os.listdir(folder_path):
    file_extension = os.path.splitext(filename)[1].lower()  # 확장자를 추출하고 그 확장자를 소문자로 변환
    if file_extension in image_extesions:
        if filename.startswith("rock"):  # rock로 시작하는 파일 선별
            rockImage.append(os.path.join(folder_path, filename))  # 리스트에 넣음
            
#게임정의
def initGame() :
    global gamePad, clock, background, fighter, missile, explosion, missileSound, gmaeOverSound
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('비행기 슈팅 팡팡')              # 게임 이름
    background = pygame.image.load('object/background.png')    # 배경 그림
    fighter = pygame.image.load('object/fighter.png')          # 전투기 그림
    missile = pygame.image.load('object/missile.png')          # 미사일 그림
    explosion = pygame.image.load('object/explosion.png')      # 폭발 그림
    pygame.mixer.music.load('배경 음악')                        # 배경 음악
    pygame.mixer.music.play(-1)                                # 배경 음악 재생
    missileSound = pygame.mixer.Sound('미사일 사운드')          # 미사일 사운드
    gameOverSound = pygame.mixer.sound('게임오버 사운드')       # 게임 오버 사운드
    clock = pygame.time.Clock()
    
#게임에 등장하는 객체를 드로잉
def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y))
    
    
# 게임 메세지 출력
def writeMessage(text):
    global gamePad
    textfont = pygame.font.Font('NanumGothic.ttf', 80)
    text = textfont.render(text, True, (255, 0, 0))
    textpos = text.get_rect()
    textpos.center = (padWidth/2, padHeight/2)
    gamePad.blit(text, textpos)
    pygame.display.update()
    sleep(2)
    runGame()
    
# 전투기가 운석과 충돌했을 때 메셎 출력
def crash():
    global gamePad
    writeMessage('전투기 파괴!')
    
# 게임 오버 메세지 보이기
def gameOver():
    global gamePad
    writeMessage('게임 오버!')
    
#게임 런 정의
def runGame():
    global gamepad, clock, background, fighter, missile, explosion, missileSound
    
    #전투기 크기
    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]
    
    #전투기 시작 위치 (x,y)
    x = padWidth * 0.45
    y = padHeight * 0.9
    fighterX = 0
    fighterY = 0
    fighterSpeed = 5
    
    #미사일 좌표 리스트
    missileXY = []
    
    #운석 랜덤 생성
    rock = pygame.image.load(random.choice(rockImage))
    rockSize = rock.get_rect().size
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]
    
    #운석 초기위치 설정
    rockX = random.randrange(0, padWidth - rockWidth)
    rockY = 0
    rockSpeed = 2
    
    # 전투기 미사일에 맞았을 경우 True
    isShot = False
    shotCount = 0
    rockPassed = 0
    
    # 운석 카운트
    def writeScore(count):
        global gamePad
        font = pygame.font.Font('NanumGothic.ttf', 20)
        text = font.render('파괴한 운석 수:' + str(count), True, (255, 255, 255))
        gamePad.blit(text, (10,0))
            
    #운석이 화면 아래로 통과한 개수
    def writePassed(count):
        global gamePad
        font = pygame.font.Font('NanumGothic.ttf', 20)
        text = font.render('놓친 운석 : ' + str(count), True, (250,0,0))
        gamePad.blit(text, (360,0))    
        
    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]: #게임 종료
                pygame.quit()
                sys.exit()
            
            #전투기 이동
            if event.type in [pygame.KEYDOWN]:
                if event.key == pygame.K_LEFT:  #비행기 왼쪽 이동
                    fighterX -= fighterSpeed
                    
                elif event.key == pygame.K_RIGHT: #비행기 오른쪽 이동
                    fighterX += fighterSpeed
                    
                elif event.key == pygame.K_DOWN:  #비행기 위로 이동
                    fighterY += fighterSpeed
                
                elif event.key == pygame.K_UP:  #비행기 아래로 이동
                    fighterY -= fighterSpeed
                    
                elif event.key == pygame.K_SPACE:
                    missileSound.play()
                    missileX = x + fighterWidth/2
                    missileY = y - fighterHeight
                    missileXY.append([missileX, missileY]);
                    
            if event.type in [pygame.KEYUP]:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:  #비행기 멈춤
                    fighterX = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    fighterY = 0
            
                
        drawObject(background, 0, 0) #배경화면 다시 그리기
        
        # 전투기 위치 재조정
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
            
        #전투기가 충돌했는지 체크
        if y < rockY + rockHeight:
            if(rockX > x and rockX < x + fighterHeight) or \
                (rockX + rockWidth > x and rockX + rockWidth < x + fighterWidth):
                crash()
        
        drawObject(fighter, x, y) # 비행기를 게임 화면의 (x,y)좌표에 그림
        
        if rockPassed == 3:  # 운석 세개 놓치면 게임 오버
            gameOver()
        
        # 미사일 발사 화면에 그리기
        if len(missileXY) != 0:
            for i, bxy in enumerate(missileXY):  # 미사일 요소의 반복
                bxy[1] -= 10                     # 미사일의 y좌표 -10(위로이동)
                missileXY[i][1] = bxy[1]
                
                #미사일이 운성을 맞추었을 경우
                if bxy[1] < rockY:
                    if bxy[0] > rockX and bxy[0] < rockX + rockWidth:
                        missileXY.remove(bxy)
                        isShot = True
                        shotCount +=1
                
                if bxy[1] <= 0: #미사일이 화면밖으로 벗어나면
                    try:
                        missileXY.remove(bxy)  # 미사일 제거
                    except:
                        pass
        if len(missileXY) != 0:
            for bx, by in missileXY:
                drawObject(missile, bx, by)
                
        # 운석 맞춘 점수 표시
        writeScore(shotCount)
                
        rockY += rockSpeed # 운석이 아래로 움직임
        
        #운석이 지구로 떨어진 경우
        if rockY > padHeight:
            #새로운 운석 (랜덤)
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            rockPassed += 1

        # 놓친 운석 수 표시
        writePassed(rockPassed)
            
        # 운석을 맞춘 경우
        if isShot:
            #운석 폭발
            drawObject(explosion, rockX, rockY)
            
            #새로운 운석 (랜덤)
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
            rockX = random.randrange(0, padWidth - rockHeight)
            rockY = 0
            isShot = False
            
            #운석 맞추면 속도 증가
            rockSpeed += 0.02
            if rockSpeed >= 10:
                rockSpeed = 10
            
        
            
        drawObject(rock, rockX, rockY)  #운석 그리기
            
        pygame.display.update() #게임화면을 다시그림
            
        clock.tick(60)
    pygame.quit()
        
initGame()
runGame()

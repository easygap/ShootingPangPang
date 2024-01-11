import pygame
import sys
import random
import os
from time import sleep

# 1.0 우주선, 미사일, 배경
# 1.1 운석 생성 및 랜덤 낙하
# 1.2 운석 맞출시 폭발
# 1.3 운석 맞추면 카운트, 3개이상 놓칠 경우 게임오버
# 1.4 사운드 (미구현)
# 1.5 v키 입력시 5발씩 발사
# 1.6 운석이 여러개 떨어짐
# 1.6.1 v키 쿨타임
# 1.6.2 운석 카운트 픽스
# 1.6.2.1 남은생명으로 변경
# 1.6.2.2 운석 위로 지나가도 충돌 X
# 1.6.2.3 쿨타임 텍스트 표기
# 1.6.2.4 사운드 추가
# 1.6.2.5 Game Over 이후 재시작 안되는 오류 수정
# 1.6.2.6 스킬(v) 사용 후 재사용까지 남은 시간 표시
# 1.6.2.7 스킬(v) 비행기 중앙에서 발사




# 게임 기본 화면
BLACK = (0, 0, 0)
padWidth = 480
padHeight = 640

#쿨다운 표가 위해 초기화
pygame.font.init()

# 배경 이미지 초기 위치
bg_y1 = 0
bg_y2 = -padHeight

# 배경 이미지 스크롤 속도
background_scroll_speed = 5

# 운석 이미지 불러오기
rockImage = []
image_extesions = ['.png']
folder_path = "rock"
for filename in os.listdir(folder_path):
    file_extension = os.path.splitext(filename)[1].lower()  # 확장자를 추출하고 그 확장자를 소문자로 변환
    if file_extension in image_extesions:
        if filename.startswith("rock"):  # rock로 시작하는 파일 선별
            rockImage.append(os.path.join(folder_path, filename))  # 리스트에 넣음

# 게임 초기화
def initGame():
    global gamePad, clock, background, fighter, missile, explosion, cooldown_font, missilesound, crashsound, rocksound, life_image
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('비행기 슈팅 팡팡')  # 게임 이름
    background = pygame.image.load('object/background.png')  # 배경 그림
    fighter = pygame.image.load('object/fighter.png')  # 전투기 그림
    missile = pygame.image.load('object/missile.png')  # 미사일 그림
    explosion = pygame.image.load('object/explosion.png') #폭발 그림
    life_image = pygame.image.load('object/life.png')
    cooldown_font = pygame.font.Font('NanumGothic.ttf', 20) # 쿨다운폰트
    missilesound = pygame.mixer.Sound('sound/shot.wav')
    crashsound = pygame.mixer.Sound('sound/big.wav')
    rocksound = pygame.mixer.Sound('sound/small.wav')
    clock = pygame.time.Clock()

# 게임에 등장하는 객체를 드로잉
def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y))
    
    
# 생명 이미지 그리기
def drawLife(count):
    global gamePad, life_image
    for i in range(count):
        life_x = 450 - (i * 30)  # 각 생명 이미지의 x 좌표를 조정하여 겹치지 않게 배치합니다.
        life_y = 10  # 생명 이미지의 y 좌표
        gamePad.blit(life_image, (life_x, life_y))

# 게임 메세지 출력
def writeMessage(text):
    global gamePad
    textfont = pygame.font.Font('NanumGothic.ttf', 80)
    text = textfont.render(text, True, (255, 0, 0))
    textpos = text.get_rect()
    textpos.center = (padWidth / 2, padHeight / 2)
    gamePad.blit(text, textpos)
    pygame.display.update()
    sleep(2)
    runGame()

# 전투기가 운석과 충돌했을 때 메세지 출력
def crash():
    global gamePad
    writeMessage('전투기 파괴!')

# 게임 오버 메세지 보이기
def gameOver():
    global gamePad
    writeMessage('게임 오버!')
    
# 비행기와 운석 간의 충돌 감지 함수
def isCollision(x1, y1, x2, y2, width1, height1, width2, height2):
    if x1 + width1 > x2 and x1 < x2 + width2 and y1 + height1 > y2 and y1 < y2 + height2:
        return True
    return False

#쿨타임 상태 표시용 변수와 폰트 설정
cooldown_font = pygame.font.Font('NanumGothic.ttf', 20)
cooldown_text = None
cooldown_time = 0
cooldown_duration = 2 # 쿨타임 기간(초)

#쿨타임 표시 시각화
def updateCooldownText():
    global cooldown_text, cooldown_time
    if cooldown_time > 0:
        text = "쿨타임 : {:.1f}".format(cooldown_time)
        cooldown_text = cooldown_font.render(text, True, (255, 255, 255))
    else:
        cooldown_text = cooldown_font.render("사용 가능", True, (255, 255, 255))

# 운석 클래스 정의
class Rock:
    def __init__(self):
        self.image = pygame.image.load(random.choice(rockImage))
        self.size = self.image.get_rect().size
        self.width = self.size[0]
        self.height = self.size[1]
        self.x = random.randrange(0, padWidth - self.width)
        self.y = 0
        self.speed = random.uniform(1, 3)  # 운석의 떨어지는 속도 (랜덤)
        
    def move(self):
        self.y += self.speed
        # 운석이 화면 아래로 벗어나면 다시 위로 올려놓기
        if self.y > padHeight:
            self.x = random.randrange(0, padWidth - self.width)
            self.y = 0
            
# 게임 루프 정의
def runGame():
    global gamepad, clock, background, fighter, missile, explosion, missile_interval, missile_group, bg_y1, bg_y2, cooldown_time, last_frame_time

    # 전투기 크기
    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]

    # 전투기 시작 위치 (x, y)
    x = padWidth * 0.45
    y = padHeight * 0.9
    fighterX = 0
    fighterY = 0
    fighterSpeed = 5

    # 미사일 좌표 리스트
    missileXY = []

    # 운석 객체들을 저장할 리스트
    rocks = [Rock() for _ in range(10)]  # 5개의 운석 생성

    # 전투기 미사일에 맞았을 경우 True
    isShot = False
    shotCount = 0
    life = 10

    # 미사일 발사 간격 설정 (초 단위)
    missile_interval = 0

    # 미사일 속도 및 방향 설정
    missile_speed = 10

    # 미사일 그룹 설정
    missile_group = []

    # 운석 카운트
    def writeScore(count):
        global gamePad
        font = pygame.font.Font('NanumGothic.ttf', 20)
        text = font.render('파괴한 운석 수:' + str(count), True, (255, 255, 255))
        gamePad.blit(text, (10, 0))

    # 운석이 화면 아래로 통과한 개수
    # def writePassed(count):
    #   global gamePad
    #    font = pygame.font.Font('NanumGothic.ttf', 20)
    #    text = font.render('남은 생명 : ' + str(count), True, (250, 0, 0))
    #    gamePad.blit(text, (360, 0))

    onGame = False
    while not onGame:
        current_time = pygame.time.get_ticks() / 1000  # 현재 시간 가져오기
        # 생명 이미지 그리기
        drawLife(life)
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:  # 게임 종료
                pygame.quit()
                sys.exit()  

            # 전투기 이동
            if event.type in [pygame.KEYDOWN]:
                if event.key == pygame.K_LEFT:  # 비행기 왼쪽 이동
                    fighterX -= fighterSpeed

                elif event.key == pygame.K_RIGHT:  # 비행기 오른쪽 이동
                    fighterX += fighterSpeed

                elif event.key == pygame.K_DOWN:  # 비행기 위로 이동
                    fighterY += fighterSpeed

                elif event.key == pygame.K_UP:  # 비행기 아래로 이동
                    fighterY -= fighterSpeed

                elif event.key == pygame.K_SPACE: # 미사일 발사
                        missilesound.play()
                        missileX = x + fighterWidth / 2
                        missileY = y - fighterHeight
                        missile_group.append([missileX, missileY])
                        
                elif event.key == pygame.K_v: # v키
                    missilesound.play()
                    current_time = pygame.time.get_ticks() / 1000  

                    if cooldown_time <= 0:
                        # 비행기의 중앙에서 미사일을 발사하도록 계산
                        missileX = x + fighterWidth / 2 - (10 * 20 / 2)  # 20발 미사일이므로 중앙에서 좌우로 (10 * 20 / 2) 픽셀씩 이동
                        missileY = y - fighterHeight
                        for i in range(20):
                            missile_group.append([missileX, missileY])
                            missileX += 10  # 미사일 간의 간격을 10으로 설정
                        cooldown_time = cooldown_duration

            if event.type in [pygame.KEYUP]:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:  # 비행기 멈춤
                    fighterX = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    fighterY = 0

        updateCooldownText()    # 게임 구동 중 쿨타임 텍스트 업데이트
        
        if cooldown_text:       # 쿨타임 텍스트 그리기
            gamePad.blit(cooldown_text, (10, padHeight - 40))
        
        pygame.display.update()  # 게임 화면 리로드

        # 배경 이미지 위치 업데이트
        bg_y1 += background_scroll_speed
        bg_y2 += background_scroll_speed

        # 하나의 배경 이미지가 화면 아래로 벗어나면 다시 위로 올려놓기
        if bg_y1 >= padHeight:
            bg_y1 = -padHeight

        if bg_y2 >= padHeight:
            bg_y2 = -padHeight

        gamePad.blit(background, (0, bg_y1))
        gamePad.blit(background, (0, bg_y2))

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

        drawObject(fighter, x, y)  # 비행기를 게임 화면의 (x,y)좌표에 그림

        if life == 0:  # 라이프가 0되면 게임오버
            gameOver()

        # 미사일 발사 간격 설정
        if missile_interval > 0:
            missile_interval -= 1

        if len(missile_group) != 0:
            for missileXY in missile_group:
                missileXY[1] -= missile_speed  # 미사일의 y좌표 - 미사일 속도

                # 미사일이 화면 위로 벗어나면 제거
                if missileXY[1] <= 0:
                    missile_group.remove(missileXY)

        # 미사일 그리기
        if len(missile_group) != 0:
            for missileXY in missile_group:
                drawObject(missile, missileXY[0], missileXY[1])

                # 미사일이 화면 위로 벗어나면 제거
                if missileXY[1] <= 0:
                    missile_group.remove(missileXY)
                
        # 운석 맞춘 점수 표시
        writeScore(shotCount)

        for rock in rocks:
            rock.move()  # 운석을 아래로 움직임

            # 운석이 화면 아래로 벗어났을 때 다시 위로 배치
            if rock.y + rock.height > padHeight:
                rock.x = random.randrange(0, padWidth - rock.width)
                rock.y = 0
                rock.speed = random.uniform(1, 3)
                life -= 1  # 운석이 화면 아래로 벗어났으므로 카운트 증가

            drawObject(rock.image, rock.x, rock.y)  # 운석 그리기

            # 운석과 미사일 충돌 체크
            for missile_pos in missile_group:
                missileX, missileY = missile_pos
                if isCollision(rock.x, rock.y, missileX, missileY, rock.width, rock.height, missile.get_width(), missile.get_height()):
                    missile_group.remove(missile_pos)  # 충돌한 미사일 제거
                    isShot = True
                    shotCount += 1

            # 운석 폭발 처리
            if isShot:
                rocksound.play()
                # 운석 폭발 이미지 그리기
                drawObject(explosion, rock.x, rock.y)
                pygame.display.update()

                # 새로운 운석 생성
                rock.x = random.randrange(0, padWidth - rock.width)
                rock.y = 0
                isShot = False

                # 운석 맞추면 속도 증가
                rock.speed += 0.02
                if rock.speed >= 10:
                    rock.speed = 10

        # 운석과 비행기 충돌 체크
            if isCollision(x, y, rock.x, rock.y, fighterWidth, fighterHeight, rock.width, rock.height):
                crashsound.play()
                crash()

        # 남은 생명 표시
        # writePassed(life)
        # 쿨타임 갱신
        if cooldown_time > 0:
            cooldown_time -= (current_time - last_frame_time)  # 경과 시간을 빼서 쿨타임 감소
            if cooldown_time < 0:
                cooldown_time = 0  # 쿨타임이 음수가 되지 않도록 보정

        last_frame_time = current_time  # 현재 시간을 저장

        # 쿨타임 상태 표시 업데이트
        updateCooldownText()
        
        drawLife(life)

        # 쿨타임 텍스트 그리기
        if cooldown_text:
            gamePad.blit(cooldown_text, (10, padHeight - 40))

        pygame.display.update()  # 게임 화면을 다시 그림

        clock.tick(60)
    pygame.quit()

initGame()
runGame()

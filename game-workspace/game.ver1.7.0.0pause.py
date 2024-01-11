import pygame
import sys
import random
import os
from time import sleep

# 게임 기본 화면
BLACK = (0, 0, 0)
padWidth = 480
padHeight = 640

# 쿨다운 표시를 위해 초기화
pygame.font.init()

# 게임 일시 정지 상태
paused = False

# 배경 이미지 초기 위치
bg_y1 = 0
bg_y2 = -padHeight

# 배경 이미지 스크롤 속도
background_scroll_speed = 5

# 운석 이미지 불러오기
rockImage = []
image_extensions = ['.png']
folder_path = "rock"
for filename in os.listdir(folder_path):
    file_extension = os.path.splitext(filename)[1].lower()  # 확장자를 추출하고 그 확장자를 소문자로 변환
    if file_extension in image_extensions:
        if filename.startswith("rock"):  # rock로 시작하는 파일 선별
            rockImage.append(os.path.join(folder_path, filename))  # 리스트에 넣음

# 게임 초기화
def initGame():
    global gamePad, clock, background, fighter, missile, explosion, cooldown_font, paused
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption('비행기 슈팅 팡팡')  # 게임 이름
    background = pygame.image.load('object/background.png')  # 배경 그림
    fighter = pygame.image.load('object/fighter.png')  # 전투기 그림
    missile = pygame.image.load('object/missile.png')  # 미사일 그림
    explosion = pygame.image.load('object/explosion.png') # 폭발 그림
    cooldown_font = pygame.font.Font('NanumGothic.ttf', 20) # 쿨다운 폰트
    paused = False
    clock = pygame.time.Clock()

# 게임에 등장하는 객체를 드로잉
def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y))

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

# 쿨타임 상태 표시용 변수와 폰트 설정
cooldown_font = pygame.font.Font('NanumGothic.ttf', 20)
cooldown_text = None
cooldown_time = 0
cooldown_duration = 2  # 쿨타임 기간(초)

# 운석 맞춘 점수 표시
def writeScore(count):
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf', 20)
    text = font.render('파괴한 운석 수: ' + str(count), True, (255, 255, 255))
    gamePad.blit(text, (10, 0))

# 운석이 화면 아래로 통과한 개수
def writePassed(count):
    global gamePad
    font = pygame.font.Font('NanumGothic.ttf', 20)
    text = font.render('남은 생명: ' + str(count), True, (250, 0, 0))
    gamePad.blit(text, (360, 0))

# 쿨타임 상태 표시 업데이트
def updateCooldownText():
    global cooldown_text, cooldown_time
    if cooldown_time > 0:
        text = "쿨타임: {:.1f}".format(cooldown_time)
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
            
remaining_lives = 5

# 게임 루프 정의
def runGame():
    global gamepad, clock, background, fighter, missile, explosion, missile_interval, missile_direction, missile_group, bg_y1, bg_y2, cooldown_time, paused, remaining_lives

    last_frame_time = pygame.time.get_ticks() / 1000  # 게임 루프 진입 시간 초기화

    # 남은 생명 표시용 폰트 설정
    remaining_lives_font = pygame.font.Font('NanumGothic.ttf', 20)

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
    rocks = [Rock() for _ in range(5)]  # 5개의 운석 생성

    # 전투기 미사일에 맞았을 경우 True
    isShot = False
    shotCount = 0
    rockPassed = 5

    # 미사일 발사 간격 설정 (초 단위)
    missile_interval = 0

    # 미사일 속도 및 방향 설정
    missile_speed = 10
    missile_direction = 0  # 0은 정면, -1은 왼쪽으로, 1은 오른쪽으로

    # 미사일 그룹 설정
    missile_group = []

    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused  # 일시 중지 상태 토글

        if not paused:
            current_time = pygame.time.get_ticks() / 1000
            if 'last_frame_time' not in locals():
                last_frame_time = current_time

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = False  # 일시 중지 상태 해제

                # 전투기 이동
                if event.type in [pygame.KEYDOWN]:
                    if event.key == pygame.K_LEFT:
                        fighterX -= fighterSpeed
                    elif event.key == pygame.K_RIGHT:
                        fighterX += fighterSpeed
                    elif event.key == pygame.K_DOWN:
                        fighterY += fighterSpeed
                    elif event.key == pygame.K_UP:
                        fighterY -= fighterSpeed
                    elif event.key == pygame.K_SPACE:
                        missileX = x + fighterWidth / 2
                        missileY = y - fighterHeight
                        missile_group.append([missileX, missileY])
                    elif event.key == pygame.K_v:
                        current_time = pygame.time.get_ticks() / 1000
                        if cooldown_time <= 0:
                            for i in range(20):
                                missileX = x + fighterWidth / 2 + (i - 2) * 10
                                missileY = y - fighterHeight
                                missile_group.append([missileX, missileY])
                            cooldown_time = cooldown_duration

                if event.type in [pygame.KEYUP]:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        fighterX = 0
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        fighterY = 0
                        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = not paused

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

            drawObject(fighter, x, y)

            if rockPassed == 0:
                gameOver()

            if missile_interval > 0:
                missile_interval -= 1

            if len(missile_group) != 0:
                for missileXY in missile_group:
                    missileXY[1] -= missile_speed

                    if missileXY[1] <= 0:
                        missile_group.remove(missileXY)

            if len(missile_group) != 0:
                for missileXY in missile_group:
                    drawObject(missile, missileXY[0], missileXY[1])

                    if missileXY[1] <= 0:
                        missile_group.remove(missileXY)

            writeScore(shotCount)

            for rock in rocks:
                rock.move()

                if rock.y + rock.height > padHeight:
                    rock.x = random.randrange(0, padWidth - rock.width)
                    rock.y = 0
                    rock.speed = random.uniform(1, 3)
                    rockPassed -= 1

                drawObject(rock.image, rock.x, rock.y)

                for missile_pos in missile_group:
                    missileX, missileY = missile_pos
                    if isCollision(rock.x, rock.y, missileX, missileY, rock.width, rock.height, missile.get_width(), missile.get_height()):
                        missile_group.remove(missile_pos)
                        isShot = True
                        shotCount += 1

                if isShot:
                    drawObject(explosion, rock.x, rock.y)
                    pygame.display.update()
                    rock.x = random.randrange(0, padWidth - rock.width)
                    rock.y = 0
                    isShot = False
                    rock.speed += 0.01
                    if rock.speed >= 10:
                        rock.speed = 10

                if isCollision(x, y, rock.x, rock.y, fighterWidth, fighterHeight, rock.width, rock.height):
                    remaining_lives -= 1
                    if remaining_lives <= 0:
                        crash()
                    else:
                        rock.x = random.randrange(0, padWidth - rock.width)
                        rock.y = 0

            writePassed(rockPassed)

            if cooldown_time > 0:
                cooldown_time -= (current_time - last_frame_time)
                if cooldown_time < 0:
                    cooldown_time = 0

            last_frame_time = current_time
            updateCooldownText()

            if cooldown_text:
                gamePad.blit(cooldown_text, (10, padHeight - 40))

            # 남은 생명 표시
            remaining_lives_text = remaining_lives_font.render('남은 생명: ' + str(remaining_lives), True, (250, 0, 0))
            gamePad.blit(remaining_lives_text, (360, 0))

            pygame.display.update()
            clock.tick(60)
    pygame.quit()

initGame()
runGame()

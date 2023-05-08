import pygame
import random

# 게임 화면 크기 설정
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# 공 크기 설정
BALL_SIZE = 25

# 색깔 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# 초기화
pygame.init()

# 게임 화면 생성
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("공 튀기기 게임")

# 공 생성
ball_x = random.randint(BALL_SIZE, SCREEN_WIDTH - BALL_SIZE)
ball_y = random.randint(BALL_SIZE, SCREEN_HEIGHT - BALL_SIZE)
ball_speed_x = random.randint(1, 3)
ball_speed_y = random.randint(1, 3)

# 패들 생성
paddle_width = 80
paddle_height = 10
paddle_x = (SCREEN_WIDTH - paddle_width) // 2
paddle_y = SCREEN_HEIGHT - 50

# 게임 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 화면 색깔 채우기
    screen.fill(WHITE)

    # 공 그리기
    pygame.draw.circle(screen, BLUE, (ball_x, ball_y), BALL_SIZE)

    # 패들 그리기
    pygame.draw.rect(screen, RED, (paddle_x, paddle_y, paddle_width, paddle_height))

    # 공 움직이기
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # 공이 벽에 부딪히면 방향 전환
    if ball_x < BALL_SIZE or ball_x > SCREEN_WIDTH - BALL_SIZE:
        ball_speed_x = -ball_speed_x
    if ball_y < BALL_SIZE:
        ball_speed_y = -ball_speed_y

    # 패들과 공이 충돌하면 방향 전환
    if ball_y > paddle_y - BALL_SIZE and ball_x > paddle_x and ball_x < paddle_x + paddle_width:
        ball_speed_y = -ball_speed_y

    # 패들 움직이기
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle_x -= 5
    if keys[pygame.K_RIGHT]:
        paddle_x += 5

    # 패들이 화면 밖으로 나가지 않도록 제한
    if paddle_x < 0:
        paddle_x = 0
    if paddle_x > SCREEN_WIDTH - paddle_width:
        paddle_x = SCREEN_WIDTH - paddle_width

    # 화면 업데이트
    pygame.display.update()

# 게임 종료
pygame.quit()

import pygame
import sys
from pygame.locals import *

#Задаём глобальные переменные ширину и длинну экрана, толщину линий, размеры ракетки и расстояние от края экрана
WINDOWWIDTH = 800
WINDOWHEIGHT = 600
LINETHICKNESS = 12
ROCKETSIZE = 80
ROCKETOFFSET = 20

# Изменяя этот параметр можно ускорять или замедлять игру
global FPS
FPS = 200

# Определяем цвета площадки
BLACK     = (0  ,0  ,0  )
WHITE     = (255,255,255)

#Функция расиует арену, на которой будем играть 
def drawArena():
    DISPLAYSURF.fill((0,0,0))
    #Рисуем разметку
    pygame.draw.rect(DISPLAYSURF, WHITE, ((0,0),(WINDOWWIDTH,WINDOWHEIGHT)), LINETHICKNESS*2)
    #Рисуем центральную линию
    pygame.draw.line(DISPLAYSURF, WHITE, ((WINDOWWIDTH/2),0),((WINDOWWIDTH/2),WINDOWHEIGHT), (int)(LINETHICKNESS/4))

#Рисуем рокетку
def drawRocket(rocket):
    #Останавливаем движение рокетки, если она опустится слишком низко к границе
    if rocket.bottom > WINDOWHEIGHT - LINETHICKNESS:
        rocket.bottom = WINDOWHEIGHT - LINETHICKNESS
    #Тоже самое, если рокетка слишком высоко
    elif rocket.top < LINETHICKNESS:
        rocket.top = LINETHICKNESS
    #рисуем рокетку
    pygame.draw.rect(DISPLAYSURF, WHITE, rocket)

#рисуем игровой шар
def drawBall(ball):
    pygame.draw.rect(DISPLAYSURF, WHITE, ball)

#перемещаем шарик и возвращаем его координаты
def moveBall(ball, ballDirX, ballDirY):
    ball.x += ballDirX
    ball.y += ballDirY
    return ball

#Проверка на столкновения с границами и рикошет шарика
#Функция возвращает новое направление
def checkEdgeCollision(ball, ballDirX, ballDirY):
    if ball.top == (LINETHICKNESS) or ball.bottom == (WINDOWHEIGHT - LINETHICKNESS):
        ballDirY = ballDirY * -1
    if ball.left == (LINETHICKNESS) or ball.right == (WINDOWWIDTH - LINETHICKNESS):
        ballDirX = ballDirX * -1
    return ballDirX, ballDirY

#Проверка на столкновение шарика с рокеткой и рикошет от неё     
def checkHitBall(ball, rocket1, rocket2, ballDirX):
    if ballDirX == -1 and rocket1.right == ball.left and rocket1.top < ball.bottom and rocket1.bottom > ball.top:
        return -1
    elif ballDirX == 1 and rocket2.left == ball.right and rocket2.top < ball.bottom and rocket2.bottom > ball.top:
        return -1
    else: return 1

#Функция проверяет условия получение очков игроком и возвращает новый счёт
def checkPointScored(rocket1, ball, score, ballDirX, FPS):
    #сбрасывает очки, если игрок проиграл
    if ball.left == LINETHICKNESS:
        FPS = 200
        return 0
    #+1 если игкрок отбил шар
    elif ballDirX == -1 and rocket1.right == ball.left and rocket1.top < ball.top and rocket1.bottom > ball.bottom:
        score += 1
        if score > 5:
            ##ускоряет игру при достижении очков кратного пяти
            FPS += 100 * (score % 5)
        return score
    # +5 если игкроку удалась обыграть ИИ
    elif ball.right == WINDOWWIDTH - LINETHICKNESS:
        score += 5
        if score > 5:
            FPS += 100 * (score % 5)
        return score
    #если ни одно из условий не выполнилось возвращает счёт неизменным
    else: return score

#ИИ для компьютера 
def artificialIntelligence(ball, ballDirX, Rocket2):
    #если шарик движется к игроку, то центрирует рокетку
    if ballDirX == -1:
        if Rocket2.centery < (WINDOWHEIGHT/2):
            Rocket2.y += 1
        elif Rocket2.centery > (WINDOWHEIGHT/2):
            Rocket2.y -= 1
    #если от игрока, то следит за шариком 
    elif ballDirX == 1:
        if Rocket2.centery < ball.centery:
            Rocket2.y += 1
        else:
            Rocket2.y -=1
    return Rocket2

#Отображает текущий счёт
def displayScore(score):
    resultSurf = BASICFONT.render('Счёт = %s' %(score), True, WHITE)
    resultRect = resultSurf.get_rect()
    resultRect.topleft = (WINDOWWIDTH - 250, 25)
    DISPLAYSURF.blit(resultSurf, resultRect)

#Основная функция
def main():
    pygame.init()
    global DISPLAYSURF
    #Определяем шрифт
    global BASICFONT, BASICFONTSIZE
    BASICFONTSIZE = 20
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT)) 
    pygame.display.set_caption('Pong')

    #Инициация переменных
    #все данные сохраняются в параметрах прямоугольников
    ballX = WINDOWWIDTH/2 - LINETHICKNESS/2
    ballY = WINDOWHEIGHT/2 - LINETHICKNESS/2
    playerOnePosition = (WINDOWHEIGHT - ROCKETSIZE) /2
    playerTwoPosition = (WINDOWHEIGHT - ROCKETSIZE) /2
    score = 0

    #Отслеживание положения шарика
    ballDirX = -1 ## -1 = left 1 = right
    ballDirY = -1 ## -1 = up 1 = down

    #Создаёт прямоугольники с параметрами координат для шарика и рокеток
    Rocket1 = pygame.Rect(ROCKETOFFSET,playerOnePosition, LINETHICKNESS,ROCKETSIZE)
    Rocket2 = pygame.Rect(WINDOWWIDTH - ROCKETOFFSET - LINETHICKNESS, playerTwoPosition, LINETHICKNESS,ROCKETSIZE)
    ball = pygame.Rect(ballX, ballY, LINETHICKNESS, LINETHICKNESS)

    #Рисуем начальные позиции объектов
    drawArena()
    drawRocket(Rocket1)
    drawRocket(Rocket2)
    drawBall(ball)

    pygame.mouse.set_visible(0) # make cursor invisible

    #основной цикл
    while True: 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # изменение положения рокетки в зависимости от положения мыши
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                Rocket1.y = mousey

        drawArena()
        drawRocket(Rocket1)
        drawRocket(Rocket2)
        drawBall(ball)

        ball = moveBall(ball, ballDirX, ballDirY)
        ballDirX, ballDirY = checkEdgeCollision(ball, ballDirX, ballDirY)
        score = checkPointScored(Rocket1, ball, score, ballDirX, FPS)
        ballDirX = ballDirX * checkHitBall(ball, Rocket1, Rocket2, ballDirX)
        Rocket2 = artificialIntelligence (ball, ballDirX, Rocket2)

        displayScore(score)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()

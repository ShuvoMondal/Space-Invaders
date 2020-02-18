import pygame
import random
import math
from pygame import mixer

pygame.init()
background = pygame.image.load('background2.png')

mixer.music.load('background.wav')
mixer.music.play(-1)

screen = pygame.display.set_mode((1000,700))
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')

pygame.display.set_icon(icon)
playerImg = pygame.image.load('player.png')
playerX,playerY = 480,600
playerX_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 8
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,935))
    enemyY.append(random.randint(40,150))
    enemyX_change.append(5)
    enemyY_change.append(25)

bulletImg = pygame.image.load('bullet.png')
bulletX,bulletY = 0,600
bulletX_change = 0
bulletY_change = 15
bullet_state = "ready"

score_value = 0
font = pygame.font.Font('Gameplay.ttf',32)
textX,textY = 10,10

font1 = pygame.font.Font('Gameplay.ttf',80)

def player(x,y):
    screen.blit(playerImg, (x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i], (x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(x+16,y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX,2)+math.pow(enemyY-bulletY,2))
    if distance<27:
        return True
    else:
        return False

def showScore(x,y):
    score = font.render("Score: "+str(score_value), True, (255,255,255))
    screen.blit(score, (x,y))

def gameOver():
    game_over = font1.render("GAME OVER", True, (255,255,255))
    screen.blit(game_over, (270,300))

running = True
while running:
    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                playerX_change = -5
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bulletSound = mixer.Sound('laser.wav')
                    bulletSound.play()
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a or event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 936:
        playerX = 936

    for i in range(num_of_enemies):
        if enemyY[i] > 550:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            gameOver()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 6
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 936:
            enemyX_change[i] = -6
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            collisionSound = mixer.Sound('explosion.wav')
            collisionSound.play()
            bulletY = 600
            bullet_state = 'ready'
            enemyX[i],enemyY[i] = random.randint(0,935),random.randint(40,150)
            score_value += 1
        
        enemy(enemyX[i],enemyY[i],i)

    if bulletY <= 0:
        bulletY = 600
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change


    player(playerX,playerY)
    showScore(textX,textY)
    pygame.display.update()

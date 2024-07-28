import random
import pygame
import math

pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('space_dark.jpg')
background = pygame.transform.scale(background, (800, 600))

# Title and icon
pygame.display.set_caption("Space Game")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('space-invaders.png')
playerImg = pygame.transform.scale(playerImg, (64, 64))
playerX = 380
playerY = 480
playerX_change = 0

explosionImg = pygame.image.load("blast.png")
explosionImg = pygame.transform.scale(explosionImg, (54, 54))


#2nd boss
bossImg= pygame.image.load("luffy.png")
bossImg= pygame.transform.scale(bossImg, (80,80))
bossX=random.randint(0,750)
bossY=random.randint(40,200)
bossX_change= 0.1
bossY_change=10

#2nd boss_fire
boss_fireImg = pygame.image.load('play.png')
boss_fireImg = pygame.transform.scale(boss_fireImg, (60, 60))
boss_fireX = 0
boss_fireY = 520
boss_fireX_change = 0.01
boss_fireY_change = 1
boss_fire_state = "ready"

#enemy bomb

bombImg = pygame.image.load("nuclear-bomb.png")
bombImg= pygame.transform.scale(bombImg,(25,25))
bombs=[]




# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
number_of_enemies = 6

for i in range(number_of_enemies):
    enemy_Img = pygame.image.load('alien.png')
    enemy_Img = pygame.transform.scale(enemy_Img, (54, 54))
    enemyImg.append(enemy_Img)
    enemyX.append(random.randint(0, 750))
    enemyY.append(random.randint(40, 200))
    enemyX_change.append(0.2)
    enemyY_change.append(40)

#player health bar
player_health = 100
max_health = 100
health_bar_width = 200
health_bar_height = 20

# Fire
fireImg = pygame.image.load('laserBullet.png')
fireImg = pygame.transform.scale(fireImg, (54, 54))
fireX = 0
fireY = 520
fireX_change = 0
fireY_change = .5
fire_state = "ready"


#bullets
bullets=[]

MAX_BULLETS = 5
score = 0
explosion_time = 0
explosion_position = (0, 0)

fire_rate = 100
last_fire_time = 0


game_over = False

font = pygame.font.Font(None,36)

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def second_boss(x,y):
    screen.blit(bossImg,(x,y))

def fire_bullet(x, y):
    bullets.append([x + 16, y + 10])

def collision_detect(fireX, fireY, enemyX, enemyY):
    distance = math.sqrt((math.pow(fireX - enemyX, 2)) + (math.pow(fireY - enemyY, 2)))
    if distance < 27:
        return True
    else:
        return False

def collision_player(playerX,playerY, enemyX,enemyY):
    distance = math.sqrt((math.pow(playerX-enemyX , 2)) + (math.pow(playerY-enemyY, 2)))
    if distance<27:
        return True
    else:
        return False
def explosion(x, y):
    screen.blit(explosionImg, (x, y))

def show_score(x,y):
    score_surface = font.render(f"Score: {score}", True, (255, 255,255))
    screen.blit(score_surface, (x,y))

def drop_bomb(x,y):
    bombs.append([x,y])

def move_bombs():
    global game_over, explosion_position, explosion_time, player_health
    bombs_to_remove = []
    for bomb in bombs:
        bomb[1] += 0.2  # Adjust speed as necessary
        screen.blit(bombImg, (bomb[0], bomb[1]))

        if collision_player(playerX, playerY, bomb[0], bomb[1]):
            player_health -= 10  # Reduce health by 10 (or any amount you prefer)
            explosion_position = (playerX, playerY)
            explosion_time = pygame.time.get_ticks()
            game_over = player_health <= 0  # Set game over if health drops to 0
            bombs_to_remove.append(bomb)

    for bomb in bombs_to_remove:
        if bomb in bombs:
            bombs.remove(bomb)



def draw_health_bar(x, y, health):
    # Draw the background of the health bar
    pygame.draw.rect(screen, (255, 0, 0), (x, y, health_bar_width, health_bar_height))
    # Draw the current health
    pygame.draw.rect(screen, (0, 255, 0), (x, y, (health / max_health) * health_bar_width, health_bar_height))


def reset_game():
    global playerX, playerY, playerX_change,fireX,fireY,fire_state,score, explosion_position, explosion_time, game_over,enemyY,enemyX
    playerX = 380
    playerY = 480
    playerX_change = 0
    fireX = 0
    fireY = 520
    fire_state = "ready"
    score = 0
    explosion_time = 0
    explosion_position = (0, 0)
    game_over = False
    for i in range(number_of_enemies):
        enemyX[i] = random.randint(0, 750)
        enemyY[i] = random.randint(40, 200)

MAX_BULLETS = 20  # Define a maximum number of bullets
space_held_down=False

running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keystrokes
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE:
                space_held_down = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_SPACE:
                space_held_down = False

    if space_held_down and pygame.time.get_ticks() - last_fire_time >= fire_rate:
        fireX = playerX
        if len(bullets) < MAX_BULLETS:
            fire_bullet(fireX, fireY)
        last_fire_time = pygame.time.get_ticks()

    # Player movement
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(number_of_enemies):
        if not game_over:
            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 0.2
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -0.2
                enemyY[i] += enemyY_change[i]

        # Collision detection with player and enemy
        collision_with_player = collision_player(playerX, playerY, enemyX[i], enemyY[i])
        if collision_with_player:
            player_health -= 10  # Reduce health by 10
            explosion_position = (playerX, playerY)
            explosion_time = pygame.time.get_ticks()
            game_over = player_health <= 0  # Set game over if health drops to 0
            break

        enemy(enemyX[i], enemyY[i], i)

    # 2nd boss movement
    for i in range(1):
        if not game_over:
            bossX += bossX_change
            if bossX <= 0:
                bossX_change = 0.1
                bossY += bossY_change
            elif bossX >= 736:
                bossX_change = -0.1
                bossY += bossY_change

    if game_over:
        explosion(explosion_position[0], explosion_position[1])
        font = pygame.font.Font(None, 74)
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(game_over_text, (250, 250))

        play_again_text = font.render("Play Again", True, (255, 255, 255))
        play_again_rect = play_again_text.get_rect(center=(400, 350))
        screen.blit(play_again_text, play_again_rect.topleft)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_again_rect.collidepoint(mouse_pos):
                    reset_game()
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    # Display the explosion for a short duration
    if explosion_time > 0:
        if pygame.time.get_ticks() - explosion_time < 500:  # Display for 500 ms
            explosion(explosion_position[0], explosion_position[1])
        else:
            explosion_time = 0  # Reset the explosion time

    # Collision detection and fire movement
    bullets_to_remove = []
    for bullet in bullets:
        screen.blit(fireImg, (bullet[0], bullet[1]))
        bullet[1] -= fireY_change
        if bullet[1] <= 0:
            bullets_to_remove.append(bullet)
        else:
            for i in range(number_of_enemies):
                if collision_detect(enemyX[i], enemyY[i], bullet[0], bullet[1]):
                    bullets_to_remove.append(bullet)
                    score += 1
                    explosion_position = (enemyX[i], enemyY[i])
                    explosion_time = pygame.time.get_ticks()
                    drop_bomb(enemyX[i], enemyY[i])  # Drop a bomb when enemy is destroyed
                    enemyX[i] = random.randint(0, 750)
                    enemyY[i] = random.randint(40, 150)
                    break  # Exit the inner loop once a collision is detected

    for bullet in bullets_to_remove:
        if bullet in bullets:
            bullets.remove(bullet)

    if score >= 20:
        second_boss(bossX, bossY)

    move_bombs()  # Move bombs and check for collisions with the player

    draw_health_bar(10, 50, player_health)  # Draw the health bar

    show_score(10, 10)
    player(playerX, playerY)

    pygame.display.update()

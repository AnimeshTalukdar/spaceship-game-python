import os.path

import pygame

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
white = (255, 255, 255)
brown = (99, 55, 11)
pygame.display.set_caption("First game")
FPS = 60
vel = 5
border = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)
bulletVel = 7
maxBullets = 3
space= pygame.transform.scale(pygame.image.load(os.path.join("Assets","space.png")),(WIDTH,HEIGHT))
red_bullet_color = (255, 255, 0)
yellow_bullet_color = (255, 0, 255)

HEALTH = 3

yellowHit = pygame.USEREVENT + 1
redHit = pygame.USEREVENT + 2


pygame.font.init()

HEALTH_FONT = pygame.font.SysFont("comicsans",40)
WINNER_FONT = pygame.font.SysFont("comicsans",100)
spaceShipWidth, spaceShipHeight = 55, 40
yellowSpaceShip = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png"))
redSpaceShip = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
yellowSpaceShip = pygame.transform.scale(yellowSpaceShip, (spaceShipWidth, spaceShipHeight))
redSpaceShip = pygame.transform.scale(redSpaceShip, (spaceShipWidth, spaceShipHeight))
yellowSpaceShip = pygame.transform.rotate(yellowSpaceShip, 90)
redSpaceShip = pygame.transform.rotate(redSpaceShip, 270)


def draw_window(red, yellow, red_bullets, yellow_bullets,red_health,yellow_health):
    WIN.blit(space,(0,0))

    red_health_text = HEALTH_FONT.render("Health: "+str(red_health),1,white)
    yellow_health_text = HEALTH_FONT.render("Health: "+str(yellow_health),1,white)

    WIN.blit(yellowSpaceShip, (yellow.x - spaceShipWidth // 2, yellow.y - spaceShipHeight // 2))
    WIN.blit(redSpaceShip, (red.x - spaceShipWidth // 2, red.y - spaceShipHeight // 2))
    WIN.blit(red_health_text,(WIDTH-red_health_text.get_width()-10,10))
    WIN.blit(yellow_health_text,(10,10))


    pygame.draw.rect(WIN, brown, border)

    for bullet in red_bullets:
        pygame.draw.rect(WIN, red_bullet_color, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, yellow_bullet_color, bullet)

    pygame.display.update()


def handle_movement(keys_pressed, yellow, red):
    if keys_pressed[pygame.K_a] and yellow.x - vel > 0:  # left
        yellow.x -= vel
    if keys_pressed[pygame.K_w] and yellow.y - vel > 0:  # up
        yellow.y -= vel
    if keys_pressed[pygame.K_s] and yellow.y + vel < HEIGHT - spaceShipHeight // 2:  # down
        yellow.y += vel
    if keys_pressed[pygame.K_d] and yellow.x + vel < WIDTH // 2 - spaceShipWidth // 2:  # right
        yellow.x += vel

    if keys_pressed[pygame.K_LEFT] and red.x - vel > WIDTH // 2 + spaceShipWidth // 2:  # left
        red.x -= vel
    if keys_pressed[pygame.K_UP] and red.y - vel > 0:  # up
        red.y -= vel
    if keys_pressed[pygame.K_DOWN] and red.y + vel < HEIGHT - spaceShipHeight // 2:  # down
        red.y += vel
    if keys_pressed[pygame.K_RIGHT] and red.x + vel < WIDTH:  # right
        red.x += vel


def handle_bullets(red_bullets, yellow_bullets, red, yellow):
    for bullet in yellow_bullets:
        bullet.x += bulletVel
        if red.colliderect(bullet):
            yellow_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(redHit))

        if bullet.x>WIDTH:
            yellow_bullets.remove(bullet)
    for bullet in red_bullets:
        bullet.x -= bulletVel
        if yellow.colliderect(bullet):
            red_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(yellowHit))

        if bullet.x<0:
            red_bullets.remove(bullet)

def draw_winner (winner):
    draw_text= WINNER_FONT.render(winner,1,white)
    WIN.blit(draw_text,((WIDTH//2-draw_text.get_width()//2),HEIGHT/2-draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)
def main():
    red = pygame.Rect(800, HEIGHT // 2, spaceShipWidth, spaceShipHeight)
    yellow = pygame.Rect(100, HEIGHT // 2, spaceShipWidth, spaceShipWidth)
    clock = pygame.time.Clock()

    red_bullets = []
    yellow_bullets = []
    red_health=HEALTH
    yellow_health=HEALTH

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type==redHit:
                red_health-=1
            if event.type==yellowHit:
                yellow_health-=1

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < maxBullets:
                    bullet = pygame.Rect(yellow.x + yellow.width // 2, yellow.y + 5, 10, 5)
                    yellow_bullets.append(bullet)
                if event.key == pygame.K_RCTRL and len(red_bullets) < maxBullets:
                    bullet = pygame.Rect(red.x - red.height // 2, red.y + 5, 10, 5)
                    red_bullets.append(bullet)


        draw_window(red, yellow, red_bullets, yellow_bullets,red_health,yellow_health)
        keys_pressed = pygame.key.get_pressed()
        handle_movement(keys_pressed, yellow, red)

        handle_bullets(red_bullets, yellow_bullets, red, yellow)

        winner_text=""
        if red_health <=0:
            winner_text = "Yellow Wins!"
        if yellow_health<=0:
            winner_text = "Red Wins!"
        if winner_text !="":
            draw_winner(winner_text)
            break



    main()


if __name__ == "__main__":
    main()

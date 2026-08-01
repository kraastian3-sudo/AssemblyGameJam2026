import sys, pygame, random
pygame.joystick.init()
pygame.init()

if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print("Controller:", joystick.get_name())
else:
    joystick = None
    print("No controller connected.")

WIDTH = 1280
HEIGHT = 1024

PAD_WIDTH = 20
PAD_HEIGHT = 150

PADDLE_SPEED = 8

BALL_RADIUS = 20

ball_x = WIDTH // 2
ball_y = HEIGHT // 2

ball_speed_x = 7
ball_speed_y = 5

# Left paddle
left_paddle = pygame.Rect(
    50,
    HEIGHT // 2 - PAD_HEIGHT // 2,
    PAD_WIDTH,
    PAD_HEIGHT
)

# Right paddle
right_paddle = pygame.Rect(
    WIDTH - 50 - PAD_WIDTH,
    HEIGHT // 2 - PAD_HEIGHT // 2,
    PAD_WIDTH,
    PAD_HEIGHT
)

# ball hitbox
ball_rect = pygame.Rect(
    ball_x - BALL_RADIUS,
    ball_y - BALL_RADIUS,
    BALL_RADIUS * 2,
    BALL_RADIUS * 2
)

# score 
left_score = 0
right_score = 0

font = pygame.font.Font(None, 72)

black = 0, 0, 0
white = 255, 255, 255

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My First Pygame")

clock = pygame.time.Clock()

running = True

while running:

    # Check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #gameloop

    #controls
    # if joystick:
        # Left stick vertical axis
        #axis = joystick.get_axis(1)

        # Ignore tiny movements (stick drift)
        #if abs(axis) > 0.1:
            #left_paddle.y += int(axis * PADDLE_SPEED)    

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        right_paddle.y -= PADDLE_SPEED

    if keys[pygame.K_DOWN]:
        right_paddle.y += PADDLE_SPEED

    
    if keys[pygame.K_w]:
        left_paddle.y -= PADDLE_SPEED

    if keys[pygame.K_s]:
        left_paddle.y += PADDLE_SPEED

    # Keep paddle on screen
    left_paddle.y = max(0, min(left_paddle.y, HEIGHT - PAD_HEIGHT))   

            # Keep paddle on screen
    right_paddle.y = max(0, min(right_paddle.y, HEIGHT - PAD_HEIGHT))     


    # Ball movement
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    if ball_y - BALL_RADIUS <= 0:
        ball_speed_y *= -1

    if ball_y + BALL_RADIUS >= HEIGHT:
        ball_speed_y *= -1
        
    if ball_rect.colliderect(left_paddle):
        ball_x = left_paddle.right + BALL_RADIUS
        ball_speed_x *= -1

    if ball_rect.colliderect(right_paddle):
        ball_x = right_paddle.left - BALL_RADIUS
        ball_speed_x *= -1

    #sync with ball hitbox
    ball_rect.center = (ball_x, ball_y)

    # scoring
    if ball_x < 0:
        ball_x = WIDTH // 2
        ball_y = HEIGHT // 2
        right_score += 1

    if ball_x > WIDTH:
        ball_x = WIDTH // 2
        ball_y = HEIGHT // 2
        left_score += 1

        ball_speed_x *= random.choice([-1, 1])

    # Fill background
    screen.fill((white))

    # scores
    left_text = font.render(str(left_score), True, (black))
    right_text = font.render(str(right_score), True, (black))

    screen.blit(left_text, (WIDTH // 2 - 100, 30))
    screen.blit(right_text, (WIDTH // 2 + 70, 30))

    pygame.draw.rect(screen, (black), left_paddle)
    pygame.draw.rect(screen, (black), right_paddle)
    pygame.draw.circle(screen, (black), (ball_x, ball_y), BALL_RADIUS)

    # Update screen
    pygame.display.flip()

    # Limit FPS
    clock.tick(60)

pygame.quit()
sys.exit()
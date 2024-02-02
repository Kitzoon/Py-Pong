import pygame, random

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True
delta_time = 0

font = pygame.font.Font(None, 45)
pygame.display.set_caption("Py-Pong")

paddle = {
    "width": 15,
    "height": 135,
    "x": screen.get_width() / 15,
    "y": screen.get_height() / 3,
    "move_speed": 300,
    "score": 0
}

bot_paddle = {
    "width": paddle["width"],
    "height": paddle["height"],
    "x": screen.get_width() / 1.125,
    "y": screen.get_height() / 3,
    "move_speed": paddle["move_speed"],
    "score": 0,
    "random_movement": 0
}

ball = {
    "direction": "left",
    "y_direction": "none",
    "x": screen.get_width() / 2,
    "y": screen.get_height() / 2.3,
    "move_speed": 250,
    "radius": 10,
    "busy": False
}

audio = {
    "lose": pygame.mixer.Sound("audio/lose.mp3"),
    "win": pygame.mixer.Sound("audio/win.mp3"),
    "hit": pygame.mixer.Sound("audio/hitBall.mp3")
}

def check_collision(object_col):
    if object_col.colliderect(pygame.Rect(ball["x"] - ball["radius"], ball["y"] - ball["radius"], 2 * ball["radius"], 2 * ball["radius"])):
        return True
    else:
        return False

def score(who_scored):
    # to make sure the score function isnt spammed
    if ball["busy"] is False:
        # reset ball
        ball["x"] = screen.get_width() / 2
        ball["y"] = screen.get_height() / 2.3
        ball["y_direction"] = "none"
        ball["direction"] = "left"
        ball["busy"] = True

        # reset player paddle
        paddle["x"] = screen.get_width() / 15
        paddle["y"] = screen.get_height() / 3

        # reset bot paddle
        bot_paddle["x"] = screen.get_width() / 1.125
        bot_paddle["y"] = screen.get_height() / 3

        who_scored["score"] += 1
        ball["busy"] = False

while running:
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # background color
    screen.fill("black")

    # player paddle
    player_paddle_object = pygame.draw.rect(screen, "white", (paddle["x"], paddle["y"], paddle["width"], paddle["height"]))
    # bot paddle
    bot_paddle_object = pygame.draw.rect(screen, "white", (bot_paddle["x"], bot_paddle["y"], bot_paddle["width"], bot_paddle["height"]))
    # ball
    ball_object = pygame.draw.circle(screen, "white", pygame.Vector2(ball["x"], ball["y"]), ball["radius"])

    player_border = pygame.draw.rect(screen, "black", (screen.get_width() / 105, screen.get_height() / 60, 5, 1000))
    bot_border = pygame.draw.rect(screen, "black", (screen.get_width() / 1.01, screen.get_height() / 60, 5, 1000))

    ceiling_border = pygame.draw.rect(screen, "black", (screen.get_width() / 100, screen.get_height() / 60, 1000, 5))
    floor_border = pygame.draw.rect(screen, "black", (screen.get_width() / 100, screen.get_height() / 1.02, 1000, 5))

    # text score
    score_text = font.render(str(paddle["score"]) + " - " + str(bot_paddle["score"]), True, "white")
    text_rect = score_text.get_rect()
    text_rect.center = (screen.get_width() / 2, screen.get_height() / 8)

    # controls
    if pygame.key.get_pressed()[pygame.K_s] and not check_collision(ceiling_border):
        paddle["y"] += (paddle["move_speed"] * delta_time)
    
    if pygame.key.get_pressed()[pygame.K_w] and not check_collision(floor_border):
        paddle["y"] -= (paddle["move_speed"] * delta_time)

    if ball["direction"] == "left" and not ball["busy"]:
        ball["x"] -= (ball["move_speed"] * delta_time)
    
    if ball["direction"] == "right" and not ball["busy"]:
        ball["x"] += (ball["move_speed"] * delta_time)

        # bot movement
        if bot_paddle["random_movement"] == 0:
            bot_paddle["y"] = ball["y"]
        else:
            bot_paddle["y"] = ball["y"] * 1.05

    if ball["y_direction"] == "up" and not ball["busy"]:
        ball["y"] += (ball["move_speed"] * delta_time)
    
    if ball["y_direction"] == "down" and not ball["busy"]:
        ball["y"] -= (ball["move_speed"] * delta_time)
    
    if check_collision(player_paddle_object):
        ball["direction"] = "right"
        audio["hit"].play()
        ball["y_direction"] = random.choice(["up", "down"])
    
    if check_collision(bot_paddle_object):
        ball["direction"] = "left"
        audio["hit"].play()
        ball["y_direction"] = random.choice(["up", "down"])
        bot_paddle["random_movement"] = random.choice([0, 1])
    
    if check_collision(ceiling_border):
        ball["y_direction"] = "up"
        audio["hit"].play()
    
    if check_collision(floor_border):
        ball["y_direction"] = "down"
        audio["hit"].play()
    
    if check_collision(player_border) and ball["busy"] is False:
        print("player lost!")
        audio["lose"].play()
        score(bot_paddle)
    
    if check_collision(bot_border) and ball["busy"] is False:
        print("bot lost!")
        audio["win"].play()
        score(paddle)

    # flip() the display to put your work on screen
    delta_time = clock.tick(60) / 1000
    screen.blit(score_text, text_rect)
    pygame.display.flip()

pygame.quit()
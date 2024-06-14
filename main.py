import pygame
import sys
import random


class Block(object):
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)


class Ball(Block):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed_x = 7 * random.choice((1, -1))
        self.speed_y = 7 * random.choice((1, -1))
        self.opponent_score = 0
        self.player_score = 0
        self.score_time = True
        self.current_time = 0
        self.gameover_time = 0

    def draw_image(self, output, color):
        pygame.draw.ellipse(output, color, self.rect)

    def movement(self, obj1, obj2):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            pygame.mixer.Sound.play(pong_sound)
            self.speed_y *= -1

        if self.rect.left <= 0:
            if self.player_score == 7:
                self.gameover_time = pygame.time.get_ticks()
            else:
                pygame.mixer.Sound.play(score_sound)
                self.score_time = pygame.time.get_ticks()
                self.player_score += 1

        if self.rect.right >= screen_width:
            if self.opponent_score == 7:
                self.gameover_time = pygame.time.get_ticks()
            else:
                pygame.mixer.Sound.play(score_sound)
                self.score_time = pygame.time.get_ticks()
                self.opponent_score += 1

        if self.rect.colliderect(obj1):
            pygame.mixer.Sound.play(pong_sound)
            if abs(self.rect.right - obj1.left) < 12:
                self.speed_x *= -1
            elif abs(self.rect.bottom - obj1.top) < 12 and self.speed_y > 0:
                self.speed_y *= -1
            elif abs(self.rect.top - obj1.bottom) < 12 and self.speed_y < 0:
                self.speed_y *= -1

        if self.rect.colliderect(obj2):
            pygame.mixer.Sound.play(pong_sound)
            if abs(self.rect.left - obj2.right) < 12:
                self.speed_x *= -1
            elif abs(self.rect.bottom - obj2.top) < 12 and self.speed_y > 0:
                self.speed_y *= -1
            elif abs(self.rect.top - obj2.bottom) < 12 and self.speed_y < 0:
                self.speed_y *= -1

    def acceleration(self):
        # Acceleration
        accelerate_rate = 0.003
        if self.speed_x > 0 and self.speed_y > 0:
            self.speed_x += accelerate_rate
            self.speed_y += accelerate_rate
        elif self.speed_x > 0 and self.speed_y < 0:
            self.speed_x += accelerate_rate
            self.speed_y -= accelerate_rate
        elif self.speed_x < 0 and self.speed_y > 0:
            self.speed_x -= accelerate_rate
            self.speed_y += accelerate_rate
        else:
            self.speed_x -= accelerate_rate
            self.speed_y -= accelerate_rate

    def start(self):
        self.score_time = pygame.time.get_ticks()
        self.restart()

    def name(self):
        if self.current_time - self.score_time < 3000:
            player1 = sys_font.render("Opponent", True, light_grey)
            screen.blit(player1, (10, 10))
            player2 = sys_font.render("Player", True, light_grey)
            screen.blit(player2, (screen_width - 80, 10))

    def restart(self):

        self.current_time = pygame.time.get_ticks()
        self.rect.center = (screen_width / 2, screen_height / 2)
        self.name()

        if self.current_time - self.score_time < 1000:
            number_three = game_font.render("3", True, light_grey)
            screen.blit(number_three, (screen_width / 2 - 10, screen_height / 2 + 20))
        if 1000 < self.current_time - self.score_time < 2000:
            number_two = game_font.render("2", True, light_grey)
            screen.blit(number_two, (screen_width / 2 - 10, screen_height / 2 + 20))
        if 2000 < self.current_time - self.score_time < 3000:
            number_one = game_font.render("1", True, light_grey)
            screen.blit(number_one, (screen_width / 2 - 10, screen_height / 2 + 20))

        if self.current_time - self.score_time < 3000:
            self.speed_x, self.speed_y = 0, 0
        else:
            self.speed_x = 7 * random.choice((1, -1))
            self.speed_y = 7 * random.choice((1, -1))
            self.score_time = None

    def win(self, message):
        self.rect.center = (screen_width / 2, screen_height / 2)
        self.speed_x, self.speed_y = 0, 0
        self.current_time = pygame.time.get_ticks()
        player.restart()
        opponent.restart()
        if self.current_time - self.gameover_time < 5000:
            game_set1 = set_font.render(message, True, light_grey)
            screen.blit(game_set1, (screen_width / 2 - 210, 70))
        if self.current_time - self.gameover_time > 5000:
            pygame.mixer.music.unload()
            self.opponent_score = 0
            self.player_score = 0
            self.current_time = 0
            self.gameover_time = 0
            main_menu()


class Player(Block):
    def __init__(self, x, y, width, height, speed):
        super().__init__(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def draw_image(self, output, color):
        pygame.draw.rect(output, color, self.rect)

    def movement(self, evt):
        if evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_DOWN or evt.key == pygame.K_s:
                self.speed += 7
            if evt.key == pygame.K_UP or evt.key == pygame.K_w:
                self.speed -= 7
        if evt.type == pygame.KEYUP:
            if evt.key == pygame.K_DOWN or evt.key == pygame.K_s:
                self.speed -= 7
            if evt.key == pygame.K_UP or evt.key == pygame.K_w:
                self.speed += 7

    def limit(self):
        self.rect.y += self.speed

        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

    def restart(self):
        self.rect.x = self.x
        self.rect.y = self.y


class Opponent(Block):
    def __init__(self, x, y, width, height, speed):
        super().__init__(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def draw_image(self, output, color):
        pygame.draw.rect(output, color, self.rect)

    def ai(self, circle):
        if abs(self.rect.x - circle.x) < 0.75 * screen_width:
            if self.rect.top + 40 < circle.centery:
                self.rect.top += self.speed
            if self.rect.bottom - 40 > circle.centery:
                self.rect.bottom -= self.speed

        if abs(self.rect.x - circle.x) > 0.75 * screen_width:
            if self.rect.top + 30 < screen_height/2:
                self.rect.top += self.speed
            if self.rect.bottom - 30 > screen_height/2:
                self.rect.bottom -= self.speed

        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height

    def restart(self):
        self.rect.x = self.x
        self.rect.y = self.y


class Button(object):
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.check = False

    def draw_image(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))


def mouse_clicked():
    # Checks for left-clicking on the mouse
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                return True


def music():
    # Randomly choose a music to play and checks if it is still playing a song before randomise again
    if not pygame.mixer.music.get_busy():
        choice = random.randint(1, 4)
        if choice == 1:
            pygame.mixer.music.load('Files/8 Bit Adventure.mp3')
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.play(0)
        if choice == 2:
            pygame.mixer.music.load('Files/Electro Fever.mp3')
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.play(0)
        if choice == 3:
            pygame.mixer.music.load('Files/Haters Gonna Hate.mp3')
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.play(0)


def run_game():
    #
    ball.start()

    # Plays music and cleanly exits the code when 'X' button is pressed
    while True:
        if checked_button.check and not unchecked_button.check:
            music()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            player.movement(event)  # Checks input of player for the movement of object

        # Game Logic
        opponent.ai(ball.rect)
        player.limit()
        ball.acceleration()
        ball.movement(player.rect, opponent.rect)

        # Display all the objects on screen
        screen.fill(bg_color)
        ball.draw_image(screen, light_grey)
        player.draw_image(screen, light_grey)
        opponent.draw_image(screen, light_grey)
        pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))
        pygame.draw.circle(screen, light_grey, (screen_width / 2, screen_height / 2), 200, width=3)

        # Conditions to end the game
        if ball.gameover_time:
            if ball.player_score == 7:
                ball.win("You have won")
            if ball.opponent_score == 7:
                ball.win("You have lost")

        # Restarts the ball when it is scored
        if ball.score_time and ball.player_score != 7 and ball.opponent_score != 7:
            ball.restart()
            player.restart()
            opponent.restart()

        # Display player score
        player_text = game_font.render(f"{ball.player_score}", True, light_grey)
        screen.blit(player_text, (screen_width / 2 + 45, 30))

        opponent_text = game_font.render(f"{ball.opponent_score}", True, light_grey)
        screen.blit(opponent_text, (screen_width / 2 - 60, 30))

        # Screen updater
        pygame.display.flip()
        clock.tick(60)


def main_menu():
    while True:
        screen.fill(bg_color)

        # Gets the position of the mouse
        pos = pygame.mouse.get_pos()

        # Reads whether the mouse is on top of a button
        if start_button.rect.collidepoint(pos) and start_button2.rect.collidepoint(pos):
            start_button2.draw_image()
            if mouse_clicked():
                run_game()
        else:
            start_button.draw_image()

        if exit_button.rect.collidepoint(pos) and exit_button2.rect.collidepoint(pos):
            exit_button2.draw_image()
            if mouse_clicked():
                pygame.quit()
                sys.exit()
        else:
            exit_button.draw_image()

        if option_button.rect.collidepoint(pos) and option_button2.rect.collidepoint(pos):
            option_button2.draw_image()
            if mouse_clicked():
                option_menu()
        else:
            option_button.draw_image()

        cover.draw_image()

        # To close the program cleanly when 'X' button is pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Screen updater
        pygame.display.flip()
        clock.tick(60)


def option_menu():
    while True:

        screen.fill(bg_color2)
        esc_button.draw_image()
        w_key.draw_image()
        up_key.draw_image()
        s_key.draw_image()
        down_key.draw_image()
        if checked_button.check and not unchecked_button.check:
            checked_button.draw_image()
        if unchecked_button.check and not checked_button.check:
            unchecked_button.draw_image()

        pos = pygame.mouse.get_pos()

        if checked_button.rect.collidepoint(pos) and unchecked_button.rect.collidepoint(pos):
            if mouse_clicked():
                if checked_button.check and not unchecked_button.check:
                    checked_button.check = False
                    unchecked_button.check = True
                elif unchecked_button.check and not checked_button.check:
                    checked_button.check = True
                    unchecked_button.check = False

        escape_message = sys_font.render('Press escape to Return', True, light_grey)
        screen.blit(escape_message, (90, 20))
        control_message = sys_font.render('Control:', True, light_grey)
        screen.blit(control_message, (15, 110))
        slash_message = set_font.render('/', True, light_grey)
        screen.blit(slash_message, (80, 150))
        screen.blit(slash_message, (80, 230))
        up_message = sys_font.render("Player's upward movement", True, light_grey)
        screen.blit(up_message, (190, 160))
        down_message = sys_font.render("Player's downward movement", True, light_grey)
        screen.blit(down_message, (190, 240))
        music_header = sys_font.render('Music:', True, light_grey)
        screen.blit(music_header, (15, 330))
        music_message = sys_font.render('Enable Music', True, light_grey)
        screen.blit(music_message, (110, 395))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu()

        # Screen updater
        pygame.display.flip()
        clock.tick(60)


# Initializing pygame
pygame.init()
clock = pygame.time.Clock()

# Initializing game screen
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong by Brad Loo')

# Load images
start_image = pygame.image.load('Files/start_btn(1).png').convert_alpha()
start_image2 = pygame.image.load('Files/start_btn(2).png').convert_alpha()
exit_image = pygame.image.load('Files/exit_btn(1).png').convert_alpha()
exit_image2 = pygame.image.load('Files/exit_btn(2).png').convert_alpha()
option_image = pygame.image.load('Files/option_btn(1).png').convert_alpha()
option_image2 = pygame.image.load('Files/option_btn(2).png').convert_alpha()
esc_image = pygame.image.load('Files/escape.png').convert_alpha()
w_image = pygame.image.load('Files/W_key.png').convert_alpha()
up_image = pygame.image.load('Files/UP_key.png').convert_alpha()
s_image = pygame.image.load('Files/S_key.png').convert_alpha()
down_image = pygame.image.load('Files/DOWN_key.png').convert_alpha()
checked_image = pygame.image.load('Files/checked.png').convert_alpha()
unchecked_image = pygame.image.load('Files/unchecked.png').convert_alpha()
cover = pygame.image.load("Files/Cover.png").convert_alpha()

# Load Buttons
start_button = Button(200, 520, start_image, 0.8)
exit_button = Button(880, 520, exit_image, 0.8)
option_button = Button(530, 520, option_image, 0.8)
start_button2 = Button(200, 520, start_image2, 0.8)
exit_button2 = Button(880, 520, exit_image2, 0.8)
option_button2 = Button(530, 520, option_image2, 0.8)
esc_button = Button(15, 10, esc_image, 2)
w_key = Button(15, 150, w_image, 1.75)
up_key = Button(110, 150, up_image, 1.75)
s_key = Button(15, 230, s_image, 1.75)
down_key = Button(110, 230, down_image, 1.75)
checked_button = Button(0, 360, checked_image, 0.2)
unchecked_button = Button(0, 360, unchecked_image, 0.2)
cover = Button(200, 0, cover, 3)

# Load Objects
ball = Ball(screen_width/2 - 15, screen_height/2 - 15, 30, 30)
player = Player(screen_width - 20, screen_height/2 - 70, 10, 140, 0)
opponent = Opponent(10, screen_height/2 - 70, 10, 140, 10)

# Initializing Colors
bg_color = pygame.Color('grey12')
bg_color2 = pygame.Color('#353535')
light_grey = (200, 200, 200)

# Initializing Fonts
game_font = pygame.font.Font("freesansbold.ttf", 32)
sys_font = pygame.font.SysFont('bahnschrift', 24)
set_font = pygame.font.Font("freesansbold.ttf", 64)

# Initializing Sounds
pong_sound = pygame.mixer.Sound("Files/pong.ogg")
score_sound = pygame.mixer.Sound("Files/score.ogg")
pong_sound.set_volume(0.2)
score_sound.set_volume(0.2)

# Initializing Options
unchecked_button.check = True

main_menu()

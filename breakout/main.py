"""Main module of the game"""
import pygame
from random import randint
from breakout.variables import *
from breakout.paddle import Paddle
from breakout.ball import Ball
from breakout.brick import Brick


class Breakout():
    """Main class of the game"""
    def __init__(self, ai = False):
        if not ai:
            pygame.init()
            self.screen = pygame.display.set_mode(SIZE)
            self.__set_window_parameters()
            self.clock = pygame.time.Clock()
        self.carry_on = False
        self.score = 0
        self.lives = 3
        self.sprites = pygame.sprite.Group()
        self.paddle = Paddle(LIGHTBLUE, 100, 10)
        self.ball = Ball(WHITE, 10, 10)
        self.bricks = pygame.sprite.Group()

    def start(self):
        """Method starting the game"""
        self.carry_on = True
        self.__init_game()

    def step(self, action, fps=True):
        """Game step for AI development"""
        if self.carry_on:
            self.hit = 0
            score = self.score
            lives = self.lives
            if fps:
                self.__capture_events()
            self.__move_paddle(action)

            self.__game_tick()
            if fps:
                self.__paint_background()
                self.__paint_score()

                self.__game_paint()

                pygame.display.flip()
            if fps:
                self.clock.tick(60)

            observation = self.__get_observation()
            reward = 0
            if score != self.score:
                reward += self.score - score
            if lives != self.lives:
                reward -= (lives - self.lives) * 10
            if self.hit != 0:
                reward += 5
        return observation, reward, not self.carry_on

    def get_input_size(self):
        observation = self.__get_observation()
        return len(observation)
    
    def get_output_size(self):
        return 3

    def __get_observation(self):
        observation = self.__get_bricks_position()
        observation.append(self.paddle.rect.x / 700)
        observation.append(self.ball.rect.x / 790)
        observation.append(self.ball.rect.y / 590)
        observation.append((self.ball.velocity[0] + 8) / 16)
        observation.append((self.ball.velocity[1] + 8) / 16)
        return observation

    def get_observation(self):
        return self.__get_observation()

    def __get_bricks_position(self):
        bricks = self.bricks.sprites()
        bricksDict = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
        for brick in bricks:
            x = int((brick.rect.x - 60)/100)
            y = 0
            if brick.rect.y == 60:
                y = 0
            if brick.rect.y == 100:
                y = 0.5
            if brick.rect.y == 140:
                y = 1
            if x in bricksDict and y > bricksDict[x]:
                bricksDict[x] = y
            elif x not in bricksDict:
                bricksDict[x] = y
        return list(bricksDict.values())

    def __set_window_parameters(self):
        pygame.display.set_caption(TITLE)

    def __capture_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.carry_on = False

    def __move_paddle(self, action):
        if action == 1:
            self.paddle.move_left(10)
        elif action == 2:
            self.paddle.move_right(10)
        elif action == 0:
            self.paddle.not_moving()

    def __paint_background(self):
        self.screen.fill(DARKBLUE)
        pygame.draw.line(self.screen, WHITE, [0, 38], [800, 38], 2)

    def __paint_score(self):
        font = pygame.font.Font(None, 34)
        text = font.render("Score: " + str(self.score), 1, WHITE)
        self.screen.blit(text, (20,10))
        text = font.render("Lives: " + str(self.lives), 1, WHITE)
        self.screen.blit(text, (650,10))

    def __init_game(self):
        self.paddle.paint()
        self.paddle.rect.x = 350
        self.paddle.rect.y = 560
        self.sprites.add(self.paddle)
        self.ball.paint()
        self.ball.rect.x = 345
        self.ball.rect.y = 460
        self.sprites.add(self.ball)
        self.__create_bricks()

    def __create_bricks(self):
        for i in range(7):
            brick = Brick(RED,80,30)
            brick.paint()
            brick.rect.x = 60 + i* 100
            brick.rect.y = 60
            self.sprites.add(brick)
            self.bricks.add(brick)
        for i in range(7):
            brick = Brick(ORANGE,80,30)
            brick.paint()
            brick.rect.x = 60 + i* 100
            brick.rect.y = 100
            self.sprites.add(brick)
            self.bricks.add(brick)
        for i in range(7):
            brick = Brick(YELLOW,80,30)
            brick.paint()
            brick.rect.x = 60 + i* 100
            brick.rect.y = 140
            self.sprites.add(brick)
            self.bricks.add(brick)

    def __game_tick(self):
        self.sprites.update()
        if self.ball.rect.x>=790:
            self.ball.velocity[0] = -self.ball.velocity[0]
        if self.ball.rect.x<=0:
            self.ball.velocity[0] = -self.ball.velocity[0]
        if self.ball.rect.y>590:
            self.ball.velocity[1] = -self.ball.velocity[1]
            self.lives -= 1
            self.ball.restore()
            if self.lives == 0:
                self.__game_over()
        if self.ball.rect.y<40:
            self.ball.velocity[1] = -self.ball.velocity[1]
        self.__check_ball_colides_paddle()
        self.__check_ball_colides_brick()

    def __check_ball_colides_paddle(self):
        if pygame.sprite.collide_mask(self.ball, self.paddle):
            self.ball.rect.x -= self.ball.velocity[0]
            self.ball.rect.y = self.paddle.rect.y -20
            self.ball.bounce_paddle(self.paddle)
            self.hit = 5

    def __check_ball_colides_brick(self):
        brick_collision_list = pygame.sprite.spritecollide(self.ball,self.bricks,False)
        for brick in brick_collision_list:
            self.ball.bounce()
            self.score += 1
            brick.kill()
            if len(self.bricks)==0:
                self.__game_finish()

    def close(self):
        pygame.quit()

    def __game_finish(self):
        self.__create_bricks()

    def __game_over(self):
        self.carry_on=False

    def __game_paint(self):
        self.sprites.draw(self.screen)

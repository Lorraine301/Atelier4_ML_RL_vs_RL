import pygame
import random

class Game:

    def __init__(self, agent1, agent2, mode="RL_RL"):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.agent1 = agent1
        self.agent2 = agent2
        self.mode = mode

        self.screen_width = 1280
        self.screen_height = 820
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Pong RL vs RL")

        self.bg_color = pygame.Color("grey12")
        self.light_grey = (200, 200, 200)

        self.reset()

    # RESET
    def reset(self):
        self.ball = pygame.Rect(self.screen_width//2 - 15,
                                self.screen_height//2 - 15, 30, 30)
        self.player = pygame.Rect(self.screen_width - 10,
                                  self.screen_height//2 - 70, 10, 140)
        self.opponent = pygame.Rect(10,
                                    self.screen_height//2 - 70, 10, 140)

        self.ball_speed_x = 7 * random.choice((1, -1))
        self.ball_speed_y = 7 * random.choice((1, -1))
        self.player_speed = 0
        self.opponent_speed = 0

        self.player_score = 0
        self.opponent_score = 0

   
    # GAME MECHANICS
    def ball_animation(self):
        self.ball.x += self.ball_speed_x
        self.ball.y += self.ball_speed_y

        if self.ball.top <= 0 or self.ball.bottom >= self.screen_height:
            self.ball_speed_y *= -1

        if self.ball.left <= 0:
            self.player_score += 1
            self.ball_restart()

        if self.ball.right >= self.screen_width:
            self.opponent_score += 1
            self.ball_restart()

        if self.ball.colliderect(self.player) or self.ball.colliderect(self.opponent):
            self.ball_speed_x *= -1

    def ball_restart(self):
        self.ball.center = (self.screen_width//2, self.screen_height//2)
        self.ball_speed_x *= random.choice((1, -1))
        self.ball_speed_y *= random.choice((1, -1))
    
    # mouvments des joueurs
    def move_player(self, action):
        self.player_speed = 6 * action
        self.player.y += self.player_speed
        self.player.y = max(0, min(self.screen_height-140, self.player.y))

    def move_opponent(self, action):
        self.opponent_speed = 6 * action
        self.opponent.y += self.opponent_speed
        self.opponent.y = max(0, min(self.screen_height-140, self.opponent.y))

    
    # STATES (discrétisés)
  
    def state_player(self):
        return (
            int(self.ball.y / 50),
            1 if self.ball_speed_y > 0 else -1,
            int(self.player.y / 50)
        )

    def state_opponent(self):
        return (
            int(self.ball.y / 50),
            1 if self.ball_speed_y > 0 else -1,
            int(self.opponent.y / 50)
        )

    # Pour deux agents RL

    def play(self, training=True, steps=2000, render=False):

        self.reset()

        rewards1, rewards2 = [], []

        s1 = self.state_player()
        s2 = self.state_opponent()

        for _ in range(steps):

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return rewards1, rewards2

            a1 = self.agent1.get_action(s1)
            a2 = self.agent2.get_action(s2)

            self.move_player(a1)
            self.move_opponent(a2)

            self.ball_animation()

            r1, r2 = 0, 0

            if self.player_score:
                r1, r2 = 1, -1
                self.player_score = 0

            if self.opponent_score:
                r1, r2 = -1, 1
                self.opponent_score = 0

            s1_ = self.state_player()
            s2_ = self.state_opponent()

            if training:
                self.agent1.update(s1, s1_, a1, None, r1)
                self.agent2.update(s2, s2_, a2, None, r2)

            rewards1.append(r1)
            rewards2.append(r2)

            s1, s2 = s1_, s2_

            if render:
                self.screen.fill(self.bg_color)
                pygame.draw.rect(self.screen, self.light_grey, self.player)
                pygame.draw.rect(self.screen, self.light_grey, self.opponent)
                pygame.draw.ellipse(self.screen, self.light_grey, self.ball)
                pygame.display.flip()
                self.clock.tick(60)

        return rewards1, rewards2

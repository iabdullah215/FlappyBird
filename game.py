import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 600, 400
GRAVITY = 0.25
FLAP_FORCE = -5
PIPE_WIDTH = 50
PIPE_HEIGHT = 300
PIPE_GAP = 100

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

bird_img = pygame.image.load("bird.png")
background_img = pygame.image.load("background.png")
pipe_img = pygame.image.load("pipe.png")

bird_img = pygame.transform.scale(bird_img, (50, 50))
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

class Bird:
    def __init__(self):
        self.x = WIDTH
        self.y = HEIGHT
        self.velocity = 0

    def flap(self):
        self.velocity = FLAP_FORCE

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self):
        screen.blit(bird_img, (self.x, self.y))

class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(50, HEIGHT - PIPE_GAP - 50)

    def move(self):
        self.x -= 2

    def collides_with_bird(self, bird):
        return (
            bird.x < self.x + PIPE_WIDTH
            and bird.x + 50 > self.x
            and (bird.y < self.height or bird.y + 50 > self.height + PIPE_GAP)
        )

    def draw(self):
        screen.blit(pipe_img, (self.x, 0), (0, 0, PIPE_WIDTH, self.height))
        screen.blit(
            pipe_img,
            (self.x, self.height + PIPE_GAP),
            (0, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT - self.height - PIPE_GAP),
        )

def game_loop():
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = [Pipe(WIDTH + i * (WIDTH // 2)) for i in range(2)]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        bird.update()

        if pipes[-1].x < WIDTH - WIDTH // 2:
            pipes.append(Pipe(WIDTH))

        for pipe in pipes:
            pipe.move()
            if pipe.collides_with_bird(bird):
                print("Game Over!")
                pygame.quit()
                sys.exit()

        pipes = [pipe for pipe in pipes if pipe.x + PIPE_WIDTH > 0]

        screen.blit(background_img, (0, 0))
        bird.draw()
        for pipe in pipes:
            pipe.draw()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    game_loop()

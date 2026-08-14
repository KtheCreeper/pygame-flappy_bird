import pygame
import random
from tools import *
import sys
import copy

class Pipe:
    def __init__(self, object:Object, speed:int, flip:bool, scored:bool=False):
        self.object:Object = object
        if flip == True:
            self.object.frames[0].transform(flip_y=True)

        self.speed:float = speed
        self.rect:pygame.Rect = self.object.frames[0].image.get_rect(topleft=(self.object.x, self.object.y))
        self.scored = scored

    def update(self, dt:float) -> int:
        self.object.x -= int(round(self.speed * dt, 0))
        self.rect.x = self.object.x
        if not self.scored and self.object.x <= 30:
            self.scored = True
            return 1
        else:
            return 0

    def draw(self, screen:pygame.Surface) -> None:
        self.object.render(screen, 0)

def spawn_pipes(pipes:list[Pipe,], pipe_sprite:Sprite, pipe_speed:int) -> list[Pipe]:
    gap:int = 150
    pipe_height:int = pipe_sprite.image.get_height()
    pipe_width:int = pipe_sprite.image.get_width()
    gap_center:int = random.randint(150, 400)
    bottom_y:int = gap_center + gap // 2
    top_y:int = gap_center - gap // 2 - pipe_height

    pipes.append(Pipe(Object([copy.deepcopy(pipe_sprite)], pipe_width, pipe_height, 700, top_y), pipe_speed, True))
    pipes.append(Pipe(Object([copy.deepcopy(pipe_sprite)], pipe_width, pipe_height, 700, bottom_y), pipe_speed, False, scored=True))

    return pipes

def main():
    pygame.init()
    screen:pygame.Surface = pygame.display.set_mode((550,550))
    pygame.display.set_caption('Flappy bird')
    logo:pygame.Surface = pygame.image.load("assets\\Game Objects\\yellowbird-downflap.png").convert_alpha()
    pygame.display.set_icon(logo)
    running:bool = True
    clock:pygame.time.Clock = pygame.time.Clock()
    delta_time:float = 0.1
    game:bool = False

    acceleration:int = 15
    velocity:int = 0
    space:list[str] = ["up", "locked"]
    scale:float = 1

    bird_frames:list[Sprite] = []
    for frame in ["down","mid","up"]:
        bird_frames.append(Sprite(pygame.image.load(f"assets\\Game Objects\\yellowbird-{frame}flap.png").convert_alpha(), scale=scale))
    bird_object = Object(bird_frames, bird_frames[0].image.get_width(), bird_frames[0].image.get_height(), 30, 30)

    pipe_image:pygame.Surface = pygame.image.load("assets\\Game Objects\\pipe-green.png").convert_alpha()
    pipe_sprite: Sprite = Sprite(pipe_image)

    pipes:list[Pipe] = []
    pipe_timer:float = 0
    pipe_interval:float = 1.8
    pipe_speed:int = 300

    text:Text = Text(pygame.font.Font("assets\\UI\\m6x11plus.ttf", 32), screen.get_width() - 150, 15, (255,255,255))
    score = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and space[1] == "unlocked":
                space = ["down", "unlocked"]
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                space = ["up", "unlocked"]


        screen.fill("grey")

        if velocity > 75 and bird_object.y != 600:
            frame = 0
        elif 75 > velocity > -50 or bird_object.y == 600:
            frame = 1
        else:
            frame = 2

        bird_object.render(screen,frame)
        bird_rect:pygame.Rect = bird_object.frames[frame].image.get_rect(topleft=(30, int(bird_object.y)))

        if game:

            velocity = min(acceleration + velocity, 450)
            bird_object.y = round(max(min(bird_object.y + (velocity * delta_time), 550), 0))
            if space == ["down", "unlocked"]:
                space[1] = "locked"
                velocity = -400

            pipe_timer += delta_time
            if pipe_timer >= pipe_interval:
                pipe_timer = 0
                pipes = spawn_pipes(pipes, pipe_sprite, pipe_speed)

            for pipe in pipes:
                score += pipe.update(delta_time)
                pipe.draw(screen)
                if bird_rect.colliderect(pipe.rect):
                    print("Hit pipe!")
                    sys.exit(0)

        text.render(screen, f"Score: {score}")

        pygame.display.flip()
        delta_time = clock.tick(60) / 1000
        delta_time = max(0.001, min(0.1, delta_time))

if __name__ == "__main__":
    main()

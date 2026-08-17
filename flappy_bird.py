import pygame
import random
from tools import *
import sys
import os
from typing import Optional

def resource_path(relative_path: str) -> str:
    meipass: Optional[str] = getattr(sys, "_MEIPASS", None)
    if meipass is not None:
        return os.path.join(meipass, relative_path)
    return os.path.join(relative_path)


class Pipe:
    def __init__(self, object:Object, speed:int, flip:bool, scored:bool=False):
        self.object:Object = object
        if flip:
            self.object.frames[0].transform(flip_y=True)

        self.speed:float = speed
        self.rect:pygame.Rect = self.object.frames[0].image.get_rect(
            topleft=(self.object.x, self.object.y)
        )
        self.scored = scored

    def update(self, dt:float) -> int:
        self.object.x -= int(round(self.speed * dt, 0))
        self.rect.x = self.object.x
        if not self.scored and self.object.x <= 30:
            self.scored = True
            return 1
        return 0

    def draw(self, screen:pygame.Surface) -> None:
        self.object.render(screen, 0)


def spawn_pipes(pipes: list[Pipe],pipe_sprite: Sprite,pipe_speed: int,scaling: dict[str, float]) -> list[Pipe]:

    pipe_width = pipe_sprite.width
    pipe_height = pipe_sprite.height

    gap = int(150 * scaling["universal"] * scaling["pipe"])
    gap_center = random.randint(
    int(150 * scaling["universal"] * scaling["pipe"]),
    int(400 * scaling["universal"] * scaling["pipe"]))
    top_y = gap_center - gap // 2 - pipe_height
    bottom_y = gap_center + gap // 2

    bottom_sprite = Sprite(pipe_sprite.image, 1.0)
    bottom_object = Object(
        [bottom_sprite],
        pipe_width,
        pipe_height,
        700,
        bottom_y,
        pipe_sprite.original_width,
        pipe_sprite.original_height
    )
    pipes.append(Pipe(bottom_object, pipe_speed, flip=False, scored=True))

    top_sprite = Sprite(pipe_sprite.image, 1.0)
    top_object = Object(
        [top_sprite],
        pipe_width,
        pipe_height,
        700,
        top_y,
        pipe_sprite.original_width,
        pipe_sprite.original_height
    )
    pipes.append(Pipe(top_object, pipe_speed, flip=True))

    return pipes

def main():
    pygame.init()

    scaling:dict[str,float] = {
        "universal": 1.5,
        "background": 1,
        "bird": 1,
        "pipe": 1
    }


    temp_background_sprite:Sprite = Sprite(pygame.image.load(
            resource_path("assets\\Game Objects\\background-day.png")), scaling["universal"] * scaling["background"])

    screen = pygame.display.set_mode((temp_background_sprite.image.width, temp_background_sprite.image.height))

    del temp_background_sprite

    pygame.display.set_caption('Flappy bird')

    logo = pygame.image.load(
        resource_path("assets\\Game Objects\\yellowbird-downflap.png")
    ).convert_alpha()
    pygame.display.set_icon(logo)

    running = True
    clock = pygame.time.Clock()
    delta_time = 0.1
    game = False

    background_sprite:Sprite = Sprite(
        pygame.image.load(
        resource_path("assets\\Game Objects\\background-day.png")
    ).convert_alpha(), scaling["universal"] * scaling["background"]
    )
    background_object:Object = Object([background_sprite],background_sprite.width, background_sprite.height, 0, 0)

    acceleration = 15
    velocity = 0
    space = ["up", "locked"]

    bird_frames:list[Sprite,] = []
    for frame in ["down", "mid", "up"]:
        bird_frames.append(
            Sprite(
                pygame.image.load(
                    resource_path(f"assets\\Game Objects\\yellowbird-{frame}flap.png")
                ).convert_alpha(),
                scaling["universal"] * scaling["bird"]
            )
        )

    bird_object = Object(
        bird_frames,
        bird_frames[0].image.get_width(),
        bird_frames[0].image.get_height(),
        30, 30
    )

    pipe_image = pygame.image.load(
        resource_path("assets\\Game Objects\\pipe-green.png")
    ).convert_alpha()
    pipe_sprite = Sprite(pipe_image, scaling["universal"] * scaling["pipe"])

    pipes = []
    pipe_timer = 0
    pipe_interval = 1.4 * scaling["universal"]
    pipe_speed = 145 * scaling["universal"]

    text = Text(
        pygame.font.Font(
            resource_path("assets\\UI\\m6x11plus.ttf"),
            32
        ),
        screen.get_width() - 150,
        15,
        (255, 255, 255)
    )

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

        background_object.render(screen, 0)
        

        if velocity > 75 and bird_object.y != 600:
            frame = 0
        elif 75 > velocity > -50 or bird_object.y == 600:
            frame = 1
        else:
            frame = 2

        bird_object.render(screen, frame)
        bird_rect = bird_object.frames[frame].image.get_rect(
            topleft=(30, int(bird_object.y))
        )

        if game:
            velocity = min(acceleration + velocity, 450)
            bird_object.y = round(
                max(min(bird_object.y + (velocity * delta_time), screen.get_height()), 0)
            )

            if space == ["down", "unlocked"]:
                space[1] = "locked"
                velocity = -400

            pipe_timer += delta_time
            if pipe_timer >= pipe_interval:
                pipe_timer = 0
                pipes = spawn_pipes(pipes, pipe_sprite, round(pipe_speed), scaling)

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

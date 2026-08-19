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


def spawn_pipes(pipes: list[Pipe],pipe_sprite: Sprite,pipe_speed: int,scaling: dict[str, float], x:int) -> list[Pipe]:

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
        x,
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
        x,
        top_y,
        pipe_sprite.original_width,
        pipe_sprite.original_height
    )
    pipes.append(Pipe(top_object, pipe_speed, flip=True))

    return pipes

class Game():
    def __init__(self):

        pygame.init()

        scaling:dict[str,float] = {"universal": 1, "background": 1, "base": 1, "bird": 1, "pipe": 1}


        temp_background_sprite:Sprite = Sprite(pygame.image.load(
                resource_path("assets\\Game Objects\\background-day.png")), scaling["universal"] * scaling["background"])
        screen = pygame.display.set_mode((temp_background_sprite.image.width, temp_background_sprite.image.height), pygame.RESIZABLE)
        old_screen_size = (temp_background_sprite.image.width, temp_background_sprite.image.height)
        del temp_background_sprite
        pygame.display.set_caption('Flappy bird')
        logo = pygame.image.load(
            resource_path("assets\\Game Objects\\yellowbird-downflap.png")
        ).convert_alpha()
        pygame.display.set_icon(logo)
        del logo

        background_sprite:Sprite = Sprite(
            pygame.image.load(
            resource_path("assets\\Game Objects\\background-day.png")
        ).convert_alpha(), scaling["universal"] * scaling["background"]
        )
        background_object:Object = Object([background_sprite],background_sprite.width, background_sprite.height, 0, 0)

        base_sprite:Sprite = Sprite(
                    pygame.image.load(
                    resource_path("assets\\Game Objects\\base.png")
                ).convert_alpha(), scaling["universal"] * scaling["base"]
                )
        base_object:Object = Object([base_sprite],base_sprite.width, base_sprite.height, 0, (screen.height - base_sprite.height))

        

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
            30, 100
        )

        pipe_image = pygame.image.load(
            resource_path("assets\\Game Objects\\pipe-green.png")
        ).convert_alpha()
        pipe_sprite = Sprite(pipe_image, scaling["universal"] * scaling["pipe"])

        text = Text(
            pygame.font.Font(
                resource_path("assets\\UI\\m6x11plus.ttf"),
                32
            ),
            screen.get_width() - 150,
            15,
            (255, 255, 255)
        )

        self.high_score = 0
        self.background_object = background_object
        self.base_object = base_object
        self.scaling = scaling
        self.screen = screen
        self.bird_object = bird_object
        self.pipe_sprite = pipe_sprite
        self.text = text
        self.old_screen_size = old_screen_size

    def rescale(self, new_size: tuple[int, int]):
        self.scaling["universal"] = new_size[1] / self.old_screen_size[1]

        bg_sprite = self.background_object.frames[0]
        bg_scale_y = new_size[1] / bg_sprite.original_height
        self.background_object.bulk_transform(scale=bg_scale_y)
        self.background_object.bulk_tile((new_size[0], bg_sprite.height))

        base_scale_y = self.scaling["universal"] * self.scaling["base"]
        self.base_object.bulk_transform(scale=base_scale_y)
        self.base_object.y = new_size[1] - self.base_object.height
        self.base_object.bulk_tile((new_size[0], self.base_object.height))

        bird_scale = self.scaling["universal"] * self.scaling["bird"]
        self.bird_object.bulk_transform(scale=bird_scale)

        pipe_scale = self.scaling["universal"] * self.scaling["pipe"]
        self.pipe_sprite.transform(scale=pipe_scale)

        self.text.x = new_size[0] - 150

        self.screen = pygame.display.set_mode(new_size, pygame.RESIZABLE)

        self.old_screen_size = new_size



    def run(self):
        acceleration = 10 * self.scaling["universal"]
        velocity = 0
        space = {"bar_down": False, "jump_locked": False, "can_jump": True}
        running = True
        clock = pygame.time.Clock()
        delta_time = 0.1
        playing = False
        pipes = []
        pipe_timer = 0
        pipe_interval = 1.4 * self.scaling["universal"]
        pipe_speed = 145 * self.scaling["universal"]
        score = 0
        floor_height_for_bird = self.base_object.y - self.bird_object.height

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or event.type == pygame.FINGERMOTION and space["jump_locked"] == False:
                    space["bar_down"] = True
                    space["jump_locked"] = False

                if (event.type == pygame.KEYUP and event.key == pygame.K_SPACE) or event.type == pygame.FINGERUP:
                    space["bar_down"] = False
                    space["jump_locked"] = False

                if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or event.type == pygame.FINGERDOWN:
                    playing = True

            current_size = self.screen.get_size()
            if current_size != self.old_screen_size:
                self.rescale(current_size)

            self.screen.fill("grey")

            self.background_object.render(self.screen, 0)
            

            if velocity > 75 and self.bird_object.y != 600:
                frame = 0
            elif 75 > velocity > -50 or self.bird_object.y == 600:
                frame = 1
            else:
                frame = 2

            self.bird_object.render(self.screen, frame)
            self.bird_rect = self.bird_object.frames[frame].image.get_rect(
                topleft=(30, int(self.bird_object.y))
            )

            if playing:
                velocity = min(acceleration + velocity, 450)
                self.bird_object.y = round(max(min(self.bird_object.y + (velocity * delta_time), floor_height_for_bird), 0))

                if self.bird_object.y == 0:
                    space["can_jump"] = False
                elif self.bird_object.y == floor_height_for_bird:
                    running = False

                if space["bar_down"] and not space["jump_locked"] and space["can_jump"]:
                    space["jump_locked"] = True
                    velocity = -250 * self.scaling["universal"]

                pipe_timer += delta_time
                if pipe_timer >= pipe_interval:
                    pipe_timer = 0
                    pipes = spawn_pipes(pipes, self.pipe_sprite, round(pipe_speed), self.scaling, self.screen.width)

                for pipe in pipes:
                    score += pipe.update(delta_time)
                    pipe.draw(self.screen)
                    if self.bird_rect.colliderect(pipe.rect):
                        space["can_jump"] = False
                    if pipe.object.x < 0:
                        del pipe

            self.bird_object.render(self.screen, frame)
            self.base_object.render(self.screen, 0)

            self.text.render(self.screen, f"Score: {score}\nHigh: {self.high_score}")

            pygame.display.flip()
            delta_time = clock.tick(60) / 1000
            delta_time = max(0.001, min(0.1, delta_time))


        self.bird_object.y = 100
        self.high_score = max(score, self.high_score)

if __name__ == "__main__":
    game = Game()
    while True:
        game.run()
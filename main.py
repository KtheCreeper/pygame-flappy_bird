import pygame
import random

def get_image(sheet:pygame.Surface, frame:int, width:int, height:int, scale:int, colour:tuple[int,int,int]):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), (frame * width, 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(colour)
    return image

class Pipe:
    def __init__(self, image:pygame.Surface, x:int, y:int, speed:int, flip:str):
        # Flip pipe if needed
        if flip == "down":
            self.image:pygame.Surface = pygame.transform.flip(image, False, True)
        else:
            self.image:pygame.Surface = image

        self.x:float = x
        self.y:float = y
        self.speed:float = speed
        self.rect:pygame.Rect = self.image.get_rect(topleft=(x, y))

    def update(self, dt:float):
        self.x -= self.speed * dt
        self.rect.x = int(self.x)

    def draw(self, screen:pygame.Surface):
        screen.blit(self.image, (self.x, self.y))

def spawn_pipes():
    gap:int = 150
    bottom_y:int = random.randint(200, 450)
    top_y:int = bottom_y - gap - pipe_sprite.get_height()

    # Top pipe (flipped)
    pipes.append(Pipe(pipe_sprite, 700, top_y, pipe_speed, "down"))

    # Bottom pipe (normal)
    pipes.append(Pipe(pipe_sprite, 700, bottom_y, pipe_speed, "up"))

pygame.init()
screen:pygame.Surface = pygame.display.set_mode((550,550))
running:bool = True
clock:pygame.time.Clock = pygame.time.Clock()
delta_time:float = 0.1

y:float = 30
acceleration:float = 15
velocity:float = 0
space:list[str] = ["up", "locked"]

bird_frames:list[pygame.Surface] = []
for frame in ["down","mid","up"]:
    bird_frames.append(pygame.image.load(f"assets\\Game Objects\\yellowbird-{frame}flap.png").convert_alpha())

pipe_sprite:pygame.Surface = pygame.image.load("assets\\Game Objects\\pipe-green.png").convert_alpha()

pipes:list[Pipe] = []
pipe_timer:float = 0
pipe_interval:float = 1.8
pipe_speed:int = 200

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and space[1] == "unlocked":
            space = ["down", "unlocked"]
        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            space = ["up", "unlocked"]

    screen.fill("grey")

    if velocity > 75 and y != 600:
        frame = 0
    elif 75 > velocity > -50 or y == 600:
        frame = 1
    else:
        frame = 2

    screen.blit(bird_frames[frame], (30, y))
    bird_rect:pygame.Rect = bird_frames[frame].get_rect(topleft=(30, int(y)))

    velocity = min(acceleration + velocity, 450)
    y = max(min(y + (velocity * delta_time), 550), 0)
    if space == ["down", "unlocked"]:
        space[1] = "locked"
        velocity = -400

    pipe_timer += delta_time
    if pipe_timer >= pipe_interval:
        pipe_timer = 0
        spawn_pipes()

    for pipe in pipes:
        pipe.update(delta_time)
        pipe.draw(screen)
        if bird_rect.colliderect(pipe.rect):
            print("Hit pipe!")
            running = False

    pygame.display.flip()
    delta_time = clock.tick(60) / 1000
    delta_time = max(0.001, min(0.1, delta_time))
import pygame

def get_image(sheet:pygame.Surface, frame:int, width:int, height:int, scale:int, colour:tuple[int,int,int]):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), (frame * width, 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(colour)
    return image

pygame.init()
screen:pygame.Surface = pygame.display.set_mode((640,640))
running:bool = True
clock:pygame.time.Clock = pygame.time.Clock()
delta_time:float = 0.1

y:float = 30
acceleration:float = 10
velocity:float = 0 #Speed the bird is FALLING
space:list[str] = ["up", "locked"]

birds_frames:list[pygame.Surface] = []
bird_sprites_sheet:pygame.Surface = pygame.image.load("assets\\Bird1-5 (2).png").convert()
for frame in range(3):
    birds_frames.append(get_image(bird_sprites_sheet, frame, 16, 16, 2, (0,0,0)))


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
        frame = 0 #Falling
    elif 75 > velocity > -50 or y == 600:
        frame = 2 #Flat
    else:
        frame = 1 #Rising

    screen.blit(birds_frames[frame], (30, y))

    velocity = min(acceleration + velocity, 450)
    y = max(min(y + (velocity * delta_time), 600), 0)

    if space == ["down", "unlocked"]:
        space[1] = "locked"
        velocity = -500

    pygame.display.flip()
    delta_time = clock.tick(60) / 1000
    delta_time = max(0.001, min(0.1, delta_time))
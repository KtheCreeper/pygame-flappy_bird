import pygame

def get_image(sheet, frame, width, height, scale, colour):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), (frame * width, 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(colour)
    return image

pygame.init()
screen = pygame.display.set_mode((640,640))
running = True
clock = pygame.time.Clock()
delta_time = 0.1

y = 30

birds_frames = []
bird_ss = pygame.image.load("assets\\Bird1-5 (2).png").convert()
for frame in range(4):
    birds_frames.append(get_image(bird_ss, frame, 16, 16, 2, (0,0,0)))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("grey")

    screen.blit(birds_frames[0], (30, y))
    y += 10 * delta_time

    pygame.display.flip()
    delta_time = clock.tick(60) / 1000
    delta_time = max(0.001, min(0.1, delta_time))
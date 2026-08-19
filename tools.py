import pygame

def sprite_split(sprite:Sprite, frame_width:int=1, frame_height:int=1, scale:float=1, flip_x:bool=False, flip_y:bool=False) -> list[Sprite]:
    image = sprite.image
    sheet_width, sheet_height = image.get_size()
    frames:list[Sprite] = []

    columns:int = sheet_width // frame_width
    rows:int = sheet_height // frame_height

    for y in range(rows):
        for x in range(columns):
            frame:pygame.Surface = pygame.Surface((frame_width, frame_height)).convert_alpha()
            frame.blit(image, (0, 0), (x * frame_width, y * frame_height, frame_width, frame_height))

            if scale != 1:
                frame = pygame.transform.scale(frame, (frame_width * scale, frame_height * scale))
            image = pygame.transform.flip(image, flip_x, flip_y)

            frames.append(Sprite(frame))

    return frames




class Sprite():
    def __init__(self, image:pygame.Surface,  scale:float=1):
        self.original_width, self.original_height = image.get_size()
        if scale != 1:
            image = pygame.transform.scale(image,(round(self.original_width * scale), round(self.original_height * scale)))
        self.image = image
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def transform(self, scale:float=1, flip_x:bool=False, flip_y:bool=False) -> None:
        if scale != 1:
            self.image = pygame.transform.scale(self.image,(round(self.original_width * scale), round(self.original_height * scale)))
        self.image = pygame.transform.flip(self.image, flip_x, flip_y)
        self.width, self.height = self.image.get_size()

    def tile(self, new_size: tuple[int, int]) -> None:
        new_image = pygame.Surface(new_size, pygame.SRCALPHA)
        old_width, old_height = self.image.get_size()
        for x in range(new_size[0] // old_width + 1):
            for y in range(new_size[1] // old_height + 1):
                new_image.blit(self.image, (x * old_width, y * old_height))
        self.image = new_image
        self.width, self.height = new_image.get_size()



class Object():
    def __init__(self, frames:list[Sprite], width:int, height:int, x:int, y:int, original_width:int|None=None, original_height:int|None=None):
        self.frames = frames
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.original_width = original_width if original_width is not None else width
        self.original_height = original_height if original_height is not None else height

    def bulk_transform(self, selection: str = "-1", scale: float = 1, flip_x: bool = False, flip_y: bool = False) -> None:
        if selection == "-1":
            for frame in self.frames:
                frame.transform(scale, flip_x, flip_y)
            return
        for i, char in enumerate(selection):
            if char == "1" and i < len(self.frames):
                self.frames[i].transform(scale, flip_x, flip_y)

    def bulk_tile(self, new_size: tuple[int, int], selection: str = "-1") -> None:
        if selection == "-1":
            for frame in self.frames:
                frame.tile(new_size)
            return
        for i, char in enumerate(selection):
            if char == "1" and i < len(self.frames):
                self.frames[i].tile(new_size)


    def render(self, screen:pygame.Surface, frame:int) -> None:
        screen.blit(self.frames[frame].image, (self.x, self.y))


class Text:
    def __init__(self,font:pygame.font.Font, x:int, y:int, colour:tuple[int, int, int], background_colour:tuple[int, int, int]|None=None):
        self.font = font
        self.x = x
        self.y = y
        self.colour = colour
        self.background_colour = background_colour

    def render(self, screen: pygame.Surface, text: str) -> None:
        draw_text: pygame.Surface = self.font.render(text,True,self.colour,self.background_colour)
        text_rect: pygame.Rect = draw_text.get_rect()
        text_rect.left = self.x
        text_rect.top = self.y
        screen.blit(draw_text, text_rect)


class Button():
    def __init__(self, image:pygame.Surface, x:float, y:float, text_input:str, font:pygame.Font):
        self.image = image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.text_input = text_input
        self.font = font
        self.text = font.render(self.text_input, True, "white")
        self.text_rect = self.text.get_rect(centre=(self.x, self.y))
    
    def render(self, screen:pygame.Surface) -> None:
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_for_input(self, mouse_position:list[float,]) -> bool:
        if mouse_position[0] in range(self.rect.left, self.rect.right) and mouse_position[1] in range(self.rect.top, self.rect.bottom):
            return True
        else:
            return False

    def change_text_colour(self, colour:tuple[int,int,int]) -> None:
        self.text = self.font.render(self.text_input, True, colour)
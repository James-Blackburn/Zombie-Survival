import pygame

class Button:

    """
    Arguments
    ---------
    display = pygame window
    x = button x
    y = button y
    width = buttton width
    height = button height
    text = text on button
    font = text font
    text_colour = colour of text
    colour = button colour
    """

    def __init__(self,display,x,y,width,height,text,font,text_colour,colour):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.text_colour = text_colour
        self.colour = colour
        self.display = display
        self.font = font

        pygame.draw.rect(self.display,self.colour,(self.x,self.y,
                                              self.width,
                                              self.height))

        message = self.font.render(self.text, 1, self.text_colour)
        x = self.x+(self.width/2)
        y = self.y+(self.height/2)
        text_rect = message.get_rect(center=(x, y))
        self.display.blit(message, text_rect)

    def clicked(self):
        click = pygame.mouse.get_pressed()
        if click[0] != 1:
            return False
        m_x, m_y = pygame.mouse.get_pos()
        if m_x in range(self.x,self.x+self.width):
            if m_y in range(self.y,self.y+self.height):
                return True

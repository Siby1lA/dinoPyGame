import pygame, time, sys

pygame.init()
white = (255, 255, 255)

display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("버튼 테스트")
clock = pygame.time.Clock()


def quitgame():
    pygame.quit()
    sys.exit()

class Btn:
    def __init__(self, img, x, y, w, h, img_act, x_act, y_act, action = None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + y > mouse[0] > x and y + h > mouse[1] > y:
            gameDisplay.blit(img_act, (x_act, y_act))
            if click[0] and action != None:
                time.sleep(1)
                action()
        else:
            gameDisplay.blit(img_act, (x, y))

def menu():
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            gameDisplay.fill(white)
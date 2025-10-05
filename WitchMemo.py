"""Witch Memo Game Script"""
import pygame, sys, random, socket, getpass
from button import Button
pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

computer_name = socket.gethostname()
user_name = getpass.getuser()

BG = pygame.image.load("Image/Background/menubackgroundtest.jpg")
basecolor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) #สุ่มสีเริ่มต้น
triadic_2 = [basecolor[0] + 85, basecolor[1] + 85, basecolor[2] + 85] #การทำสีที่สองของ Triadic Theory
triadic_3 = [triadic_2[0] + 85, triadic_2[1] + 85, triadic_2[2] + 85] #การทำสีที่สามของ Triadic Theory
for i in range(3): #แปลงรหัสสีตาม Triadic Theory
    if triadic_2[i] > 255:
        triadic_2[i] -= 255
    if triadic_3[i] > 255:
        triadic_3[i] -= 255

def get_font(size):
    return pygame.font.Font("Font/SansThai.ttf", size) #นำเข้าฟอนต์จากโฟลเดอร์

def play():
    pygame.display.set_caption("Play")
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill(basecolor)
        PLAY_TEXT = get_font(45).render("Hey " + user_name + ", buddy it's not time to play.", True, triadic_2)
        PLAY_RECT = PLAY_TEXT.get_rect(center = (640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image = None, pos = (640, 460), text_input = "BACK", font = get_font(75), base_color = triadic_2, hovering_color = triadic_3)
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
        pygame.display.update()
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill(basecolor)

        OPTIONS_TEXT = get_font(45).render("You thing I had made this? You fool.", True, triadic_2)
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color = triadic_2, hovering_color = triadic_3)

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, triadic_2)
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("Image/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color = triadic_3)
        OPTIONS_BUTTON = Button(image=pygame.image.load("Image/Options Rect.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color = triadic_3)
        QUIT_BUTTON = Button(image=pygame.image.load("Image/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color = triadic_3)
        
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
            pygame.mixer_music.load("Music/003. Your Best Friend.mp3")
            pygame.mixer.music.set_volume(0.25)
            pygame.mixer.music.play(-1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
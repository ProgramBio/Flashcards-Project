import pygame
import sys
import json
import os

# -------------------------
# โหลด/บันทึก flashcards จากไฟล์
# -------------------------
FILENAME = "flashcards.json"

def load_flashcards():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return [
            {"question": "Apple", "answer": "แอปเปิ้ล"},
            {"question": "Dog", "answer": "สุนัข"},
        ]

def save_flashcards(data):
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

flashcards = load_flashcards()

# -------------------------
# ตั้งค่า pygame
# -------------------------
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flashcards Game")

font_main = pygame.font.Font("Font/IBMPlexSansThai-SemiBold.ttf", 50)
font_hint = pygame.font.Font("Font/IBMPlexSansThai-SemiBold.ttf", 25)

current_index = 0
show_answer = False
adding_mode = False
input_text_q = ""
input_text_a = ""

# -------------------------
# loop หลักของเกม
# -------------------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_flashcards(flashcards)
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if adding_mode:
                # -------------------------
                # โหมดเพิ่มการ์ดใหม่
                # -------------------------
                if event.key == pygame.K_RETURN:
                    if input_text_q and input_text_a:
                        flashcards.append({"question": input_text_q, "answer": input_text_a})
                        input_text_q, input_text_a = "", ""
                        adding_mode = False
                        save_flashcards(flashcards)
                elif event.key == pygame.K_TAB:
                    # สลับระหว่างช่องคำถาม/คำตอบ
                    if input_text_a == "":
                        input_text_a = " "
                    else:
                        input_text_a = ""
                elif event.key == pygame.K_BACKSPACE:
                    if input_text_a == "":
                        input_text_q = input_text_q[:-1]
                    else:
                        input_text_a = input_text_a[:-1]
                else:
                    if input_text_a == "":
                        input_text_q += event.unicode
                    else:
                        input_text_a += event.unicode

            else:
                # -------------------------
                # โหมดเล่นปกติ
                # -------------------------
                if event.key == pygame.K_SPACE:
                    show_answer = not show_answer
                elif event.key == pygame.K_RIGHT:
                    current_index = (current_index + 1) % len(flashcards)
                    show_answer = False
                elif event.key == pygame.K_LEFT:
                    current_index = (current_index - 1) % len(flashcards)
                    show_answer = False
                elif event.key == pygame.K_a:
                    # กด A เพื่อเข้าสู่โหมดเพิ่มการ์ด
                    adding_mode = True
                    input_text_q = ""
                    input_text_a = ""

    # -------------------------
    # วาดหน้าจอ
    # -------------------------
    screen.fill((240, 240, 240))

    if adding_mode:
        text1 = font_main.render("เพิ่มการ์ดใหม่", True, (0, 0, 200))
        text2 = font_main.render(f"คำถาม: {input_text_q}", True, (0, 0, 0))
        text3 = font_main.render(f"คำตอบ: {input_text_a}", True, (0, 128, 0))
        screen.blit(text1, (50, 100))
        screen.blit(text2, (50, 200))
        screen.blit(text3, (50, 300))

        hint = font_hint.render("พิมพ์ข้อความ | TAB=เปลี่ยนช่อง | ENTER=บันทึก", True, (100, 100, 100))
        screen.blit(hint, (50, 400))

    else:
        card = flashcards[current_index]
        if show_answer:
            text_surface = font_main.render(card["answer"], True, (0, 128, 0))
        else:
            text_surface = font_main.render(card["question"], True, (0, 0, 0))
        rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text_surface, rect)

        hint = font_hint.render("SPACE=flip | ←/→=เปลี่ยนการ์ด | A=เพิ่มการ์ดใหม่", True, (100, 100, 100))
        screen.blit(hint, (20, HEIGHT - 40))

    pygame.display.flip()

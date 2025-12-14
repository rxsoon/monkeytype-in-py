import pygame
import random
import time
import json
import os

pygame.init()

# ================== WINDOW ==================
WIDTH, HEIGHT = 1000, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Monkeytype – Python Edition")
clock = pygame.time.Clock()

# ================== FONTS ==================
FONT_BIG = pygame.font.Font(None, 64)
FONT = pygame.font.Font(None, 36)
FONT_SMALL = pygame.font.Font(None, 24)

# ================== COLORS ==================
BG = (18, 18, 18)
WHITE = (220, 220, 220)
GREEN = (80, 220, 140)
RED = (240, 90, 90)
GRAY = (130, 130, 130)
YELLOW = (255, 200, 90)
ACCENT = (90, 160, 255)

# ================== WORDS ==================
# List of words used for typing test
WORDS = "the and you that was for are with his they this have from one had word but not what all were when your can said there use an each which she do how their if will up other about out many then them these so some her would make like him into time has look two more write go see number no way could people my than first water been call who oil its now find long down day did get come made may part over new sound take only little work know place year live me back give most very after thing our just name good sentence man think say great where help through much before line right too mean old any same tell boy follow came want show also around form three small set put end does another well large must big even such because turn here why ask went men read need land different home us move try kind hand picture again change off play spell air away animal house point page letter mother answer found study still learn should america world high every near add food between own below country plant last school father keep tree never start city earth eye light thought head under story saw left few while along might close something seem next hard open example begin life always those both paper together got group often run important until children side feet car mile night walk white sea began grow took river four carry state once book hear stop without second later miss idea enough eat face watch far indian real almost let above girl sometimes mountain cut young talk soon list song being leave family it's body music color stand sun questions fish area mark dog horse birds problem complete room knew since ever piece told usually didn't friends easy heard order red door sure become top ship across today during short better best however low hours black products happened whole measure remember early waves reached listen wind rock space covered fast several hold himself toward five step morning passed vowel true hundred against pattern numeral table north slowly money map farm pulled draw voice seen cold cried plan notice south sing war ground fall king town I'll unit figure certain field travel wood fire upon done english road half ten fly gave box finally wait correct oh quickly person became shown minutes strong verb stars front feel fact inches street decided contain course surface produce building ocean class note nothing rest carefully scientists inside wheels stay green known island week less machine base ago stood plane system behind ran round boat game force brought understand warm common bring explain dry though language shape deep thousands yes clear equation yet government filled heat full hot check object rule among noun power cannot able six size dark ball material special heavy fine pair circle include built matter square syllables perhaps bill felt suddenly test direction center farmers ready anything divided general energy subject europe moon region return believe dance members picked simple cells paint mind love cause rain exercise eggs train blue wish drop developed window difference distance heart sit sum summer wall forest probably legs sat main winter wide written length reason kept interest arms brother race present beautiful store job edge past sign record finished discovered wild happy beside gone sky glass million west lay weather root instruments meet third months paragraph raised represent soft teacher clothes flowers shall cross himself grammar grass ice mother plural held hair describe cook floor result burn hill safe cat century consider type law bit coast copy phrase silent tall sand soil roll temperature finger industry value fight lie beat excite natural view sense capital chair danger fruit rich thick soldier process operate practice separate difficult doctor please protect noon whose locate ring character insect caught period indicate radio spoke atom human history effect electric expect crop modern element hit student corner party supply bone rail imagine provide agree thus gentle woman captain guess necessary sharp wing create neighbor wash bat rather crowd corn compare poem string bell depend meat rub tube famous dollar stream fear sight thin triangle planet hurry chief colony clock mine tie enter major fresh search send yellow gun allow print dead spot desert suit current lift rose arrive master track parent shore division sheet substance favor connect post spend chord fat glad original share station dad bread charge proper bar offer segment slave duck instant market degree populate chick dear enemy reply drink support speech nature range steam motion path liquid log meant quotient teeth shell neck oxygen sugar death pretty skill women season solution magnet silver thank branch match suffix especially fig afraid huge sister steel discuss forward similar guide experience score apple bought led pitch coat mass card band rope slip win dream evening condition feed tool total basic smell valley nor double seat arrive middle wild rock instrument scale neighbor safety blew noon depth model ship literature clock speed method organ pay section dress cloud surprise quiet stone tiny climb cool design poor lot experiment bottom key iron single stick flat twenty skin smile crease hole jump baby eight village meet root buy raise solve metal whether push seven paragraph third".split()

# ================== GAME STATE ==================
STATE_MENU = "menu"
STATE_GAME = "game"
STATE_RESULTS = "results"
STATE_LEADERBOARD = "leaderboard"
state = STATE_MENU

# ================== SETTINGS ==================
word_count_options = [30, 60, 120]
selected_word_count = 30

color_modes = ["standard", "gradient", "rainbow", "neon"]
selected_color_mode = "standard"
rainbow_colors = [(255,0,0),(255,127,0),(255,255,0),(0,255,0),(0,0,255),(75,0,130),(139,0,255)]

TARGET_TEXT = ""
input_text = ""
start_time = None
end_time = None
finished = False

correct_typed = 0
total_typed = 0

cursor_visible = True
cursor_timer = 0
fade_alpha = 255
slide_y = HEIGHT

# ================== LEADERBOARD ==================
leaderboard_file = "leaderboard.json"
leaderboard_data = {}
if os.path.exists(leaderboard_file):
    with open(leaderboard_file, "r") as f:
        leaderboard_data = json.load(f)

# ================== FUNCTIONS ==================
def save_leaderboard(wpm, accuracy):
    """Save top 10 scores for current word count to JSON file."""
    global selected_word_count
    key = str(selected_word_count)
    if key not in leaderboard_data:
        leaderboard_data[key] = []
    leaderboard_data[key].append({"wpm": wpm, "accuracy": accuracy})
    leaderboard_data[key] = sorted(leaderboard_data[key], key=lambda x: -x["wpm"])[:10]
    with open(leaderboard_file, "w") as f:
        json.dump(leaderboard_data, f, indent=4)

def new_text():
    """Generate new typing test text based on selected word count."""
    return " ".join(random.choices(WORDS, k=selected_word_count))

def calc_wpm():
    """Calculate current words per minute."""
    if not start_time:
        return 0
    elapsed = max(time.time() - start_time, 1)
    return int((len(input_text) / 5) / (elapsed / 60))

def get_char_color(index, correct):
    """Return color of each character based on mode and correctness."""
    if not correct:
        return RED
    if selected_color_mode == "standard":
        return GREEN
    elif selected_color_mode == "gradient":
        r, g, b = 80, 220, 140
        factor = index / max(len(input_text),1)
        g_new = int(g * (1-factor) + 100 * factor)
        return (r, g_new, b)
    elif selected_color_mode == "rainbow":
        return rainbow_colors[index % len(rainbow_colors)]
    elif selected_color_mode == "neon":
        return (120, 255, 180)
    return GREEN

def draw_typing_text():
    """Draw visible lines of text with scrolling effect and cursor."""
    x_start = 50
    y_start = 200
    max_width = WIDTH - 100
    line_height = 45
    max_visible_lines = 5

    lines = []
    current_line = []
    x = x_start

    # Split text into lines
    for i, char in enumerate(TARGET_TEXT):
        correct = input_text[i] == char if i < len(input_text) else False
        color = get_char_color(i, correct)
        surf = FONT.render(char, True, color)

        if x + surf.get_width() > x_start + max_width:
            lines.append(current_line)
            current_line = []
            x = x_start
        current_line.append((surf, char, x))
        x += surf.get_width()

    if current_line:
        lines.append(current_line)

    # Determine how many lines should be visible
    char_count_lines = [sum(1 for _, _, _ in line) for line in lines]
    cumulative = []
    total = 0
    for c in char_count_lines:
        total += c
        cumulative.append(total)

    visible_lines = []
    for idx, line in enumerate(lines):
        if idx < max_visible_lines or (idx >= max_visible_lines and len(input_text) >= cumulative[idx - 1]):
            visible_lines.append(line)
    if len(visible_lines) > max_visible_lines:
        visible_lines = visible_lines[-max_visible_lines:]

    # Draw the lines
    y = y_start
    for line in visible_lines:
        for surf, _, x_pos in line:
            screen.blit(surf, (x_pos, y))
        y += line_height

    # Draw cursor
    if not finished and cursor_visible:
        if visible_lines:
            last_line = visible_lines[-1]
            if last_line:
                last_surf, _, last_x = last_line[-1]
                cursor = FONT.render("|", True, YELLOW)
                screen.blit(cursor, (last_x + last_surf.get_width(), y - line_height))

def reset_game():
    """Reset all game variables to start a new test."""
    global TARGET_TEXT, input_text, start_time, end_time, finished
    global correct_typed, total_typed, state, fade_alpha, slide_y
    TARGET_TEXT = new_text()
    input_text = ""
    start_time = None
    end_time = None
    finished = False
    correct_typed = 0
    total_typed = 0
    fade_alpha = 255
    slide_y = HEIGHT
    state = STATE_GAME

# ================== MAIN LOOP ==================
running = True
while running:
    clock.tick(60)
    screen.fill(BG)

    # Cursor blinking
    cursor_timer += 1
    if cursor_timer > 30:
        cursor_visible = not cursor_visible
        cursor_timer = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # -------- MENU --------
        if state == STATE_MENU:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset_game()
                elif event.key == pygame.K_1:
                    selected_word_count = 30
                elif event.key == pygame.K_2:
                    selected_word_count = 60
                elif event.key == pygame.K_3:
                    selected_word_count = 120
                elif event.key == pygame.K_l:
                    state = STATE_LEADERBOARD
                elif event.key == pygame.K_c:
                    idx = color_modes.index(selected_color_mode)
                    selected_color_mode = color_modes[(idx + 1) % len(color_modes)]

        # -------- GAME --------
        elif state == STATE_GAME:
            if event.type == pygame.KEYDOWN and not finished:
                if start_time is None:
                    start_time = time.time()
                if event.key == pygame.K_BACKSPACE:
                    if input_text:
                        input_text = input_text[:-1]
                else:
                    if event.unicode and len(input_text) < len(TARGET_TEXT):
                        input_text += event.unicode
                        total_typed += 1
                        idx = len(input_text) - 1
                        if idx < len(TARGET_TEXT) and event.unicode == TARGET_TEXT[idx]:
                            correct_typed += 1

                # End test
                if len(input_text) >= len(TARGET_TEXT):
                    finished = True
                    end_time = time.time()
                    state = STATE_RESULTS
                    wpm_final = calc_wpm()
                    accuracy = int((correct_typed / max(total_typed, 1)) * 100)
                    save_leaderboard(wpm_final, accuracy)

        # -------- RESULTS --------
        elif state == STATE_RESULTS:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    state = STATE_MENU

        # -------- LEADERBOARD --------
        elif state == STATE_LEADERBOARD:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    state = STATE_MENU

    # ================== DRAW ==================
    if state == STATE_MENU:
        title = FONT_BIG.render("MONKEYTYPE", True, GREEN)
        subtitle = FONT.render("Python Edition", True, GRAY)
        hint = FONT_SMALL.render("SPACE: Start | L: Leaderboard | C: Color mode", True, WHITE)
        words_select = FONT_SMALL.render(f"Word count: 1-30 2-60 3-120 (current: {selected_word_count}) | Color: {selected_color_mode}", True, WHITE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 160))
        screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, 230))
        screen.blit(hint, (WIDTH//2 - hint.get_width()//2, 300))
        screen.blit(words_select, (WIDTH//2 - words_select.get_width()//2, 340))

    elif state == STATE_GAME:
        header = FONT_BIG.render("Typing Test", True, GREEN)
        screen.blit(header, (WIDTH//2 - header.get_width()//2, 40))
        draw_typing_text()
        wpm_text = FONT_SMALL.render(f"WPM: {calc_wpm()}", True, GRAY)
        screen.blit(wpm_text, (50, 420))

    elif state == STATE_RESULTS:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(fade_alpha)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        fade_alpha = max(0, fade_alpha - 8)

        slide_y = max(120, slide_y - 12)
        panel = pygame.Rect(300, slide_y, 400, 260)
        pygame.draw.rect(screen, (30, 30, 30), panel, border_radius=16)
        pygame.draw.rect(screen, ACCENT, panel, 2, border_radius=16)

        elapsed = max(end_time - start_time, 1)
        wpm_final = int((len(TARGET_TEXT) / 5) / (elapsed / 60))
        accuracy = int((correct_typed / max(total_typed, 1)) * 100)

        t1 = FONT.render("RESULTS", True, ACCENT)
        t2 = FONT_SMALL.render(f"WPM: {wpm_final}", True, WHITE)
        t3 = FONT_SMALL.render(f"Accuracy: {accuracy}%", True, WHITE)
        t4 = FONT_SMALL.render("Press R to return to menu", True, GRAY)

        screen.blit(t1, (WIDTH//2 - t1.get_width()//2, slide_y + 20))
        screen.blit(t2, (340, slide_y + 90))
        screen.blit(t3, (340, slide_y + 130))
        screen.blit(t4, (WIDTH//2 - t4.get_width()//2, slide_y + 200))

    elif state == STATE_LEADERBOARD:
        title = FONT_BIG.render("LEADERBOARD", True, ACCENT)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
        key = str(selected_word_count)
        if key in leaderboard_data:
            for idx, entry in enumerate(leaderboard_data[key]):
                text = FONT_SMALL.render(f"{idx+1}. WPM: {entry['wpm']} | Accuracy: {entry['accuracy']}%", True, WHITE)
                screen.blit(text, (WIDTH//2 - text.get_width()//2, 150 + idx*35))
        else:
            text = FONT_SMALL.render("No records yet", True, WHITE)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, 200))

        back_text = FONT_SMALL.render("Press R to return to menu", True, GRAY)
        screen.blit(back_text, (WIDTH//2 - back_text.get_width()//2, HEIGHT - 60))

    pygame.display.flip()

pygame.quit()

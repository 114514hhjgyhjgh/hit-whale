import pygame
import sys
import random
import os
from pygame.locals import *

# 初始化pygame
pygame.init()
pygame.mixer.init()

# 游戏窗口设置 - 改为1920x1080
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Whack-a-Mole Game')

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (100, 100, 255)
GRAY = (200, 200, 200)

# 游戏参数
FPS = 60
clock = pygame.time.Clock()
score = 0
game_time = 60  # 计时模式的时间（秒）
time_left = game_time

# 使用英文字体，增大字体大小以适应高分辨率
font = pygame.font.SysFont('arial', 48)  # 增大字体
title_font = pygame.font.SysFont('arial', 72, bold=True)  # 增大标题字体
button_font = pygame.font.SysFont('arial', 42)  # 增大按钮字体

# 地鼠洞的位置 - 调整为适应1920x1080分辨率（4x4网格）
holes = [
    # 第一行
    (300, 200), (600, 200), (900, 200), (1200, 200),
    # 第二行
    (300, 400), (600, 400), (900, 400), (1200, 400),
    # 第三行
    (300, 600), (600, 600), (900, 600), (1200, 600),
    # 第四行
    (300, 800), (600, 800), (900, 800), (1200, 800)
]

# 图片尺寸调整
MOLE_SIZE = 150  # 增大地鼠尺寸
HOLE_SIZE_WIDTH = 180  # 增大地洞宽度
HOLE_SIZE_HEIGHT = 120  # 增大地洞高度
HAMMER_SIZE = 120  # 增大锤子尺寸

# 加载资源
def load_resources():
    resources = {}
    
    # 设置图片文件夹路径
    image_folder = 'mm'
    
    # 加载普通地鼠图片
    try:
        mole_normal_path = os.path.join(image_folder, 'mole_normal.png')
        resources['mole_normal'] = pygame.image.load(mole_normal_path).convert_alpha()
        resources['mole_normal'] = pygame.transform.scale(resources['mole_normal'], (MOLE_SIZE, MOLE_SIZE))
    except:
        print(f"Cannot load mole image: {mole_normal_path}")
        resources['mole_normal'] = pygame.Surface((MOLE_SIZE, MOLE_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(resources['mole_normal'], (150, 75, 0), (MOLE_SIZE//2, MOLE_SIZE//2), MOLE_SIZE//2 - 5)
        pygame.draw.circle(resources['mole_normal'], (200, 150, 100), (MOLE_SIZE//2, MOLE_SIZE//3), MOLE_SIZE//5)
        pygame.draw.circle(resources['mole_normal'], BLACK, (MOLE_SIZE//2 - 10, MOLE_SIZE//3 - 5), 8)
        pygame.draw.circle(resources['mole_normal'], BLACK, (MOLE_SIZE//2 + 10, MOLE_SIZE//3 - 5), 8)
        pygame.draw.ellipse(resources['mole_normal'], (200, 0, 0), 
                           (MOLE_SIZE//2 - 25, MOLE_SIZE//2 - 10, 50, 20))
    
    # 加载被击中的地鼠图片
    try:
        mole_hit_path = os.path.join(image_folder, 'mole_hit.png')
        resources['mole_hit'] = pygame.image.load(mole_hit_path).convert_alpha()
        resources['mole_hit'] = pygame.transform.scale(resources['mole_hit'], (MOLE_SIZE, MOLE_SIZE))
    except:
        print(f"Cannot load hit mole image: {mole_hit_path}")
        resources['mole_hit'] = pygame.Surface((MOLE_SIZE, MOLE_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(resources['mole_hit'], (200, 0, 0), (MOLE_SIZE//2, MOLE_SIZE//2), MOLE_SIZE//2 - 5)
        pygame.draw.circle(resources['mole_hit'], (255, 200, 200), (MOLE_SIZE//2, MOLE_SIZE//3), MOLE_SIZE//5)
        pygame.draw.circle(resources['mole_hit'], BLACK, (MOLE_SIZE//2 - 10, MOLE_SIZE//3 - 5), 8)
        pygame.draw.circle(resources['mole_hit'], BLACK, (MOLE_SIZE//2 + 10, MOLE_SIZE//3 - 5), 8)
        pygame.draw.ellipse(resources['mole_hit'], (100, 0, 0), 
                           (MOLE_SIZE//2 - 25, MOLE_SIZE//2 - 10, 50, 20))
        pygame.draw.line(resources['mole_hit'], WHITE, 
                        (MOLE_SIZE//3, MOLE_SIZE//3), 
                        (2*MOLE_SIZE//3, 2*MOLE_SIZE//3), 5)
        pygame.draw.line(resources['mole_hit'], WHITE, 
                        (2*MOLE_SIZE//3, MOLE_SIZE//3), 
                        (MOLE_SIZE//3, 2*MOLE_SIZE//3), 5)
    
    # 加载地洞图片
    try:
        hole_path = os.path.join(image_folder, 'hole.png')
        resources['hole'] = pygame.image.load(hole_path).convert_alpha()
        resources['hole'] = pygame.transform.scale(resources['hole'], (HOLE_SIZE_WIDTH, HOLE_SIZE_HEIGHT))
    except:
        print(f"Cannot load hole image: {hole_path}")
        resources['hole'] = pygame.Surface((HOLE_SIZE_WIDTH, HOLE_SIZE_HEIGHT), pygame.SRCALPHA)
        pygame.draw.ellipse(resources['hole'], BROWN, (0, 0, HOLE_SIZE_WIDTH, HOLE_SIZE_HEIGHT))
        pygame.draw.ellipse(resources['hole'], BLACK, (10, 10, HOLE_SIZE_WIDTH-20, HOLE_SIZE_HEIGHT-20))
    
    # 加载锤子图片
    try:
        hammer_path = os.path.join(image_folder, 'hammer.png')
        resources['hammer'] = pygame.image.load(hammer_path).convert_alpha()
        resources['hammer'] = pygame.transform.scale(resources['hammer'], (HAMMER_SIZE, HAMMER_SIZE))
        resources['hammer_down'] = pygame.transform.rotate(resources['hammer'], 45)
    except:
        print(f"Cannot load hammer image: {hammer_path}")
        resources['hammer'] = pygame.Surface((HAMMER_SIZE, HAMMER_SIZE), pygame.SRCALPHA)
        # 锤子手柄
        pygame.draw.rect(resources['hammer'], (150, 75, 0), 
                        (HAMMER_SIZE//2 - 8, 15, 16, HAMMER_SIZE//2))
        # 锤头
        pygame.draw.rect(resources['hammer'], (100, 100, 100), 
                        (HAMMER_SIZE//4, 10, HAMMER_SIZE//2, 25))
        
        resources['hammer_down'] = pygame.Surface((HAMMER_SIZE, HAMMER_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(resources['hammer_down'], (150, 75, 0), 
                        (HAMMER_SIZE//2 - 8, 15, 16, HAMMER_SIZE//2))
        pygame.draw.rect(resources['hammer_down'], (100, 100, 100), 
                        (HAMMER_SIZE//4, 10, HAMMER_SIZE//2, 25))
        resources['hammer_down'] = pygame.transform.rotate(resources['hammer_down'], 45)
    
    # 加载背景图片
    try:
        background_path = os.path.join(image_folder, 'background.jpg')
        resources['background'] = pygame.image.load(background_path).convert()
        resources['background'] = pygame.transform.scale(resources['background'], (WINDOW_WIDTH, WINDOW_HEIGHT))
    except:
        print(f"Cannot load background image: {background_path}")
        resources['background'] = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        resources['background'].fill(GREEN)
        # 添加草地纹理
        for i in range(0, WINDOW_WIDTH, 30):
            for j in range(0, WINDOW_HEIGHT, 30):
                pygame.draw.line(resources['background'], (0, 100, 0), 
                                (i, j), (i, j+15), 3)
    
    # 加载音效
    try:
        resources['hit_sound'] = pygame.mixer.Sound('hit.wav')
    except:
        print("Cannot load hit sound")
        resources['hit_sound'] = None
    
    # 加载背景音乐
    try:
        pygame.mixer.music.load('background_music.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    except:
        print("Cannot load background music")
    
    return resources

# 按钮类
class Button:
    def __init__(self, x, y, width, height, text, color=LIGHT_BLUE, hover_color=BLUE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.is_hovered = False
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.current_color, self.rect, border_radius=20)
        pygame.draw.rect(surface, BLACK, self.rect, 4, border_radius=20)
        
        text_surface = button_font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        self.current_color = self.hover_color if self.is_hovered else self.color
        return self.is_hovered
        
    def is_clicked(self, pos, click):
        return self.rect.collidepoint(pos) and click

# 锤子类
class Hammer:
    def __init__(self, hammer_img, hammer_down_img):
        self.normal_image = hammer_img
        self.down_image = hammer_down_img
        self.current_image = hammer_img
        self.position = (0, 0)
        self.is_swinging = False
        self.swing_start_time = 0
        self.swing_duration = 200
    
    def update_position(self, pos):
        self.position = pos
    
    def swing(self):
        self.is_swinging = True
        self.swing_start_time = pygame.time.get_ticks()
        self.current_image = self.down_image
    
    def update(self):
        if self.is_swinging:
            current_time = pygame.time.get_ticks()
            if current_time - self.swing_start_time > self.swing_duration:
                self.is_swinging = False
                self.current_image = self.normal_image
    
    def draw(self, surface):
        hammer_rect = self.current_image.get_rect(center=self.position)
        surface.blit(self.current_image, hammer_rect)

# 地鼠类
class Mole:
    def __init__(self, hole_pos):
        self.hole_pos = hole_pos
        self.is_visible = False
        self.is_hit = False
        self.visible_time = 0
        self.hit_time = 0
        self.max_visible_time = 1500
        self.hit_display_time = 300
        
    def show(self):
        self.is_visible = True
        self.is_hit = False
        self.visible_time = pygame.time.get_ticks()
        
    def hide(self):
        self.is_visible = False
        self.is_hit = False
        
    def hit(self):
        if self.is_visible and not self.is_hit:
            self.is_hit = True
            self.hit_time = pygame.time.get_ticks()
            return True
        return False
            
    def update(self):
        current_time = pygame.time.get_ticks()
        
        if self.is_hit:
            if current_time - self.hit_time > self.hit_display_time:
                self.hide()
        elif self.is_visible:
            if current_time - self.visible_time > self.max_visible_time:
                self.hide()
                
    def draw(self, surface, mole_normal_img, mole_hit_img, hole_img):
        hole_rect = hole_img.get_rect(center=self.hole_pos)
        surface.blit(hole_img, hole_rect)
        
        if self.is_visible:
            if self.is_hit:
                mole_rect = mole_hit_img.get_rect(center=self.hole_pos)
                surface.blit(mole_hit_img, mole_rect)
            else:
                mole_rect = mole_normal_img.get_rect(center=self.hole_pos)
                surface.blit(mole_normal_img, mole_rect)
            
    def check_hit(self, pos):
        if not self.is_visible or self.is_hit:
            return False
            
        distance = ((pos[0] - self.hole_pos[0]) ** 2 + (pos[1] - self.hole_pos[1]) ** 2) ** 0.5
        return distance < MOLE_SIZE//2  # 根据新的地鼠尺寸调整碰撞检测

# 显示模式选择窗口
def show_mode_selection():
    # 增大按钮尺寸以适应高分辨率
    button_width = 400
    button_height = 80
    free_mode_button = Button(WINDOW_WIDTH//2 - button_width//2, 400, button_width, button_height, "Free Mode")
    time_mode_button = Button(WINDOW_WIDTH//2 - button_width//2, 550, button_width, button_height, "Time Mode")
    quit_button = Button(WINDOW_WIDTH//2 - button_width//2, 700, button_width, button_height, "Quit Game", RED, (255, 100, 100))
    
    selected_mode = None
    
    while selected_mode is None:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_click = True
        
        free_mode_button.check_hover(mouse_pos)
        time_mode_button.check_hover(mouse_pos)
        quit_button.check_hover(mouse_pos)
        
        if free_mode_button.is_clicked(mouse_pos, mouse_click):
            selected_mode = "free"
        elif time_mode_button.is_clicked(mouse_pos, mouse_click):
            selected_mode = "time"
        elif quit_button.is_clicked(mouse_pos, mouse_click):
            pygame.quit()
            sys.exit()
        
        # 绘制模式选择界面
        window.fill(GREEN)
        
        title_text = title_font.render("Whack-a-Mole Game", True, WHITE)
        subtitle_text = font.render("Select Game Mode", True, WHITE)
        
        window.blit(title_text, (WINDOW_WIDTH//2 - title_text.get_width()//2, 200))
        window.blit(subtitle_text, (WINDOW_WIDTH//2 - subtitle_text.get_width()//2, 300))
        
        free_mode_button.draw(window)
        time_mode_button.draw(window)
        quit_button.draw(window)
        
        free_desc = font.render("Free Mode: No time limit, play as long as you want", True, WHITE)
        time_desc = font.render("Time Mode: 60 seconds challenge, get the highest score", True, WHITE)
        
        window.blit(free_desc, (WINDOW_WIDTH//2 - free_desc.get_width()//2, 480))
        window.blit(time_desc, (WINDOW_WIDTH//2 - time_desc.get_width()//2, 630))
        
        pygame.display.update()
        clock.tick(FPS)
    
    return selected_mode

# 显示游戏结束画面
def show_game_over(mode, final_score):
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    window.blit(overlay, (0, 0))
    
    game_over_text = title_font.render("Game Over!", True, WHITE)
    
    if mode == "time":
        score_text = font.render(f"Final Score: {final_score}", True, WHITE)
    else:
        score_text = font.render(f"Total Hits: {final_score}", True, WHITE)
    
    restart_text = font.render("Press R to return to Menu, ESC to Quit", True, WHITE)
    
    window.blit(game_over_text, (WINDOW_WIDTH//2 - game_over_text.get_width()//2, 300))
    window.blit(score_text, (WINDOW_WIDTH//2 - score_text.get_width()//2, 450))
    window.blit(restart_text, (WINDOW_WIDTH//2 - restart_text.get_width()//2, 550))
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_r:
                    return "menu"
                elif event.key == K_ESCAPE:
                    return "quit"
        clock.tick(FPS)
    
    return "quit"

# 游戏主循环
def game_loop(mode):
    global score, time_left
    
    resources = load_resources()
    moles = [Mole(hole) for hole in holes]
    hammer = Hammer(resources['hammer'], resources['hammer_down'])
    last_mole_time = pygame.time.get_ticks()
    mole_interval = 800
    start_time = pygame.time.get_ticks()
    
    pygame.mouse.set_visible(False)
    
    running = True
    game_active = True
    
    while running:
        current_time = pygame.time.get_ticks()
        
        # 只在计时模式下进行时间计算
        if game_active and mode == "time":
            time_left = game_time - (current_time - start_time) // 1000
            if time_left <= 0:
                time_left = 0
                game_active = False
        
        mouse_pos = pygame.mouse.get_pos()
        hammer.update_position(mouse_pos)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                return "quit"
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and game_active:
                    hammer.swing()
                    for mole in moles:
                        if mole.check_hit(event.pos):
                            if mole.hit():
                                score += 1
                                if resources['hit_sound']:
                                    resources['hit_sound'].play()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return "menu"
        
        if game_active:
            if current_time - last_mole_time > mole_interval:
                last_mole_time = current_time
                num_moles = random.randint(1, 4)  # 增加同时出现的地鼠数量
                available_moles = [m for m in moles if not m.is_visible]
                if available_moles:
                    moles_to_show = min(num_moles, len(available_moles))
                    for _ in range(moles_to_show):
                        mole = random.choice(available_moles)
                        mole.show()
                        available_moles.remove(mole)
            
            for mole in moles:
                mole.update()
        
        hammer.update()
        
        window.blit(resources['background'], (0, 0))
        
        for mole in moles:
            mole.draw(window, resources['mole_normal'], resources['mole_hit'], resources['hole'])
        
        hammer.draw(window)
        
        # 调整UI位置
        score_text = font.render(f'Score: {score}', True, WHITE)
        window.blit(score_text, (50, 50))
        
        if mode == "time":
            time_text = font.render(f'Time: {time_left}s', True, WHITE)
            window.blit(time_text, (WINDOW_WIDTH - 250, 50))
        else:
            mode_text = font.render('Free Mode - Press ESC for Menu', True, WHITE)
            window.blit(mode_text, (WINDOW_WIDTH - 500, 50))
        
        if not game_active and mode == "time":
            pygame.mouse.set_visible(True)
            result = show_game_over(mode, score)
            return result
        
        pygame.display.update()
        clock.tick(FPS)

# 主程序
def main():
    global score, time_left
    
    while True:
        selected_mode = show_mode_selection()
        
        if selected_mode == "quit":
            break
        
        score = 0
        time_left = game_time
        
        result = game_loop(selected_mode)
        
        if result == "quit":
            break
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
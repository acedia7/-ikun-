import subprocess
import pygame
import random
import math
import os
x = 100
y = 100
os.environ['SDL_VIDEO_WINDOW_POS'] = f'{x},{y}'
import pgzrun

# 定义游戏相关属性  # ai
TITLE = '坤了个坤'
WIDTH = 600
HEIGHT = 720

# 自定义游戏常量 # ai
T_WIDTH = 60
T_HEIGHT = 66

# 下方牌堆的位置
DOCK = Rect((90, 564), (T_WIDTH * 7, T_HEIGHT))

# 上方的所有牌
tiles = []
# 牌堆里的牌
docks = []

# 当前关卡状态
is_start_screen = True# 是否在开始界面
current_level = 1
max_levels = 3  # 最高关卡数

time_left = 60  # 每个关卡的时间限制，初始为60秒   # ai
game_over = False  # 游戏失败标志
game_complete = False
# 暂停标志
is_paused = False  # 游戏是否暂停
is_timer_paused = False  # 倒计时是否暂停

# 图标的位置和图标对象  # ai
icon_pos = (500, 50)
icon = Actor('ad', icon_pos)

# ai
start_button_rect = Rect((WIDTH // 2 - 100, HEIGHT // 2), (200, 50))
# 重新开始按钮的坐标和尺寸
restart_button_rect = Rect((WIDTH // 2 - 100, HEIGHT // 2 + 100), (200, 50))

# 关卡生成函数
def generate_level(level):
    global tiles, docks, time_left, game_over, is_paused, is_timer_paused
    global is_start_screen
    global current_level
    global max_levels
    global game_complete

    # 先停止之前的定时器
    clock.unschedule(update_timer)

    tiles = []
    docks = []
    game_over = False  # 每次进入新关卡时，重置游戏失败状态
    is_paused = False
    is_timer_paused = False

    if level == 3:
        time_left = 60 * 4  # 每个关卡 60 秒的时间限制
        ts = list(range(1, 13)) * 12
        random.shuffle(ts)
        n = 0
        for k in range(7):
            for i in range(7 - k):
                for j in range(7 - k):
                    t = ts[n]
                    n += 1
                    tile = Actor(f'tile{t}')
                    tile.pos = 120 + (k * 0.5 + j) * tile.width, 100 + (k * 0.5 + i) * tile.height * 0.9
                    tile.tag = t
                    tile.layer = k
                    tile.status = 1 if k == 6 else 0
                    tiles.append(tile)
        for i in range(4):
            t = ts[n]
            n += 1
            tile = Actor(f'tile{t}')
            tile.pos = 210 + i * tile.width, 516
            tile.tag = t
            tile.layer = 0
            tile.status = 1
            tiles.append(tile)
    elif level == 2:
        time_left = 60 * 2
        ts = list(range(1, 8)) * 9
        random.shuffle(ts)
        n = 0
        for k in range(5):
            for i in range(5 - k):
                for j in range(5 - k):
                    t = ts[n]
                    n += 1
                    tile = Actor(f'tile{t}')
                    tile.pos = 180 + (k * 0.5 + j) * tile.width, 140 + (k * 0.5 + i) * tile.height * 0.9
                    tile.tag = t
                    tile.layer = k
                    tile.status = 1 if k == 4 else 0
                    tiles.append(tile)
        for i in range(8):
            t = ts[n]
            n += 1
            tile = Actor(f'tile{t}')
            tile.pos = 100 + i * tile.width, 516
            tile.tag = t
            tile.layer = 0
            tile.status = 1
            tiles.append(tile)
    elif level == 1:
        time_left = 60 * 1
        ts = list(range(1, 4)) * 3
        random.shuffle(ts)
        n = 0
        for i in range(3):
            for j in range(3):
                t = ts[n]
                n += 1
                tile = Actor(f'tile{t}')
                tile.pos = 200 + (1 * 0.5 + j) * tile.width, 180 + (1 * 0.5 + i) * tile.height * 0.9
                tile.tag = t
                tile.layer = 1
                tile.status = 1
                tiles.append(tile)

    # 开始倒计时
    clock.schedule_interval(update_timer, 1)  # 每1秒调用一次 update_timer 函数

# 游戏帧绘制函数
# 修改 draw 函数，增加通关显示
def draw():  # ai
    screen.clear()
    screen.blit('back', (0, 0))
    global game_over

    if is_start_screen:
        # 绘制开始界面
        screen.draw.text("ikun", (WIDTH // 2 - 70, HEIGHT // 2 - 100), fontsize=100, color="red")
        screen.draw.filled_rect(start_button_rect, 'red')
        screen.draw.text("Start Game", center=start_button_rect.center, fontsize=40, color="white")
    elif game_complete:
        # 绘制游戏通关界面
        screen.draw.filled_rect(Rect((WIDTH // 2 - 150, HEIGHT // 2 - 50), (300, 100)), 'green')
        screen.draw.text("You Win!You are the real IKUN", (WIDTH // 2 - 230, HEIGHT // 2 - 30), fontsize=40, color="red")
    else:
        # 绘制正常游戏界面
        for tile in tiles:
            tile.draw()
            if tile.status == 0:
                screen.blit('mask', tile.topleft)
        for i, tile in enumerate(docks):
            tile.left = (DOCK.x + i * T_WIDTH)
            tile.top = DOCK.y
            tile.draw()

        # 绘制图标
        icon.draw()

        # 显示当前关卡
        screen.draw.text(f"Level: {current_level}", (20, 20), fontsize=40, color="black")
        screen.draw.text(f"Time Left: {time_left}s", (400, 20), fontsize=40, color="black")

        # 显示暂停提示
        if is_paused:
            screen.draw.text("stop game.", (WIDTH // 2 - 200, HEIGHT // 2-100), fontsize=50, color="red")
            screen.draw.text("Please watch the media.", (WIDTH // 2 - 200, HEIGHT // 2), fontsize=50, color="red")
            screen.draw.text("waiting for kunkun....30 seconds", (WIDTH // 2 - 250, HEIGHT // 2+100), fontsize=50, color="red")

        # 超过7张，失败
        if len(docks) >= 7 and not is_paused:
            screen.blit('end', (0, 0))
            game_over = True
        # 没有剩牌，胜利
        if len(tiles) == 0 and not is_paused:
            screen.blit('win', (0, 0))
            next_level()  # 通关后进入下一关

        if game_over:
            screen.draw.text(" You Lose!", (WIDTH // 2 - 100, HEIGHT // 2), fontsize=50, color="red")
            screen.draw.filled_rect(restart_button_rect, 'gray')
            screen.draw.text("Restart", center=restart_button_rect.center, fontsize=40, color="white")


# 倒计时函数
def update_timer():  # ai
    global time_left, game_over
    if time_left > 0:
        time_left -= 1
    elif time_left <= 0 and not game_over:
        game_over = True
        clock.unschedule(update_timer)  # 停止计时

# 鼠标点击响应
def on_mouse_down(pos):   # ai
    global docks, is_paused
    global is_start_screen
    global current_level
    if is_start_screen and start_button_rect.collidepoint(pos):
        # 点击开始按钮后进入第1关
        is_start_screen = False
        generate_level(1)
        return

    if game_over and restart_button_rect.collidepoint(pos):
        current_level = 1
        restart_current_level(current_level)  # 点击重新开始按钮时，从level 1重新开始
        return
    if is_paused or game_over:  # 如果游戏暂停或失败，不响应输入
        return

    # 检查是否点击了图标
    if icon.collidepoint(pos):
        play_video()  # 点击图标后播放视频并暂停
        return

    if len(docks) >= 7 or len(tiles) == 0:
        return
    for tile in reversed(tiles):
        if tile.status == 1 and tile.collidepoint(pos):
            tile.status = 2
            tiles.remove(tile)
            diff = [t for t in docks if t.tag != tile.tag]
            if len(docks) - len(diff) < 2:
                docks.append(tile)
            else:
                docks = diff
            for down in tiles:
                if down.layer == tile.layer - 1 and down.colliderect(tile):
                    for up in tiles:
                        if up.layer == down.layer + 1 and up.colliderect(down):
                            break
                    else:
                        down.status = 1
            return

# 重新开始当前关卡
def restart_current_level(current_level):
    print(f"重新开始关卡 {current_level}")
    tiles.clear()
    docks.clear()  # 清空选中的牌
    global time_left
    if current_level == 1:
        time_left = 60
    elif current_level == 2:
        time_left = 120
    elif current_level == 3:
        time_left = 60*4
    generate_level(current_level)  # 重新生成当前关卡

# 播放视频并暂停游戏
def play_video():  # ai
    global is_paused

    print("播放视频 15 秒...")
    video_path = os.path.abspath("./images/kun1.mp4")  # 获取视频文件的绝对路径
    os.startfile(video_path)  # 使用系统默认应用播放视频

    # 暂停游戏和倒计时
    pygame.mixer.music.pause()  # 暂停背景音乐
    is_paused = True
    clock.unschedule(update_timer)  # 停止倒计时
    clock.schedule_unique(resume_game, 30)  # 30 秒后恢复游戏

# 恢复游戏
def resume_game(): # ai
    global is_paused
    print("恢复游戏")
    pygame.mixer.music.unpause()  # 恢复背景音乐
    is_paused = False
    clock.schedule_interval(update_timer, 1)  # 恢复倒计时
    restart_current_level(current_level)

# 进入下一关卡
def next_level():  # ai
    global current_level, game_complete
    if current_level < max_levels:
        current_level += 1
        generate_level(current_level)
    else:
        # 设置游戏已通关标志
        game_complete = True
        print("已通关所有关卡！")
        clock.unschedule(update_timer)  # 停止倒计时


# 生成初始关卡
generate_level(1)
music.play('bgm')

pgzrun.go()

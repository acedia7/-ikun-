#logic.py
'''
考虑到pygame-zero框架的特殊性使得测试案例不好写，所以这里简单的封装了游戏的部分基本逻辑用于测试
'''
# ai
def generate_level_logic(level):
    """仅处理关卡生成的逻辑层面，不涉及图形"""
    if level == 1:
        return 9, 60  # 关卡1应有9个 tiles，60秒倒计时
    elif level == 2:
        return 45, 120  # 关卡2应有45个 tiles，120秒倒计时
    elif level == 3:
        return 100, 240  # 关卡3应有100个 tiles，240秒倒计时
    return 0, 0  # 默认情况

def restart_level_logic(level):
    """根据关卡设置初始时间"""
    if level == 1:
        return 60
    elif level == 2:
        return 120
    elif level == 3:
        return 240
    return 0

def update_timer_logic(time_left):
    """倒计时逻辑，时间为0时游戏结束"""
    if time_left > 0:
        return time_left - 1, False  # 倒计时未结束
    else:
        return 0, True  # 倒计时结束，游戏结束


def next_level_logic(current_level, max_levels=3):
    """处理进入下一关的逻辑"""
    if current_level < max_levels:
        return current_level + 1, False  # 进入下一关
    else:
        return current_level, True  # 游戏通关

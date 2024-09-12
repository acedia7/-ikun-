# logic test
'''
改代码仅对游戏简单逻辑进行测试
'''

import unittest
from logic import generate_level_logic, restart_level_logic, update_timer_logic, next_level_logic

class TestGameLogic(unittest.TestCase):

    def test_generate_level_logic(self):
        """测试生成关卡的逻辑"""
        tiles, time_left = generate_level_logic(1)
        self.assertEqual(tiles, 9)  # 关卡1应生成9个 tiles
        self.assertEqual(time_left, 60)  # 关卡1倒计时时间为60秒

        tiles, time_left = generate_level_logic(2)
        self.assertEqual(tiles, 45)
        self.assertEqual(time_left, 120)

        tiles, time_left = generate_level_logic(3)
        self.assertEqual(tiles, 100)
        self.assertEqual(time_left, 240)

    def test_restart_level_logic(self):
        """测试关卡重启逻辑"""
        time_left = restart_level_logic(1)
        self.assertEqual(time_left, 60)

        time_left = restart_level_logic(2)
        self.assertEqual(time_left, 120)

        time_left = restart_level_logic(3)
        self.assertEqual(time_left, 240)

    def test_update_timer_logic(self):
        """测试计时器逻辑"""
        time_left, game_over = update_timer_logic(10)
        self.assertEqual(time_left, 9)
        self.assertFalse(game_over)

        time_left, game_over = update_timer_logic(1)
        self.assertEqual(time_left, 0)
        self.assertTrue(game_over)  # 当时间为0时，游戏应该结束

    def test_next_level_logic(self):
        """测试进入下一关逻辑"""
        current_level, game_complete = next_level_logic(1)
        self.assertEqual(current_level, 2)
        self.assertFalse(game_complete)

        current_level, game_complete = next_level_logic(2)
        self.assertEqual(current_level, 3)
        self.assertFalse(game_complete)

        current_level, game_complete = next_level_logic(3)
        self.assertEqual(current_level, 3)
        self.assertTrue(game_complete)  # 关卡达到最大值时，应该完成游戏




if __name__ == '__main__':
    unittest.main()

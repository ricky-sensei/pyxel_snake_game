import pyxel
import random
screen_width = 160
screen_height = 160
position_list = []
for i in range(10):
    for j in range(10):
        position_list.append([i, j])  

class App:
    def __init__(self):
        self.init_game()
        pyxel.init(screen_width, screen_height)
        pyxel.load("my_resource.pyxres")
        pyxel.run(self.update, self.draw)

    def init_game(self):
        self.game_over = False
        self.head_direction = 90
        # １から１０までのグリッド
        self.snake_dx = 0
        self.snake_dy = 0
        self.snake_position = [[self.snake_dx, self.snake_dy]]  
        self.previous_snake = []
        self.item_position = [[5, 5], [8, 6], [2, 7]]  

    def update_snake(self):
        if self.head_direction == 90:
            self.snake_dx += 1
        elif self.head_direction == 180:
            self.snake_dy += 1
        elif self.head_direction == 270:
            self.snake_dx -= 1
        elif self.head_direction == 0:
            self.snake_dy -= 1

        # 移動先がsnake_positionにあるか、もしくは画面外に行ったときはゲームオーバー
        if [self.snake_dx, self.snake_dy] in self.snake_position or not 0 <= self.snake_dx <= 9 or not 0 <= self.snake_dy <= 9:
            self.game_over = True
        self.previous_snake = self.snake_position
        if [self.snake_dx, self.snake_dy] in self.item_position:
            self.item_position.append(random.choice([pos for pos in position_list if pos not in self.item_position and pos not in self.snake_position]))
            self.item_position.remove([self.snake_dx, self.snake_dy])
            self.snake_position = [[self.snake_dx, self.snake_dy]] + self.snake_position
        else:
            self.snake_position = [[self.snake_dx, self.snake_dy]] + self.snake_position[:-1]

    def update(self):
        if self.game_over and pyxel.btnp(pyxel.KEY_SPACE):
            self.init_game()
            return
        else:
            # 頭の向きを変更
            if pyxel.btnp(pyxel.KEY_RIGHT):
                self.head_direction = 90
            elif pyxel.btnp(pyxel.KEY_DOWN):
                self.head_direction = 180
            elif pyxel.btnp(pyxel.KEY_LEFT):
                self.head_direction = 270
            elif pyxel.btnp(pyxel.KEY_UP):
                self.head_direction = 0
            if pyxel.frame_count % 10 == 0:
                self.update_snake()

    def draw(self):
        pyxel.cls(0)
        self.draw_grid()
        if self.game_over:
            pyxel.text(0, 0, "GAME OVER", 7)
            pyxel.text(0, 10, "PRESS SPACE TO CONTINUE", 7)
        else:
            pyxel.blt(self.snake_dx * 16, self.snake_dy * 16, 0, 0, 0, 16, 16, 0, rotate=self.head_direction)
            for body in self.snake_position[1:]:
                pyxel.blt(body[0]*16, body[1]*16, 0, 16, 0, 16, 16, 0)
            for i in self.item_position:
                pyxel.blt(i[0]*16, i[1]*16, 0, 32, 0, 16, 16, 0) 

    # グリッド線（あとで消す）
    def draw_grid(self):
        grid_size = 16
        color = 13  # ピンク

        # 縦線
        for x in range(0, screen_width, grid_size):
            pyxel.line(x, 0, x, screen_height, color)

        # 横線
        for y in range(0, screen_height, grid_size):
            pyxel.line(0, y, screen_width, y, color)

App()

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

    # ゲーム開始時やリセット時に実行する関数
    def init_game(self):
        self.game_over = False
        self.head_houkou = 90
        # １から１０までのグリッド
        self.head_position = [0, 0]

        """ 
        self.snake_body = [self.head_position]
        としたいところだが、参照の場合破壊的変更で、head_positionが変更されるたびにsnake_bodyも変更されてしまう。
        本来はtuppleをつかうところだが、教えてないのでリストでいく
        """
        self.snake_body = [[self.head_position[0], self.head_position[1]]]  
        self.item_position = [[5, 5], [8, 6], [2, 7]]  

    # へびの場所を更新
    def update_snake(self):
        if self.head_houkou == 90:
            self.head_position[0] += 1
        elif self.head_houkou == 180:
            self.head_position[1] += 1
        elif self.head_houkou == 270:
            self.head_position[0] -= 1
        elif self.head_houkou == 0:
            self.head_position[1] -= 1

        # 移動先がsnake_bodyにあるか、もしくは画面外に行ったときはゲームオーバー
        if [self.head_position[0], self.head_position[1]] in self.snake_body or not 0 <= self.head_position[0] <= 9 or not 0 <= self.head_position[1] <= 9:
            self.game_over = True
        """
        ①以前のヘビの場所リスト(previous_snake)に,現在のヘビの場所リストをコピー
        ②ヘビを移動
          もし移動先にアイテムがあったら:
            新しいアイテムをitem_positionに追加
            ぶつかった場所の座標をitem_positionから削除
            移動先の座標にprevious_snakeを足したものを、新しいsnake_bodyに設定
          もし移動先にアイテムがなかったら:
            移動先の座標にp、revious_snakeから最後の一つ(尻尾)を取り除いたものを足したものを、新しいsnake_bodyに設定
            
        """

        if [self.head_position[0], self.head_position[1]] in self.item_position:
            self.item_position.append(random.choice([pos for pos in position_list if pos not in self.item_position and pos not in self.snake_body]))
            self.item_position.remove([self.head_position[0], self.head_position[1]])
            self.snake_body = [[self.head_position[0], self.head_position[1]]] + self.snake_body
        else:
            self.snake_body = [[self.head_position[0], self.head_position[1]]] + self.snake_body[:-1]


    def update(self):
        if self.game_over and pyxel.btnp(pyxel.KEY_SPACE):
            self.init_game()
            return
        else:
            # 頭の向きを変更
            if pyxel.btnp(pyxel.KEY_RIGHT):
                self.head_houkou = 90
            elif pyxel.btnp(pyxel.KEY_DOWN):
                self.head_houkou = 180
            elif pyxel.btnp(pyxel.KEY_LEFT):
                self.head_houkou = 270
            elif pyxel.btnp(pyxel.KEY_UP):
                self.head_houkou = 0
            if pyxel.frame_count % 10 == 0:
                self.update_snake()

    def draw(self):
        pyxel.cls(0)
        self.draw_grid()
        if self.game_over:
            pyxel.text(0, 0, "GAME OVER", 7)
            pyxel.text(0, 10, "PRESS SPACE TO CONTINUE", 7)
        else:
            pyxel.blt(self.head_position[0] * 16, self.head_position[1] * 16, 0, 0, 0, 16, 16, 0, rotate=self.head_houkou)
            for body in self.snake_body[1:]:
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

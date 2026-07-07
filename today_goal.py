import pyxel
from random import randint

# 定数
screen_width = 160
screen_hight = 160


class App:
    def __init__(self):
        # 変数を定義:selfをつける
        self.game_over = False
        self.kakudo = 90
        self.head_position = [3, 3]

        # main.pyからの変更点:
        # appendしたあとに0番を消すため、体は「しっぽ → 頭に近い体」の順番にする
        # main.pyでは [[2, 3], [1, 3]] だったが、ここでは [[1, 3], [2, 3]] にする
        self.body_position = [[1, 3], [2, 3]]

        self.item_pos_list = [[randint(0, 9), randint(0, 9)]]
        pyxel.init(screen_width, screen_hight)
        pyxel.load("my_resource.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        # 方向キーが押されたときの処理:角度を変える
        if pyxel.btnp(pyxel.KEY_RIGHT):
            self.kakudo = 90
        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.kakudo = 180
        elif pyxel.btnp(pyxel.KEY_LEFT):
            self.kakudo = 270
        elif pyxel.btnp(pyxel.KEY_UP):
            self.kakudo = 0

        # 10フレームごとに指定の方向に1マスすすむ
        if pyxel.frame_count % 10 == 0:
            # main.pyからの変更点:
            # 頭を動かす前に、今の頭の場所を保存しておく
            # この場所が、次の体の最後の要素になる
            old_head_position = [self.head_position[0], self.head_position[1]]

            if self.kakudo == 90:
                self.head_position[0] += 1
            if self.kakudo == 270:
                self.head_position[0] -= 1
            if self.kakudo == 0:
                self.head_position[1] -= 1
            if self.kakudo == 180:
                self.head_position[1] += 1

            # main.pyからの変更点:
            # 頭があった場所を体リストの最後に追加する
            self.body_position.append(old_head_position)

            # main.pyからの変更点:
            # 0番の要素、つまり一番古いしっぽを削除する
            del self.body_position[0]

            # 枠外に出たらゲームオーバー
            if self.head_position[0] >= 10 or self.head_position[0] <= -1 or self.head_position[1] >= 10 or self.head_position[1] <= -1:
                self.game_over = True

            if self.head_position == self.item_pos_list[0]:
                self.new_item_pos = [randint(0, 9), randint(0, 9)]

                while self.new_item_pos == self.item_pos_list[0]:
                    self.new_item_pos = [randint(0, 9), randint(0, 9)]

                self.item_pos_list[0] = self.new_item_pos

    def draw(self):
        pyxel.cls(0)
        self.draw_grid()

        # ゲームオーバーじゃなければキャラクターを表示
        if self.game_over == False:
            pyxel.blt(self.head_position[0] * 16, self.head_position[1] * 16, 0, 0, 0, 16, 16, 0, rotate=self.kakudo)
            for i in self.body_position:
                pyxel.blt(i[0] * 16, i[1] * 16, 0, 16, 0, 16, 16, 0, rotate=self.kakudo)

        elif self.game_over == True:
            pyxel.text(0, 0, "GAME OVER", 7)

        # アイテムをランダムなところに表示
        pyxel.blt(self.item_pos_list[0][0] * 16, self.item_pos_list[0][1] * 16, 0, 16 * 3, 0, 16, 16, 0)

    # グリッド線を表示
    def draw_grid(self):
        grid_size = 16
        color = 13  # ピンク

        # 縦線
        for x in range(0, screen_width, grid_size):
            pyxel.line(x, 0, x, 160, color)

        # 横線
        for y in range(0, 160, grid_size):
            pyxel.line(0, y, screen_width, y, color)


App()

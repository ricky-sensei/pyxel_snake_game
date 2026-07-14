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
        self.body_position = [[1, 3], [2, 3]]

        # ーーーーーー変更ーーーーーーー
        # sample.pyと同じように、アイテムを3個配置する
        self.item_pos_list = [[5, 5], [8, 6], [2, 7]]

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
            # 頭を動かす前の場所を保存する
            self.old_head_position = [self.head_position[0], self.head_position[1]]

            if self.kakudo == 90:
                self.head_position[0] += 1
            if self.kakudo == 270:
                self.head_position[0] -= 1
            if self.kakudo == 0:
                self.head_position[1] -= 1
            if self.kakudo == 180:
                self.head_position[1] += 1

            # 頭があった場所を、頭に一番近い体として追加する
            self.body_position.append(self.old_head_position)

            # ーーーーーー変更ーーーーーーー
            # 枠外だけでなく、自分の体にぶつかったときもゲームオーバーにする
            if (
                self.head_position in self.body_position
                or self.head_position[0] >= 10
                or self.head_position[0] <= -1
                or self.head_position[1] >= 10
                or self.head_position[1] <= -1
            ):
                self.game_over = True

            # ーーーーーー変更ーーーーーーー
            # 0番だけではなく、3個のうちどのアイテムでも取れるようにする
            if self.head_position in self.item_pos_list:
                get_item_number = self.item_pos_list.index(self.head_position)
                self.new_item_pos = [randint(0, 9), randint(0, 9)]

                # ーーーーーー変更ーーーーーーー
                # 新しいアイテムが、他のアイテムやヘビと重ならないようにする
                while (
                    self.new_item_pos in self.item_pos_list
                    or self.new_item_pos == self.head_position
                    or self.new_item_pos in self.body_position
                ):
                    self.new_item_pos = [randint(0, 9), randint(0, 9)]

                self.item_pos_list[get_item_number] = self.new_item_pos

                # アイテムを取ったときは、しっぽを消さずに体を1個伸ばす
            else:
                # アイテムを取っていないときは、一番古いしっぽを消す
                del self.body_position[0]

    def draw(self):
        pyxel.cls(0)
        self.draw_grid()

        # ゲームオーバーじゃなければキャラクターとアイテムを表示
        if self.game_over == False:
            pyxel.blt(
                self.head_position[0] * 16,
                self.head_position[1] * 16,
                0,
                0,
                0,
                16,
                16,
                0,
                rotate=self.kakudo,
            )

            # ーーーーーー変更ーーーーーーー
            # sample.pyに合わせて、体の画像は回転させずに表示する
            for i in self.body_position:
                pyxel.blt(i[0] * 16, i[1] * 16, 0, 16, 0, 16, 16, 0)

            # ーーーーーー変更ーーーーーーー
            # すべてのアイテムをプレイ中だけ表示する
            for i in self.item_pos_list:
                pyxel.blt(i[0] * 16, i[1] * 16, 0, 32, 0, 16, 16, 0)

        elif self.game_over == True:
            pyxel.text(0, 0, "GAME OVER", 7)

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

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
        # self.head_position[1] = 0
        self.item_pos_list = [[3,5],[2,5]]
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
        if pyxel.frame_count % 10 == 0:  #->upgrade_snake()
            if self.kakudo == 90:
                self.head_position[0] += 1
            if self.kakudo == 270:
                self.head_position[0] -= 1
            if self.kakudo == 0:
                self.head_position[1] -= 1
            if self.kakudo == 180:
                self.head_position[1] += 1
            
            # 枠外に出たらゲームオーバー
            if self.head_position[0] >= 10 or self.head_position[0] <= -1 or self.head_position[1] >= 10 or self.head_position[1] <= -1:
                self.game_over = True
            
            # if self.game_over == True:
            #     print("ゲームオーバーしてもリッキーはイケメン")
            

        
        
    def draw(self):
        pyxel.cls(0)
        self.draw_grid()

        # ゲームオーバーじゃなければキャラクターを表示
        if self.game_over == False:
            pyxel.blt(self.head_x * 16, self.head_y * 16, 0, 0, 0, 16, 16, 0, rotate=self.kakudo)
        elif self.game_over == True:
            pyxel.text(0, 0, "GAME OVER", 7)
        
        # アイテムをランダムなところに表示
        pyxel.blt(self.item_pos_list[0][0]* 16, self.item_pos_list[0][1] * 16, 0, 16 * 3, 0, 16, 16, 0)


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

    # def update_snake(self):
    #     if self.kakudo == 90:
    #         self.head_x += 1
    #     if self.kakudo == 270:
    #         self.head_x -= 1
    #     if self.kakudo == 0:
    #         self.head_y -= 1
    #     if self.kakudo == 180:
    #         self.head_y += 1

App()


"""
リストの使い方

頭のポジション:
self.head_x, self.head_yと2つになっているのを、self.head_position[] にまとめる

upgrade_snakeにまとめる

snake_body リストを仮で作り、headについていくようにする


アイテムにぶつかったとき
[ ]尻尾をひとつ増やす
    [ ]当たる前の体のリストの最後の要素を取り出す
    [ ]移動したあとの体のリストを作成
    [ ]最後の要素を移動したあとのリストに追加
    [ ]体リストをみながら、体のパーツを表示

"""

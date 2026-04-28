import pyxel
# 定数
screen_width = 160
screen_hight = 160

class App:
    def __init__(self):
        # 変数
        self.kakudo = 0
        self.head_x = 0
        self.head_y = 0
        pyxel.init(screen_width, screen_hight)
        pyxel.load("my_resource.pyxres")
        pyxel.run(self.update, self.draw)
    def update(self):
        if pyxel.btnp(pyxel.KEY_RIGHT):
            self.kakudo = 90
            self.head_x += 1
        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.kakudo = 180
            self.head_y += 1
        elif pyxel.btnp(pyxel.KEY_LEFT):
            self.kakudo = 270
            self.head_x -= 1
        elif pyxel.btnp(pyxel.KEY_UP):
            self.kakudo = 0
            self.head_y -= 1
        
        
    def draw(self):
        pyxel.cls(0)
        pyxel.blt(self.head_x * 16, self.head_y * 16, 0, 0, 0, 16, 16, 0, rotate=self.kakudo)
        # 画像を回転させたい場合：rotate 画像を拡大したい場合：scale の引数を追加できる
App()
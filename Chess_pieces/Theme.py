
import pygame as p


class boardTheme:
    def __init__(self):
        self.path = "D:/P/pieces"
        self.walnut_theme = [p.Color(255, 206, 158), p.Color(209, 139, 71)]  # [0] is white, [1] is black
        self.sad_theme = [p.Color(192, 192, 192), p.Color(136, 136, 136)]
        self.glass_theme = [p.Color(107, 117, 136), p.Color(58, 69, 89)]
        self.brown_theme = [p.Color(124, 76, 62), p.Color(81, 42, 42)]
        self.grey_theme = [p.Color(89, 89, 89), p.Color(54, 54, 54)]
        self.theme_list = {0: self.walnut_theme, 1: self.glass_theme, 2: self.grey_theme, 3: self.sad_theme,
                           4: self.brown_theme}

    def getTheme(self, value):
        return self.theme_list[value]

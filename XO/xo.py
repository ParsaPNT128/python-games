import pygame as pg
from random import *

vector = pg.math.Vector2
window = 300
cell = window // 3
cell_center = vector(cell / 2)
INF = float('inf')

class xo:
    def __init__(self, game):
        self.game = game
        self.field_image = self.get_scaled_image(path= "./XO/field.png", res= [window] * 2)
        self.o_image = self.get_scaled_image(path= "./XO/o.png", res= [cell] * 2)
        self.x_image = self.get_scaled_image(path= "./XO/x.png", res= [cell] * 2)
        self.game_array = [[INF, INF, INF], 
                            [INF, INF, INF],
                            [INF, INF, INF]]
        self.player = randint(0, 1)
        self.line = [[(0,0), (0,1), (0,2)], [(1,0), (1,1), (1,2)], [(2,0), (2,1), (2,2)],
                    [(0,0), (1,0), (2,0)], [(0,1), (1,1), (2,1)], [(0,2), (1,2), (2,2)],
                    [(0,0), (1,1), (2,2)], [(0,2), (1,1), (2,0)]]
        self.winner = None
        self.font = pg.font.SysFont("Verdana", cell // 4, True)
        self.game_steps = 0
        
    def check_winner(self):
        for x in self.line:
            sum_line = sum([self.game_array[i][j] for i,j in x])
            if sum_line in {0, 3}:
                if sum_line == 0:
                    self.winner = "O"
                else:
                    self.winner = "X"

                self.winner_line = [vector(x[0][::-1])*cell+cell_center, vector(x[2][::-1])*cell+cell_center]
        
    def run_game_process(self):
        current_cell = vector(pg.mouse.get_pos()) // cell
        col, row = map(int, current_cell)
        left_click = pg.mouse.get_pressed()[0]
        if left_click and self.game_array[row][col] == INF and not self.winner:
            self.game_array[row][col] = self.player
            self.player = not self.player
            self.game_steps += 1
            self.check_winner()
        
    def draw_objects(self):
        for y, row in enumerate(self.game_array):
            for x, obj in enumerate(row):
                if obj != INF:
                    self.game.screen.blit(self.x_image if obj else self.o_image, vector(x, y)* cell)

    def run(self):
        self.print_caption()
        self.draw()
        self.run_game_process()

    def draw_winner(self):
        if self.winner:
            pg.draw.line(self.game.screen, "red", *self.winner_line, cell//8)
            label = self.font.render(f'Player "{self.winner}" wins', True, "White", "Black")
            self.game.screen.blit(label, (window // 2 - label.get_width() // 2, window // 4))
    
    def draw(self):
        self.game.screen.blit(self.field_image, (0, 0))
        self.draw_objects()
        self.draw_winner()

    @staticmethod
    def get_scaled_image(path, res):
        img = pg.image.load(path)
        return pg.transform.smoothscale(img, res)

    def print_caption(self):
        pg.display.set_caption(f'player {"xo"[self.player]} turn')
        if self.winner:
            pg.display.set_caption(f'player {self.winner} turn')

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode([window]*2)
        self.xo = xo(self)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            if event.type == pg.K_SPACE:
                self.new_game()

    def new_game(self):
        self.xo = xo(self)

    def run(self):
        while True:
            self.xo.run()
            self.check_events()
            pg.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()

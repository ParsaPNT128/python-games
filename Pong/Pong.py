import pygame as pg

pg.init()

screen = pg.display.set_mode((900, 600))
pg.display.set_caption("Pong")
font20 = pg.font.Font('freesansbold.ttf', 20)

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)

player1Score = 0
player2Score = 0

class Stricker:
    def __init__(self, posX, posY, width, height, color, speed):
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed
        self.strickRect = pg.Rect(posX, posY, width, height) 
        self.myStrickRect = pg.draw.rect(screen, self.color, self.strickRect)

    def display(self):
        self.myStrickRect = pg.draw.rect(screen, self.color, self.strickRect)

    def getRect(self):
        return self.myStrickRect

    def displayScore(self, text, score, x, y, color):
        text = font20.render(text + str(score), True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)
        screen.blit(text, textRect)

    def update(self, y):
        self.posY = self.posY + self.speed * y
        if self.posY <= 0:
            self.posY = 0
        elif self.posY + self.height >= 600:
            self.posY = 600 - self.height
            self.strickRect = (self.posX, self.posY, self.width, self.height)

class Ball:
    def __init__(self, posX, posY, radius, color, speed):
        self.posX = posX
        self.posY = posY
        self.radius = radius
        self.color = color
        self.speed = speed
        self.x = 1
        self.y = -1
        self.myBall = pg.draw.circle(screen, self.color, (self.posX, self.posY), self.radius)
        self.firstTime = 1

    def display(self):
        self.myBall = pg.draw.circle(screen, self.color, (self.posX, self.posY), self.radius)

    def getBall(self):
        return self.myBall

    def update(self):
        self.posX = self.posX + self.speed * self.x
        self.posY = self.posY + self.speed * self.y
        if self.posY <= 0 or self.posY >= 600:
            self.y = self.y * -1
        if self.posX <= 0 and self.firstTime:
            self.firstTime = 0
            return 1
        elif self.posX >= 900 and self.firstTime:
            self.firstTime = 0
            return -1
        else:
            return 0

    def reset(self):
        self.posX = 450
        self.pox = 300
        self.x = self.x * -1
        self.firstTime = 1

    def hit(self):
        self.x = self.x * -1

player1 = Stricker(20, 0, 10, 100, green, 1)
player2 = Stricker(870, 0, 10, 100, green, 1)
ball = Ball(450, 300, 10, white, 1)

player1Y = 0
player2Y = 0
list_of_players = [player1, player2]
run = True
while run:
    screen.fill(black)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                player2Y = -1
            if event.key == pg.K_DOWN:
                player2Y = 1
            if event.key == pg.K_w:
                player1Y = -1
            if event.key == pg.K_s:
                player1Y = 1

    for p in list_of_players:
        if pg.Rect.colliderect(ball.getBall(), p.getRect()):
            ball.hit()

    player1.update(player1Y)
    player2.update(player2Y)

    point = ball.update()
    if point == -1:
        player1Score += 1
    elif point == 1:
        player2Score += 1
    if point:
        ball.reset()

    player1.display()
    player2.display()
    ball.display()
    player1.displayScore("Player1 : ", player1Score, 100, 20, white)
    player2.displayScore("Player2 : ", player2Score, 800, 20, white)

    pg.display.update()
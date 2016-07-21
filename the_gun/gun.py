from tkinter import *
from random import choice, randint
import math
screen_width = 400
screen_height = 300
timer_delay = 100
stvol=50

class Ball:
    initial_number = 20
    minimal_radius = 15
    maximal_radius = 40
    available_colors = ['green', 'blue', 'red']

    def __init__(self):
        """
        Cоздаёт шарик в случайном месте игрового холста canvas,
        при этом шарик не выходит за границы холста!
        """
        R = randint(Ball.minimal_radius, Ball.maximal_radius)
        x = randint(0, screen_width-1-2*R)
        y = randint(0, screen_height-1-2*R)
        self._R = R
        self._x = x
        self._y = y
        fillcolor = choice(Ball.available_colors)
        self._avatar = canvas.create_oval(x, y, x+2*R, y+2*R,
                                          width=1, fill=fillcolor,
                                          outline=fillcolor)
        self._Vx = randint(-2, +2)
        self._Vy = randint(-2, +2)

    def fly(self):
        self._x += self._Vx
        self._y += self._Vy
        # отбивается от горизонтальных стенок
        if self._x < 0:
            self._x = 0
            self._Vx = -self._Vx
        elif self._x + 2*self._R >= screen_width:
            self._x = screen_width - 2*self._R -1
            self._Vx = -self._Vx
        # отбивается от вертикальных стенок
        if self._y < 0:
            self._y = 0
            self._Vy = -self._Vy
        elif self._y + 2*self._R >= screen_height:
            self._y = screen_height - 2*self._R  - 1
            self._Vy = -self._Vy

        canvas.coords(self._avatar, self._x, self._y,
                      self._x + 2*self._R, self._y + 2*self._R)


class Gun:
    def __init__(self):
        self._x = 0
        self._y = screen_height-1
        self._lx = +30
        self._ly = -30
        self._avatar = canvas.create_line(self._x, self._y,
                                          self._x+self._lx,
                                          self._y+self._ly)



    def shoot(self):
        """
        :return возвращает объект снаряда (класса Ball)
        """
        shell = Ball()
        shell._R = 5
        shell._x = self._x + self._lx
        shell._y = self._y + self._ly- shell._R
        shell._Vx = self._lx/10
        shell._Vy = self._ly/10

        shell.fly()
        return shell


def init_game():
    """
    Создаём необходимое для игры количество объектов-шариков,
    а также объект - пушку.
    """
    global balls, gun, shells_on_fly
    balls = [Ball() for i in range(Ball.initial_number)]
    gun = Gun()
    shells_on_fly = []

def init_main_window():
    global root, canvas, scores_text, scores_value
    root = Tk()
    root.title("Пушка")
    scores_value = IntVar()
    canvas = Canvas(root, width=screen_width, height=screen_height,
                    bg="white")
    scores_text = Entry(root, textvariable=scores_value)
    canvas.grid(row=1, column=0, columnspan=3)
    scores_text.grid(row=0, column=2)
    canvas.bind('<Button-1>', click_event_handler)
    canvas.bind('<Button-3>', change)


def timer_event():
    # все периодические рассчёты, которые я хочу, делаю здесь
    for ball in balls:
        ball.fly()
    for shell in shells_on_fly:
        shell.fly()
        for ball in balls:
            if ball._x<shell._x<ball._x+ball._R*2 and  ball._x<shell._x+2*shell._R<ball._x+ball._R*2  and ball._y-ball._R*2<shell._y<ball._y and ball._y-ball._R*2<shell._y-2*shell._R<ball._y:
                #canvas.coords(ball._avatar, ball._x,screen_height-1-2*ball._R,ball._x + 2*ball._R,screen_height-1)
                canvas.coords(ball._avatar, ball._x,screen_height-1-2,ball._x + 2,screen_height-1)
                balls.remove(ball)
                canvas.coords(shell._avatar, shell._x,screen_height-1-2,shell._x + 2,screen_height-1)
                shells_on_fly.remove(shell)
                break

    canvas.after(timer_delay, timer_event)


def click_event_handler(event):
    global shells_on_fly
    shell = gun.shoot()
    shells_on_fly.append(shell)


def change(event):
          x = canvas.canvasx(event.x)
          y = screen_height-canvas.canvasy(event.y)
          alpha=math.atan(y/x)
          gun._lx= int( stvol * math.cos(alpha))
          gun._ly =-int( stvol * math.sin(alpha))
          canvas.coords(gun._avatar ,gun._x, gun._y,gun._x+gun._lx,gun._y+gun._ly)


if __name__ == "__main__":
    init_main_window()
    init_game()
    timer_event()
    root.mainloop()
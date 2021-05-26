import numpy as np
import sys
from matplotlib import pyplot as plt
from dataclasses import dataclass
import time

def step_line(x0: int, y0: int, x1: int, y1: int):
    dy_higher = abs(y1 - y0) > abs(x1 - x0)

    if dy_higher:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    k = (y1 - y0) / (x1 - x0)
    b = y0 - k * x0

    for x in range(x0, x1 + 1):
        y = round(k * x + b)
        if dy_higher:
            x, y = y, x
        yield x, y

def dda_line(x0: int, y0: int, x1: int, y1: int):
    dx = x1 - x0
    dy = y1 - y0
    steps = max(abs(dx), abs(dy))

    incX = dx / steps
    incY = dy / steps

    x = x0
    y = y0

    for i in range(steps + 1):
        yield round(x), round(y)
        x += incX
        y += incY

def bresenham_line(x0: int, y0: int, x1: int, y1: int):
    dx = x1 - x0
    dy = y1 - y0
    dy_higher = abs(dy) > abs(dx)

    if dy_higher ^ (dx < 0):
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    step = 1
    if dy < 0:
        step = -1

    def bresenham_line_first(x0, y0, x1, y1):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        d = 2 * dy - dx
        y = y0

        for x in range(x0, x1 + 1):
            yield x, y
            if d >= 0:
                y += step
                d -= 2 * dx;
            d += 2 * dy;

    for (x, y) in bresenham_line_first(x0, y0, x1, y1):
        if dy_higher:
            (x, y) = (y, x)
        yield (x, y)

def bresenham_circle(x0 : int, y0: int, r: int):
    x = 0
    y = r
    d = 3 - 2 * r

    def circle8_at(x, y):
        yield x0 + x, y0 + y
        yield x0 - x, y0 + y
        yield x0 + x, y0 - y
        yield x0 - x, y0 - y
        yield x0 + y, y0 + x
        yield x0 - y, y0 + x
        yield x0 + y, y0 - x
        yield x0 - y, y0 - x

    while y >= x:
        yield from circle8_at(x, y)
        x += 1
        if d > 0:
            y -= 1
            d += 4 * (x - y) + 10
        else:
            d += 4 * x + 6

@dataclass
class Rect:
    minX: int
    minY: int
    maxX: int
    maxY: int

def to_pixel_array(pixels_at: list, line: Rect):
    dx = line.maxX - line.minX
    dy = line.maxY - line.minY
    arr = np.ones((dy + 1, dx + 1))

    for v in pixels_at:
        x, y = v
        arr[y - line.minY, x - line.minX] = 0

    return arr


def main():

    method = sys.argv[1]

    start = time.perf_counter()

    def show_line(method):
        x0 = int(sys.argv[2])
        y0 = int(sys.argv[3])
        x1 = int(sys.argv[4])
        y1 = int(sys.argv[5])
        line = method(x0,y0,x1,y1)
        rect = Rect(x0,y0,x1,y1)
        show(line, rect)

    def show(pixels_at: list, line: Rect):
        print("Time: ", time.perf_counter() - start)
        plt.pcolormesh(to_pixel_array(pixels_at, line), edgecolors='black', linewidth=1, cmap=plt.cm.gray, snap=True)
        plt.gca().set_aspect('equal')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.show()

    if method == 'bresenham_line':
        show_line(bresenham_line)
    elif method == 'dda_line':
        show_line(dda_line)
    elif method == 'step_line':
        show_line(step_line)
    elif method == 'bresenham_circle':
        x0 = int(sys.argv[2])
        y0 = int(sys.argv[3])
        r = int(sys.argv[4])
        circle = bresenham_circle(x0,y0,r)
        rect = Rect(x0 - r, y0 - r, x0 + r, y0 + r)
        show(circle, rect)


if __name__ == "__main__":
    main()

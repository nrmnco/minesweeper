import pygame as pg
import random as r

num_of_rows = 10
num_of_bombs = 15
bomb_coord = [] # хранит координаты бомб
mark_coord = [] # хранит координаты отмеченных клеток
pg.init()
pg.font.init()


# проверка все ли бомбы отмечены
def bomb_check(bomb_coord, mark_coord, num_of_bombs):
    global bomb_counter
    bomb_counter = 0
    for coord in mark_coord:
        if coord in bomb_coord and bomb_counter != num_of_bombs:
            bomb_counter += 1
        else:
            break
    
    if bomb_counter == num_of_bombs:
        return True
    else:
        return False
    
    
# проверка все ли клетки открыты
def cell_check(arr):
    for row in arr:
        for col in row:
            if col.opened == False and col.value != -1:
                return False
            
    return True



# заполнение игрового поля бомбами и цифрами
def filling_cells(num_of_bombs, num_of_rows, arr, bomb_coord):
    for i in range(num_of_bombs):
        x_bomb = r.randint(0, num_of_rows-1)
        y_bomb = r.randint(0, num_of_rows-1)

        # делаем так что бомбы не находятся вокруг клетки выбранной в первый раз и чтобы координаты бомб не совпадали
        while [x_bomb, y_bomb] in angle_ind or arr[x_bomb][y_bomb].value == -1:
            empty_cells = [(x, y) for x in range(num_of_rows) for y in range(num_of_rows) if arr[x][y].value != -1]
            x_bomb, y_bomb = r.choice(empty_cells)

        arr[x_bomb][y_bomb].value = -1
        bomb_coord.append([x_bomb, y_bomb])

        # заполняем цифрами
        for row in [x_bomb-1, x_bomb, x_bomb+1]:
                for col in [y_bomb-1, y_bomb, y_bomb+1]:
                    if row == x_bomb and col == y_bomb:
                        continue
                    elif row >= 0 and col >= 0:
                        try:
                            if arr[row][col].value != -1:
                                arr[row][col].value += 1
                        except:
                            pass


# открытие клеток
def open_cells(x, y):
    # если клетка уже открыта
    if arr[x][y].opened != False:
        return

    arr[x][y].opened = True

    # ищем все соседние клетки
    for i in range(-1, 2):
        for j in range(-1, 2):
            new_x = x + i
            new_y = y + j
            if 0 <= new_x < num_of_rows and 0 <= new_y < num_of_rows:
                if arr[new_x][new_y].value == 0:
                    open_cells(new_x, new_y)
                elif arr[new_x][new_y].value > 0:
                    arr[new_x][new_y].opened = True



class Cell():
    def __init__(self, size):
        self.value = 0
        self.size = size // num_of_rows
        self.x = 0
        self.y = 0
        self.opened = False
        self.myfont = pg.font.SysFont("calibri.ttf", self.size)
        self.marked = False

    def set_coord(self, x, y):
        self.x = x * self.size
        self.y = y * self.size

    def draw_cell(self):
        if self.opened == True:
            text = self.myfont.render(str(self.value), True, 'red')
            surf = pg.Surface((self.size, self.size))
            surf.fill('red')
            pg.draw.rect(surf, 'white', pg.Rect(2, 2, self.size-4, self.size-4))
            surf.blit(text, (self.size - self.size//1.4, self.size - self.size//1.3))
            screen.blit(surf, (self.x, self.y))
        elif self.marked == True:
            surf = pg.Surface((self.size, self.size))
            surf.fill('red')
            pg.draw.rect(surf, 'purple', pg.Rect(2, 2, self.size-4, self.size-4))
            screen.blit(surf, (self.x, self.y))
        else:
            surf = pg.Surface((self.size, self.size))
            surf.fill('red')
            pg.draw.rect(surf, 'white', pg.Rect(2, 2, self.size-4, self.size-4))
            screen.blit(surf, (self.x, self.y))



size = 640
screen = pg.display.set_mode((size, size))
clock = pg.time.Clock()
running = True
arr = [[Cell(size) for x in range(num_of_rows)] for i in range(num_of_rows)]
counter = 0




while running:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.MOUSEBUTTONDOWN:

            if event.button == 1:

                # первый ход
                if counter < 1:
                    pos=pg.mouse.get_pos()
                    x = pos[0] // (size // num_of_rows)
                    y = pos[1] // (size // num_of_rows)
                    angle_ind = [[x-1,y-1], [x+1, y-1], [x-1, y+1], [x+1, y+1], [x, y-1], [x, y+1], [x-1, y], [x+1, y], [x, y]]
                    filling_cells(num_of_bombs, num_of_rows, arr, bomb_coord)
                    open_cells(x, y)
                    counter += 1

                # последующие ходы
                else:
                    
                    pos=pg.mouse.get_pos()
                    x = pos[0] // (size // num_of_rows)
                    y = pos[1] // (size // num_of_rows)
                    if arr[x][y].marked != True:
                        if arr[x][y].value == -1:
                            print('lose')
                            exit()
                        
                        if arr[x][y].value == 0:
                            open_cells(x, y)

                        else:
                            arr[x][y].opened = True


            # отмечаем клетку
            elif event.button == 3:
                pos=pg.mouse.get_pos()
                x = pos[0] // (size // num_of_rows)
                y = pos[1] // (size // num_of_rows)

                if arr[x][y].marked == False:
                    arr[x][y].marked = True
                    mark_coord.append([x, y])

                else:
                    arr[x][y].marked = False
                    mark_coord.remove([x, y])

            
    # проверка на выигрыш
    if bomb_check(bomb_coord, mark_coord, num_of_bombs) and cell_check(arr):
        print('win')
        exit()
        

                
    # Рисуем игровое поле
    for i in range(num_of_rows):
        for j in range(num_of_rows):
            arr[i][j].set_coord(i, j)
            arr[i][j].draw_cell()

    
    pg.display.flip()
    clock.tick(60)

pg.quit()

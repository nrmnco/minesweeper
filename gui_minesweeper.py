import pygame as pg
import pygame.freetype
import random as r
import time
import pickle


# объявляем все необходимые переменные и массивы
num_of_rows = 10
num_of_bombs = 5
bomb_coord = [] # хранит координаты бомб
mark_coord = [] # хранит координаты отмеченных клеток
arr = []
size = 720
screen = pg.display.set_mode((size, size))
pg.display.set_caption('Minesweeper')
clock = pg.time.Clock()
running = True
counter = 0
pg.init()
pg.font.init()
menu_font = pg.font.SysFont("calibri.ttf", 75)
menu_font_small = pg.font.SysFont("calibri.ttf", 50)
menu_font_small_fr = pygame.freetype.SysFont("calibri.ttf", 50)
window = 0 # отвечает за окошки(0 - главное меню, 1 - игра, 2 - настройки, 3 - победа, 4 - поражение)
t0 = 0
t1 = 0
timer = 0
best_time = 1000000



#=========================================================================================================


board = pg.Surface((size, size+100))
text_back = menu_font_small.render('Go back', False, (50, 50, 50))


# рисуем окошко меню
menu = pg.Surface((size, size+100))

def set_menu():
    text_play = menu_font.render('Play', True, (50, 50, 50))
    text_settings = menu_font.render('Settings', True, (50, 50, 50))
    text_exit = menu_font.render('Exit', True, (50, 50, 50))
    menu.fill('white')

    # play кнопка
    pg.draw.rect(menu, (87, 84, 84), pg.Rect(size//3, size//7, size//3, size//8))
    pg.draw.rect(menu, 'grey', pg.Rect(size//3+3, size//7+3, size//3-6, size//8-6))

    # settings кнопка
    pg.draw.rect(menu, (87, 84, 84), pg.Rect(size//3, size//7+150, size//3, size//8))
    pg.draw.rect(menu, 'grey', pg.Rect(size//3+3, size//7+150+3, size//3-6, size//8-6))

    # exit кнопка
    pg.draw.rect(menu, (87, 84, 84), pg.Rect(size//3, size//7+300, size//3, size//8))
    pg.draw.rect(menu, 'grey', pg.Rect(size//3+3, size//7+300+3, size//3-6, size//8-6))



    menu.blit(text_play, (size//3+65, size//7+25))
    menu.blit(text_settings, (size//3+15, size//7+175))
    menu.blit(text_exit, (size//3+65, size//7+325))





# рисуем окошко настроек
settings = pg.Surface((size, size+100))
text_easy = menu_font.render('Easy', True, (50, 50, 50))
text_medium = menu_font.render('Medium', True, (50, 50, 50))
text_hard = menu_font.render('Hard', True, (50, 50, 50))
settings.fill('white')

# easy кнопка
pg.draw.rect(settings, (87, 84, 84), pg.Rect(size//3, size//7, size//3, size//8))
pg.draw.rect(settings, 'grey', pg.Rect(size//3+3, size//7+3, size//3-6, size//8-6))

# medium кнопка
pg.draw.rect(settings, (87, 84, 84), pg.Rect(size//3, size//7+150, size//3, size//8))
pg.draw.rect(settings, 'grey', pg.Rect(size//3+3, size//7+150+3, size//3-6, size//8-6))

# hard кнопка
pg.draw.rect(settings, (87, 84, 84), pg.Rect(size//3, size//7+300, size//3, size//8))
pg.draw.rect(settings, 'grey', pg.Rect(size//3+3, size//7+300+3, size//3-6, size//8-6))


settings.blit(text_easy, (size//3+55, size//7+25))
settings.blit(text_medium, (size//3+25, size//7+175))
settings.blit(text_hard, (size//3+55, size//7+325))
settings.blit(text_back, (size//3+50, size//7+450))




# рисуем окошко в случае победы
victory = pg.Surface((size, size+100))
victory.fill((247,247,247))
img_vict = pg.image.load('images\confetti.png').convert()
img_vict = pg.transform.scale(img_vict, (300, 300))
text_vict = menu_font.render('Congratulations!!!', True, (50, 50, 50))
victory.blit(text_vict, (size//5, size-200))
victory.blit(text_back, (size//2.5, size-100))
victory.blit(img_vict, (size//3.5, size//6))




# рисуем окошко в случае поражения
defeat = pg.Surface((size, size+100))
defeat.fill('black')
img_def = pg.image.load('images\sad.png').convert()
img_def = pg.transform.scale(img_def, (300, 300))
text_def = menu_font.render('You lose :c', True, (50, 50, 50))
defeat.blit(text_def, (size//3.25, size-200))
defeat.blit(text_back, (size//2.5, size-100))
defeat.blit(img_def, (size//3.5, size//6))




#=========================================================================================================



def save_best_time(time):
    global best_time
    with open("best_time.pickle", "wb") as file:
        pickle.dump(time, file)



def load_best_time():
    global best_time
    try:
        with open("best_time.pickle", "rb") as file:
            best_time = pickle.load(file)
    except FileNotFoundError:
        best_time = 100000





def change_cell_size(arr, num_of_rows, size):
    for i in arr:
        for j in i:
            j.set_size(num_of_rows, size)


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



#=========================================================================================================



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
            if self.value == 0:
                surf = pg.Surface((self.size, self.size))
                surf.fill((87, 84, 84))
                pg.draw.rect(surf, 'white', pg.Rect(2, 2, self.size-4, self.size-4))
                board.blit(surf, (self.x, self.y))

            else:
                text = self.myfont.render(str(self.value), True, 'red')
                surf = pg.Surface((self.size, self.size))
                surf.fill((87, 84, 84))
                pg.draw.rect(surf, 'white', pg.Rect(2, 2, self.size-4, self.size-4))
                surf.blit(text, (self.size - self.size//1.4, self.size - self.size//1.3))
                board.blit(surf, (self.x, self.y))

        elif self.marked == True:
            surf = pg.Surface((self.size, self.size))
            surf.fill((87, 84, 84))
            pg.draw.rect(surf, (250, 0, 0), pg.Rect(2, 2, self.size-4, self.size-4))
            board.blit(surf, (self.x, self.y))

        else:
            surf = pg.Surface((self.size, self.size))
            surf.fill((87, 84, 84))
            pg.draw.rect(surf, 'grey', pg.Rect(2, 2, self.size-4, self.size-4))
            board.blit(surf, (self.x, self.y))

    def set_size(self, num_of_rows, size):
        self.size = size // num_of_rows


#=========================================================================================================

load_best_time()

# основной цикл
while running:
    load_best_time()
    # обрабатываем клики мыши
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.MOUSEBUTTONDOWN:
            pos=pg.mouse.get_pos()
            x = pos[0]
            y = pos[1]

            if 5 <= x <= 155 and 5 <= y <= 44:
                window = 0

            if window == 0:

                if size // 3 <= x <= 2 * size // 3 and size//7 <= y <= ((size//7) + (size//8)):
                    window = 1
                    # объявляем 2д список с клетками в качестве значений
                    arr = [[Cell(size) for x in range(num_of_rows)] for i in range(num_of_rows)]


                elif size // 3 <= x <= 2 * size // 3 and size//7+150 <= y <= ((size//7+150) + (size//8)):
                    window = 2

                elif size // 3 <= x <= 2 * size // 3 and size//7+300 <= y <= ((size//7+300) + (size//8)):
                    running = False

            elif window == 1 and y > 50:
                x = x // (size // num_of_rows)
                y = (y-50) // (size // num_of_rows)

                if event.button == 1:
                    # первый ход
                    t0 = time.time()
                    if counter < 1:
                        angle_ind = [[x-1,y-1], [x+1, y-1], [x-1, y+1], [x+1, y+1], [x, y-1], [x, y+1], [x-1, y], [x+1, y], [x, y]]
                        filling_cells(num_of_bombs, num_of_rows, arr, bomb_coord)
                        open_cells(x, y)
                        counter += 1

                    # последующие ходы
                    else:

                        if arr[x][y].marked != True:

                            if arr[x][y].value == -1:
                                window = 4
                            
                            if arr[x][y].value == 0:
                                open_cells(x, y)

                            else:
                                arr[x][y].opened = True


                # отмечаем клетку
                elif event.button == 3:

                    if arr[x][y].marked == False and arr[x][y].opened == False:
                        arr[x][y].marked = True
                        mark_coord.append([x, y])

                    elif arr[x][y].opened == False:
                        arr[x][y].marked = False
                        mark_coord.remove([x, y])

            elif window == 2:

                if size // 3 <= x <= 2 * size // 3 and size//7 <= y <= ((size//7) + (size//8)):
                    num_of_rows = 10
                    num_of_bombs = 10
                    change_cell_size(arr, num_of_rows, size)
                    window = 0

                elif size // 3 <= x <= 2 * size // 3 and size//7+150 <= y <= ((size//7+150) + (size//8)):
                    num_of_rows = 15
                    num_of_bombs = 30
                    change_cell_size(arr, num_of_rows, size)
                    window = 0

                elif size // 3 <= x <= 2 * size // 3 and size//7+300 <= y <= ((size//7+300) + (size//8)):
                    num_of_rows = 20
                    num_of_bombs = 50
                    change_cell_size(arr, num_of_rows, size)
                    window = 0

                elif size//3+30 <= x <= size//3+200 and size//7+430 <= y <= size//7+490:
                    window = 0

            elif window == 3:

                if size//3 <= x <= size//1.5 and size-120 <= y <= size-60:
                    window = 0
                    counter = 0
                    bomb_coord = []
                    mark_coord = []

            elif window == 4:
                pos=pg.mouse.get_pos()
                x = pos[0]
                y = pos[1]

                if size//3 <= x <= size//1.5 and size-120 <= y <= size-50:
                    window = 0
                    counter = 0
                    bomb_coord = []
                    mark_coord = []     


    # меню
    if window == 0:
        best_time = round(float(best_time), 5)
        menu.fill('white')
        set_menu()
        text_time = menu_font_small.render('Best time: ' + str(best_time), True, (50, 50, 50))
        menu.blit(text_time, (size//4+30, size//7+420))
        screen.blit(menu, (0, 0))

    # основная игра
    elif window == 1:
        screen.fill('white')
        if counter > 0:
            t1 = time.time()
        dt = t1 - t0
        out= str(dt)
        
        if float(out) > float(timer):
            timer = out

        screen.blit(text_back, (10, 10))
        menu_font_small_fr.render_to(screen, (size-250, 10), out, pg.Color((50,50,50)))


        # проверка на выигрыш
        if bomb_check(bomb_coord, mark_coord, num_of_bombs) and cell_check(arr):
            window = 3
            load_best_time
            if float(best_time) >= float(timer):
                save_best_time(timer)
            else:
                save_best_time(best_time)

        # Рисуем игровое поле
        for i in range(num_of_rows):
            for j in range(num_of_rows):
                arr[i][j].set_coord(i, j)
                arr[i][j].draw_cell()

        screen.blit(board, (0, 50))

    # настройки
    elif window == 2:
        screen.blit(settings, (0, 0))

    # победа
    elif window == 3:
        screen.blit(victory, (0, 0))
    
    # поражение
    elif window == 4:
        screen.blit(defeat, (0, 0))





    pg.display.flip()
    clock.tick(60)

pg.quit()

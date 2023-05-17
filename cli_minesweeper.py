import random as r



#==========================================================
#==========================ФУНКЦИИ=========================
#==========================================================

# открытие клеток
def open_cells(x, y):
    # если клетка уже открыта
    if arr[x][y] != ' ':
        return

    arr[x][y] = arr_with_values[x][y]

    # ищем все соседние клетки
    for i in range(-1, 2):
        for j in range(-1, 2):
            new_x = x + i
            new_y = y + j
            if 0 <= new_x < num_of_rows and 0 <= new_y < num_of_rows:
                if arr_with_values[new_x][new_y] == 0:
                    open_cells(new_x, new_y)
                else:
                    arr[new_x][new_y] = arr_with_values[new_x][new_y]


# красивый вывод игрового поля
def output(arr):
    print('\nx/y ', end='')
    for col in range(num_of_rows):
        if col < 9:
            print(f'{col}    ', end='')
        else:
            print(f'{col}   ', end='')
    print()
    
    for row in range(num_of_rows):

        if row < 10:
            print(f'{row}  ', end='')
        else:
            print(f'{row} ', end='')

        for col in range(num_of_rows):
            print(f'[{arr[row][col]}]  ', end='')
        if row < 10:
            print(f'{row}  ', end='')
        else:
            print(f'{row} ', end='')
        print()

    print('x/y ', end='')
    for col in range(num_of_rows):
        if col < 9:
            print(f'{col}    ', end='')
        else:
            print(f'{col}   ', end='')
    print()



# проверка выигрыша
def victory_check(bomb_coord, mark_coord):
    global counter
    counter = 0
    for coord in mark_coord:
        if coord in bomb_coord and counter != num_of_bombs:
            counter += 1
        else:
            break


#==========================================================
#==========================ФУНКЦИИ=========================
#==========================================================


#       <========================================>


#==========================================================
#=====================ОСНОВНОЙ КОД=========================
#==========================================================

num_of_rows = -1
while num_of_rows < 10 or num_of_rows > 30:
    num_of_rows = int(input('введите количество строк и столбцов '))
num_of_bombs = 0
while num_of_bombs < 1 or num_of_bombs > num_of_rows**2 // 4:
    num_of_bombs = int(input('введите количество бомб на игровом поле '))   
method = 1
counter = 0
arr = [[' ' for x in range(num_of_rows)] for i in range(num_of_rows)] # хранит то что игрок будет видеть
arr_with_values = [[0 for x in range(num_of_rows)] for i in range(num_of_rows)] # хранит расположения бомб, цифры и тд
bomb_coord = []
mark_coord = []


# первый выбор клетки
x, y = map(int, input('введите координаты x и y ').split())

angle_ind = [[x-1,y-1], [x+1, y-1], [x-1, y+1], [x+1, y+1], [x, y-1], [x, y+1], [x-1, y], [x+1, y]]

# заполнение игрового поля бомбами и цифрами  and arr_with_values[x_bomb][y_bomb] == -1
for i in range(num_of_bombs):
    x_bomb = r.randint(0, num_of_rows-1)
    y_bomb = r.randint(0, num_of_rows-1)

    # делаем так что бомбы не находятся вокруг клетки выбранной в первый раз и чтобы координаты бомб не совпадали
    while [x_bomb, y_bomb] in angle_ind or arr_with_values[x_bomb][y_bomb] == -1: # проверка на расположение по углам
        x_bomb = r.randint(0, num_of_rows-1)
        y_bomb = r.randint(0, num_of_rows-1)

    arr_with_values[x_bomb][y_bomb] = -1
    bomb_coord.append([x_bomb, y_bomb])

    # заполняем цифрами
    for row in [x_bomb-1, x_bomb, x_bomb+1]:
            for col in [y_bomb-1, y_bomb, y_bomb+1]:
                if row == x_bomb and col == y_bomb:
                    continue
                else:
                    try:
                        if arr_with_values[row][col] != -1:
                            arr_with_values[row][col] += 1
                    except:
                        pass


while True:
    if method == 1:
        if arr_with_values[x][y] == 0:
            open_cells(x, y)
        else:
            arr[x][y] = arr_with_values[x][y]

        output(arr)

        # проверка не попал ли игрок на мину
        if arr_with_values[x][y] == -1:
            print('поражение')
            break

    elif method == 2:
        if arr[x][y] == ' ':
            arr[x][y] = 'X'
            mark_coord.append([x, y])
        else:
            print('поле уже открыто')

        victory_check(bomb_coord, mark_coord)
        output(arr)

        if counter == num_of_bombs:
            print('Победа!!!!')
            break

    elif method == 3:
        if arr[x][y] == 'X':
            arr[x][y] = ' '
            mark_coord.remove([x, y])
            output(arr)
        else:
            print('эта клетка не отмечена')

    else:
        print('действие может быть равен только 1, 2 или 3')

    
    method = int(input("""
    Введите действие:
    1 - открыть клетку
    2 - отметить клетку
    3 - удалить отметку с клетки
    действие - """))
    x, y = map(int, input('введите координаты x и y ').split())
        
#==========================================================
#=====================ОСНОВНОЙ КОД=========================
#==========================================================
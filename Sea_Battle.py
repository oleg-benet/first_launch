import math
import random


class SymbolQuantityExcess(Exception):
    # pass
    def __init__(self, message="Превышение количества символов. Повторите ввод"):
        self.message = message
        super().__init__(self.message)


class SymbolOutOfRange(Exception):

    def __init__(self, message="Вы ввели неверный символ.Повторите ввод"):
        self.message = message
        super().__init__(self.message)


class ErrorPlacement(Exception):

    def __init__(self, message="Попытка расположить судно за пределами поля.Попробуйте еще раз"):
        self.message = message
        super().__init__(self.message)


class ShotOutOfBoard(Exception):

    def __init__(self, message="Выстрел за пределы поля. Повторите выстрел"):
        self.message = message
        super().__init__(self.message)


class RepeatShot(Exception):

    def __init__(self, message="Сюда уже стреляли"):
        self.message = message
        super().__init__(self.message)


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f'Dot: {self.x, self.y}'


class Ship:

    def __init__(self, length, stem, angle, vital):
        self.length = length
        self.stem = stem
        self.angle = angle
        self.vital = vital

    def dots(self):
        ship_elements = []
        for i in range(self.length):
            ship_dot = Dot(self.stem.x + i * round(math.cos(self.angle)),
                           self.stem.y + i * round(math.sin(self.angle)))
            ship_elements.append(ship_dot)
        return ship_elements


class Board:
    def __init__(self, surface, group, hid, alive_ships):
        self.surface = surface
        self.group = group
        self.hid = hid
        self.alive_ships = alive_ships

    def add_ship(self, ship_dots):
        try:
            for dot in ship_dots:
                if dot not in kit_of_boarddots:
                    raise ErrorPlacement
        except ErrorPlacement as e:
            print(e)
            print()
            return False

        else:
            for dot in ship_dots:
                self.surface[dot.x][dot.y] = 9632
        return self.surface

    def screen_of_battle(self):
        mask = []
        if self.hid:
            for i in range(7):
                for j in range(7):
                    print(chr(self.surface[i][j]), end=" | ")
                print()
        else:
            for i in range(7):
                for j in range(7):
                    if self.surface[i][j] == 9632:
                        d = Dot(i, j)
                        mask.append(d)
                        self.surface[i][j] = 9711
            for i in range(7):
                for j in range(7):
                    print(chr(self.surface[i][j]), end=" | ")
                print()
            for dot in mask:
                self.surface[dot.x][dot.y] = 9632

    def contour(self, ship_dots):
        blanc_dot_list = []
        omega = (- math.pi) / 4
        for dot in ship_dots:
            # print(dot)
            for i in range(8):
                blanc_dot = Dot(dot.x + round(math.cos(omega * i)),
                                dot.y + round(math.sin(omega * i)))
                if blanc_dot not in ship_dots and blanc_dot not in blanc_dot_list:
                    blanc_dot_list.append(blanc_dot)
        return blanc_dot_list

    @staticmethod
    def out(dot):
        if (dot.x > 6 or dot.x < 1) or (dot.y > 6 or dot.y < 1):
            return True
        else:
            return False

    def shot(self, dot):
        try:
            if self.surface[dot.x][dot.y] == 9587 or self.surface[dot.x][dot.y] == 932:
                raise RepeatShot
        except RepeatShot as e:
            print(e)
        else:

            for ship in self.group:
                if dot in ship.dots():
                    print("Ранил!")
                    ship.vital -= 1
                    if ship.vital == 0:
                        print("Убил!!!")
                        self.alive_ships -= 1

            if self.surface[dot.x][dot.y] == 9632:
                self.surface[dot.x][dot.y] = 9587
                return 1
            else:
                self.surface[dot.x][dot.y] = 932
                print("Промазал!")
                return 2


class Player:
    def __init__(self, my_board, enemy_board):
        self.my_board = my_board
        self.enemy_board = enemy_board

    @staticmethod
    def ask():
        pass

    def move(self):
        attempt = 0
        while attempt == 0:
            dot = self.ask()
            attempt = self.enemy_board.shot(dot)
            if attempt == 1:
                return True


class AI(Player):

    @staticmethod
    def ask():
        input('Ходит компьютер. Подтвердите генерацию хода компьютера нажатием клавиши "Enter"')
        print()
        ask_x = random.randint(1, 6)
        ask_y = random.randint(1, 6)
        d = Dot(ask_x, ask_y)
        return d


class User(Player):

    @staticmethod
    def ask():
        global ask_x, ask_y
        while True:
            try:
                ask_x = input("Ваш ход. Введите номер горизонтальной линии цели: ")
                if len(ask_x) > 1:
                    raise SymbolQuantityExcess
                if ord(ask_x) < 49 or ord(ask_x) > 54:
                    raise SymbolOutOfRange
                ask_y = input("Введите номер вертикальной линии цели: ")
                if len(ask_y) > 1:
                    raise SymbolQuantityExcess
                if ord(ask_y) < 49 or ord(ask_y) > 54:
                    raise SymbolOutOfRange
                break
            except SymbolQuantityExcess as e:
                print(e)
                print()
            except SymbolOutOfRange as e:
                print(e)
                print()
        d = Dot(int(ask_x), int(ask_y))
        return d


class Game:
    def __init__(self, user, user_board, ai, ai_board):
        self.user = user
        self.user_board = user_board
        self.ai = ai
        self.ai_board = ai_board

    def random_board(self):
        number1 = [32, 49, 50, 51, 52, 53, 54]

        self.user_board.surface = [[9711] * 7 for i in range(7)]  # квадратная матрица доски игрока
        for i in range(7):
            self.user_board.surface[i][0] = number1[i]
            self.user_board.surface[0][i] = number1[i]

        self.ai_board.surface = [[9711] * 7 for i in range(7)]  # квадратная матрица доскт AI
        for i in range(7):
            self.ai_board.surface[i][0] = number1[i]
            self.ai_board.surface[0][i] = number1[i]

        global kit_of_boarddots
        all_random_ship_dots = []
        all_random_contour_dots = []
        alfa = math.pi / 2
        compass = {2: 0, 4: 3 * alfa, 6: alfa, 8: 2 * alfa}
        switch = [self.user_board, self.ai_board]
        for n in range(2):
            while len(switch[n].group) < 7:
                all_random_ship_dots.clear()
                all_random_contour_dots.clear()
                switch[n].group.clear()
                for i in range(1, 7):
                    for j in range(1, 7):
                        switch[n].surface[i][j] = 9711
                for i in range(3):  # цикл по трем типам кораблей
                    for j in range(2 ** i):  # цикл по количеству кораблей (1,2,4)
                        count = 0  # в соответствующем типе кораблей
                        while count < 1000:
                            count += 1
                            # print(count)
                            rand_num = random.randint(0, 35)  # генерация индекса массива точек поля
                            rand_head = kit_of_boarddots[rand_num]  # координаты носа корабля
                            rand_num = random.randint(1, 4)  # генерация направления корабля
                            rand_direct = 2 * rand_num  # ключ словаря азимутов
                            rand_vessel = Ship(3 - i, rand_head, compass[rand_direct],
                                               3 - i)  # создание экземпляра  корабля
                            rand_ship_dot_list = rand_vessel.dots()  # точки созданного корабля
                            if select_dots(rand_ship_dot_list, all_random_ship_dots,
                                           # проверка нахождения точек корабля в
                                           all_random_contour_dots):  # в списке точек всех уже имеющихся
                                continue  # кораблей и в списке точек их контуров
                            try:
                                for dot in rand_ship_dot_list:
                                    if dot not in kit_of_boarddots:
                                        raise ErrorPlacement
                            except ErrorPlacement:
                                continue
                            else:
                                for dot in rand_ship_dot_list:
                                    switch[n].surface[dot.x][dot.y] = 9632
                                all_random_ship_dots = all_random_ship_dots + rand_ship_dot_list
                                all_random_contour_dots = all_random_contour_dots + \
                                                          switch[n].contour(rand_ship_dot_list)
                                switch[n].group.append(rand_vessel)
                                switch[n].add_ship(rand_ship_dot_list)
                                print()
                                break

    def greet(self):
        print('                  Игра "Морской бой" приветствует Вас!')
        print('          Поля игрока и компьютера генерируются случайным образом.')
        print('   Координата целевой клетки - пересечение горизонтальной и вертикальной линий')
        print(' Чтобы компьютер сделал ход, Вам необходимо дать разрешение нажатием клавиши "Enter" ')
        print('                 В общем, можно просто читать подсказки ))')

        print("                     Символы, отображаемые на поле:")
        print("                            Корабль:   ", chr(9632))
        print("                             Промах:   ", chr(932))
        print("                          Попадание:   ", chr(9587))
        print("                        Пустая клетка  ", chr(9711))
        print()
        print()

    def loop(self):

        # name = [self.user, self.ai_board]
        draw = ["Первым/первой ходите Вы", "Первым ходит компьютер"]
        winner = ["Победа компьютера.Увы", "Победа Ваша!!!"]
        info = ["          Поле компьютера", "                Ваше поле"]
        # player = [self.user, self.ai]
        board = [self.ai_board, self.user_board]
        count = 1
        switch = {0: [self.user, self.ai_board], 1: [self.ai, self.user_board]}
        input('Подбросим монетку, чтобы определить чей ход. Подтвердите клавишей "Enter"')
        k = random.randint(0, 1)
        # k = 0
        print(draw[k])
        print()
        # board[k].screen_of_battle()
        while count:
            list = switch[k]
            print(info[k])
            board[k].screen_of_battle()
            while list[0].move():
                count = list[1].alive_ships
                # print(info[k])
                board[k].screen_of_battle()
                if count == 0:
                    break
                # print(count)
            print(info[k])
            board[k].screen_of_battle()
            k = (k + 1) % 2
        print(winner[k])

    def start(self):
        self.greet()
        self.loop()


def select_dots(list1, list2, list3):
    n = 0
    for dot in list1:
        if dot in list2 or dot in list3:
            n = 1
    if n:
        return True
    else:
        return False


fleet = []  # список кораблей ирока
navy = []  # список кораблей AI

battle_scene = []  # пустая матрица поля игрока
ai_battle_scene = []  # пустая матрица поля крмпьютера

kit_of_boarddots = []  # линейный список возможных точек поля
for i in range(6):
    for j in range(6):
        a = Dot(i + 1, j + 1)
        kit_of_boarddots.append(a)

your_b = Board(battle_scene, fleet, True, 7)  # экземпляр доски пользователя
comp_b = Board(ai_battle_scene, navy, False, 7)  # экземпляр доски ИИ

you = User(your_b, comp_b)  # экземпляр пользователя
comp = AI(comp_b, your_b)  # экземпляр ИИ

new_game = Game(you, your_b, comp, comp_b)  # экземпляр игры

new_game.random_board()

new_game.start()

# Элементы заполнения матрицы поля подобраны так, чтобы исключить расползание столбцов при выводе в консоль
# x = 9587
# o = 9711
# T = 932
# black_square = 9632

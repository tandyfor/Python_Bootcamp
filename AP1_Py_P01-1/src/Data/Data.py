import random

class Display:
    """
    Класс игрового поля.
    """
    def __init__(self, y, x):
        """
        Создание матриц.

        Args:
            y (int): Высота игрового поля.
            x (int): Ширина игрового поля.
        """
        self.__step_y = y // 3 - 1
        self.__step_x = x // 3 - 1
        self.__init_struct(y, x)
        self.__init_acctive(y, x)

    def __init_struct(self, y, x):
        """
        Создание структурной матрицы.

        Args:
            y (int): Высота игрового поля.
            x (int): Ширина игрового поля.
        """
        self.__display_struct = [[int(0) for i in range(x + 1)] for j in range(y + 1)]
        self.__doors_generator()
        self.rooms = [[Room(self.__step_y, self.__step_x, self.__doors[i][j]) \
                       for j in range(3)] for i in range(3)]
        for i in range(3):
            for j in range(3):
                self.__add_room(i, j, self.rooms[i][j].get_room())
        
        self.__add_exit_door()
        self.__add_character()
        self.__cross_corridor()

    def __init_acctive(self, y, x):
        """
        Создание активной матрицы.

        Args:
            y (int): Высота игрового поля.
            x (int): Ширина игрового поля.
        """
        self.__display_active = [[Const.NONE for i in range(x + 1)] \
                                 for j in range(y + 1)]

    def __doors_generator(self):
        """
        Генератор дверей.
        """
        self.__room_counter = 1
        self.__doors = [[{'up': False, 'right': False, 'down': \
                        False, 'left': False, 'count': 0} \
                        for _ in range(3)] for _ in range(3)]
        self.__make_door(0, 0)

    def __make_door(self, y, x):
        """
        Создание двери.
        """
        while self.__room_counter < 9:
            direction = random.random()
            if direction < 0.25:
                if x < 2:
                    if self.__doors[y][x + 1]['count'] == 0:
                        self.__room_counter += 1
                    if not self.__doors[y][x]['right']:
                        self.__doors[y][x]['count'] += 1
                        self.__doors[y][x + 1]['count'] += 1
                        self.__doors[y][x]['right'] = True
                        self.__doors[y][x + 1]['left'] = True
                    self.__make_door(y, x + 1)
            elif direction < 0.5:
                if y < 2 and random.random() >= 0.5:
                    if self.__doors[y + 1][x]['count'] == 0:
                        self.__room_counter += 1
                    if not self.__doors[y][x]['down']:
                        self.__doors[y][x]['count'] += 1
                        self.__doors[y + 1][x]['count'] += 1
                        self.__doors[y][x]['down'] = True
                        self.__doors[y + 1][x]['up'] = True
                    self.__make_door(y + 1, x)
            elif direction < 0.75:
                if x > 0 and random.random() >= 0.5:
                    if self.__doors[y][x - 1]['count'] == 0:
                        self.__room_counter += 1
                    if not self.__doors[y][x]['left']:
                        self.__doors[y][x]['count'] += 1
                        self.__doors[y][x - 1]['count'] += 1
                        self.__doors[y][x]['left'] = True
                        self.__doors[y][x - 1]['right'] = True
                    self.__make_door(y, x - 1)
            else:
                if y > 0 and random.random() >= 0.5:
                    if self.__doors[y - 1][x]['count'] == 0:
                        self.__room_counter += 1
                    if not self.__doors[y][x]['up']:
                        self.__doors[y][x]['count'] += 1
                        self.__doors[y - 1][x]['count'] += 1
                        self.__doors[y][x]['up'] = True
                        self.__doors[y - 1][x]['down'] = True
                    self.__make_door(y - 1, x)


    def __add_room(self, y, x, room):
        """
        Добавление комнат в структурную матрицу.
        """
        for i in range(len(room)):
            for j in range(len(room[i])):
                self.__display_struct[y * (self.__step_y + 1) + i]\
                    [x * (self.__step_x + 1) + j] = room[i][j]

    def __cross_corridor(self):
        """
        Создание коридоров.
        """
        for i in range(1, 3):
            status = False
            for j in range(0, (self.__step_y + 1) * 3):
                left = self.__display_struct[j][i * (self.__step_x) + i // 2 - 1]
                right = self.__display_struct[j][i * (self.__step_x) + i // 2 + 1]
                if (left == Const.DOOR or left == Const.CORRIDOR) \
                    and (right == Const.DOOR or right == Const.CORRIDOR):
                    self.__display_struct[j][i * (self.__step_x) + i // 2 ] = Const.CORRIDOR
                elif left == Const.DOOR or left == Const.CORRIDOR \
                    or right == Const.DOOR or right == Const.CORRIDOR:
                    if status:
                        self.__display_struct[j][i * (self.__step_x) + i // 2 ] = Const.CORRIDOR
                    status = True if status == False else False
                if status: self.__display_struct[j][i * (self.__step_x) + i // 2 ] = Const.CORRIDOR
        for i in range(1, 3):
            status = False
            for j in range(0, (self.__step_x + 1) * 3):
                up = self.__display_struct[i * (self.__step_y) + i // 2 - 1][j]
                down = self.__display_struct[i * (self.__step_y) + i // 2 + 1][j]
                if (up == Const.DOOR or up == Const. CORRIDOR) \
                    and (down == Const.DOOR or down == Const. CORRIDOR):
                    self.__display_struct[i * (self.__step_y) + i // 2][j] = Const.CORRIDOR
                elif (up == Const.DOOR or up == Const. CORRIDOR) \
                    or (down == Const.DOOR or down == Const. CORRIDOR):
                    if status:
                        self.__display_struct[i * (self.__step_y) + i // 2][j] = Const.CORRIDOR
                    status = True if status == False else False
                if status:
                    self.__display_struct[i * (self.__step_y) + i // 2][j] = Const.CORRIDOR

    def __add_exit_door(self):
        """
        Добавление в структурную матрицу перехода на следующий уровень.
        """
        y_index = random.randint(0, 2)
        x_index = random.randint(0, 2)
        self.__exit_door_room = [y_index, x_index]
        self.__exit_door_y = self.rooms[y_index][x_index].get_position_y() \
            + (self.__step_y + 1) * y_index
        self.__exit_door_x = self.rooms[y_index][x_index].get_position_x() \
            + (self.__step_x + 1) * x_index
        self.__display_struct[self.__exit_door_y][self.__exit_door_x] = Const.EXIT_DOOR

    def __add_character(self):
        """
        Установка стартовых координат главного героя.
        """
        y_index = random.randint(0, 2)
        x_index = random.randint(0, 2)
        self.__character_start_room = [y_index, x_index]
        if self.__character_start_room == self.__exit_door_room:
            self.__add_character()
        else:
            self.__character_start_y = self.rooms[y_index][x_index].get_position_y() \
                + (self.__step_y + 1) * y_index
            self.__character_start_x = self.rooms[y_index][x_index].get_position_x() \
                + (self.__step_x + 1) * x_index

    def add_active(self, type):
        """
        Добавление элемента на активную матрицу.
        """
        y_index = random.randint(0, 2)
        x_index = random.randint(0, 2)
        while self.__character_start_room == [y_index, x_index]:
            y_index = random.randint(0, 2)
            x_index = random.randint(0, 2)
        pos_y, pos_x = self.rooms[y_index][x_index].get_item_position()
        pos_y += (self.__step_y + 1) * y_index
        pos_x += (self.__step_x + 1) * x_index
        if self.__check_active_position(pos_y, pos_x):
            self.__display_active[pos_y][pos_x] = type
        else:
            pos_y, pos_x = self.add_active(type)
        return [pos_y, pos_x]

    def __check_active_position(self, pos_y, pos_x):
        """
        Проверка на допустимость добавления элемента в активную матрицу.

        Args:
            pos_y (int): Координата по оси Y.
            pos_x (int): Координата по оси X.
        """
        if pos_y != self.__character_start_y and \
            pos_x != self.__character_start_x and \
            self.__display_active[pos_y][pos_x] == Const.NONE and \
            self.__display_struct[pos_y][pos_x] == Const.ROOM_SPACE:
            return True
        else:
            return False

    def enemy_down(self, y, x):
        """
        Удаление элемента из активной матрицу.

        Args:
            y (int): Координата по оси Y.
            x (int): Координата по оси X.
        """
        self.__display_active[y][x] = Const.NONE

    def get_display_struct(self):
        """
        Возвращает структурную матрицу.
        """
        return self.__display_struct
    
    def get_display_active(self):
        """
        Возвращает активную матрицу.
        """
        return self.__display_active

    def set_display_active(self, y, x, value):
        """
        Устанавливает значение по коодинатам в активную матрицу.

        Args:
            y (int): Координата по оси Y.
            x (int): Координата по оси X.
            value (int): Значение.
        """
        self.__display_active[y][x] = value

    def get_start_character_position_y(self):
        """
        Возвращает стартовые координаты главного героя по оси Y.
        """
        return self.__character_start_y

    def get_start_character_position_x(self):
        """
        Возвращает стартовые координаты главного героя по оси X.
        """
        return self.__character_start_x
    
class Level:
    """
    Класс уровня игровой сессии.
    """
    def __init__(self):
        """
        Инициализация уровня.
        """
        self.__level__ = 0

    def get_level(self):
        """
        Возвращает текущий уровень.
        """
        return self.__level__
    
    def level_up(self):
        """
        Увеличивает уровень на 1.
        """
        self.__level__ += 1

class Const:
    """
    Класс констант проекта.
    """

    EMPTY_FIELD = 0
    HORIZONTAL_WALL = 1
    VERTICAL_WALL = 2
    UPPER_LEFT_CORNER = 3
    UPPER_RIGHT_CORNER = 4
    LOWER_LEFT_CORNER = 5
    LOWER_RIGHT_CORNER = 6
    
    ROOM_SPACE = 7
    DOOR = 8
    CORRIDOR = 9

    NONE = 10
    CHARACTER = 11
    ZOMBIE = 12
    VAMPIRE = 13
    GHOST = 14
    OGRE = 15
    SNAKE_MAGICIAN = 16
    MIMIC = 17

    TREASURE = 18
    WEAPON = 19
    ARMOR = 20
    POTION = 21
    SCROLL = 22
    FOOD = 23
    KEY = 24

    EXIT_DOOR = 25

    CONTINUE = 0
    MAIN_MENU = 1
    NEW_GAME = 2
    LOAD_GAME = 3
    SAVE_GAME = 4
    LEADER_BORD = 5
    INFORMATION = 6


    PROCESS = 0
    WIN = 1
    LOSE = 2

    RED = 1
    GREEN = 2
    BLUE = 3
    YELLOW = 4
    BROWN = 5
    GREY = 6
    WHITE = 7

class Room:
    """
    Класс комнаты.
    """
    def __init__(self, height_max, width_max, doors):
        """
        Инициализация комнаты.

        Args:
            height_max (int): Макимальноя высота комнаты.
            width_max (int): Максимальная ширина комнаты.
            doors: Словарь расположения дверей в комнате.
        """
        self.__doors = doors
        self.__room = [[Const.EMPTY_FIELD for _ \
                        in range(width_max)] for _ in range(height_max)]
        self.__generate(height_max - 1, width_max - 1)

    def __generate(self, height_max, width_max):
        """
        Создание комнаты.

        Args:
            height_max (int): Макимальноя высота комнаты.
            width_max (int): Максимальная ширина комнаты.
        """
        self.__height = random.randint(7, height_max)
        self.__width = random.randint(7, width_max)
        self.__y = random.randint(0, height_max - self.__height)
        self.__x = random.randint(0, width_max - self.__width)
        self.__room[self.__y][self.__x] = Const.UPPER_LEFT_CORNER
        self.__room[self.__y][self.__x + self.__width] = Const.UPPER_RIGHT_CORNER
        self.__room[self.__y + self.__height][self.__x] = Const.LOWER_LEFT_CORNER
        self.__room[self.__y + self.__height][self.__x + self.__width] = Const.LOWER_RIGHT_CORNER
        for i in range(self.__y + 1, self.__y + self.__height):
            self.__room[i][self.__x] = Const.VERTICAL_WALL
            self.__room[i][self.__x + self.__width] = Const.VERTICAL_WALL
            for j in range(self.__x + 1, self.__x + self.__width):
                self.__room[i][j] = Const.ROOM_SPACE
        for j in range(self.__x + 1, self.__x + self.__width):
            self.__room[self.__y][j] = Const.HORIZONTAL_WALL
            self.__room[self.__y + self.__height][j] = Const.HORIZONTAL_WALL
        if self.__doors['up']: 
            x_door = random.randint(self.__x + 1, self.__x + self.__width - 1)    
            self.__room[self.__y][x_door] = Const.DOOR
            for i in range(0, self.__y):
                self.__room[i][x_door] = Const.CORRIDOR
        if self.__doors['right']:
            y_door = random.randint(self.__y + 1, self.__y + self.__height - 1)
            self.__room[y_door][self.__x + self.__width] = Const.DOOR
            for i in range(self.__x + self.__width + 1, width_max + 1):
                self.__room[y_door][i] = Const.CORRIDOR
        if self.__doors['down']:
            x_door = random.randint(self.__x + 1, self.__x + self.__width - 1)
            self.__room[self.__y + self.__height][x_door] = Const.DOOR
            for i in range(self.__y + self.__height + 1, height_max + 1):
                self.__room[i][x_door] = Const.CORRIDOR
        if self.__doors['left']:
            y_door = random.randint(self.__y + 1, self.__y + self.__height - 1)
            self.__room[y_door][self.__x] = Const.DOOR
            for i in range(0, self.__x):
                self.__room[y_door][i] = Const.CORRIDOR
        self.__start_y, self.__start_x = self.get_item_position()

    def get_item_position(self):
        """
        Возвращает координаты элемента в комнате.
        """
        y, x = 0, 0
        while True:
            y = random.randint(self.__y + 1, self.__y + self.__height - 1)
            x = random.randint(self.__x + 1, self.__x + self.__width - 1)
            if self.__room[y][x + 1] != Const.DOOR \
                and self.__room[y][x - 1] != Const.DOOR \
                and self.__room[y + 1][x] != Const.DOOR \
                and self.__room[y - 1][x] != Const.DOOR:
                break
        return [y, x]

    def get_position_y(self):
        """
        Возвращает стартовоую позицию героя в комнате по оси Y.
        """
        return self.__start_y

    def get_position_x(self):
        """
        Возвращает стартовоую позицию героя в комнате по оси X.
        """
        return self.__start_x

    def get_room(self):
        """
        Возвращает матрицу комнаты.
        """
        return self.__room

class Character:
    """
    Класс главного героя.
    """
    def __init__(self, y, x):
        """
        Инициализация главного героя.

        Args:
            y (int): Размер игрового поля по оси Y.
            x (int): Размер игрового поля по оси X.
        """
        self.init_position(y, x)
        self.__sleep = False
        self.__radius = 5
        self.__max_hp = 100
        self.__hp = 100
        self.__dexterity = 30
        self.__dexterity_weapon = 0
        self.__dexterity_armor = [{'type': 'helmet', 'dex': 0},\
                                {'type': 'gloves', 'dex': 0},\
                                {'type': 'boots', 'dex': 0},\
                                {'type': 'cuirass', 'dex': 0},\
                                {'type': 'shield', 'dex': 0}]
        self.__strength = 30
        self.__strength_weapon = 0
        self.__max_strength = 50
        self.__armor = 0
        self.__strength_armor = [{'type': 'helmet', 'armor': 0},\
                                {'type': 'gloves', 'armor': 0},\
                                {'type': 'boots', 'armor': 0},\
                                {'type': 'cuirass', 'armor': 0},\
                                {'type': 'shield', 'armor': 0}]
        self.__gold = 0
        self.__experience = 0
        self.__max_experience = 15
        self.init_potions()
        self.__character_name = self.__init_character_name()

    def __init_character_name(self):
        f_name = random.choice(('Frodo', 'Bilbo', 'Legolas', 'Bronn', 'Thaiwin'))
        s_name = random.choice(('Baggins', 'Lannister', 'Darkwather', 'Barateon', 'Jaccoby', 'Soprano', 'Dante'))
        nickname = random.choice(('Big', 'Pig', 'Bastard', 'Great', 'Little'))
        return f"{nickname} {f_name} {s_name}"

    def get_character_name(self):
        return self.__character_name

    def init_potions(self):
        """
        Инициализация эффектов зелий.
        """
        self.potions = {'max HP': 0,\
                        'dexterity': 0,\
                        'strength': 0}
        self.__set_total_max_hp()
        if self.__hp > self.__max_hp_total:
            self.__hp = self.__max_hp_total
        self.__set_total_str()

    def init_position(self, y, x):
        """
        Инициализация матрицы положения героя.
        """
        self.__position = [[Const.EMPTY_FIELD for i in range(x + 1)] for j in range(y + 1)]

    def set_position(self, y, x):
        """
        Установка позиции героя в его матрице положения.

        Args:
            y (int): Координаты героя по оси Y.
            x (int): Координаты героя по оси X.
        """
        self.__position_y = y
        self.__position_x = x
        self.__fog_of_war()
        self.__position[y][x] = Const.CHARACTER

    def get_position(self):
        """
        Возвращает координаты героя.
        """
        return self.__position

    def get_position_y(self):
        """
        Возвращает координаты героя по оси Y.
        """
        return self.__position_y

    def get_position_x(self):
        """
        Возвращает координаты героя по оси X.
        """
        return self.__position_x

    def __fog_of_war(self):
        """
        Задает область видимости вокруг героя.
        """
        for i in range(max(0, self.__position_y - self.__radius), \
                       min(self.__position_y + self.__radius + 1, len(self.__position))):
            for j in range(max(0, self.__position_x - self.__radius), \
                           min(self.__position_x + self.__radius + 1, len(self.__position[i]))):
                if (i - self.__position_y) ** 2 + (j - self.__position_x) ** 2 <= self.__radius ** 2:
                    try:
                        self.__position[i][j] = Const.NONE
                    except:
                        pass

    def move(self, step_y, step_x):
        """
        Задает перемещение главного героя.

        Args:
            step_y (int): Перемещение по оси Y.
            step_x (int): Перемещение по оси X.
        """
        self.__position[self.__position_y][self.__position_x] = Const.NONE
        self.__position_y +=  step_y
        self.__position_x +=  step_x
        self.__fog_of_war()
        self.__position[self.__position_y][self.__position_x] = Const.CHARACTER

    def get_max_hp(self):
        """
        Возвращает максимально здоровье героя.
        """
        return self.__max_hp_total
    
    def get_hp(self):
        """
        Возвращает текущее здоровье героя.
        """
        return self.__hp
    
    def get_dex(self):
        """
        Возвращает ловкость героя.
        """
        return self.__dexterity \
            + self.__dexterity_weapon \
            + sum([i['dex'] for i in self.__dexterity_armor]) \
            + self.potions['dexterity']
    
    def get_str(self):
        """
        Возвращает силу героя.
        """
        return self.__strength_total
    
    def get_max_str(self):
        """
        Возвращает максимальную силу героя.
        """
        return self.__max_strength
    
    def get_armor(self):
        """
        Возвращает броню героя.
        """
        return self.__armor \
            + sum([i['armor'] for i in self.__strength_armor])
    
    def get_gold(self):
        """
        Возвращает золото героя.
        """
        return self.__gold

    def get_experience(self):
        """
        Возвращает опыт героя.
        """
        return self.__experience
    
    def get_max_experience(self):
        """
        Возвращает значение опыта для улучшения героя.
        """
        return self.__max_experience

    def set_heal(self, hp):
        """
        Изменяет здоровье героя.

        Args:
            hp (int): Значение изменения.
        """
        self.__hp += hp
        if self.__hp > self.__max_hp_total: self.__hp = self.__max_hp_total

    def __set_total_str(self):
        """
        Задает итоговое значение силы героя.
        """
        self.__strength_total = self.__strength \
            + self.__strength_weapon \
            + self.potions['strength']
        if self.__strength_total > self.__max_strength:
            self.__strength_total = self.__max_strength
        
    def __set_total_max_hp(self):
        """
        Задает итоговое значение максимального здоровья героя.
        """
        self.__max_hp_total = self.__max_hp \
        + self.potions['max HP']

    def add_max_hp(self, hp):
        """
        Изменяет значения максимального здоровья героя.

        Args:
            hp (int): Значение изменения.
        """
        self.__max_hp += hp
        self.__set_total_max_hp()
        if self.__max_hp_total < 1:
            self.__max_hp = 1
            self.potions['max HP'] = 0
        if self.__hp > self.__max_hp_total: self.__hp = self.__max_hp_total

    def add_str(self, str):
        """        
        Изменяет силу героя.

        Args:
            str (int): Значение изменения.
        """
        self.__strength += str
        if self.__strength < 1:
            self.__strength = 1
            self.potions['strength'] = 0
        self.__set_total_str()
        if self.__strength_total > self.__max_strength:
            self.__strength_total = self.__max_strength

    def add_max_str(self, str):
        """
        Изменяет значения максимальной силы героя.

        Args:
            str (int): Значение изменения.
        """
        self.__max_strength += str
        if self.__max_strength < 1: self.__strength = 1
        self.__set_total_str()

    def set_str_weapon(self, weapon):
        """
        Устанавливает силу оружия и меня пересчитывает суммарную силу героя.
        """
        self.__strength_weapon = weapon
        self.__set_total_str()

    def set_dex_weapon(self, weapon):
        """
        Устанавливает ловкость оружия героя.
        """
        self.__dexterity_weapon = weapon

    def add_dex(self, dex):
        """        
        Изменяет ловкость героя.

        Args:
            dex (int): Значение изменения.
        """
        self.__dexterity += dex
        if self.__dexterity < 1:
            self.__dexterity = 1
            self.potions['dexterity'] = 0

    def set_str_armor(self, armor, type):
        """
        Задает значение показателя брони.

        Args:
            armor (int): Показатель брони.
            type (str): Тип брони.
        """
        for i in self.__strength_armor:
            if i['type'] == type:
                i['armor'] = armor

    def set_dex_armor(self, armor, type):
        """
        Задает ловкости брони.

        Args:
            armor (int): Ловкость брони.
            type (str): Тип брони.
        """
        for i in self.__dexterity_armor:
            if i['type'] == type:
                i['dex'] = armor

    def add_armor(self, armor):
        """
        Изменяет значения брони героя.

        Args:
            armor (int): Значение изменения.
        """
        self.__armor += armor
        if self.__armor < 0: self.__armor = 0

    def damage(self, str, dex):
        """
        Наносит урон герою.

        Args:
            str (int): Сила атакующего.
            dex (int): Ловкость атакующего.
        """
        if self.get_dex() > 0 and ((dex / self.__dexterity) - 1) < random.random():
            if str > self.get_armor():
                self.__hp -= str - self.get_armor()
        else:
            self.__hp -= str

    def add_gold(self, gold):
        """
        Изменяет значения золота героя.

        Args:
            gold (int): Значение изменения.
        """
        self.__gold += gold

    def add_exp(self, exp):
        """
        Изменяет значения опыта героя.

        Args:
            exp (int): Значение изменения.
        """
        self.__experience += exp
        if self.__experience >= self.__max_experience:
            self.__level_up(self.__experience - self.__max_experience)

    def __level_up(self, exp):
        """
        Улучшение героя.

        Args:
            exp (int): Опыт сверх улучшения.
        """
        self.__max_strength += 5
        self.__max_hp += 5
        self.__set_total_max_hp()
        self.__hp = self.__max_hp_total
        self.__max_experience = int(self.__max_experience * 1.2)
        self.__experience = exp
        if self.__experience >= self.__max_experience:
            self.__level_up(self.__experience - self.__max_experience)

    def add_potion_max_hp(self, max_hp):
        """
        Изменеи значения максимального здоровья героя зельем.

        Args:
            max_hp (int): Значение изменения.
        """
        self.potions['max HP'] += max_hp
        self.__set_total_max_hp()

    def add_potion_dex(self, dex):
        """
        Изменеи значения ловкости героя зельем.

        Args:
            dex (int): Значение изменения.
        """
        self.potions['dexterity'] += dex

    def add_potion_str(self, str):
        """
        Изменеи значения силы героя зельем.

        Args:
            str (int): Значение изменения.
        """
        self.potions['strength'] += str
        self.__set_total_str()

    def get_sleep(self):
        """
        Возврацает статус сна.
        """
        return self.__sleep
    
    def set_sleep(self, value):
        """
        Устанавливает статус сна.

        Args:
            value (bool): Статус сна.
        """
        self.__sleep = value

class Inventory:
    """
    Класс инвентаря.
    """
    def __init__(self):
        """
        Инициализация инвентаря.
        """
        self.__weapons = []
        self.__armor = []
        self.__potions = []
        self.__scrolls = []
        self.__food = []

    def add_weapon(self, level):
        """
        Добавление оружия в инвентарь.
        """
        self.__weapons.append(Weapon(level))

    def add_armor(self, level):
        """
        Добавление брони в инвентарь.
        """
        self.__armor.append(Armor(level))

    def add_potion(self, level):
        """
        Добавление зелья в инвентарь.
        """
        self.__potions.append(Potion(level))

    def add_scroll(self, level):
        """
        Добавление оружисвитка в инвентарь.
        """
        self.__scrolls.append(Scroll(level))

    def add_food(self, level):
        """
        Добавление еды в инвентарь.
        """
        self.__food.append(Food(level))

    def get_weapons_list(self):
        """
        Возвращает список оружия.
        """
        list = []
        for weapon in self.__weapons:
            list.append(f'{'(√)' if weapon.check_select() else '( )'}\
  {weapon.get_name()};\
 strength: {weapon.get_str()};\
 dexterity: {weapon.get_dex()};\
 price: {weapon.get_price()}')
        return list
    
    def get_weapons(self):
        """
        Возвращает массив оружия.
        """
        return self.__weapons

    def get_armor_list(self):
        """
        Возвращает список брони.
        """
        list = []
        for armor in self.__armor:
            list.append(f'{'(√)' if armor.check_select() else '( )'}\
  {armor.get_name()};\
 armor: {armor.get_armor()};\
 dexterity: {armor.get_dex()};\
 price: {armor.get_price()}')
        return list
    
    def get_armor(self):
        """
        Возвращает массив брони.
        """
        return self.__armor

    def get_potions_list(self):
        """
        Возвращает список зелий.
        """
        list = []
        for potion in self.__potions:
            list.append(f'{potion.get_name()};\
 effect: {potion.get_effect()};\
 power: {potion.get_power()};\
 price: {potion.get_price()}')
        return list
    
    def get_potions(self):
        """
        Возвращает массив зелий.
        """
        return self.__potions

    def del_potion(self, pos):
        """
        Удаляет зелье из массива.

        Args:
            pos (int): Позиция в массиве.
        """
        self.__potions.pop(pos)

    def get_scrolls_list(self):
        """
        Возвращает список свитков.
        """
        list = []
        for scroll in self.__scrolls:
            list.append(f'{scroll.get_name()};\
 effect: {scroll.get_effect()};\
 power: {scroll.get_power()};\
 price: {scroll.get_price()}')
        return list

    def get_scrolls(self):
        """
        Возвращает массив свитков.
        """
        return self.__scrolls

    def del_scroll(self, pos):
        """
        Удаляет свиток из массива.

        Args:
            pos (int): Позиция в массиве.
        """
        self.__scrolls.pop(pos)
    
    def get_food_list(self):
        """
        Возвращает список еды.
        """
        list = []
        for food in self.__food:
            list.append(f'{food.get_name()};\
 heal: {food.get_power()};\
 price: {food.get_price()}')
        return list
    
    def get_food(self):
        """
        Возвращает массив еды.
        """
        return self.__food

    def del_food(self, pos):
        """
        Удаляет еду из массива.

        Args:
            pos (int): Позиция в массиве.
        """
        self.__food.pop(pos)

class Enemy:
    """
    Класс монстров.
    """

    def __init__(self, type, pos):
        """
        Инициализация монстра.

        Args:
            type (int): Тип монстра.
            pos: координаты монстра.
        """
        self.__type = type
        self.__position = pos
        self.__first_damage = True
        self.__visibility = False
        self.__rest = False
        match type:
            case Const.ZOMBIE:
                self.__hp = 120
                self.__dexterity = 20
                self.__strength = 40
                self.__armor = 0
                self.__hostility = 5
                self.__gold = random.randint(3, 6)
                self.__experience = 10
            case Const.VAMPIRE:
                self.__hp = 120
                self.__dexterity = 120
                self.__strength = 40
                self.__armor = 5
                self.__hostility = 7
                self.__gold = random.randint(14, 28)
                self.__experience = 15
            case Const.GHOST:
                self.__hp = 40
                self.__dexterity = 120
                self.__strength = 20
                self.__armor = 10
                self.__hostility = 3
                self.__gold = random.randint(18, 36)
                self.__experience = 20
            case Const.OGRE:
                self.__hp = 160
                self.__dexterity = 20
                self.__strength = 80
                self.__armor = 20
                self.__hostility = 5
                self.__gold = random.randint(24, 48)
                self.__experience = 30
            case Const.SNAKE_MAGICIAN:
                self.__hp = 80
                self.__dexterity = 60
                self.__strength = 40
                self.__armor = 10
                self.__hostility = 9
                self.__gold = random.randint(30, 60)
                self.__experience = 25
            case Const.MIMIC:
                self.__hp = 120
                self.__dexterity = 80
                self.__strength = 20
                self.__armor = 0
                self.__hostility = 3
                self.__gold = random.randint(36, 72)
                self.__experience = 10

    def get_type(self):
        """
        Возвращает тип монстра.
        """
        return self.__type

    def get_max_hp(self):
        """
        Возвращает максимальное здоровье монстра.
        """
        return self.__max_hp
    
    def get_hp(self):
        """
        Возвращает здоровье монстра.
        """
        return self.__hp
    
    def get_dex(self):
        """
        Возвращает ловкость монстра.
        """
        return self.__dexterity
    
    def get_str(self):
        """
        Возвращает силу монстра.
        """
        return self.__strength
    
    def get_hostility(self):
        """
        Возвращает агрессивность монстра.
        """
        return self.__hostility

    def set_pos(self, pos):
        """
        Задает координаты монстра.
        """
        self.__position = pos

    def get_pos(self):
        """
        Возвращает координаты монстра.
        """
        return self.__position

    def damage(self, str, dex):
        """
        Наносит урон монстру.

        Args:
            str (int): Сила атакующего.
            dex (int): Ловкость атакующего.
        """
        if self.__type != Const.VAMPIRE or \
        self.__first_damage == False:
            if ((dex / self.__dexterity) - 1) < random.random():
                if str > self.__armor:
                    self.__hp -= str - self.__armor
            else:
                self.__hp -= str
        self.__first_damage = False

    def check_range(self, y, x):
        """
        Пвроверяет входят ли координаты в радиус агрессии монстра.

        Args:
            y (int): Координата по оси Y.
            x (int): Координата по оси X.
        """
        return ((y - self.__position[0]) ** 2 + (x - self.__position[1]) ** 2) <= (self.__hostility ** 2)

    def get_gold(self):
        """
        Возвращает золото монстра.
        """
        return self.__gold

    def get_exp(self):
        """
        Возвращает опыт за монстра.
        """
        return self.__experience
    
    def visibility_on(self):
        """
        Включает невидимость призрака.
        """
        self.__visibility = True

    def visibility_off(self):
        """
        Выключает невидимость призрака.
        """
        self.__visibility = False

    def get_visibility(self):
        """
        Возвращает невидимость.
        """
        return self.__visibility
    
    def get_rest(self):
        """
        Возвращает статус отдыха.
        """
        return self.__rest
    
    def set_rest(self, value):
        """
        Устанавливает статус отдыха.

        Args:
            value (bool): Статус отдыха.    
        """
        self.__rest = value
    
class Weapon:
    """
    Класс оружия.
    """
    def __init__(self, level):
        """
        Инициализация оружия.
        """
        self.__select = False
        self.__type = random.choice(['knife', 'sword', 'axe', 'hammer', 'spear'])
        self.__material_list = ['wooden ']
        self.__grade_list = ['Broken ', 'Simple ']
        if level > 4: 
            self.__material_list.append('bronze ')
        if level > 5: 
            self.__grade_list.append('Improved ')
        if level > 8: 
            self.__material_list.append('iron ')
        if level > 10: 
            self.__grade_list.append('Great ')
        if level > 12: 
            self.__material_list.append('steel ')
        if level > 15: 
            self.__grade_list.append('Ideal ')
        if level > 16: 
            self.__material_list.append('adamantine ')
        match self.__type:
            case 'knife':
                self.__strength = 10
                self.__dexterity = -5
            case 'sword':
                self.__strength = 20
                self.__dexterity = -10
            case 'axe':
                self.__strength = 24
                self.__dexterity = -12
            case 'hammer':
                self.__strength = 40
                self.__dexterity = -20
            case 'spear':
                self.__strength = 30
                self.__dexterity = -15
        self.__material = random.choice(self.__material_list)
        match self.__material:
            case 'bronze ':
                self.__strength += 5
            case 'iron ':
                self.__strength += 10
            case 'steel ':
                self.__strength += 15
            case 'adamantine ':
                self.__strength += 20
        self.__grade = random.choice(self.__grade_list)
        match self.__grade:
            case 'Broken ':
                self.__strength = int(self.__strength * 0.7)
            case 'Improved ':
                self.__strength = int(self.__strength * 1.3)
            case 'Great ':
                self.__strength = int(self.__strength * 1.6)
            case 'Ideal ':
                self.__strength = int(self.__strength * 2)
        self.__name = self.__grade + self.__material + self.__type
        self.__price = (self.__strength + self.__dexterity) * 2

    def check_select(self):
        """
        Проверяет используется ли оружие.
        """
        return self.__select
    
    def unuse(self):
        """
        Снимает оружие.
        """
        self.__select = False

    def use(self):
        """
        Использует оружие.
        """
        self.__select = True
    
    def get_name(self):
        """
        Возвращает название оружия.
        """
        return self.__name
    
    def get_type(self):
        """
        Возвращает тип оружия.
        """
        return self.__type

    def get_str(self):
        """
        Возвращает силу оружия.
        """
        return self.__strength
    
    def get_dex(self):
        """
        Возвращает ловкость оружия.
        """
        return self.__dexterity
    
    def get_price(self):
        """
        Возвращает стоимость оружия.
        """
        return self.__price
    
class Armor:
    """
    Класс брони.
    """
    def __init__(self, level):
        """
        Инициализирует броню.
        """
        self.__select = False
        self.__type = random.choice(['helmet', 'gloves', 'boots', 'cuirass', 'shield'])
        self.__material_list = ['leather ']
        self.__grade_list = ['Broken ', 'Simple ']
        if level > 4: 
            self.__material_list.append('bone ')
        if level > 5: 
            self.__grade_list.append('Improved ')
        if level > 8: 
            self.__material_list.append('chainmail ')
        if level > 10: 
            self.__grade_list.append('Great ')
        if level > 12: 
            self.__material_list.append('plate ')
        if level > 15: 
            self.__grade_list.append('Ideal ')
        if level > 16: 
            self.__material_list.append('adamantine ')
        self.__material = random.choice(self.__material_list)
        self.__grade = random.choice(self.__grade_list)
        match self.__type:
            case 'helmet':
                self.__armor = 3
                self.__dexterity = -1
            case 'gloves':
                self.__armor = 2
                self.__dexterity = -1
            case 'boots':
                self.__armor = 2
                self.__dexterity = -1
            case 'cuirass':
                self.__armor = 10
                self.__dexterity = -5
            case 'shield':
                self.__armor = 5
                self.__dexterity = -3
        match self.__material:
            case 'bone ':
                self.__armor += 1
                self.__dexterity -= 1
            case 'chainmail ':
                self.__armor += 3
                self.__dexterity -= 2
            case 'plate ':
                self.__armor += 5
                self.__dexterity -= 3
            case 'adamantine ':
                self.__armor += 7
                self.__dexterity -= 4
        match self.__grade:
            case 'Broken ':
                self.__armor = int(self.__armor * 0.7)
            case 'Improved ':
                self.__armor = int(self.__armor * 1.3)
            case 'Great ':
                self.__armor = int(self.__armor * 1.6)
            case 'Ideal ':
                self.__armor = int(self.__armor * 2)
        self.__name = self.__grade + self.__material + self.__type
        self.__price = (self.__armor + self.__dexterity) * 2

    def check_select(self):
        """
        Проверяет используется ли броня.
        """
        return self.__select
    
    def unuse(self):
        """
        Снимает броню.
        """
        self.__select = False

    def use(self):
        """
        Надевает броню.
        """
        self.__select = True
    
    def get_name(self):
        """
        Возвращает название брони.
        """
        return self.__name
    
    def get_type(self):
        """
        Возвращает тип брони.
        """
        return self.__type
    
    def get_armor(self):
        """
        Возвращает мощность брони.
        """
        return self.__armor
    
    def get_dex(self):
        """
        Возвращает ловкость брони.
        """
        return self.__dexterity
    
    def get_price(self):
        """
        Возвращает стоимость брони.
        """
        return self.__price
    
class Potion:
    """
    Класс зелий.
    """
    def __init__(self, level):
        """
        Инициализация зелья.
        """
        self.__grade_list = ['Weak ', 'Simple ']
        if level > 5: 
            self.__grade_list.append('Improved ')
        if level > 10: 
            self.__grade_list.append('Great ')
        if level > 15: 
            self.__grade_list.append('Ideal ')
        self.__grade = random.choice(self.__grade_list)
        match self.__grade:
            case 'Weak ':
                self.__power = 1
            case 'Simple ':
                self.__power = 3
            case 'Improved ':
                self.__power = 5
            case 'Great ':
                self.__power = 9
            case 'Ideal ':
                self.__power = 15
        self.__effect = random.choice(['HP',\
                                    'max HP',\
                                    'dexterity',\
                                    'strength'])
        match self.__effect:
            case 'HP':
                self.__power *= 5
                self.__price = self.__power * 5
            case 'max HP':
                self.__power *= 3
                self.__price = self.__power * 3
            case 'dexterity':
                self.__price = self.__power * 5
            case 'strength':
                self.__price = self.__power * 5
        self.__name = self.__grade + self.__effect + ' potion'
    
    def get_name(self):
        """
        Возвращает название зелья.
        """
        return self.__name
    
    def get_effect(self):
        """
        Возвращает эффект зелья.
        """
        return self.__effect
    
    def get_power(self):
        """
        Возвращает мощность зелья.
        """
        return self.__power
    
    def get_price(self):
        """
        Возвращает стоимость зелья.
        """
        return self.__price
    
class Scroll:
    """
    Класс свитков.
    """
    def __init__(self, level):
        """
        Инициализация свитка.
        """
        self.__chaotic = True if random.random() < 0.25 else False
        self.__grade_list = ['Weak ', 'Simple ']
        if level > 5: 
            self.__grade_list.append('Improved ')
        if level > 10: 
            self.__grade_list.append('Great ')
        if level > 15: 
            self.__grade_list.append('Ideal ')
        self.__grade = random.choice(self.__grade_list)
        match self.__grade:
            case 'Weak ':
                self.__power = 3
            case 'Simple ':
                self.__power = 5
            case 'Improved ':
                self.__power = 9
            case 'Great ':
                self.__power = 15
            case 'Ideal ':
                self.__power = 25
        self.__effect = random.choice(['armor',\
                                    'max HP',\
                                    'dexterity',\
                                    'strength',\
                                    'max strength'])
        match self.__effect:
            case 'armor':
                self.__price = self.__power * 5
            case 'max HP':
                self.__price = self.__power * 3
            case 'dexterity':
                self.__price = self.__power * 3
            case 'strength':
                self.__price = self.__power * 3
            case 'max strength':
                self.__price = self.__power * 5
        self.__name = self.__grade + self.__effect + ' scroll'

    def check_chaotic(self):
        """
        Проверяет свиток на хаотичность.
        """
        return self.__chaotic
    
    def get_name(self):
        """
        Возвращает имя свитка.
        """
        return self.__name
    
    def get_effect(self):
        """
        Возвращает эффект свитка.
        """
        return self.__effect
    
    def get_power(self):
        """
        Возвращает мощность свитка.
        """
        return self.__power
    
    def get_price(self):
        """
        Возвращает стоимость свитка.
        """
        return self.__price

class Food:
    """
    Класс еды.
    """
    def __init__(self, level):
        """
        Инициализация еды.
        """
        self.__name_list = ['Apple', 'Egg']
        if level > 5: 
            self.__name_list.append('Cheese')
        if level > 10: 
            self.__name_list.append('Chicken')
        if level > 15: 
            self.__name_list.append('Steak')
        self.__name = random.choice(self.__name_list)
        match self.__name:
            case 'Apple':
                self.__power = 10
            case 'Egg':
                self.__power = 15
            case 'Cheese':
                self.__power = 25
            case 'Chicken':
                self.__power = 35
            case 'Steak':
                self.__power = 50
        self.__price = self.__power * 2

    def get_name(self):
        """
        Возвращает название еды.
        """
        return self.__name
    
    def get_power(self):
        """
        Возвращает мощность еды.
        """
        return self.__power
    
    def get_price(self):
        """
        Возвращает стоимость еды.
        """
        return self.__price
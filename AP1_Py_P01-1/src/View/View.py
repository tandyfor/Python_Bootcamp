import curses
import time
import sys
import os

import random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Data')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Session')))
from Data import Const
from Session import Gaming_session, Datalayer

class View:
    """
    Класс визуализации.
    """
                                                 
    def __init__(self, stdscr):
        self.__init_screen(stdscr)
        self.__init_colors()
        self.__running = True 
        self.__init_saves()
        self.__menu_status = Const.MAIN_MENU
        self.__session_status = False
        self.__run()

    def __init_saves(self):
        """
        Создает директорию для сохранений.
        """
        self.__save_dir = '../saves/'
        os.makedirs(self.__save_dir, exist_ok=True)  

    def __init_screen(self, stdscr):
        """
        Инициализирует экран приложения.
        """
        curses.noecho()
        curses.curs_set(0)
        while True:
            self.__screen = stdscr
            self.__screen.keypad(True)
            self.__y_max, self.__x_max = self.__screen.getmaxyx()
            self.__y_max -= 1
            self.__x_max -= 1
            if self.__y_max >= 32 and self.__x_max >= 90:
                break
            else:
                self.__screen.clear()
                self.__screen.addstr(self.__y_max // 2, (self.__x_max - 16) // 2, 'too small screen')
                self.__screen.refresh()
                self.__screen.getch()        
        self.__display_start_y = 0 if self.__y_max <= 32 else (self.__y_max - 32) // 2
        self.__display_start_x = 0 if self.__x_max <= 90 else (self.__x_max - 90) // 2

    def __init_colors(self):
        """
        Инициализация цветовых пар.
        """
        curses.start_color()
        curses.init_pair(Const.RED, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(Const.GREEN, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(Const.BLUE, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(Const.YELLOW, 227, curses.COLOR_BLACK)
        curses.init_pair(Const.BROWN, 137, curses.COLOR_BLACK)
        curses.init_pair(Const.GREY, 248, curses.COLOR_BLACK)
        curses.init_pair(Const.WHITE, curses.COLOR_WHITE, curses.COLOR_BLACK)

    def __run(self):
        """
        Запускает визуализацию приложения.
        """
        while self.__running:
            match self.__menu_status:
                case Const.CONTINUE:
                    self.__continue_session()
                case Const.MAIN_MENU:
                    self.__main_menu()
                case Const.NEW_GAME:
                    self.__new_game()
                case Const.LOAD_GAME:
                    self.__load_game(0)
                case Const.SAVE_GAME:
                    self.__save_game()
                case Const.LEADER_BORD:
                    self.__leader_bord(0)
                case Const.INFORMATION:
                    self.__info(0)
    # Menu

    def __main_menu(self):
        """
        Вывод главного меню приложения.
        """
        self.__screen.clear()
        choises = ['NEW GAME', '', 'LOAD GAME', 'SAVE GAME', 'LEADER BORD', 'INFORMATION', '', 'EXIT']
        position = 0
        if self.__session_status:
            choises[1] = 'CONTINUE'
            position = 1
        status = self.__displaying_menu_lines(choises, position)
        self.__screen.refresh()
        match status:
            case 0:
                self.__menu_status = Const.NEW_GAME
            case 1:
                self.__menu_status = Const.CONTINUE
            case 2:
                self.__menu_status = Const.LOAD_GAME
            case 3:
                self.__menu_status = Const.SAVE_GAME
            case 4:
                self.__menu_status = Const.LEADER_BORD
            case 5:
                self.__menu_status = Const.INFORMATION
            case 7:
                self.__running = False

    def __continue_session(self):
        """
        Возобновление текущей сессии.
        """
        self.__screen.clear()
        self.__display_session()

    def __new_game(self):
        """
        Создание и запуск новой сессии.
        """
        self.__start_time = time.time()
        self.__gaming_session = Gaming_session(30, 90)
        self.__session_status = True
        self.__screen.clear()
        self.__display_session()
        
    def __load_game(self, position):
        """
        Загрузка и запуск сохраненной сессии.
        """ 
        self.__screen.clear()
        self.__border('LOAD GAME', 0, 'press "q" for esc')
        max_size = self.__y_max - 3
        items = os.listdir(self.__save_dir)
        save_list = sorted([item for item in items if os.path.isfile(os.path.join(self.__save_dir, item))], reverse=True)
        if len(save_list) > 0:
            start_x = (self.__x_max + 2 - max([len(i) for i in save_list])) // 2
            start_y = (self.__y_max - len(save_list) + 1) // 2
            if start_y < 2:
                start_y = 2
            while True:
                for y in range(1, self.__y_max):
                    for x in range(1, self.__x_max):
                        self.__screen.addch(y, x, ' ')
                if len(save_list) == 0:
                    self.__screen.addstr(2, 2, 'No saves')
                elif len(save_list) > max_size:
                    if position < max_size:
                        sup_list = save_list[:max_size]
                        for line in range(len(sup_list)):
                            if line == position:
                                self.__screen.addstr(line + start_y, start_x, os.path.splitext(sup_list[line])[0], curses.A_REVERSE)
                            else:
                                self.__screen.addstr(line + start_y, start_x, os.path.splitext(sup_list[line])[0])
                    else:
                        sup_pos = position - max_size + 1
                        sup_list = save_list[sup_pos: max_size + sup_pos]
                        for line in range(len(sup_list)):
                            if line  == max_size - 1:
                                self.__screen.addstr(line + start_y, start_x, os.path.splitext(sup_list[line])[0], curses.A_REVERSE)
                            else:
                                self.__screen.addstr(line + start_y, start_x, os.path.splitext(sup_list[line])[0])
                else:
                    for line in range(len(save_list)):
                        if line == position:
                            self.__screen.addstr(line + start_y, start_x, os.path.splitext(save_list[line])[0], curses.A_REVERSE)
                        else:
                            self.__screen.addstr(line + start_y, start_x, os.path.splitext(save_list[line])[0])
                match self.__screen.getkey():
                    case 'q':
                        self.__menu_status = Const.MAIN_MENU
                        break
                    case 'Q':
                        self.__menu_status = Const.MAIN_MENU
                        break
                    case '\n':
                        self.__gaming_session = Datalayer.load(save_list[position])
                        self.__session_status = True
                        self.__screen.clear()
                        self.__display_session()
                        break
                    case 'KEY_UP':
                        position -= 1
                        if position < 0 :
                            position = len(save_list) - 1
                    case 'KEY_DOWN':
                        position += 1
                        if position > len(save_list) - 1 :
                            position = 0
                    case 'KEY_RESIZE':
                        self.__init_screen(self.__screen)
                        self.__screen.clear()
                        self.__load_game(position)
                        break
        else:
            self.__screen.addstr(2, 2, "No saves")
            match self.__screen.getkey():
                case 'q':
                    self.__menu_status = Const.MAIN_MENU
                case 'Q':
                    self.__menu_status = Const.MAIN_MENU
                case 'KEY_RESIZE':
                    self.__init_screen(self.__screen)
                    self.__screen.clear()
                    self.__load_game()

    def __save_game(self):
        """
        Сохранение текущей сессии.
        """
        self.__screen.clear()
        self.__border('SAVE GAME', 0, 'press any key for esc')
        message = ''
        if self.__session_status:
            self.__gaming_session.datalayer.save()
            message = 'Game saved'
        else:
            message = 'No active game to save!'
        self.__screen.addstr(self.__y_max // 2, (self.__x_max - len(message)) // 2, message)
        self.__screen.refresh()
        self.__menu_status = Const.MAIN_MENU
        self.__screen.getkey()

    def __leader_bord(self, position):
        """
        Вывод на экран таблицу лидеров.
        """
        self.__border('LEADER BORD', 0, 'press "q" for esc')
        leader_list = Datalayer.get_leader_list()
        while True:
            for y in range(1, self.__y_max):
                for x in range(1, self.__x_max):
                    self.__screen.addch(y, x, ' ')
            if leader_list:
                message_list = []
                for i in range(len(leader_list)):
                    message_list.append(f"name: {leader_list[i][0]} level: {\
                        leader_list[i][1]} total: {leader_list[i][2]}")
                max_size = self.__y_max - 3
                start_y = (self.__y_max - len(message_list) + 1) // 2
                if start_y < 2:
                    start_y = 2
                start_x = (self.__x_max + 2 - max([len(i) for i in message_list])) // 2
                if len(message_list) > max_size:
                    if position < max_size:
                        sup_list = message_list[:max_size]
                        for line in range(len(sup_list)):
                            if line == position:
                                self.__screen.addstr(line + start_y, start_x, sup_list[line], curses.A_REVERSE)
                            else:
                                self.__screen.addstr(line + start_y, start_x, sup_list[line])
                    else:
                        sup_pos = position - max_size + 1
                        sup_list = message_list[sup_pos: max_size + sup_pos]
                        for line in range(len(sup_list)):
                            if line  == max_size - 1:
                                self.__screen.addstr(line + start_y, start_x, sup_list[line], curses.A_REVERSE)
                            else:
                                self.__screen.addstr(line + start_y, start_x, sup_list[line])
                else:
                    for line in range(len(message_list)):
                        if line == position:
                            self.__screen.addstr(start_y + line, start_x, message_list[line], curses.A_REVERSE)
                        else:
                            self.__screen.addstr(start_y + line, start_x, message_list[line])
            else:
                message = 'No results'
                self.__screen.addstr(self.__y_max // 2, (self.__x_max - len(message)) // 2, message)
            match self.__screen.getkey():
                case '\n':
                    if leader_list:
                        self.__leader(leader_list[position][0])                        
                        self.__border('LEADER BORD', 0, 'press "q" for esc')
                case 'q':
                    self.__menu_status = Const.MAIN_MENU
                    break
                case 'Q':
                    self.__menu_status = Const.MAIN_MENU
                    break
                case 'KEY_UP':
                    if leader_list:
                        position -= 1
                        if position < 0 :
                            position = len(leader_list) - 1
                case 'KEY_DOWN':
                    if leader_list:
                        position += 1
                        if position > len(leader_list) - 1 :
                            position = 0
                case 'KEY_RESIZE':
                    self.__init_screen(self.__screen)
                    self.__screen.clear()
                    self.__leader_bord(position)
                    break

    def __leader(self, name):
        """
        Вывод информацию о выбранном прохождении.
        """
        self.__screen.clear()
        self.__border(name, 0, 'press any key for esc')
        output = Datalayer.get_results(name)
        start_y = (self.__y_max - len(output)) // 2
        start_x = (self.__x_max - max(len(i) for i in output)) // 2
        for i in range(len(output)):
            self.__screen.addstr(start_y + i, start_x, output[i])
        self.__screen.getkey()

    def __display_session(self):
        """
        Вывод на экран текущей сессии.
        """
        while True:
            start_time = time.time()
            self.__display(self.__gaming_session.get_display())
            self.__display(self.__gaming_session.get_active())
            self.__display(self.__gaming_session.get_character_position())
            self.__characteristics(False)
            self.__screen.refresh()
            status = Const.PROCESS
            match self.__screen.getkey():
                case '\n':
                    self.__menu_status = Const.MAIN_MENU
                    break
                case 'd':
                    status = self.__gaming_session.move(0, 1)
                case 'a':
                    status = self.__gaming_session.move(0, -1)
                case 'w':
                    status = self.__gaming_session.move(-1, 0)
                case 's':
                    status = self.__gaming_session.move(1, 0)
                case 'KEY_RIGHT':
                    status = self.__gaming_session.move(0, 1)
                case 'KEY_LEFT':
                    status = self.__gaming_session.move(0, -1)
                case 'KEY_UP':
                    status = self.__gaming_session.move(-1, 0)
                case 'KEY_DOWN':
                    status = self.__gaming_session.move(1, 0)
                case 'i':
                    self.__inventory(0, 0)
                case 'KEY_F(5)':
                    self.__gaming_session.datalayer.quick_save()
                case 'KEY_F(9)':
                    if os.path.exists('../saves/quick_save.json'):
                        self.__gaming_session = Datalayer.load('quick_save.json')
                        self.__session_status = True
                        self.__screen.clear()
                        self.__display_session()
                        break
                case 'KEY_RESIZE':
                    self.__init_screen(self.__screen)
                    self.__screen.clear()
                    self.__display_session()
                    break
            match status:
                case Const.LOSE:
                    self.__lose()
                    break
                case Const.WIN:
                    self.__win()
                    break
            self.__gaming_session.update_run_time(time.time() - start_time)
                

    def __statistics(self, str):
        """
        Вывод статистики сессии.
        """
        self.__screen.clear()
        output = (str, '') + self.__gaming_session.get_statistics()
        start_y = (self.__y_max - len(output)) // 2
        start_x = (self.__x_max - max(len(i) for i in output)) // 2
        for i in range(len(output)):
            self.__screen.addstr(start_y + i, start_x if i != 0 else \
                                 (self.__x_max - len(output[i])) // 2, output[i])
        self.__menu_status = Const.MAIN_MENU
        self.__session_status = False
        self.__screen.getkey()

    def __lose(self):
        """
        Вывод экрана проигрыша.
        """
        self.__statistics('You are dead!')

    def __win(self):
        """
        Вывод экрана выигрыша.
        """
        self.__statistics('Congratulations! You win!')

    def __inventory(self, tab_position, item_position):
        """
        Вывод на экран инвенторя.
        """
        tab = ['WEAPONS', 'ARMOR', 'POTIONS', 'SCROLLS', 'FOOD']
        while True:
            self.__border('INVENTORY', 2, 'press "i" for esc')
            self.__characteristics(True)
            self.__tabs(tab_position, tab)
            self.__inventory_items(item_position, tab[tab_position], 0)        
            self.__screen.refresh()
            match self.__screen.getkey():
                case 'i':
                    self.__screen.clear()
                    self.__menu_status = Const.CONTINUE
                    break
                case 'KEY_LEFT':
                    tab_position -= 1
                    if tab_position < 0: tab_position = len(tab) - 1
                    item_position = 0
                    item_position = self.__inventory_items(item_position, tab[tab_position], 0)
                case 'KEY_RIGHT':
                    tab_position += 1
                    if tab_position > len(tab) - 1: tab_position = 0
                    item_position = 0
                    item_position = self.__inventory_items(item_position, tab[tab_position], 0)
                case 'KEY_UP':
                    item_position = self.__inventory_items(item_position, tab[tab_position], -1)
                case 'KEY_DOWN':
                    item_position = self.__inventory_items(item_position, tab[tab_position], 1)
                case '\n':
                    item_position = self.__use(tab[tab_position], item_position)
                case 'KEY_RESIZE':
                    self.__init_screen(self.__screen)
                    self.__screen.clear()
                    self.__inventory(tab_position, item_position)
                    break

    def __border(self, name, step_y, esc):
        """
        Выводит на экран рамку с названием.

        Args:
            name (str): Название.
            step_y (int): Отступ края рамки от нижней границы экрана по оси Y.
            esc (str): Кнопка выхода.
        """
        if step_y < 0: step_y = 0
        if step_y > self. __y_max - 2: step_y = self. __y_max - 2
        for i in range (1, self.__y_max - step_y):
            for j in range (1, self.__x_max):
                self.__screen.addch(i, j, ' ')
        for i in range (1, self.__y_max - step_y):
            self.__screen.addch(i, 0, '║', curses.color_pair(Const.BROWN))
            self.__screen.addch(i, self.__x_max, '║', curses.color_pair(Const.BROWN))
        for i in range (1, self.__x_max):
            self.__screen.addch(0, i, '═', curses.color_pair(Const.BROWN))
            self.__screen.addch(self.__y_max - step_y, i, '═', curses.color_pair(Const.BROWN))
        self.__screen.addch(0, 0, '╔', curses.color_pair(Const.BROWN))
        self.__screen.addch(0, self.__x_max, '╗', curses.color_pair(Const.BROWN))
        self.__screen.addch(self.__y_max - step_y, 0, '╚', curses.color_pair(Const.BROWN))
        try:
            self.__screen.addch(self.__y_max - step_y, self.__x_max, '╝', curses.color_pair(Const.BROWN))
        except:
            pass
        self.__screen.addstr(0, 2, name, curses.color_pair(Const.BROWN))
        self.__screen.addstr(self.__y_max - step_y, 2, esc, curses.color_pair(Const.BROWN))

    def __tabs(self, select, tab):
        """
        Вывод горизонтальных вкладок.

        Args:
            select (int): Выбранная позиция в списке вкладок.
            tab (str): Список вкладок.
        """
        step_x = (self.__x_max - 2) // len(tab)
        start_x = (self.__x_max + 2 - len(tab[-1]) - step_x * (len(tab) - 1)) // 2
        for col in range(len(tab)):
            if col == select:
                self.__screen.addstr(1, start_x + step_x * col, tab[col], curses.color_pair(Const.BROWN))
            else:
                self.__screen.addstr(1, start_x + step_x * col, tab[col], curses.color_pair(Const.GREY))

    def __inventory_items(self, position, list_name, step):
        """
        Выводит на экран содержание категории инвентаря.

        Args:
            position (int): Выбранная позиция в списке отображаемой категории.
            list_name (str): Список категорий.
            step (int): Расстояние по оси X между первыми символами названий категорий.
        """
        list = []
        max_size = self.__y_max - 5
        match list_name:
            case 'WEAPONS':
                list = self.__gaming_session.get_weapons_list()
            case 'ARMOR':
                list = self.__gaming_session.get_armor_list()
            case 'POTIONS':
                list = self.__gaming_session.get_potions_list()
            case 'SCROLLS':
                list = self.__gaming_session.get_scrolls_list()
            case 'FOOD':
                list = self.__gaming_session.get_food_list()

        if len(list) == 0:
            self.__screen.addstr(3, 2, "it's empty for now")
            return 0
        if len(list) > max_size:
            if position < max_size - 1:
                sup_list = list[:max_size]
                for line in range(len(sup_list)):
                    if line + step == position:
                        self.__screen.addstr(line + 3, 2, sup_list[line], curses.A_REVERSE)
                    else:
                        self.__screen.addstr(line + 3, 2, sup_list[line])
                return self.__change_line_position(step, position, list)
            else:
                sup_pos = position - max_size + 1
                sup_list = list[sup_pos: max_size + sup_pos]
                for line in range(len(sup_list)):
                    if line  == max_size - 1:
                        self.__screen.addstr(line + 3, 2, sup_list[line], curses.A_REVERSE)
                    else:
                        self.__screen.addstr(line + 3, 2, sup_list[line])
                return self.__change_line_position(step, position, list)
        else:
            for line in range(len(list)):
                if line + step == position:
                    self.__screen.addstr(line + 3, 2, list[line], curses.A_REVERSE)
                else:
                    self.__screen.addstr(line + 3, 2, list[line])
            return self.__change_line_position(step, position, list)
        
    def __use(self, tab, pos):
        """
        Использует выбранный предмет.

        Args:
            tab (str): Выбранная категория.
            pos (int): Позиция в списке выбранной категории.
        """
        match tab:
            case 'WEAPONS':
                self.__use_weapon(pos)
            case 'ARMOR':
                self.__use_armor(pos)
            case 'POTIONS':
                pos = self.__use_potion(pos)
            case 'SCROLLS':
                pos = self.__use_scroll(pos)
            case 'FOOD':
                pos = self.__use_food(pos)
        return pos

    def __use_weapon(self, pos):
        """
        Использование оружия.
        """
        self.__gaming_session.use_weapon(pos)

    def __use_armor(self, pos):
        """
        Использование брони.
        """
        self.__gaming_session.use_armor(pos)

    def __use_potion(self, pos):
        """
        Использование зелья.
        """
        if pos >= self.__gaming_session.use_potion(pos):
            pos -= 1
        return pos

    def __use_scroll(self, pos):
        """
        Использование свитка.
        """
        if pos >= self.__gaming_session.use_scroll(pos):
            pos -= 1
        return pos

    def __use_food(self, pos):
        """
        Использование еды.
        """
        if pos >= self.__gaming_session.use_food(pos):
            pos -= 1
        return pos

    def __info(self, tab_position):
        """
        Выводит на экран меню информации.
        """
        tab = ['RULES', 'CONTROL', 'MONSTERS', 'THINGS', 'DEVELOPERS']
        while True:
            self.__border('INFORMATION', 0, 'press "q" for esc')
            self.__tabs(tab_position, tab)
            self.__info_categories(tab[tab_position])
            self.__screen.refresh()
            match self.__screen.getkey():
                case 'q':
                    self.__menu_status = Const.MAIN_MENU
                    break
                case 'Q':
                    self.__menu_status = Const.MAIN_MENU
                    break
                case 'KEY_LEFT':
                    tab_position -= 1
                    if tab_position < 0: tab_position = len(tab) - 1
                case 'KEY_RIGHT':
                    tab_position += 1
                    if tab_position > len(tab) - 1: tab_position = 0
                case 'KEY_RESIZE':
                    self.__init_screen(self.__screen)
                    self.__screen.clear()
                    self.__info(tab_position)
                    break

    def __info_categories(self, category_name):
        """
        Выводит на экран категории меню информации.

        Args:
            x (int): Начальная координата по оси X.
            category_name (str): Имя категории.
        """
        match category_name:
            case 'RULES':
                self.__info_rules()
            case 'CONTROL':
                self.__info_control()
            case 'MONSTERS':
                self.__info_monsters()
            case 'THINGS':
                self.__info_items(3)
            case 'DEVELOPERS':
                self.__info_developers()

    def __do_lines(self, text):
        """
        Разбивает текст на строки.

        Args:
            text (str): Текст.
        """
        words = text.split()
        step = (self.__x_max - 90) // 4
        max_size = self.__x_max - 8 - step
        line_counter = 0
        lines = ['']
        for word in words:
            if len(lines[line_counter]) + 1 + len(word) > max_size:
                line_counter += 1
                lines.append(word)
            else:
                lines[line_counter] += ' ' + word
        return lines

    def __info_rules(self):
        """
        Выводит правила игры.
        """
        text = str('The main goal of the game is to go through\
             the 21st level of the dungeon as a rogue and collect\
             the maximum amount of treasures. In the dungeon, the\
             rogue will find various useful items and ammunition.\
             There will also be monsters that you can kill or avoid.\
             To advance to the next level, you need to find a passage\
             marked with the symbol D. Every 5 levels of the dungeon you\
             can find a treasure chest. Any item in the game has some\
             chance of being a mimic.')
        lines = self.__do_lines(text)
        start_y = (self.__y_max - len(lines)) // 2
        start_x = (self.__x_max - max(len(line) for line in lines)) // 2
        for i in range(len(lines)):
            self.__screen.addstr(i + start_y, start_x, lines[i])
        self.__screen.refresh()

    def __info_control(self):
        """
        Выводит информацию об управлении.
        """
        # text = str('Movement: WASD keys and arrow keys')
        lines = self.__do_lines('Movement: WASD keys and arrow keys')
        lines.extend(self.__do_lines('Return to main menu: enter key'))
        lines.extend(self.__do_lines('Inventory: I key'))
        lines.extend(self.__do_lines('Quick Save: F5'))
        lines.extend(self.__do_lines('Quick Load: F9'))
        start_y = (self.__y_max - len(lines)) // 2
        start_x = (self.__x_max - max(len(line) for line in lines)) // 2
        for i in range(len(lines)):
            self.__screen.addstr(i + start_y, start_x, lines[i])
        self.__screen.refresh()

    def __info_monsters(self):
        """
        Выводит на экран информацию о монстрах.

        Args:
            y (int): Начальная координата по оси Y.
        """
        zombie = self.__do_lines("- zombie. Low agility. Average strength,\
             hostility. High health.")
        len_z = len(zombie) + 1
        vampire = self.__do_lines("- vampire. High agility, hostility and \
            health. Average strength. Reduces a certain amount of the \
            player's maximum health upon a successful attack. The first\
             blow to a vampire is always a miss.")
        len_v = len(vampire) + 1
        ghost = self.__do_lines("- ghost. High agility. Low strength, \
            hostility and health. Invisible until the player enters his \
            area of hostility. If the player leaves the area of hostility,\
             the ghost will become invisible again.")
        len_g = len(ghost) + 1
        ogre = self.__do_lines("- ogre. Walks around the room two squares \
            apart. Very high strength and health, but after each attack it \
            rests for one turn, then is guaranteed to counterattack. Low \
            agility. Average hostility.")
        len_o = len(ogre) + 1
        snake = self.__do_lines("- snake magician. Very high agility. Each\
             successful attack has a chance of putting the player to sleep\
             for one turn. High hostility.")
        len_s = len(snake) + 1
        mimic = self.__do_lines("- mimic. Before interacting with the player,\
             it imitates objects. High agility, low strength, high health \
            and low hostility.")
        lines = zombie
        lines.append("")
        lines.extend(vampire)
        lines.append("")
        lines.extend(ghost)
        lines.append("")
        lines.extend(ogre)
        lines.append("")
        lines.extend(snake)
        lines.append("")
        lines.extend(mimic)
        start_y = (self.__y_max - len(lines)) // 2
        start_x = (self.__x_max - max(len(line) for line in lines)) // 2
        for i in range(len(lines)):
            self.__screen.addstr(i + start_y, start_x, lines[i])
        pos = start_y
        self.__screen.addstr(pos, (start_x - 1), 'z', curses.color_pair(Const.GREEN))
        pos += len_z
        self.__screen.addstr(pos, (start_x - 1), 'v', curses.color_pair(Const.RED))
        pos += len_v
        self.__screen.addstr(pos, (start_x - 1), 'g', curses.color_pair(Const.WHITE))
        pos += len_g
        self.__screen.addstr(pos, (start_x - 1), 'O', curses.color_pair(Const.YELLOW))
        pos += len_o
        self.__screen.addstr(pos, (start_x - 1), 's', curses.color_pair(Const.WHITE))
        pos += len_s
        self.__screen.addstr(pos, (start_x - 1), 'm', curses.color_pair(Const.WHITE))
        self.__screen.refresh()

    def __info_items(self, y):
        """
        Выводит на экран информацию о вещах.

        Args:
            y (int): Начальная координата по оси Y.
        """
        door = self.__do_lines("- door. Passage to the next level of \
            the game. When you switch, the game automatically saves.")
        len_d = len(door) + 1
        treasure = self.__do_lines("- treasure. The treasure may contain\
             weapons, armor, potions, scrolls, and food. There may also \
            be a large amount of gold. The player will also gain experience.")
        len_t = len(treasure) + 1
        weapon = self.__do_lines("- weapon. There are five types of weapons\
             in the game: knife, sword, axe, hammer and spear. The weapons also\
             have five grades and five materials. The higher the level of the\
             dungeon, the greater the chance that you will get a weapon of a\
             high grade or from good material. Only one weapon can be used at\
             a time.")
        len_w = len(weapon) + 1
        armor = self.__do_lines("- armor. There are five types of armor in the\
             game: helmet, gloves, boots, cuirass and shield. The armor also has\
             five grades and five materials. The higher the level of the dungeon,\
             the greater the chance that you will get armor of a high grade or\
             made of good material. Only one armor of each type can be used\
             at a time.")
        len_a = len(armor) + 1
        potion = self.__do_lines("- potion. Potions can temporarily increase the\
             following player characteristics: heat points, maximum number of heat\
             points, agility and strength. The effect of potions ends when you\
             move to the next dungeon level. The higher the dungeon level, the\
             greater the chance of finding more effective potions.")
        len_p = len(potion) + 1
        scroll = self.__do_lines("- scroll. Scrolls can increase the following\
             player characteristics: armor, maximum number of heat points, \
            agility, strength and strength limit. But be careful, there is a\
             chance that the scroll will be cursed. If the scroll is cursed,\
             it will reduce the characteristic. The characteristic cannot go\
             lower than 1. The higher the level of the dungeon, the greater\
             the chance of finding more effective scrolls.")
        len_s = len(scroll) + 1
        food = self.__do_lines("- food. Food restores the character's heat\
             points. The higher the level of the dungeon, the more satisfying\
             food you can find.")
        lines = door
        lines.append("")
        lines.extend(treasure)
        lines.append("")
        lines.extend(weapon)
        lines.append("")
        lines.extend(armor)
        lines.append("")
        lines.extend(potion)
        lines.append("")
        lines.extend(scroll)
        lines.append("")
        lines.extend(food)
        start_y = (self.__y_max - len(lines) + 3) // 2
        start_x = (self.__x_max - max(len(line) for line in lines)) // 2
        for i in range(len(lines)):
            self.__screen.addstr(i + start_y, start_x, lines[i])
        pos = start_y
        self.__screen.addstr(pos, (start_x - 1), 'D')
        pos += len_d
        self.__screen.addstr(pos, (start_x - 1), '◘')
        pos += len_t
        self.__screen.addstr(pos, (start_x - 1), '♠')
        pos += len_w
        self.__screen.addstr(pos, (start_x - 1), '+')
        pos += len_a
        self.__screen.addstr(pos, (start_x - 1), '♣')
        pos += len_p
        self.__screen.addstr(pos, (start_x - 1), '♦')
        pos += len_s
        self.__screen.addstr(pos, (start_x - 1), '♥')
        self.__screen.refresh()

    def __info_developers(self):
        """
        Выводит информацию о разработчиках.
        """
        lines = self.__do_lines('This game was developed by Cindycan and\
             Tandyfor as part of the 21-school educational project in 2024.')
        lines.append('')
        lines.extend(self.__do_lines('The game is written in the Python\
             programming language using the curses library in the spirit\
             of the classic 1980 game Rogue.'))
        start_y = (self.__y_max - len(lines)) // 2
        start_x = (self.__x_max - max(len(line) for line in lines)) // 2
        for i in range(len(lines)):
            self.__screen.addstr(i + start_y, start_x, lines[i])
        self.__screen.refresh()

    # Support

    def __displaying_menu_lines(self, choises, position):
        """
        Выводит на экран пункты меню и выделяет выбранный пункт.

        Args:
            choises: Список пунктов.
        """
        start_y = (self.__y_max - len(choises)) // 2
        start_x = (self.__x_max - max(len(s) for s in choises) - 1) // 2
        # position = 1 if choises[1] == 'CONTINUE' else 0
        while True:
            for line in range(len(choises)):
                if line == position:
                    self.__screen.addstr(line + start_y, start_x, choises[line], curses.A_REVERSE)
                else:
                    self.__screen.addstr(line + start_y, start_x, choises[line], curses.A_NORMAL)
            match self.__screen.getkey():
                case '\n':
                    break
                case 'KEY_UP':
                    position = self.__change_line_position(-1, position, choises)
                case 'KEY_DOWN':
                    position = self.__change_line_position(1, position, choises)
                case 'KEY_RESIZE':
                    self.__init_screen(self.__screen)
                    self.__screen.clear()
                    position = self.__displaying_menu_lines(choises, position)
                    break
        return position
    
    def __change_line_position(self, step, position, lines):
        """
        Сдвиг селектора.

        Args:
            step (int): Шаг.
            position (int): Искомая позтция.
            lines: Список строк.
        """
        position += step
        if position >= len(lines): position = 0
        elif position < 0: position = len(lines) - 1
        if lines[position] == '': position = self.__change_line_position(step, position, lines)
        return position
    
    # Show

    def __display(self, display):
        """
        Визуализирует на экран элементы матрицы.

        Args:
            display: Матрица.
        """
        for y in range(len(display)):
            for x in range(len(display[y])):
                self.__display_element(y + self.__display_start_y, x + self.__display_start_x, display[y][x])

    def __display_element(self, y, x, symbol):
        """
        Визуализирует на экран элемент матрицы.

        Args:
            y (int): Координата по оси Y.
            x (int): Координата по оси X.
            symbol (int): Элемент матрицы.
        """
        match symbol:
            case Const.EMPTY_FIELD:
                self.__screen.addch(y, x, ' ')
            case Const.HORIZONTAL_WALL:
                self.__screen.addch(y, x, '═', curses.color_pair(Const.BROWN))
            case Const.VERTICAL_WALL:
                self.__screen.addch(y, x, '║', curses.color_pair(Const.BROWN))
            case Const.UPPER_LEFT_CORNER:
                self.__screen.addch(y, x, '╔', curses.color_pair(Const.BROWN))
            case Const.UPPER_RIGHT_CORNER:
                self.__screen.addch(y, x, '╗', curses.color_pair(Const.BROWN))
            case Const.LOWER_LEFT_CORNER:
                self.__screen.addch(y, x, '╚', curses.color_pair(Const.BROWN))
            case Const.LOWER_RIGHT_CORNER:
                self.__screen.addch(y, x, '╝', curses.color_pair(Const.BROWN))
            case Const.ROOM_SPACE:
                self.__screen.addch(y, x, '-', curses.color_pair(Const.GREEN))
            case Const.DOOR:
                self.__screen.addch(y, x, '╬', curses.color_pair(Const.BROWN))
            case Const.CORRIDOR:
                self.__screen.addch(y, x, '▒')
            case Const.CHARACTER:
                self.__screen.addch(y, x, '☺', curses.color_pair(Const.YELLOW))
            case Const.ZOMBIE:
                self.__screen.addch(y, x, 'z', curses.color_pair(Const.GREEN))
            case Const.VAMPIRE:
                self.__screen.addch(y, x, 'v', curses.color_pair(Const.RED))
            case Const.GHOST:
                if self.__gaming_session.check_visibility(y - self.__display_start_y,\
                                                          x - self.__display_start_x):
                    self.__screen.addch(y, x, 'g')
            case Const.OGRE:
                self.__screen.addch(y, x, 'O', curses.color_pair(Const.YELLOW))
            case Const.SNAKE_MAGICIAN:
                self.__screen.addch(y, x, 's')
            case Const.MIMIC:
                self.__screen.addch(y, x, 'm')
            case Const.TREASURE:
                self.__screen.addch(y, x, '◘')
            case Const.FOOD:
                self.__screen.addch(y, x, '♥')
            case Const.POTION:
                self.__screen.addch(y, x, '♣')
            case Const.SCROLL:
                self.__screen.addch(y, x, '♦')
            case Const.WEAPON:
                self.__screen.addch(y, x, '♠')
            case Const.ARMOR:
                self.__screen.addch(y, x, '+')
            case Const.KEY:
                self.__screen.addch(y, x, 'k')
            case Const.EXIT_DOOR:
                self.__screen.addch(y, x, 'D')

    def __characteristics(self, inventory):
        """
        Выводит в футер экрана текущие характеристики.

        Args:
            inventory (bool): Статус инвенторя.
        """
        y_position = self.__y_max - 1
        list = []
        for i in range(self.__x_max + 1):
            try:
                self.__screen.addch(y_position, i, ' ')
            except:
                pass
        list.append(self.__level__status())
        list.append(self.__hits__status())
        list.append(self.__str__status())
        list.append(self.__dex__status())
        list.append(self.__gold__status())
        list.append(self.__armor__status())
        list.append(self.__experience__status())
        step = (self.__x_max - sum([len(i) for i in list])) // (len(list) + 1)
        x_position = (self.__x_max - sum([len(i) for i in list]) - step * (len(list) + 1)) // 2 + step
        for i in range(len(list)):
            try:
                self.__screen.addstr(y_position, x_position, list[i])
            except:
                pass
            x_position += step + len(list[i])
        if inventory:
            for i in range(self.__x_max):
                self.__screen.addch(self.__y_max, i, ' ')
        else:
            self.__screen.addstr(self.__y_max, 2, 'press "enter" for esc', curses.color_pair(Const.GREY))
        self.__time()


    def __level__status(self):
        """
        Возвращает строку с текущим уровенем сессии.
        """
        return f"Level: {self.__gaming_session.get_level()}"

    def __hits__status(self):
        """
        Возвращает строку с текущим и максимальным значением здоровья персонажа.
        """
        return f"Hits: {self.__gaming_session.get_hp()}({self.__gaming_session.get_max_hp()})"
        
    def __str__status(self):
        """
        Возвращает строку с текущим и максимальным значением силы персонажа.
        """
        return f"Str: {self.__gaming_session.get_str()}({self.__gaming_session.get_max_str()})"

    def __dex__status(self):
        """
        Возвращает строку с текущим и максимальным значением ловкости персонажа.
        """
        return f"Dex: {self.__gaming_session.get_dex()}"

    def __gold__status(self):
        """
        Возвращает строку с текущим значением золота персонажа.
        """
        return f"Gold: {self.__gaming_session.get_gold()}"

    def __armor__status(self):
        """
        Возвращает строку с текущим значением брони персонажа.
        """
        return f"Armor: {self.__gaming_session.get_armor()}"

    def __experience__status(self):
        """
        Возвращает строку с текущим значением опыта персонажа и значение следующего апа.
        """
        return f"Exp: {self.__gaming_session.get_experience()}({self.__gaming_session.get_max_experience()})"

    # time

    def __time(self):
        """
        Считает врямя с начала сессии и выводит результат в правый нижний угол экрана.
        """
        current_time = self.__gaming_session.get_run_time()
        H = current_time // 3600
        M = current_time % 3600 // 60
        S = current_time % 60
        str_time = f"{int(H):02}:{int(M):02}:{int(S):02}"
        self.__screen.addstr(self.__y_max, self.__x_max - len(str_time) - 6, f'time: {str_time}')

if __name__ == "__main__":
    curses.wrapper(View)
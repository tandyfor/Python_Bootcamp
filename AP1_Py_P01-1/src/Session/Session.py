import random
import time
import sys
import os

import pickle
import base64
import json

from collections import namedtuple

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Data')))

from Data import Display, Level, Character, Const, Inventory, Enemy

class Datalayer:
    """
    Класс для работы с сохранениями и статистикой.
    """

    __save_dir = '../saves/'

    def __init__(self):
        self.__sesion = None

    def set_session(self, session):
        self.__session = session

    def save(self, filename=False):
        """
        Сохранение.
        """
        stat = self.__stat_update()
        filename = time.strftime("%Y-%m-%d %H:%M:%S.json") if not filename else filename
        pickled_obj = pickle.dumps(self.__session)
        encoded_bytes = base64.b64encode(pickled_obj)
        with open(self.__save_dir + filename, 'w') as file:
            json.dump({'save' : encoded_bytes.decode('utf-8'),\
                       'stat': stat}, file)

    @classmethod
    def load(self, filename: str):
        """
        Загрузка игры.
        """
        if os.path.exists(self.__save_dir + filename):
            with open(self.__save_dir + filename, 'r') as file:
                load_data = json.load(file)
            decode_data = base64.b64decode(load_data['save'].encode('utf-8'))
            self.__session = pickle.loads(decode_data)
            return self.__session
        else:
            return False


    def autosave(self):
        """
        Автосохранение.
        """
        self.save('autosave.json')
    
    def quick_save(self):
        """
        Быстрое сохранение.
        """
        self.save('quick_save.json')

    def update_stat(self):
        """
        Сохранение статистики в случае смерити или победы.
        """
        stat = self.__stat_update()
        if os.path.exists(self.__save_dir + 'autosave.json'):
            with open(self.__save_dir + 'autosave.json', 'r') as file:
                load_data = json.load(file)
                load_data['stat'] = stat
        else:
            load_data = {}
            load_data['stat'] = stat
        
        with open(self.__save_dir + 'autosave.json', 'w') as file:
            json.dump(load_data, file)


    def __get_stat(self):
        """
        Возвращает namedtuple с текущими статистиками персонажа.
        """
        return self.__session.get_stat_tuple()

    
    def __stat_update(self):
        """
        Обновление статистики.
        """
        name = self.__session.get_character_name()
        if not os.path.exists(self.__save_dir + 'autosave.json'):
            return {name : self.__get_stat()}
        with open(self.__save_dir + 'autosave.json', 'r') as file:
            load_data = json.load(file)
        stats = load_data.get('stat')
        if not stats:
            return {name : self.__get_stat()}
        stats[name] = self.__get_stat()
        return stats
    
    @classmethod
    def __get_total(self, stat):
        return stat[0] * 5 + stat[1] * 100 + stat[2] * 20 + stat[3] * 2 + stat[4] * 5 + stat[5] * 15 + stat[6] * 2 + (stat[7] * -2) + stat[8]       
    
    @classmethod
    def get_leader_list(self):
        """
        Возвращает список с кортежами результатов из сохранения. Или None.
        """
        if not os.path.exists(self.__save_dir + 'autosave.json'):
            return None
        with open(self.__save_dir + 'autosave.json', 'r') as file:
            load_data = json.load(file)
        stats = load_data.get('stat')
        if not stats:
            return None
        result = []
        for name, stat in stats.items():
            result.append((name, stat[1], self.__get_total(stat)))
        result.sort(key=lambda x: x[2], reverse=True)
        return result
    
    @classmethod
    def get_results(self, name):
        """
        Возвращает список с кортежем результа из сохранения. Или None.
        """
        if not os.path.exists(self.__save_dir + 'autosave.json'):
            return None
        with open(self.__save_dir + 'autosave.json', 'r') as file:
            load_data = json.load(file)
        stats = load_data.get('stat')
        if not stats:
            return None
        return (f"name: {name}",\
                f"amount of treasure: {stats.get(name)[0]}",\
                f"achieved level: {stats.get(name)[1]}",\
                f"number of opponents defeated: {stats.get(name)[2]}",\
                f"amount of food eaten: {stats.get(name)[3]}",\
                f"number of potions consumed: {stats.get(name)[4]}",\
                f"number of scrolls read: {stats.get(name)[5]}",\
                f"number of blows thrown: {stats.get(name)[6]}",\
                f"number of missed hits: {stats.get(name)[7]}",\
                f"number of cells passed: {stats.get(name)[8]}")        


class Gaming_session:
    """
    Класс игровой сессии.
    """
    def __init__(self, y, x):
        """
        Инициализация игровой сессии.

        Args:
            y (int): Высота игрового поля.
            x (int): Ширина игрового поля.
        """
        self.__y_size = y
        self.__x_size = x
        self.__status = Const.PROCESS
        self.datalayer = Datalayer()
        self.datalayer.set_session(self)
        self.__init_difficulty()
        self.__level = Level()
        self.__character = Character(self.__y_size, self.__x_size)
        self.__enemys = []
        self.__init_statistics()
        self.__init_level()
        self.__init_inventory()
        self.__run_time = 0

    def update_run_time(self, time):
        self.__run_time += time

    def get_run_time(self):
        return self.__run_time

    def __init_difficulty(self):
        """
        Инициализация сложности.
        """
        self.__difficulty_z = 0
        self.__difficulty_v = 0
        self.__difficulty_g = 0
        self.__difficulty_o = 0
        self.__difficulty_s = 0
        self.__difficulty_m = 0

    def __init_statistics(self):
        """
        Инициализирует данные статистики.
        """
        self.__treasure_counter = 0
        self.__level_counter = 1
        self.__enemy_defeated_counter = 0
        self.__food_used_counter = 0
        self.__potions_used_counter = 0
        self.__scrolls_used_counter = 0
        self.__attacks_counter = 0
        self.__missed_attacks_counter = 0
        self.__moves_counter = 0

    def get_statistics(self):
        return (f"amount of treasure: {self.__treasure_counter}",\
                f"achieved level: {self.__level_counter}",\
                f"number of opponents defeated: {self.__enemy_defeated_counter}",\
                f"amount of food eaten: {self.__food_used_counter}",\
                f"number of potions consumed: {self.__potions_used_counter}",\
                f"number of scrolls read: {self.__scrolls_used_counter}",\
                f"number of blows thrown: {self.__attacks_counter}",\
                f"number of missed hits: {self.__missed_attacks_counter}",\
                f"number of cells passed: {self.__moves_counter}")

    def get_stat_tuple(self):
        Stats = namedtuple('Stats', ('treasure_counter',\
                                    'level_counter',\
                                    'enemy_defeated_counter',\
                                    'food_used_counter',\
                                    'potions_used_counter',\
                                    'scrolls_used_counter',\
                                    'attacks_counter',\
                                    'missed_attacks_counter',\
                                    'moves_counter'))
        result = Stats(treasure_counter=self.__treasure_counter,\
                            level_counter=self.get_level(),\
                            enemy_defeated_counter=self.__enemy_defeated_counter,\
                            food_used_counter=self.__food_used_counter,\
                            potions_used_counter=self.__potions_used_counter,\
                            scrolls_used_counter=self.__scrolls_used_counter,\
                            attacks_counter=self.__attacks_counter,\
                            missed_attacks_counter=self.__missed_attacks_counter,\
                            moves_counter=self.__moves_counter)
        return result

    def get_character_name(self):
        return self.__character.get_character_name()

    # Display

    def get_display(self):
        """
        Возвращает структурную матрицу.
        """
        return self.__display.get_display_struct()
    
    def get_active(self):
        """
        Возвращает активную матрицу.
        """
        return self.__display.get_display_active()

    # Level

    def __init_level(self):
        """
        Инициализирует игровой уровень сессии.
        """
        if self.get_level() < 21:
            for enemy in self.__enemys:
                match enemy.get_type():
                    case Const.ZOMBIE:
                        self.__difficulty_z += 1
                    case Const.VAMPIRE:
                        self.__difficulty_v += 1
                    case Const.GHOST:
                        self.__difficulty_g += 1
                    case Const.OGRE:
                        self.__difficulty_o += 1
                    case Const.SNAKE_MAGICIAN:
                        self.__difficulty_s += 1
                    case Const.MIMIC:
                        self.__difficulty_m += 1
            for enemy in self.__enemys:
                y, x = enemy.get_pos()
                self.__display.enemy_down(y, x)
            self.__enemys.clear()
            self.__display = Display(self.__y_size, self.__x_size)
            self.__init_character()
            self.__level.level_up()
            self.__add_items()
            self.__add_enemys()
        else:
            self.__status = Const.WIN

    def get_level(self):
        """
        Возвращает текущий уровень сессиии.
        """
        return self.__level.get_level()

    def __add_item(self, type):
        """
        Добавляет в активную матрицу предмет.

        Args:
            type (int): Тип предмета.
        """
        self.__display.add_active(type)

    def __add_items(self):
        """
        Добавляет в активную матрицу предметы.
        """
        if self.__level.get_level() % 5 == 0:
            self.__add_item(Const.TREASURE)
        for _ in range(10):
            self.__add_item(random.randint(Const.WEAPON, Const.FOOD))

    def __add_enemy(self, type):
        """
        Добавляет в активную матрицу монстра.

        Args:
            type (int): Тип монстра.
        """
        self.__enemys.append(Enemy(type, self.__display.add_active(type)))

    def __add_enemys(self):
        """
        Добавляет в активную матрицу предметы.
        """
        for _ in range(random.randint(self.__difficulty_z,\
            self.__level.get_level() + self.__difficulty_z)):
            try:
                self.__add_enemy(Const.ZOMBIE)
            except:
                pass

        if self.__level.get_level() > 4:
            for _ in range(random.randint(self.__difficulty_v,\
                self.__level.get_level() + self.__difficulty_v)):
                self.__add_enemy(Const.VAMPIRE)

        if self.__level.get_level() > 8:
            for _ in range(random.randint(self.__difficulty_g,\
                self.__level.get_level() + self.__difficulty_g)):
                try:
                    self.__add_enemy(Const.GHOST)
                except:
                    pass

        if self.__level.get_level() > 12:
            for _ in range(random.randint(self.__difficulty_o,\
                self.__level.get_level() + self.__difficulty_o)):
                try:
                    self.__add_enemy(Const.OGRE)
                except:
                    pass

        if self.__level.get_level() > 16:
            for _ in range(random.randint(self.__difficulty_s,\
                self.__level.get_level() + self.__difficulty_s)):
                try:
                    self.__add_enemy(Const.SNAKE_MAGICIAN)
                except:
                    pass
        
        self.__init_difficulty()

    # Character

    def __init_character(self):
        """
        Инициализирует главного героя.
        """
        self.__character.init_position(self.__y_size, self.__x_size)
        self.__character.set_position(self.__display.get_start_character_position_y() \
                                      , self.__display.get_start_character_position_x())
        self.__character.init_potions()
    
    def get_character_position(self):
        """
        Возвращает координаты главного героя.
        """
        return self.__character.get_position()
    
    def get_max_hp(self):
        """
        Возвращает максимальное здоровье главного героя.
        """
        return self.__character.get_max_hp()
    
    def get_hp(self):
        """
        Возвращает здоровье главного героя.
        """
        return self.__character.get_hp()
    
    def get_dex(self):
        """
        Возвращает ловкость главного героя.
        """
        return self.__character.get_dex()
    
    def get_str(self):
        """
        Возвращает силу главного героя.
        """
        return self.__character.get_str()
    
    def get_max_str(self):
        """
        Возвращает максимальную силу главного героя.
        """
        return self.__character.get_max_str()
    
    def get_armor(self):
        """
        Возвращает броню главного героя.
        """
        return self.__character.get_armor()
    
    def get_gold(self):
        """
        Возвращает золото главного героя.
        """
        return self.__character.get_gold()

    def get_experience(self):
        """
        Возвращает опыт главного героя.
        """
        return self.__character.get_experience()
    
    def get_max_experience(self):
        """
        Возвращает максимальный опыт главного героя.
        """
        return self.__character.get_max_experience()
    
    def move(self, step_y, step_x):
        """
        Задает перемещение главного героя. Возвращает статус сессии.

        Args:
            step_y (int): Перемещение по оси Y.
            step_x (int): Перемещение по оси X.
        """
        if self.__character.get_sleep() == False:
            y = self.__character.get_position_y()
            x = self.__character.get_position_x()
            if self.__display.get_display_struct()[y + step_y][x + step_x] \
                in range(Const.ROOM_SPACE, Const.NONE) and \
                self.__character.get_dex() > 0:
                if self.__display.get_display_active()[y + step_y][x + step_x] \
                    in range(Const.ZOMBIE, Const.TREASURE):
                        self.__attack(y + step_y, x + step_x)
                        self.__attacks_counter += 1
                else:
                    match self.__display.get_display_active()[y + step_y][x + step_x]:
                        case Const.WEAPON:
                            if self.__check_mimic():
                                self.__add_mimic(y + step_y, x + step_x)
                            else:
                                self.__inventory.add_weapon(self.__level.get_level())
                                self.__display.set_display_active(y + step_y, x + step_x, Const.NONE)
                                self.__character.move(step_y, step_x)
                                self.__moves_counter += 1
                        case Const.ARMOR:
                            if self.__check_mimic():
                                self.__add_mimic(y + step_y, x + step_x)
                            else:
                                self.__inventory.add_armor(self.__level.get_level())
                                self.__display.set_display_active(y + step_y, x + step_x, Const.NONE)
                                self.__character.move(step_y, step_x)
                                self.__moves_counter += 1
                        case Const.POTION:
                            if self.__check_mimic():
                                self.__add_mimic(y + step_y, x + step_x)
                            else:
                                self.__inventory.add_potion(self.__level.get_level())
                                self.__display.set_display_active(y + step_y, x + step_x, Const.NONE)
                                self.__character.move(step_y, step_x)
                                self.__moves_counter += 1
                        case Const.SCROLL:
                            if self.__check_mimic():
                                self.__add_mimic(y + step_y, x + step_x)
                            else:
                                self.__inventory.add_scroll(self.__level.get_level())
                                self.__display.set_display_active(y + step_y, x + step_x, Const.NONE)
                                self.__character.move(step_y, step_x)
                                self.__moves_counter += 1
                        case Const.FOOD:
                            if self.__check_mimic():
                                self.__add_mimic(y + step_y, x + step_x)
                            else:
                                self.__inventory.add_food(self.__level.get_level())
                                self.__display.set_display_active(y + step_y, x + step_x, Const.NONE)
                                self.__character.move(step_y, step_x)
                                self.__moves_counter += 1
                        case Const.TREASURE:
                            if self.__check_mimic():
                                self.__add_mimic(y + step_y, x + step_x)
                            else:
                                if random.random() < 0.3:
                                    self.__inventory.add_weapon(self.__level.get_level())
                                for _ in range(3):
                                    if random.random() < 0.4:
                                        self.__inventory.add_armor(self.__level.get_level())
                                for _ in range(3):
                                    if random.random() < 0.5:
                                        self.__inventory.add_scroll(self.__level.get_level())
                                for _ in range(5):
                                    if random.random() < 0.6:
                                        self.__inventory.add_potion(self.__level.get_level())
                                for _ in range(5):
                                    if random.random() < 0.7:
                                        self.__inventory.add_food(self.__level.get_level())
                                if random.random() < 0.9:
                                    self.__character.add_gold(random.randint(100, 201) * self.__level.get_level())
                                self.__character.add_exp(5 * self.__level.get_level())
                                self.__display.set_display_active(y + step_y, x + step_x, Const.NONE)
                                self.__character.move(step_y, step_x)
                                self.__moves_counter += 1
                        case _:
                            self.__character.move(step_y, step_x)
                            self.__moves_counter += 1
            elif self.__display.get_display_struct()[y + step_y][x + step_x] == Const.EXIT_DOOR:
                self.__init_level()
                if self.__status == Const.WIN:
                    self.datalayer.update_stat()
                else:
                    self.datalayer.autosave()
        else:
            self.__character.set_sleep(False)
        self.__emenys_action()
        if self.__status == Const.LOSE:
                    self.datalayer.update_stat()
        return self.__status
    
    def __check_mimic(self):
        """
        Проверяет, является ли предмет мимиком.
        """
        return True if random.random() <= (0.1 + (self.__level.get_level() * 0.01)) \
            else False
    
    def __add_mimic(self, y, x):
        self.__enemys.append(Enemy(Const.MIMIC, [y, x]))
        self.__display.set_display_active(y, x, Const.MIMIC)


    def __attack(self, y, x):
        """
        Атака главным героем монстра.

        Args:
            step_y (int): Координаты монстра по оси Y.
            step_x (int): Координаты монстра по оси X.
        """
        for i in range(len(self.__enemys)):
            if self.__enemys[i].get_pos() == [y, x]:
                self.__enemys[i].damage(self.__character.get_str(), \
                    self.__character.get_dex())
                if self.__enemys[i].get_hp() < 1:
                    self.__character.add_gold(self.__enemys[i].get_gold())
                    self.__character.add_exp(self.__enemys[i].get_exp())
                    self.__enemys.pop(i)
                    self.__display.enemy_down(y, x)
                    self.__enemy_defeated_counter += 1
                # Контратака огра
                elif self.__enemys[i].get_type() == Const.OGRE \
                    and self.__enemys[i].get_rest() == False:
                    hp_1 = self.__character.get_hp()
                    self.__character.damage(self.__enemys[i].get_str(), \
                        self.__enemys[i].get_dex())
                    hp_2 = self.__character.get_hp()
                    if hp_1 > hp_2:
                        self.__missed_attacks_counter += 1
                    if self.__character.get_hp() < 1:
                        self.__status = Const.LOSE
                break

    # Inventory

    def __init_inventory(self):
        """
        Инициализация инвентаря.
        """
        self.__inventory = Inventory()

    def get_weapons_list(self):
        """
        Возвращает список оружия.
        """
        return self.__inventory.get_weapons_list()

    def get_armor_list(self):
        """
        Возвращает список брони.
        """
        return self.__inventory.get_armor_list()

    def get_potions_list(self):
        """
        Возвращает список зелий.
        """
        return self.__inventory.get_potions_list()

    def get_scrolls_list(self):
        """
        Возвращает список свитков.
        """
        return self.__inventory.get_scrolls_list()

    def get_food_list(self):
        """
        Возвращает список еды.
        """
        return self.__inventory.get_food_list()

    def use_weapon(self, pos):
        """
        Использование оружия.

        Args:
            pos (int): Позиция оружия в инвентаре.
        """
        if len(self.__inventory.get_weapons()) > 0:
            selected_weapon = self.__inventory.get_weapons()[pos]
            check = selected_weapon.check_select()
            for weapon in self.__inventory.get_weapons():
                weapon.unuse()
            if check == False:
                self.__inventory.get_weapons()[pos].use()
                self.__character.set_str_weapon(selected_weapon.get_str())
                self.__character.set_dex_weapon(selected_weapon.get_dex())
            else:
                self.__character.set_str_weapon(0)
                self.__character.set_dex_weapon(0)

    def use_armor(self, pos):
        """
        Использование брони.

        Args:
            pos (int): Позиция брони в инвентаре.
        """
        if len(self.__inventory.get_armor()) > 0:
            selected_armor = self.__inventory.get_armor()[pos]
            type = selected_armor.get_type()
            check = selected_armor.check_select()
            for armor in self.__inventory.get_armor():
                if armor.get_type() == type:
                    armor.unuse()
            if check == False:
                self.__inventory.get_armor()[pos].use()
                self.__character.set_str_armor(selected_armor.get_armor(), type)
                self.__character.set_dex_armor(selected_armor.get_dex(), type)
            else:
                self.__character.set_str_armor(0, type)
                self.__character.set_dex_armor(0, type)

    def use_potion(self, pos):
        """
        Использование зелья.

        Args:
            pos (int): Позиция зелья в инвентаре.
        """
        if len(self.__inventory.get_potions()) > 0:
            effect = self.__inventory.get_potions()[pos].get_effect()
            match effect:
                case 'HP':
                    self.__character.set_heal(self.__inventory.get_potions()[pos].get_power())
                case 'max HP':
                    self.__character.add_potion_max_hp(self.__inventory.get_potions()[pos].get_power())
                case 'dexterity':
                    self.__character.add_potion_dex(self.__inventory.get_potions()[pos].get_power())
                case 'strength':
                    self.__character.add_potion_str(self.__inventory.get_potions()[pos].get_power())
            self.__inventory.del_potion(pos)
            self.__potions_used_counter += 1
        return len(self.__inventory.get_potions())

    def use_scroll(self, pos):
        """
        Использование свитка.

        Args:
            pos (int): Позиция свитка в инвентаре.
        """
        if len(self.__inventory.get_scrolls()) > 0:
            effect = self.__inventory.get_scrolls()[pos].get_effect()
            chaotic = -1 if self.__inventory.get_scrolls()[pos].check_chaotic() else 1
            match effect:
                case 'armor':
                    self.__character.add_armor(self.__inventory.get_scrolls()[pos].get_power() * chaotic)
                case 'max HP':
                    self.__character.add_max_hp(self.__inventory.get_scrolls()[pos].get_power() * chaotic)
                case 'dexterity':
                    self.__character.add_dex(self.__inventory.get_scrolls()[pos].get_power() * chaotic)
                case 'strength':
                    self.__character.add_str(self.__inventory.get_scrolls()[pos].get_power() * chaotic)
                case 'max strength':
                    self.__character.add_max_str(self.__inventory.get_scrolls()[pos].get_power() * chaotic)
            self.__inventory.del_scroll(pos)
            self.__scrolls_used_counter += 1
        return len(self.__inventory.get_scrolls())

    def use_food(self, pos):
        """
        Использование еды.

        Args:
            pos (int): Позиция еды в инвентаре.
        """
        if len(self.__inventory.get_food()) > 0:
            hp = self.__inventory.get_food()[pos].get_power()
            self.__character.set_heal(hp)
            self.__inventory.del_food(pos)
            self.__food_used_counter += 1
        return len(self.__inventory.get_food())
    
    def __emenys_action(self):
        """
        Действия монстров.
        """
        for enemy in self.__enemys:
            if enemy.check_range(self.__character.get_position_y(), self.__character.get_position_x()):
                if enemy.get_type() == Const.GHOST:
                    enemy.visibility_on()
                self.__move_enemy(enemy)
            else:
                if enemy.get_type() == Const.GHOST:
                    enemy.visibility_off()

    def __check_pos(self, y, x, step_y, step_x):
        """
        Проверка возможности перемещения.

        Args:
            y (int): Текущая позиция по оси Y.
            x (int): Текущая позиция по оси X.
            step_y (int): Смещение по оси Y.
            step_x (int): Смещение по оси X.
        """
        if self.__display.get_display_struct()[y + step_y][x + step_x] \
            in range(Const.ROOM_SPACE, Const.NONE) and \
            self.__display.get_display_active()[y + step_y][x + step_x] == Const.NONE:
            return True
        else:
            return False
        
    def check_visibility(self, y, x):
        for enemy in self.__enemys:
            ememy_y, enemy_x = enemy.get_pos()
            if enemy.get_type() == Const.GHOST \
                and ememy_y == y \
                and enemy_x == x \
                and enemy.get_visibility():
                return True
        return False

    def __move_enemy(self, enemy):
        """
        Перемещение монстра.

        Args:
            enemy: Монстр из списка.
        """
        speed = enemy.get_dex() // self.__character.get_dex()
        if random.random() <= (enemy.get_dex() / self.__character.get_dex() - speed):
            speed += 1
        # Двойной шаг огра
        if enemy.get_type() == Const.OGRE:
            speed *= 2
        attack = False
        for _ in range(speed):
            y, x = enemy.get_pos()
            if (self.__character.get_position_x() < x - 1 and \
                self.__character.get_position_y() == y or\
                self.__character.get_position_x() <= x - 1 and \
                self.__character.get_position_y() != y) and \
                self.__display.get_display_struct()[y][x - 1] and\
                self.__check_pos(y, x, 0, -1):
                self.__display.set_display_active(y, x, Const.NONE)
                self.__display.set_display_active(y, x - 1, enemy.get_type())
                enemy.set_pos([y, x - 1])
            elif (self.__character.get_position_y() < y - 1 and \
                self.__character.get_position_x() == x or\
                self.__character.get_position_y() <= y - 1 and \
                self.__character.get_position_x() != x) and\
                self.__check_pos(y, x, -1, 0):
                self.__display.set_display_active(y, x, Const.NONE)
                self.__display.set_display_active(y - 1, x, enemy.get_type())
                enemy.set_pos([y - 1, x])
            elif (self.__character.get_position_x() > x + 1 and \
                self.__character.get_position_y() == y or\
                self.__character.get_position_x() >= x + 1 and \
                self.__character.get_position_y() != y) and\
                self.__check_pos(y, x, 0, 1):
                self.__display.set_display_active(y, x, Const.NONE)
                self.__display.set_display_active(y, x + 1, enemy.get_type())
                enemy.set_pos([y, x + 1])
            elif (self.__character.get_position_y() > y + 1 and \
                self.__character.get_position_x() == x or\
                self.__character.get_position_y() >= y + 1 and \
                self.__character.get_position_x() != x) and\
                self.__check_pos(y, x, 1, 0):
                self.__display.set_display_active(y, x, Const.NONE)
                self.__display.set_display_active(y + 1, x, enemy.get_type())
                enemy.set_pos([y + 1, x])
            elif self.__character.get_position_x() == x and \
                (self.__character.get_position_y() == y - 1 or \
                self.__character.get_position_y() == y + 1):
                    attack = True
                    break
            elif self.__character.get_position_y() == y and \
                (self.__character.get_position_x() == x - 1 or \
                self.__character.get_position_x() == x + 1):
                    attack = True
                    break
            else:
                break
        if attack:
            hp_1 = self.__character.get_hp()
            if enemy.get_rest():
                enemy.set_rest(False)
            else:
                self.__character.damage(enemy.get_str(), enemy.get_dex())
                # Отдых огра
                if enemy.get_type() == Const.OGRE:
                    enemy.set_rest(True)
            hp_2 = self.__character.get_hp()
            # Скилл вампира
            if enemy.get_type() == Const.VAMPIRE:
                self.__character.add_max_hp(-1)
            if hp_1 > hp_2:
                self.__missed_attacks_counter += 1
                # Скилл змея
                if enemy.get_type() == Const.SNAKE_MAGICIAN \
                    and random.random() <= 0.3:
                    self.__character.set_sleep(True)
            if self.__character.get_hp() < 1:
                self.__status = Const.LOSE
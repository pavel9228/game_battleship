import random


# Класс корабля
class Ship:
    def __init__(self, positions):  # Инициализация корабля с его позициями
        self.positions = positions  # Хранит позиции корабля
        self.hit_positions = set()  # Множество для отслеживания попаданий

    def is_sunk(self):  # Проверка, потоплен ли корабль
        return len(self.hit_positions) == len(self.positions)  # Если все позиции поражены


# Класс игрового поля
class Board:
    def __init__(self, size=6):  # Инициализация поля с заданным размером
        self.size = size
        self.grid = [["О"] * size for _ in range(size)]  # Поле из "О" (пустых клеток)
        self.ships = []  # Список кораблей на поле
        self.tried_moves = set()  # Множество для отслеживания попыток выстрелов

    def place_ship(self, ship):  # Размещение корабля на поле
        for pos in ship.positions:
            self.grid[pos[0]][pos[1]] = "■"  # Обозначение корабля на поле
        self.ships.append(ship)  # Добавление корабля в список

    def print_board(self, show_ships=False):  # Печать поля
        print("   | " + " | ".join(map(str, range(1, self.size + 1))) + " |")  # Заголовок колонок
        for i, row in enumerate(self.grid):
            display_row = [(cell if (show_ships or cell != "■") else "О") for cell in row]
            print(f"{i + 1} | " + " | ".join(display_row) + " |")  # Печать строки

    def is_valid_position(self, positions):  # Проверка, можно ли разместить корабль
        for pos in positions:
            if not (0 <= pos[0] < self.size and 0 <= pos[1] < self.size):
                return False  # Выход за границы поля
            if self.grid[pos[0]][pos[1]] != "О":
                return False  # Если клетка не пустая
            # Проверяем соседние клетки для предотвращения соприкосновения
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (0 <= pos[0] + i < self.size and
                            0 <= pos[1] + j < self.size and
                            (i != 0 or j != 0) and
                            self.grid[pos[0] + i][pos[1] + j] == "■"):
                        return False
        return True  # Позиции допустимы

    def shoot(self, position):  # Обработка выстрела
        if position in self.tried_moves:
            return "Вы уже стреляли в эту клетку!"  # Проверка на повторный выстрел
        self.tried_moves.add(position)  # Запоминаем выстрел

        for ship in self.ships:  # Проверка попадания по каждому кораблю
            if position in ship.positions:
                ship.hit_positions.add(position)  # Добавляем позицию в пораженные
                self.grid[position[0]][position[1]] = "Х"  # Помечаем попадание
                if ship.is_sunk():
                    return "Корабль потоплен!"  # Если потоплен
                return "Попадание!"  # Если попали

        self.grid[position[0]][position[1]] = "М"  # Помечаем промах
        return "Промах!"

    def all_ships_sunk(self):  # Проверка на все потопленные корабли
        return all(ship.is_sunk() for ship in self.ships)  # Если все корабли потоплены


def generate_ship_positions(length, board):  # Генерация позиций для корабля
    while True:
        orientation = random.choice(['h', 'v'])  # Случайное направление
        if orientation == 'h':
            row = random.randint(0, board.size - 1)
            col = random.randint(0, board.size - length)
            positions = [(row, col + i) for i in range(length)]  # Горизонтальный корабль
        else:
            row = random.randint(0, board.size - length)
            col = random.randint(0, board.size - 1)
            positions = [(row + i, col) for i in range(length)]  # Вертикальный корабль

        if board.is_valid_position(positions):  # Проверяем, корректна ли позиция
            return positions  # Если да, возвращаем позиции


def main():
    player_board = Board()  # Игровое поле игрока
    computer_board = Board()  # Игровое поле компьютера

    # Размещение кораблей игрока

    player_board.place_ship(Ship(generate_ship_positions(3, player_board)))  # Один 3-х палубный
    for _ in range(2):  # Два 2-х палубных
        player_board.place_ship(Ship(generate_ship_positions(2, player_board)))
    for _ in range(4):  # Четыре 1-палубных
        player_board.place_ship(Ship(generate_ship_positions(1, player_board)))

    # Размещение кораблей компьютера
    for _ in range(1):  # Один 3-х палубный
        computer_board.place_ship(Ship(generate_ship_positions(3, computer_board)))
    for _ in range(2):  # Два 2-х палубных
        computer_board.place_ship(Ship(generate_ship_positions(2, computer_board)))
    for _ in range(4):  # Четыре 1-палубных
        computer_board.place_ship(Ship(generate_ship_positions(1, computer_board)))

    print("Ваше игровое поле:")
    player_board.print_board(show_ships=True)  # Печать игрового поля игрока

    while True:  # Цикл игры
        print("\nПоле компьютера:")
        computer_board.print_board(show_ships=False)  # Печать поля компьютера без кораблей

        shot = input("Введите координаты выстрела (формат: row col): ").split()  # Ввод координат
        row, col = int(shot[0]) - 1, int(shot[1]) - 1  # Преобразование ввода в индексы
        result = computer_board.shoot((row, col))  # Выполнение выстрела
        print(result)  # Печать результата

        if computer_board.all_ships_sunk():  # Проверка, потоплены ли все корабли компьютера
            print("Вы выиграли!")  # Сообщение о выигрыше
            break  # Завершение игры


# Генерируем случайные координаты для выстрела компьютера
comp_row, comp_col = random.randint(0, 5), random.randint(0, 5)

# Обрабатываем выстрел игрока по сгенерированным координатам и сохраняем результат
result = player_board.shoot((comp_row, comp_col))

# Выводим результат выстрела компьютера на экран
print(f"Компьютер стреляет в ({comp_row + 1}, {comp_col + 1}): {result}")

# Проверяем, потоплены ли все корабли игрока
if player_board.all_ships_sunk():
    # Если все корабли потоплены, выводим сообщение о выигрыше компьютера
    print("Компьютер выиграл!")
    break  # Завершаем цикл игры

# Запускаем главную функцию, если файл выполняется как основной
if __name__ == "__main__":  # Исправлено имя на правильное
    main()  # Вызываем функцию main для начала игры

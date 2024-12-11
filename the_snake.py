from random import randrange

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты."""

    def __init__(self) -> None:
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """
        Базовый метод для отрисовки объектов игры.
        Предполагается, что этот метод будет переопределен для дочерних
        классов класса GameObject.
        """
        pass


class Apple(GameObject):
    """
    Класс, унаследованный от GameObject,
    описывающий яблоко и действия с ним.
    """

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = (0, 0)

    def randomize_position(self, snake_positions=None):
        """Задаем рандомное местоположение объекта"""
        while True:
            new_position = (
                randrange(0, SCREEN_WIDTH, GRID_SIZE),
                randrange(0, SCREEN_HEIGHT, GRID_SIZE)
            )
            if snake_positions is None:
                return new_position
            elif new_position not in snake_positions:
                return new_position

    def draw(self):
        """Метод для отрисовки яблока на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Класс, унаследованный от GameObject,
    описывающий змейку и действия с ней.
    """

    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [
            (self.position[0] - i * GRID_SIZE, self.position[1])
            for i in range(self.length)
        ]
        self.last = self.positions[-1]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = (0, 255, 0)

    def update_direction(self):
        """Обновляем направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позиции змейки."""
        head_x, head_y = self.get_head_position()
        if self.direction == UP:
            new_head = (head_x, head_y - GRID_SIZE)
        elif self.direction == DOWN:
            new_head = (head_x, head_y + GRID_SIZE)
        elif self.direction == LEFT:
            new_head = (head_x - GRID_SIZE, head_y)
        elif self.direction == RIGHT:
            new_head = (head_x + GRID_SIZE, head_y)
        else:
            return

        if new_head[0] < 0:
            new_head = (SCREEN_WIDTH - GRID_SIZE, new_head[1])
        elif new_head[0] >= SCREEN_WIDTH:
            new_head = (0, new_head[1])
        if new_head[1] < 0:
            new_head = (new_head[0], SCREEN_HEIGHT - GRID_SIZE)
        elif new_head[1] >= SCREEN_HEIGHT:
            new_head = (new_head[0], 0)

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()
        # print(f'Positions: {self.positions}, Length: {self.length}')

    def draw(self):
        """Метод для отрисовки змейки на игровом поле."""
        for position in self.positions[0:]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    def get_head_position(self):
        """
        Возвращает позицию головы змейки
        (первый элемент списка positions).
        """
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [
            (self.position[0] - i * GRID_SIZE, self.position[1])
            for i in range(self.length)
        ]
        self.last = self.positions[-1]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = (0, 255, 0)


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    direction_map = {
        pygame.K_UP: (UP, DOWN),
        pygame.K_DOWN: (DOWN, UP),
        pygame.K_LEFT: (LEFT, RIGHT),
        pygame.K_RIGHT: (RIGHT, LEFT),
    }

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key in direction_map:
                new_direction, opposite_direction = direction_map[event.key]
                if game_object.direction != opposite_direction:
                    game_object.next_direction = new_direction


def main():
    """Главный цикл игры."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()
    apple.position = apple.randomize_position(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.position = apple.randomize_position(snake.positions)
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()

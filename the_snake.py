from random import choice, randint
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

# Цвета:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость:
SPEED = 5

# Настройка окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Это базовый класс."""

    def __init__(self, bg_color=None):
        self.position = (SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)
        self.body_color = bg_color

    def draw_cell(self, surface, position):
        """Создание ячейки."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)

    def draw(self, surface):
        """Отрисовка объекта. По умолчанию pass."""
        pass


class Apple(GameObject):
    """Класс для яблока, наследуется от GameObject."""

    def __init__(self, bg_color=APPLE_COLOR):
        super().__init__(bg_color)
        self.randomize_position()

    def randomize_position(self):
        """Реализация рандомного появления яблока."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self, surface):
        """Метод draw класса Apple."""
        self.draw_cell(surface, self.position)


class Snake(GameObject):
    """Класс для змейки, наследуется от GameObject."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализация змейки с позицией и цветом."""
        super().__init__(body_color)
        self.reset()
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляем позицию змейки."""
        head_x, head_y = self.get_head_position()
        xd, yd = self.direction
        x_new = (GRID_SIZE * xd + head_x) % SCREEN_WIDTH
        y_new = (GRID_SIZE * yd + head_y) % SCREEN_HEIGHT

        self.positions.insert(0, (x_new, y_new))
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.last = None

    def draw(self, surface):
        """Метод draw класса Snake. Отрисовывает змейку."""
        for position in self.positions[:-1]:
            self.draw_cell(surface, position)
        self.draw_cell(surface, self.positions[0])

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция запуска игры."""
    pygame.init()
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        apple.draw(screen)
        snake.draw(screen)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() in snake.positions[2:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            apple.draw(screen)

        pygame.display.update()


if __name__ == '__main__':
    main()

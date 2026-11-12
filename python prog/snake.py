"""Игра «Изгиб Питона»: змейка с переходом через границы поля."""

from random import choice

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
ALL_CELLS = frozenset(
    (x * GRID_SIZE, y * GRID_SIZE)
    for x in range(GRID_WIDTH)
    for y in range(GRID_HEIGHT)
)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTIONS = (UP, DOWN, LEFT, RIGHT)
TURNS = {
    (pygame.K_UP, LEFT): UP,
    (pygame.K_UP, RIGHT): UP,
    (pygame.K_DOWN, LEFT): DOWN,
    (pygame.K_DOWN, RIGHT): DOWN,
    (pygame.K_LEFT, UP): LEFT,
    (pygame.K_LEFT, DOWN): LEFT,
    (pygame.K_RIGHT, UP): RIGHT,
    (pygame.K_RIGHT, DOWN): RIGHT,
}

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
SPEED = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Изгиб Питона')
clock = pygame.time.Clock()


class GameObject:
    """Базовый игровой объект с позицией и цветом."""

    def __init__(self, body_color=None):
        """Разместить объект в центре поля и задать его цвет."""
        self.position = CENTER
        self.body_color = body_color

    def draw(self):
        """Определить интерфейс отрисовки для дочерних классов."""
        pass


class Apple(GameObject):
    """Яблоко, появляющееся только в свободной ячейке."""

    def __init__(self, occupied_positions=(CENTER,)):
        """Задать цвет и выбрать свободное место для яблока."""
        super().__init__(APPLE_COLOR)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions=(CENTER,)):
        """Выбрать свободную ячейку; на заполненном поле убрать яблоко."""
        # Исключаем тело змейки из возможных мест появления яблока.
        free_cells = ALL_CELLS.difference(occupied_positions)
        self.position = choice(tuple(free_cells)) if free_cells else None

    def draw(self):
        """Нарисовать яблоко с рамкой, если для него есть место."""
        if self.position is not None:
            rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Змейка, хранящая координаты сегментов от головы к хвосту."""

    def __init__(self):
        """Создать зелёную змейку, первоначально движущуюся вправо."""
        super().__init__(SNAKE_COLOR)
        self.reset(RIGHT)

    def update_direction(self):
        """Применить выбранное направление на очередном шаге."""
        if self.next_direction is not None:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Сдвинуть змейку на клетку с переходом через границы поля."""
        x, y = self.get_head_position()
        dx, dy = self.direction
        # Остаток от деления переносит голову на противоположный край.
        self.positions.insert(0, (
            (x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (y + dy * GRID_SIZE) % SCREEN_HEIGHT,
        ))
        self.last = None
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self):
        """Стереть ушедший хвост и нарисовать новую голову с рамкой."""
        # Стираем хвост первым: новая голова может попасть в его клетку.
        if self.last is not None:
            rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)
        head_rect = pygame.Rect(
            self.get_head_position(), (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    def get_head_position(self):
        """Вернуть координаты головы."""
        return self.positions[0]

    def reset(self, direction=None):
        """Вернуть змейку в центр, сбросив длину и отложенный поворот."""
        self.position = CENTER
        self.length = 1
        self.positions = [self.position]
        self.direction = direction if direction is not None else choice(
            DIRECTIONS
        )
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Обработать стрелки, закрытие окна и выход по Escape."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit
            # Не разрешаем два поворота за шаг и разворот в собственное тело.
            if game_object.next_direction is None:
                game_object.next_direction = TURNS.get(
                    (event.key, game_object.direction)
                )


def main():
    """Запустить игру, обрабатывая движение, еду и самоукус."""
    pygame.init()
    snake = Snake()
    apple = Apple(snake.positions)
    record = snake.length
    screen.fill(BOARD_BACKGROUND_COLOR)
    snake.draw()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            # Восстанавливаем хвост, чтобы рост был виден на этом же шаге.
            snake.positions.append(snake.last)
            snake.last = None
            record = max(record, snake.length)
            apple.randomize_position(snake.positions)

        if (snake.get_head_position() in snake.positions[1:]
                or apple.position is None):
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(snake.positions)

        snake.draw()
        apple.draw()
        pygame.display.set_caption(
            f'Изгиб Питона | Длина: {snake.length} | Рекорд: {record}'
            ' | Стрелки — движение, Esc — выход'
        )
        pygame.display.update()


if __name__ == '__main__':
    main()

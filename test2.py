import random


class MovingText:
    def __init__(self, text, font):
        self.count = 0
        self.text = text
        self.font = font
        self.image = self.font.render(self.text[self.count], True, (174, 217, 255))
        self.rect = self.image.get_rect()
        self.reset_position()  # Устанавливаем начальную позицию
        self.speed_x = 1

    def reset_position(self):
        """Устанавливаем случайную начальную позицию."""
        self.count = (self.count + 1) % 2
        self.image = self.font.render(self.text[self.count], True, (174, 217, 255))
        self.rect.x = random.randint(-self.rect.width, 800)  # Случайная X позиция
        self.rect.y = random.randint(0, 693 - self.rect.height)  # Случайная Y позиция

    def update(self):
        """Обновляем позицию текста."""
        self.rect.x -= self.speed_x  # Двигаем влево

        # Если текст ушел за левый край, перемещаем в случайную точку справа
        if self.rect.right < 0:
            self.reset_position()
            self.rect.x = random.randint(800, 800 + 200)

    def draw(self, screen):
        """Рисуем текст."""
        screen.blit(self.image, self.rect)

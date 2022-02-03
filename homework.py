from dataclasses import dataclass
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE_CONSTANT: str = (
        "Тип тренировки: {training_type}; "
        + "Длительность: {duration:.3f} ч.; "
        + "Дистанция: {distance:.3f} км; "
        + "Ср. скорость: {speed:.3f} км/ч; "
        + "Потрачено ккал: {calories:.3f}."
    )

    def get_message(self) -> str:
        """Возвращает строку сообщения о тренировке."""
        return self.MESSAGE_CONSTANT.format(
            training_type=self.training_type,
            duration=self.duration,
            distance=self.distance,
            speed=self.speed,
            calories=self.calories,
        )


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000  # метров в километре
    LEN_STEP: float = 0.65  # коэффициент шаг в метры
    M_IN_H: int = 60  # минут в часе

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        self.action: float = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""

    COEFF_CALORIE_1: int = 18  # коэффициент формулы при беге
    COEFF_CALORIE_2: int = 20  # коэффициент формулы при беге

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (
                self.COEFF_CALORIE_1 * self.get_mean_speed()
                - self.COEFF_CALORIE_2
            )
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.M_IN_H
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_CALORIE_1: float = 0.035  # коэффициент формулы при ходьбе
    COEFF_CALORIE_2: float = 0.029  # коэффициент формулы при ходьбе

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float,
    ) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories: float = (
            (
                self.COEFF_CALORIE_1 * self.weight
                + (self.get_mean_speed() ** 2 // self.height)
                * self.COEFF_CALORIE_2
                * self.weight
            )
            * self.duration
            * self.M_IN_H
        )
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38  # коэффицент гребок в метры
    COEFF_CALORIE_1: float = 1.1  # коэффициент формулы при плавании
    COEFF_CALORIE_2: int = 2  # коэффициент формулы при плавании

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: float,
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: float = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        spent_calories: float = (
            (self.get_mean_speed() + self.COEFF_CALORIE_1)
            * self.COEFF_CALORIE_2
            * self.weight
        )
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    codes: Dict[str, Type[Training]] = {
        "SWM": Swimming,
        "RUN": Running,
        "WLK": SportsWalking,
    }
    if workout_type not in codes:
        raise ValueError("Передан неизвестный тип тренировки")
    return codes[workout_type](*data)


def main(training: Training):
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

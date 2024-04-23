from abc import ABC, abstractmethod


class Car(ABC):
    def __init__(self, brand: str, model: str, year: str) -> None:
        self.brand = brand
        self.model = model
        self.year = year

    # Abstract method
    @abstractmethod
    def print_details(self) -> None:
        pass

    # Concrete method
    @staticmethod
    def accelerate() -> None:
        """"""
        print("speed up ...")

    @staticmethod
    def break_applied() -> None:
        print("Car stop")


class Hatchback(Car):

    def print_details(self) -> None:
        print("Brand:", self.brand)
        print("Model:", self.model)
        print("Year:", self.year)

    @staticmethod
    def sunroof() -> None:
        print("Not having this feature")


class Suv(Car):

    def print_details(self) -> None:
        print("Brand:", self.brand)
        print("Model:", self.model)
        print("Year:", self.year)

    @staticmethod
    def sunroof() -> None:
        print("Available")


car1 = Hatchback("Maruti", "Alto", "2022")
car1.print_details()
car1.accelerate()
car1.sunroof()

car2 = Suv("Toyota", "RAV4", "2024")
car2.print_details()
car2.accelerate()
car2.sunroof()

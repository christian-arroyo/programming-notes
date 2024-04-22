from abc import ABC, abstractmethod

class Car(ABC):
    def __init__(self, brand: str, model: str, year: int) -> None:
        self.brand = brand
        self.model = model
        self.year = year

    # Abstract method
    @abstractmethod
    def printDetails(self) -> None:
        pass

    # Concrete method
    def accelerate(self) -> None:
        print("speed up ...")
    
    def break_applied(self) -> None:
        print("Car stop")

class Hatchback(Car):

    def printDetails(self) -> None:
        print("Brand:", self.brand)
        print("Model:", self.model)
        print("Year:", self.year)
    
    def sunroof(self) -> None:
        print("Not having this feature")

class Suv(Car):

    def printDetails(self) -> None:
        print("Brand:", self.brand)
        print("Model:", self.model)
        print("Year:", self.year)
    
    def sunroof(self) -> None:
        print("Available")


car1 = Hatchback("Maruti", "Alto", "2022"); 
car1.printDetails() 
car1.accelerate()
car1.sunroof

car2 = Suv("Toyota", "RAV4", "2024"); 
car2.printDetails() 
car2.accelerate()
car2.sunroof

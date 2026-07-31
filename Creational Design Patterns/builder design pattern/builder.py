# in python builder pattern is not necessary, as we can use default arguments and keyword arguments to achieve the same functionality. However, if we want to implement the builder pattern in python, we can do it as follows:

class car:
    def __init__(self, wheels: int = 4, engine: str = "V4", color: str = "red"):
        self.wheels = wheels
        self.engine = engine
        self.color = color


class carBuilder:
    def __init__(self):
        self._wheels = 4
        self._engine = "V4"
        self._color = "red"

    def set_wheels(self, wheels: int):
        self._wheels = wheels
        return self

    def set_engine(self, engine: str):
        self._engine = engine
        return self

    def set_color(self, color: str):
        self._color = color
        return self

    def build(self) -> car:
        return car(self._wheels, self._engine, self._color)
    
a = car()
b = car(wheels=6, engine="V8", color="blue")
c = carBuilder().set_wheels(6).set_engine("V8").set_color("blue").build()
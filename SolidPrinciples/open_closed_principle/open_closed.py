from abc import ABC, abstractmethod
import math


class Shape(ABC):
	@abstractmethod
	def area(self) -> float:
		"""Return area of the shape."""


class Rectangle(Shape):
	def __init__(self, width: float, height: float):
		self.width = width
		self.height = height

	def area(self) -> float:
		return self.width * self.height


class Circle(Shape):
	def __init__(self, radius: float):
		self.radius = radius

	def area(self) -> float:
		return math.pi * self.radius * self.radius


class AreaCalculator:
	"""
	Open for extension: add new Shape subclasses.
	Closed for modification: AreaCalculator logic stays the same.
	"""

	def total_area(self, shapes: list[Shape]) -> float:
		return sum(shape.area() for shape in shapes)


if __name__ == "__main__":
	shapes: list[Shape] = [
		Rectangle(10, 5),
		Circle(7),
	]

	calculator = AreaCalculator()
	print("Total area:", calculator.total_area(shapes))

	# New shape can be added without changing AreaCalculator.
	class Triangle(Shape):
		def __init__(self, base: float, height: float):
			self.base = base
			self.height = height

		def area(self) -> float:
			return 0.5 * self.base * self.height

	shapes.append(Triangle(8, 4))
	print("Total area after adding triangle:", calculator.total_area(shapes))
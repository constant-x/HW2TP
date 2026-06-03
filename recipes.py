class Ingredient:
    def __init__(self, name, quantity, unit):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        value = float(value)
        if value <= 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = value

    def __str__(self):
        return f"{self.name}: {self._quantity} {self.unit}"

    def __repr__(self):
        return f"Ingredient({self.name!r}, {self._quantity}, {self.unit!r})"

    def __eq__(self, other):
        if not isinstance(other, Ingredient):
            return NotImplemented
        return self.name == other.name and self.unit == other.unit


class Recipe:
    def __init__(self, title, ingredients=None):
        self.title = title
        self.ingredients = []
        if ingredients is not None:
            for ingredient in ingredients:
                self.add_ingredient(ingredient)

    def add_ingredient(self, ingredient):
        if not isinstance(ingredient, Ingredient):
            raise ValueError("Можно добавлять только объекты класса Ingredient")

        for existing in self.ingredients:
            if existing == ingredient:
                existing.quantity += ingredient.quantity
                return
        self.ingredients.append(ingredient)

    @staticmethod
    def is_valid_ratio(ratio):
        return isinstance(ratio, (int, float)) and not isinstance(ratio, bool) and ratio > 0 
        # убрал bool, потому что True == 1, False == 0
        # некорректно иметь возможность вводить True/False

    def scale(self, ratio: float):
        if not isinstance(ratio, (int, float)) or isinstance(ratio, bool):
            raise ValueError("Коэффициент должен быть числом")
        if not Recipe.is_valid_ratio(ratio):
            raise ValueError("Коэффициент должен быть положительным")

        scaled_ingredients = [
            Ingredient(ingredient.name, ingredient.quantity * ratio, ingredient.unit)
            for ingredient in self.ingredients
        ]
        return Recipe(self.title, scaled_ingredients)

    def __str__(self):
        ingredients_str = "\n".join(str(ing) for ing in self.ingredients)
        return f"Рецепт: {self.title}\nИнгредиенты:\n{ingredients_str}"

    def __len__(self):
        return len(self.ingredients)

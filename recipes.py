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


class DietaryRecipe(Recipe):
    def __init__(self, title, diet_type, ingredients=None):
        # ingredients=None чтобы можно было создать пустой рецепт, к примеру: Recipe("Торт")
        super().__init__(title, ingredients)
        self.diet_type = diet_type

    def scale(self, ratio: float):
        scaled_recipe = super().scale(ratio)
        return DietaryRecipe(self.title, self.diet_type, scaled_recipe.ingredients)

    def __str__(self):
        base_str = super().__str__()
        return f"[{self.diet_type}] {base_str}"


class ShoppingList:
    def __init__(self):
        self._items = []

    def add_recipe(self, recipe, portions):
        if not isinstance(recipe, Recipe):
            raise ValueError("Можно добавлять только объекты класса Recipe")
        if not isinstance(portions, (int, float)) or isinstance(portions, bool) or portions <= 0:
        # убрал bool, по аналогии выше
            raise ValueError("Количество порций должно быть положительным")

        scaled_recipe = recipe.scale(portions)
        for ingredient in scaled_recipe.ingredients:
            self._items.append((ingredient, recipe.title))

    def remove_recipe(self, title):
        self._items = [
            (ingredient, recipe_title)
            for ingredient, recipe_title in self._items
            if recipe_title != title
        ]

    def get_list(self):
        shopping_dict = {}
        for ingredient, _ in self._items:
            key = (ingredient.name, ingredient.unit)
            if key in shopping_dict:
                shopping_dict[key] += ingredient.quantity
            else:
                shopping_dict[key] = ingredient.quantity

        shopping_list = [
            Ingredient(name, quantity, unit)
            for (name, unit), quantity in shopping_dict.items()
        ]
        return sorted(shopping_list, key=lambda ingredient: ingredient.name)

    def __add__(self, other):
        if not isinstance(other, ShoppingList):
            return NotImplemented

        result = ShoppingList()
        for ingredient, recipe_title in self._items + other._items:
            copied_ingredient = Ingredient(
                ingredient.name,
                ingredient.quantity,
                ingredient.unit,
            )
            result._items.append((copied_ingredient, recipe_title))
        return result

    def __str__(self):
        shopping_list = self.get_list()
        return "Список покупок:\n" + "\n".join(str(ing) for ing in shopping_list)

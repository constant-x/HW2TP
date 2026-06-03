import pytest
from recipes import DietaryRecipe, Ingredient, Recipe, ShoppingList


def make_recipe(title, flour_quantity):
    recipe = Recipe(title)
    recipe.add_ingredient(Ingredient("Мука", flour_quantity, "г"))
    recipe.add_ingredient(Ingredient("Сыр", 200, "г"))
    return recipe


def test_ingredient():
    flour = Ingredient("Мука", 500, "г")

    assert flour.name == "Мука"
    assert flour.quantity == 500.0
    assert flour.unit == "г"
    assert str(flour) == "Мука: 500.0 г"
    assert repr(flour) == "Ingredient('Мука', 500.0, 'г')"
    assert flour == Ingredient("Мука", 1000, "г")
    assert flour != Ingredient("Сахар", 500, "г")
    assert flour != Ingredient("Мука", 1, "кг")

    with pytest.raises(ValueError):
        Ingredient("Мука", 0, "г")


def test_recipe_and_dietary_recipe():
    recipe = Recipe("Пицца")
    recipe.add_ingredient(Ingredient("Мука", 500, "г"))
    recipe.add_ingredient(Ingredient("Мука", 200, "г"))
    recipe.add_ingredient(Ingredient("Вода", 300, "мл"))

    assert recipe.title == "Пицца"
    assert len(recipe) == 2
    assert recipe.ingredients[0].quantity == 700.0

    scaled_recipe = recipe.scale(2)

    assert scaled_recipe is not recipe
    assert isinstance(scaled_recipe, Recipe)
    assert recipe.ingredients[0].quantity == 700.0
    assert scaled_recipe.ingredients[0].quantity == 1400.0
    assert scaled_recipe.ingredients[1].quantity == 600.0

    with pytest.raises(ValueError):
        recipe.scale(0)

    dietary_recipe = DietaryRecipe("Салат", "веган", [Ingredient("Огурец", 2, "шт")])
    scaled_dietary_recipe = dietary_recipe.scale(3)

    assert isinstance(scaled_dietary_recipe, DietaryRecipe)
    assert scaled_dietary_recipe.diet_type == "веган"
    assert scaled_dietary_recipe.ingredients[0].quantity == 6.0


def test_shopping_list():
    first_list = ShoppingList()
    second_list = ShoppingList()
    pizza = make_recipe("Пицца", 500)
    pie = make_recipe("Пирог", 300)

    first_list.add_recipe(pizza, 2)
    second_list.add_recipe(pie, 1)

    result = first_list.get_list()

    assert [(ing.name, ing.quantity, ing.unit) for ing in result] == [
        ("Мука", 1000.0, "г"),
        ("Сыр", 400.0, "г"),
    ]

    with pytest.raises(ValueError):
        first_list.add_recipe(pizza, 0)

    combined = first_list + second_list
    combined_result = combined.get_list()

    assert combined is not first_list
    assert combined is not second_list
    assert [(ing.name, ing.quantity, ing.unit) for ing in combined_result] == [
        ("Мука", 1300.0, "г"),
        ("Сыр", 600.0, "г"),
    ]
    assert [(ing.name, ing.quantity, ing.unit) for ing in first_list.get_list()] == [
        ("Мука", 1000.0, "г"),
        ("Сыр", 400.0, "г"),
    ]

    combined.remove_recipe("Пицца")
    assert [(ing.name, ing.quantity, ing.unit) for ing in combined.get_list()] == [
        ("Мука", 300.0, "г"),
        ("Сыр", 200.0, "г"),
    ]

    combined.remove_recipe("Несуществующий рецепт")

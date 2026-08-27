import pytest
from sqlalchemy.orm import Session

from mealie.db.models._model_utils.auto_init import _get_config
from mealie.db.models.group.report import ReportModel
from mealie.db.models.household.shopping_list import ShoppingList, ShoppingListItem
from mealie.db.models.recipe.ingredient import IngredientFoodModel
from mealie.db.models.recipe.recipe import RecipeModel
from tests.utils.factories import random_string
from tests.utils.fixture_schemas import TestUser


@pytest.mark.parametrize("model", [IngredientFoodModel, RecipeModel, ReportModel, ShoppingList, ShoppingListItem])
def test_get_config_always_excludes_the_primary_key(model: type) -> None:
    assert "id" in _get_config(model).exclude


def test_get_config_keeps_the_exclusions_declared_by_the_model() -> None:
    assert _get_config(ReportModel).exclude == {"entries", "id"}
    assert _get_config(IngredientFoodModel).exclude == {"households_with_ingredient_food", "id"}


def test_update_does_not_clear_the_primary_key(session: Session, unique_user: TestUser) -> None:
    food = IngredientFoodModel(session=session, group_id=unique_user.group_id, name=random_string(10))
    session.add(food)
    session.commit()
    food_id = food.id

    food.update(session=session, group_id=unique_user.group_id, id=None, name=random_string(10))

    assert food.id == food_id

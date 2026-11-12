from copy import deepcopy
from unittest.mock import patch

from django.test import TestCase

from pokemon_api import get_json, get_pokemon
from .battle import training_battle


def sample(name):
    return {
        "name": name, "types": "electric", "weight": 6, "height": 0.4,
        "abilities": "static", "image": None,
        "stats": {"hp": 35, "attack": 55, "defense": 40, "speed": 90},
    }


class PracticeTests(TestCase):
    @patch("practices.views.get_pokemon")
    def test_search_add_duplicate_remove_and_session(self, api):
        api.return_value = sample("pikachu")
        response = self.client.get("/pokemon/", {"name": "pikachu"})
        self.assertContains(response, "pikachu")
        self.client.post("/pokemon/add/", {"name": "Pikachu"})
        self.client.post("/pokemon/add/", {"name": "pikachu"})
        self.assertEqual(len(self.client.session["team"]), 1)
        self.assertContains(self.client.get("/pokemon/"), "pikachu")
        self.client.post("/pokemon/remove/", {"name": "pikachu"})
        self.assertEqual(self.client.session["team"], [])

    @patch("practices.views.get_pokemon", side_effect=ValueError("Не найден"))
    def test_failed_search_and_add(self, api):
        self.assertContains(self.client.get("/pokemon/", {"name": "bad"}), "Не найден")
        response = self.client.post("/pokemon/add/", {"name": "bad"}, follow=True)
        self.assertContains(response, "Не найден")
        self.assertEqual(self.client.session.get("team", []), [])

    @patch("practices.dog_api.dog_request")
    def test_multiple_dogs_and_unknown_breed(self, api):
        api.side_effect = [{"chow": [], "dingo": []}, "https://example.com/chow.jpg", "https://example.com/dingo.jpg"]
        response = self.client.get("/dogs/", {"breeds": " Chow, dingo, bad, chow "})
        self.assertContains(response, "chow.jpg")
        self.assertContains(response, "dingo.jpg")
        self.assertContains(response, "не найдена")
        self.assertEqual(api.call_count, 3)

    @patch("practices.dog_api.dog_request", side_effect=ValueError("API недоступен"))
    def test_dog_outage(self, api):
        self.assertContains(self.client.get("/dogs/"), "API недоступен")

    def test_battle_and_validation(self):
        session = self.client.session
        session["team"] = [sample("pikachu"), sample("bulbasaur")]
        session.save()
        response = self.client.post("/pokemon/battle/", {"first": "pikachu", "second": "pikachu"}, follow=True)
        self.assertContains(response, "два разных")
        response = self.client.post("/pokemon/battle/", {"first": "pikachu", "second": "missing"}, follow=True)
        self.assertContains(response, "из своей команды")
        response = self.client.post("/pokemon/battle/", {"first": "pikachu", "second": "bulbasaur"}, follow=True)
        self.assertContains(response, "Победитель: pikachu")

    def test_battle_does_not_change_team_and_handles_high_defense(self):
        first, second = sample("one"), sample("two")
        first["stats"]["defense"] = second["stats"]["defense"] = 999
        original = deepcopy([first, second])
        result = training_battle(first, second)
        self.assertEqual(result["winner"], "one")
        self.assertEqual(len(result["log"]), 69)
        self.assertEqual([first, second], original)

    def test_mutations_require_post(self):
        for path in ["add", "remove", "battle"]:
            self.assertEqual(self.client.get(f"/pokemon/{path}/").status_code, 405)

    @patch("pokemon_api.requests.get")
    def test_api_conversion_and_cache(self, get):
        get_json.cache_clear()
        self.addCleanup(get_json.cache_clear)
        get.return_value.status_code = 200
        get.return_value.json.return_value = {
            "name": "pikachu", "types": [{"type": {"name": "electric"}}],
            "weight": 60, "height": 4,
            "abilities": [{"ability": {"name": "static"}}],
            "sprites": {"front_default": None},
            "stats": [{"stat": {"name": "hp"}, "base_stat": 35}],
        }
        pokemon = get_pokemon(" PIKACHU ")
        self.assertEqual(pokemon["height"], 0.4)
        self.assertEqual(pokemon["weight"], 6)
        get_pokemon("pikachu")
        self.assertEqual(get.call_count, 1)

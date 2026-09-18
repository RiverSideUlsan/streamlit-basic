import unittest

from app2.persona_store import load_persona


class PersonaStoreTest(unittest.TestCase):
    def test_loads_dawon_markdown_into_the_system_message(self):
        persona = load_persona({"file_name": "다온.md"})

        self.assertIn("등산", persona["system"])
        self.assertIn("직장인 여성", persona["system"])

    def test_loads_junho_markdown_into_the_system_message(self):
        persona = load_persona({"file_name": "준호.md"})

        self.assertIn("게임", persona["system"])
        self.assertIn("직장인 남성", persona["system"])

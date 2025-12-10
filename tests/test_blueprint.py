import json
import unittest

from platform_builder.blueprint import PlatformBlueprint


class PlatformBlueprintTests(unittest.TestCase):
    def test_to_and_from_dict_round_trip(self):
        blueprint = PlatformBlueprint(
            name="Creator",
            description="Helps build other platforms",
            features=["scaffolding", "templates"],
            services={"api": "REST endpoints", "ui": "Admin console"},
        )

        as_dict = blueprint.to_dict()
        restored = PlatformBlueprint.from_dict(as_dict)

        self.assertEqual(restored.name, blueprint.name)
        self.assertEqual(restored.description, blueprint.description)
        self.assertEqual(restored.features, blueprint.features)
        self.assertEqual(restored.services, blueprint.services)

    def test_rejects_empty_name(self):
        with self.assertRaises(ValueError):
            PlatformBlueprint(name="   ", description="desc")

    def test_rejects_empty_description(self):
        with self.assertRaises(ValueError):
            PlatformBlueprint(name="Platform", description=" ")

    def test_summary_contains_sections(self):
        blueprint = PlatformBlueprint(
            name="Generator",
            description="Generates projects",
            features=["cli"],
            services={"api": "API layer"},
        )
        summary = blueprint.summary()
        self.assertIn("Platform: Generator", summary)
        self.assertIn("Features:", summary)
        self.assertIn("Services:", summary)

    def test_from_dict_validates_types(self):
        with self.assertRaises(TypeError):
            PlatformBlueprint.from_dict({"name": "P", "description": "d", "features": "wrong"})
        with self.assertRaises(TypeError):
            PlatformBlueprint.from_dict({"name": "P", "description": "d", "services": []})


if __name__ == "__main__":
    unittest.main()

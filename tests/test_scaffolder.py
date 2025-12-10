import json
import tempfile
import unittest
from pathlib import Path

from platform_builder.blueprint import PlatformBlueprint
from platform_builder.scaffolder import PlatformScaffolder, _safe_slug


class PlatformScaffolderTests(unittest.TestCase):
    def setUp(self):
        self.blueprint = PlatformBlueprint(
            name="Maker",
            description="Builds other platforms",
            features=["cli", "modules"],
            services={"API": "JSON endpoints"},
        )
        self.scaffolder = PlatformScaffolder(self.blueprint)

    def test_write_blueprint_creates_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "blueprint.json"
            result = self.scaffolder.write_blueprint(output)
            self.assertTrue(result.exists())
            data = json.loads(result.read_text(encoding="utf-8"))
            self.assertEqual(data["name"], self.blueprint.name)

    def test_scaffold_creates_expected_structure(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "platform"
            created = list(self.scaffolder.scaffold(target))
            expected_files = {
                target / "README.md",
                target / "blueprint.json",
                target / "services",
                target / "services" / "api",
                target / "services" / "api" / "README.md",
            }
            self.assertTrue(expected_files.issubset(set(created)))
            self.assertIn("Maker", (target / "README.md").read_text(encoding="utf-8"))

    def test_safe_slug_handles_empty(self):
        self.assertEqual(_safe_slug("   "), "service")
        self.assertEqual(_safe_slug("API Layer"), "api-layer")


if __name__ == "__main__":
    unittest.main()

"""Active input pins and preservation of the original snapshot.

AuthorityEffect: None.
"""

from __future__ import annotations

from contextlib import redirect_stdout
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import verify_pins


class PinPolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="sign-pins-test-")
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.here = self.repo / "research/sign_slice"
        self.here.mkdir(parents=True)
        self.source = self.repo / verify_pins.SOURCE_PATHS[0]
        self.source.parent.mkdir(parents=True)
        self.source.write_bytes(b"fixed input\n")
        (self.repo / "CLAUDE.md").write_bytes(b"old consultation\n")
        (self.here / "PROMPT.md").write_bytes(b"fixed prompt\n")
        self.git("init", "-q")
        self.git("config", "user.name", "pin-test")
        self.git("config", "user.email", "pin-test@example.invalid")
        self.git("config", "core.autocrlf", "false")
        self.git("add", "--", verify_pins.SOURCE_PATHS[0], "CLAUDE.md",
                 "research/sign_slice/PROMPT.md")
        self.git("commit", "-qm", "fixture snapshot")
        self.snapshot = self.git("rev-parse", "HEAD")
        self.path = self.here / "SOURCE_MANIFEST.json"
        self.original = {
            "snapshot_commit": self.snapshot,
            "prompt_native_sha256": hashlib.sha256(b"fixed prompt\n").hexdigest(),
            "pins": {p: self.git("rev-parse", f"HEAD:{p}")
                     for p in (*verify_pins.SOURCE_PATHS, "CLAUDE.md")},
        }
        self.store(self.original)
        for name, value in (("HERE", self.here), ("REPO", self.repo)):
            patcher = patch.object(verify_pins, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def git(self, *args: str) -> str:
        return subprocess.check_output(["git", "-C", str(self.repo), *args],
                                       text=True, encoding="utf-8").strip()

    def store(self, value: dict[str, object]) -> None:
        self.path.write_text(json.dumps(value), encoding="ascii")

    def invoke(self, *args: str) -> tuple[int, str]:
        output = io.StringIO()
        with redirect_stdout(output):
            code = verify_pins.main(list(args))
        return code, output.getvalue()

    def test_drop_unread_changed_document_preserves_snapshot(self) -> None:
        (self.repo / "CLAUDE.md").write_bytes(b"new consultation\n")
        self.git("add", "--", "CLAUDE.md")
        self.git("commit", "-qm", "change unread document")
        self.assertEqual(self.invoke("--write")[0], 0)
        current = json.loads(self.path.read_text("ascii"))
        self.assertEqual(current["snapshot_commit"], self.snapshot)
        self.assertEqual(current["prompt_native_sha256"], self.original["prompt_native_sha256"])
        self.assertEqual(set(current["pins"]), set(verify_pins.SOURCE_PATHS))
        self.assertEqual(self.invoke("--check")[0], 0)

    def test_changed_consumed_input_blocks_write(self) -> None:
        self.source.write_bytes(b"changed input\n")
        self.git("add", "--", verify_pins.SOURCE_PATHS[0])
        self.git("commit", "-qm", "change consumed input")
        before = self.path.read_bytes()
        code, output = self.invoke("--write")
        self.assertEqual(code, 1)
        self.assertIn(verify_pins.SOURCE_PATHS[0], output)
        self.assertEqual(self.path.read_bytes(), before)

    def test_empty_population_fails(self) -> None:
        self.store({**self.original, "pins": {}})
        code, output = self.invoke("--check")
        self.assertEqual(code, 1)
        self.assertIn("PIN_POPULATION", output)
        self.assertIn(verify_pins.SOURCE_PATHS[0], output)

    def test_prompt_change_blocks_write(self) -> None:
        (self.here / "PROMPT.md").write_bytes(b"changed prompt\n")
        before = self.path.read_bytes()
        code, output = self.invoke("--write")
        self.assertEqual(code, 1)
        self.assertIn("PROMPT.md", output)
        self.assertEqual(self.path.read_bytes(), before)

    def test_wrong_active_pin_names_the_source(self) -> None:
        self.assertEqual(self.invoke("--write")[0], 0)
        current = json.loads(self.path.read_text("ascii"))
        current["pins"][verify_pins.SOURCE_PATHS[0]] = "0" * 40
        self.store(current)
        code, output = self.invoke("--check")
        self.assertEqual(code, 1)
        self.assertIn(verify_pins.SOURCE_PATHS[0], output)


if __name__ == "__main__":
    unittest.main()

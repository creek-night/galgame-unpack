"""Contribution privacy/consent tests use generated files and mocked GitHub transport."""
from pathlib import Path
import copy
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills/galgame-unpack/scripts"
sys.path.insert(0, str(SCRIPTS))
import community as c
spec = importlib.util.spec_from_file_location("community_install", ROOT / "tools/install.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class CommunityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="gal-community-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.source = self.root / "private computer/game"
        self.source.mkdir(parents=True)
        self.archive = self.source / "data.pfs"
        self.archive.write_bytes(b"generated resource fixture")
        self.run = self.root / "private output"
        (self.run / "assets/cg").mkdir(parents=True)
        self.png = self.run / "assets/cg/sample.png"
        Image.new("RGBA", (2, 3), (10, 20, 30, 128)).save(self.png)
        self.manifest = self.run / "manifest.json"
        self.m = {"schema_version": 1, "source": str(self.source), "game": "private label", "status": "passed", "scope": "sample",
            "requested_categories": ["cg"], "extras": [], "compose": False,
            "sources": [{"path": str(self.archive), "sha256": hashlib.sha256(self.archive.read_bytes()).hexdigest()}],
            "outputs": [{"path": "assets/cg/sample.png", "sha256": hashlib.sha256(self.png.read_bytes()).hexdigest(),
                "category": "cg", "complete": True, "size": [2, 3], "alpha_extrema": [128, 128],
                "native_canvas_evidence": "generated", "classification_evidence": "generated", "visual_review": "generated",
                "provenance": {"source": str(self.archive)}}], "unresolved": [],
            "tools": [{"path": "private runtime"}], "environment": {"PRIVATE": "never-export-this"}}
        self.write(self.manifest, self.m)
        self.state = self.root / "_config/community.json"
        self.catalog = self.root / "catalog.json"
        self.write(self.catalog, {"schema_version": 1, "records": []})
        self.details = {"original_title": "Test Original 1", "title_source_url": "https://example.org/game",
            "edition": "generated test", "engine": "Generated PF8", "tools": [{"name": "fixture", "version": "1", "source_url": "https://example.org/tool"}],
            "packages": ["data.pfs"], "conditions": ["Generated fixture only"], "steps": ["Decode {SOURCE}/data.pfs into {RUN}/assets"],
            "limitations": ["One CG sample; no full game claim"]}
        self.out = self.root / "contribution"

    def write(self, path, value):
        path.write_text(c.encoded(value), encoding="utf-8")

    def prepared(self, mode="auto"):
        c.set_consent(self.state, mode)
        result = c.prepare(self.manifest, self.details, self.out, self.state, self.catalog)
        self.assertEqual(result["network_requests"], 0)
        return self.out / "draft.json"

    def transport(self, response=None):
        responses = [subprocess.CompletedProcess([], 0, "[]", ""), response or subprocess.CompletedProcess([], 0, "https://github.com/creek-night/galgame-unpack/issues/123\n", "")]
        return patch.object(c.subprocess, "run", side_effect=responses)

    def test_missing_and_refused_consent_read_no_run_and_send_nothing(self):
        for mode in (None, "off"):
            if mode:
                c.set_consent(self.state, mode)
            with patch.object(c.subprocess, "run") as network:
                with self.assertRaises(ValueError):
                    c.prepare(self.root / "missing.json", self.details, self.out, self.state, self.catalog)
                network.assert_not_called()
            self.assertFalse(self.out.exists())

    def test_install_asks_and_only_explicit_yes_enables_auto(self):
        for answer, mode in [("y", "auto"), ("n", "off"), ("", "unconfigured"), ("r", "review")]:
            dest = self.root / ("skill-" + mode)
            output = self.root / ("output-" + mode)
            with patch.object(c.subprocess, "run") as network, patch("builtins.print"):
                result = installer.install(dest, output, ask=lambda _: answer, interactive=True)
                self.assertEqual(result["community_mode"], mode)
                self.assertTrue((dest / "SKILL.md").is_file())
                network.assert_not_called()
            self.assertEqual(c.consent(output / "_config/community.json")["mode"], mode)

    def test_install_noninteractive_and_existing_target(self):
        dest = self.root / "installed"
        result = installer.install(dest, self.root / "output", interactive=False)
        self.assertEqual(result["community_mode"], "unconfigured")
        with self.assertRaises(FileExistsError):
            installer.install(dest, self.root / "output", choice="auto")
        self.assertFalse((self.root / "output/_config/community.json").exists())

    def test_policy_change_requires_new_choice_and_off_stays_off(self):
        for mode in ("auto", "review", "off"):
            value = c.set_consent(self.state, mode)
            value["policy_version"] = 0
            self.write(self.state, value)
            self.assertEqual(c.consent(self.state)["mode"], "off" if mode == "off" else "unconfigured")

    def test_prepare_exports_allowlist_and_measured_scope_only(self):
        draft = self.prepared()
        record = c.read_json(draft)
        public = c.preview(draft)["body"]
        for private in (str(self.root), "private label", "private runtime", "never-export-this", "environment", "source_hint"):
            self.assertNotIn(private, public)
        self.assertEqual(record["verification"]["complete_counts"], {"cg": 1})
        self.assertEqual(record["verification"]["scope"], "sample")
        self.assertEqual(record["packages"][0]["name"], "data.pfs")
        self.assertEqual(set(p.name for p in self.out.iterdir()), {"draft.json", "submission.md"})
        self.assertEqual(record["verification"]["basis"], "contributor-local-check")

    def test_private_text_and_unexpected_fields_block_export(self):
        c.set_consent(self.state, "auto")
        for value in ("X:\\Users\\Private\\game", "/home/private/game", "/secret.txt", "file:///tmp/private", "https://example.org/?token=secret", "https://person:pass@example.org/", "private@example.org", "github_pat_fakecredential", "password=abc", "X%3A%5CUsers%5CPrivate", "--key secret", "token%3Dsecret", "https://example.org/?to%6ben=secret", "https://example.org/?path=X%3A%5CUsers%5CPrivate"):
            details = copy.deepcopy(self.details)
            details["steps"] = [value]
            with self.subTest(value=value), self.assertRaises(ValueError):
                c.prepare(self.manifest, details, self.out, self.state, self.catalog)
        details = dict(self.details, raw_profile={"private": True})
        with self.assertRaises(ValueError):
            c.prepare(self.manifest, details, self.out, self.state, self.catalog)
        self.assertFalse(self.out.exists())

    def test_prepare_rechecks_source_and_output_bytes(self):
        c.set_consent(self.state, "auto")
        for path in (self.archive, self.png):
            before = path.read_bytes()
            path.write_bytes(b"changed")
            with self.assertRaises(ValueError):
                c.prepare(self.manifest, self.details, self.out, self.state, self.catalog)
            path.write_bytes(before)
        self.assertFalse(self.out.exists())

    def test_failed_run_and_bad_destination_do_not_become_success(self):
        c.set_consent(self.state, "auto")
        self.m["status"] = "partial"
        self.write(self.manifest, self.m)
        with self.assertRaises(ValueError):
            c.prepare(self.manifest, self.details, self.out, self.state, self.catalog)
        self.m["status"] = "passed"
        self.write(self.manifest, self.m)
        for out in (self.source / "draft", self.run / "draft"):
            with self.assertRaises(ValueError):
                c.prepare(self.manifest, self.details, out, self.state, self.catalog)
            self.assertFalse(out.exists())

    @patch.object(c.shutil, "which", return_value="gh")
    def test_auto_submits_without_per_run_confirmation_and_keeps_receipt(self, _):
        draft = self.prepared()
        (self.out / "submission.md").write_text("tampered private text", encoding="utf-8")
        with self.transport() as network:
            result = c.submit(draft, self.state)
            self.assertEqual(result["status"], "submitted")
            self.assertEqual(network.call_count, 2)
            args, kwargs = network.call_args
            self.assertIn("--body-file", args[0])
            self.assertNotIn("--attach", args[0])
            self.assertEqual(kwargs["input"], c.preview(draft)["body"])
            self.assertNotIn("tampered", kwargs["input"])
            self.assertFalse(kwargs["shell"])
            self.assertEqual(kwargs["env"]["GH_HOST"], "github.com")
            self.assertIn("github.com/creek-night/galgame-unpack", args[0])
        other = self.root / "next-run"
        other.mkdir()
        shutil.copy2(draft, other / "draft.json")
        with patch.object(c.subprocess, "run") as network:
            self.assertEqual(c.submit(other / "draft.json", self.state)["status"], "submitted")
            network.assert_not_called()

    @patch.object(c.shutil, "which", return_value="gh")
    def test_remote_duplicate_skips_create(self, _):
        draft = self.prepared()
        body = c.preview(draft)["body"]
        reply = subprocess.CompletedProcess([], 0, json.dumps([{"body": body, "url": "https://github.com/creek-night/galgame-unpack/issues/99"}]), "")
        with patch.object(c.subprocess, "run", return_value=reply) as network:
            self.assertEqual(c.submit(draft, self.state)["status"], "already-submitted")
            self.assertEqual(network.call_count, 1)

    @patch.object(c.shutil, "which", return_value="gh")
    def test_review_requires_exact_preview_and_revocation_blocks_upload(self, _):
        draft = self.prepared("review")
        with patch.object(c.subprocess, "run") as network:
            for confirmation in (None, "wrong"):
                with self.assertRaises(ValueError):
                    c.submit(draft, self.state, confirmation)
            network.assert_not_called()
        confirmation = c.preview(draft)["review_sha256"]
        c.set_consent(self.state, "off")
        with patch.object(c.subprocess, "run") as network:
            with self.assertRaises(ValueError):
                c.submit(draft, self.state, confirmation)
            network.assert_not_called()

    @patch.object(c.shutil, "which", return_value="gh")
    def test_withdrawal_during_lookup_cancels_upload(self, _):
        draft = self.prepared()
        def withdraw(*args, **kwargs):
            c.set_consent(self.state, "off")
            return subprocess.CompletedProcess([], 0, "[]", "")
        with patch.object(c.subprocess, "run", side_effect=withdraw) as network:
            with self.assertRaisesRegex(ValueError, "Consent changed"):
                c.submit(draft, self.state)
            self.assertEqual(network.call_count, 1)

    @patch.object(c.shutil, "which", return_value="gh")
    def test_unknown_remote_outcome_never_retries_automatically(self, _):
        draft = self.prepared()
        with self.transport(subprocess.TimeoutExpired("gh", 60)):
            self.assertEqual(c.submit(draft, self.state)["status"], "unknown")
        with patch.object(c.subprocess, "run") as network:
            with self.assertRaisesRegex(ValueError, "already attempted"):
                c.submit(draft, self.state)
            network.assert_not_called()

    @patch.object(c.shutil, "which", return_value="gh")
    def test_duplicate_query_failure_does_not_post(self, _):
        draft = self.prepared()
        with patch.object(c.subprocess, "run", return_value=subprocess.CompletedProcess([], 1, "", "login failed")) as network:
            with self.assertRaises(ValueError):
                c.submit(draft, self.state)
            self.assertEqual(network.call_count, 1)
        self.assertFalse((self.state.parent / "community-submissions").exists())

    def test_reviewed_admission_search_and_auto_skip_known_title(self):
        draft = self.prepared()
        with self.assertRaises(ValueError):
            c.admit(draft, "https://github.com/creek-night/galgame-unpack/issues/123", self.catalog, self.root / "backups")
        result = c.admit(draft, "https://github.com/creek-night/galgame-unpack/issues/123", self.catalog, self.root / "backups", True)
        self.assertEqual(result["status"], "included-locally")
        found = c.lookup("ＴＥＳＴ Original", self.catalog)["records"]
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0]["review"]["status"], "reviewed-reference")
        self.assertEqual(found[0]["record"]["verification"]["basis"], "contributor-local-check")
        details = dict(self.details, edition="another edition")
        result = c.prepare(self.manifest, details, self.root / "new draft", self.state, self.catalog)
        self.assertEqual(result["status"], "known-title-skipped")
        self.assertFalse((self.root / "new draft").exists())
        self.assertEqual(len(list((self.root / "backups").iterdir())), 1)

    def test_untrusted_record_cannot_add_commands_or_promote_evidence(self):
        draft = self.prepared()
        for field, value in (("command", "execute me"), ("verification", {"basis": "maintainer-tested"})):
            data = c.read_json(draft)
            data[field] = value
            data["id"] = c.digest({k: v for k, v in data.items() if k != "id"})
            self.write(draft, data)
            with self.assertRaises(ValueError):
                c.preview(draft)
            # Restore the original from the rendered, known local JSON block.
            body = (self.out / "submission.md").read_text(encoding="utf-8")
            self.write(draft, json.loads(body.split("```json\n", 1)[1].split("```", 1)[0]))


    @patch.object(c.shutil, "which", return_value="gh")
    def test_review_mode_accepts_approved_preview(self, _):
        draft = self.prepared("review")
        with self.transport():
            result = c.submit(draft, self.state, c.preview(draft)["review_sha256"])
        self.assertEqual(result["status"], "submitted")

    def test_existing_install_preference_is_preserved(self):
        output = self.root / "output"
        c.set_consent(output / "_config/community.json", "off")
        def unexpected_prompt(_):
            self.fail("Existing refusal must not be asked again")
        result = installer.install(self.root / "new installation", output, ask=unexpected_prompt, interactive=True)
        self.assertEqual(result["community_mode"], "off")

    @patch.object(c.shutil, "which", return_value=None)
    def test_missing_cli_keeps_draft_without_network(self, _):
        draft = self.prepared()
        with patch.object(c.subprocess, "run") as network:
            with self.assertRaises(ValueError):
                c.submit(draft, self.state)
            network.assert_not_called()
        self.assertTrue(draft.exists())


if __name__ == "__main__":
    unittest.main()

"""Exercise offline lookup in a relocated skill with synthetic source records."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SKILL = Path(__file__).resolve().parents[1] / 'skills' / 'galgame-unpack'


class ZtjalLookupTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='ztjal-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / '移动 skill'
        (self.root / 'scripts').mkdir(parents=True)
        data_dir = self.root / 'references' / 'ztjal'
        data_dir.mkdir(parents=True)
        self.script = self.root / 'scripts' / 'search_ztjal.py'
        shutil.copyfile(SKILL / 'scripts' / 'search_ztjal.py', self.script)
        self.catalog = data_dir / 'catalog.json'
        article = {
            'id': 'sample', 'title': 'Synthetic source', 'source_url': 'https://example.invalid/source',
            'author': 'fixture-author', 'published_at': '2024-01-01', 'retrieved_on': '2026-10-25',
            'license': 'fixture', 'license_url': 'https://example.invalid/license', 'kind': 'game-records',
        }
        self.records = [
            {'id': 'sample-1', 'article_id': 'sample', 'heading': 'テスト☆ゲーム A', 'section': 'Sample',
             'kind': 'game', 'source_status': 'author-record-unverified', 'source_url': article['source_url'],
             'body_markdown': 'ＧＡＲｂｒｏ－Ｍｏｄ; ToolA; preserve parameter --mode=3'},
            {'id': 'sample-2', 'article_id': 'sample', 'heading': 'テスト☆ゲーム B', 'section': 'Sample',
             'kind': 'game', 'source_status': 'author-reported-unresolved', 'source_url': article['source_url'],
             'body_markdown': 'ToolB; author could not unpack.\n' + 'long source note\n' * 80 + 'END-OF-RECORD'},
        ]
        payload = {'schema_version': 1, 'snapshot_date': '2026-10-25', 'license': {'id': 'fixture'},
                   'validation_status': 'source-text-only', 'source': {}, 'articles': [article],
                   'records': self.records, 'excluded_articles': []}
        self.catalog.write_text(json.dumps(payload, ensure_ascii=False), encoding='utf-8')
        self.before = hashlib.sha256(self.catalog.read_bytes()).hexdigest()

    def run_query(self, *args, ok=True):
        env = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
        cp = subprocess.run([sys.executable, '-X', 'utf8', '-B', str(self.script), *args],
                            cwd=self.root.parent, env=env, capture_output=True, text=True,
                            encoding='utf-8', timeout=30)
        self.assertEqual(hashlib.sha256(self.catalog.read_bytes()).hexdigest(), self.before)
        if ok:
            self.assertEqual(cp.returncode, 0, cp.stderr)
            return json.loads(cp.stdout)
        self.assertNotEqual(cp.returncode, 0)
        return cp

    def test_width_punctuation_case_and_relocation(self):
        result = self.run_query('テストゲーム', 'garbro mod')
        self.assertEqual(result['matched'], 1)
        self.assertEqual(result['results'][0]['id'], 'sample-1')
        self.assertIn('--mode=3', result['results'][0]['excerpt'])

    def test_terms_must_match_same_record(self):
        result = self.run_query('ToolA', 'ToolB')
        self.assertEqual(result['matched'], 0)
        self.assertEqual(result['results'], [])
        self.assertIn('snapshot', result['no_match_meaning'])

    def test_full_record_preserves_unresolved_status_and_provenance(self):
        result = self.run_query('--id', 'sample-2')
        self.assertEqual(result['record']['body_markdown'], self.records[1]['body_markdown'])
        self.assertEqual(result['record']['source_status'], 'author-reported-unresolved')
        self.assertEqual(result['article']['author'], 'fixture-author')
        self.assertEqual(result['article']['source_url'], 'https://example.invalid/source')
        self.assertEqual(result['validation_status'], 'source-text-only')

    def test_limit_reports_total_without_silent_loss(self):
        result = self.run_query('テストゲーム', '--limit', '1')
        self.assertEqual(result['matched'], 2)
        self.assertEqual(result['returned'], 1)
        self.assertTrue(result['truncated'])

    def test_invalid_query_and_record_fail_cleanly(self):
        self.assertIn('letter or number', self.run_query('!!!', ok=False).stderr)
        self.assertIn('Unknown record ID', self.run_query('--id', 'missing', ok=False).stderr)
        self.assertIn('--limit', self.run_query('ToolA', '--limit', '0', ok=False).stderr)

    def test_statistics_describe_snapshot_not_compatibility(self):
        result = self.run_query('--stats')
        self.assertEqual(result['articles'], 1)
        self.assertEqual(result['records'], 2)
        self.assertEqual(result['snapshot_date'], '2026-10-25')
        self.assertEqual(result['validation_status'], 'source-text-only')


if __name__ == '__main__':
    unittest.main()
#!/usr/bin/env python3
"""Search the bundled ztj records offline; this reads source notes, never runs them."""
import argparse
import json
from pathlib import Path
import sys
import unicodedata

DEFAULT_CATALOG = Path(__file__).resolve().parents[1] / 'references' / 'ztjal' / 'catalog.json'


def normalize(value):
    """Match case, width and punctuation variants without inventing translated aliases."""
    return ''.join(c for c in unicodedata.normalize('NFKC', value).casefold() if c.isalnum())


def load_catalog(path):
    data = json.loads(path.read_text(encoding='utf-8'))
    if data.get('schema_version') != 1:
        raise ValueError('Unsupported catalog schema; update the query script with the dataset.')
    return data


def article_info(article):
    return {key: article[key] for key in (
        'id', 'title', 'source_url', 'author', 'published_at', 'retrieved_on',
        'license', 'license_url', 'kind',
    )}


def search(data, terms, limit):
    articles = {item['id']: item for item in data['articles']}
    needles = [normalize(term) for term in terms]
    matches = []
    for record in data['records']:
        article = articles[record['article_id']]
        title = normalize(record['heading'])
        body = normalize(record['body_markdown'])
        haystack = title + body + normalize(record['section'] + article['title'])
        if not all(needle in haystack for needle in needles):
            continue
        score = sum(8 if needle == title else 4 if needle in title else 1 for needle in needles)
        matches.append((score, record, article))
    matches.sort(key=lambda item: (-item[0], item[1]['id']))
    results = []
    for _, record, article in matches[:limit]:
        body = record['body_markdown']
        excerpt = body[:500]
        if len(body) > len(excerpt):
            excerpt += '\n[Use --id to read the complete record.]'
        results.append({
            'id': record['id'], 'heading': record['heading'], 'section': record['section'],
            'kind': record['kind'], 'source_status': record['source_status'],
            'source_url': record['source_url'], 'article': article_info(article),
            'excerpt': excerpt,
        })
    return {
        'queries': terms, 'matched': len(matches), 'returned': len(results),
        'truncated': len(matches) > len(results), 'results': results,
        'no_match_meaning': 'No match only describes this snapshot and these spellings; try the original title or check the source site.' if not matches else None,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('terms', nargs='*', help='Game, publisher or tool terms; separate arguments are ANDed.')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--id', dest='record_id', help='Read a complete record by its snapshot ID.')
    mode.add_argument('--stats', action='store_true', help='Show snapshot and coverage counts.')
    parser.add_argument('--limit', type=int, default=8, help='Maximum search results, 1-50 (default: 8).')
    parser.add_argument('--catalog', type=Path, default=DEFAULT_CATALOG, help='Use another compatible local snapshot.')
    args = parser.parse_args(argv)
    if not 1 <= args.limit <= 50:
        parser.error('--limit must be between 1 and 50.')
    if args.terms and (args.record_id or args.stats):
        parser.error('Use search terms, --id, or --stats separately.')
    if not args.terms and not args.record_id and not args.stats:
        parser.error('Provide a search term, --id, or --stats.')
    if any(not normalize(term) for term in args.terms):
        parser.error('Search terms need at least one letter or number.')
    try:
        data = load_catalog(args.catalog)
        result = {
            'snapshot_date': data['snapshot_date'], 'license': data['license'],
            'validation_status': data['validation_status'],
        }
        if args.stats:
            result.update(
                source=data['source'], articles=len(data['articles']), records=len(data['records']),
                game_record_blocks=sum(item['kind'] == 'game' for item in data['records']),
                excluded_articles=len(data['excluded_articles']),
            )
        elif args.record_id:
            record = next((item for item in data['records'] if item['id'] == args.record_id), None)
            if record is None:
                raise ValueError('Unknown record ID in this snapshot: ' + args.record_id)
            article = next(item for item in data['articles'] if item['id'] == record['article_id'])
            context = [item for item in data['records'] if item['article_id'] == article['id'] and item['kind'] == 'context' and item['id'] != record['id']]
            result.update(record=record, article=article_info(article), article_context=context)
        else:
            result.update(search(data, args.terms, args.limit))
    except (OSError, ValueError, KeyError, TypeError, StopIteration) as exc:
        parser.exit(1, 'Catalog error: ' + str(exc) + '\n')
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
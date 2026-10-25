"""Check the distributable skill and local Markdown references, without game data."""
import ast
import json
from pathlib import Path
import re
from urllib.parse import unquote,urlsplit

ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills'/'galgame-unpack'
errors=[]
files=[p for p in SKILL.rglob('*') if p.is_file() and '__pycache__' not in p.parts]
allowed={'.md','.py','.cs','.ps1','.yaml','.txt'}
for p in files:
    if p.name!='LICENSE' and p.suffix not in allowed and p.relative_to(SKILL).as_posix()!='references/ztjal/catalog.json':errors.append(f'Unexpected bundled file: {p.relative_to(ROOT)}')
    text=p.read_text(encoding='utf-8-sig')
    if '\ufffd' in text:errors.append(f'Replacement character: {p.relative_to(ROOT)}')
    if re.search(r'(?i)\b[A-Z]:[\\/]+Users[\\/]+(?!Public\b|Default\b)[^\s`"\']+',text):
        errors.append(f'Personal user path: {p.relative_to(ROOT)}')
    if 'codex-runtimes' in text:errors.append(f'Machine runtime dependency: {p.relative_to(ROOT)}')
    if p.suffix=='.py':
        try:ast.parse(text,filename=str(p))
        except SyntaxError as e:errors.append(str(e))
main=(SKILL/'SKILL.md').read_text(encoding='utf-8')
if not main.startswith('---\n'):errors.append('Missing frontmatter')
if not re.search(r'^name: galgame-unpack$',main,re.M):errors.append('Skill name mismatch')
if not re.search(r'^description: .+',main,re.M):errors.append('Missing description')
links=0
for p in [*ROOT.glob('*.md'),*SKILL.rglob('*.md')]:
    for match in re.finditer(r'\[[^\]]*\]\(([^\)]+)\)',p.read_text(encoding='utf-8')):
        dest=match.group(1).strip('<>')
        if urlsplit(dest).scheme in ('http','https','mailto'):continue
        local,_,anchor=dest.partition('#');target=(p.parent/unquote(local)).resolve() if local else p
        if not target.is_relative_to(ROOT):errors.append(f'Outside repository: {p.relative_to(ROOT)} -> {dest}')
        elif not target.is_file():errors.append(f'Missing link: {p.relative_to(ROOT)} -> {dest}')
        elif re.fullmatch('[bemt][0-9]{2,3}',anchor) and f'id="{anchor}"' not in target.read_text(encoding='utf-8'):
            errors.append(f'Missing source anchor: {dest}')
        links+=1
for req in SKILL.glob('requirements*.txt'):
    for line in req.read_text(encoding='utf-8').splitlines():
        if line.startswith('-r ') and not (req.parent/line[3:]).is_file():errors.append('Missing requirements include: '+line)
catalog_path=SKILL/'references'/'ztjal'/'catalog.json'
if catalog_path.is_file():
    try:
        catalog=json.loads(catalog_path.read_text(encoding='utf-8'))
        assert catalog['schema_version']==1
        assert catalog['license']['id']=='CC-BY-NC-SA-3.0'
        articles={item['id']:item for item in catalog['articles']}
        records={item['id']:item for item in catalog['records']}
        assert len(articles)==len(catalog['articles']) and len(records)==len(catalog['records'])
        assert catalog['source']['fetched_articles']==catalog['source']['discovered_articles']==len(articles)+len(catalog['excluded_articles'])
        seen=[]
        for article in articles.values():
            assert article['license']=='CC-BY-NC-SA-3.0' and article['author']=='ztj'
            assert article['record_count']==len(article['record_ids'])
            for record_id in article['record_ids']:
                record=records[record_id]
                assert record['article_id']==article['id']
                assert record['source_url'].split('#',1)[0]==article['source_url']
                assert record['body_markdown'].strip()
                assert record['source_status'] in ('author-record-unverified','author-reported-unresolved')
                seen.append(record_id)
        assert len(seen)==len(set(seen))==len(records) and set(seen)==set(records)
        assert (catalog_path.parent/'NOTICE.md').is_file()
    except (ValueError,KeyError,TypeError,AssertionError) as exc:
        errors.append('Invalid or incomplete ztj catalog: '+type(exc).__name__+' '+str(exc))
else:errors.append('Missing bundled ztj catalog')
print(json.dumps({'status':'failed' if errors else 'passed','skill_files':len(files),'local_links':links,'errors':errors},ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))

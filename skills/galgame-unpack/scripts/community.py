"""Opt-in, reviewable community references; never upload raw profiles or execute records."""
import argparse
import datetime
import hashlib
import ipaddress
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import unicodedata
from urllib.parse import unquote, urlsplit

REPOSITORY = "creek-night/galgame-unpack"
POLICY_VERSION = 1
CATALOG = Path(__file__).resolve().parents[1] / "references/community/catalog.json"
BOUNDARY = "Contributor reports a local check of the stated scope; this is not maintainer reproduction, full-game coverage, or an executable profile."
DETAIL_KEYS = {"original_title", "title_source_url", "edition", "engine", "tools", "packages", "conditions", "steps", "limitations"}
RECORD_KEYS = DETAIL_KEYS | {"schema_version", "id", "license", "verification"}
CATEGORIES = {"cg", "sprites", "layers", "background", "backgrounds", "bg", "text", "scenario", "bgm", "voice", "sfx", "audio", "video", "ui", "coverage", "inferred"}


def read_json(path, max_bytes=128_000):
    path = Path(path)
    if path.stat().st_size > max_bytes:
        raise ValueError("Contribution/config file too large")
    return json.loads(path.read_text(encoding="utf-8-sig"))


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def digest(value):
    return hashlib.sha256(encoded(value).encode("utf-8")).hexdigest()


def write_new(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(encoded(value))


def consent(state):
    if not Path(state).exists():
        return {"mode": "unconfigured", "policy_version": POLICY_VERSION, "repository": REPOSITORY}
    value = read_json(state)
    if not isinstance(value, dict) or value.get("mode") not in {"off", "review", "auto"}:
        raise ValueError("Invalid local consent file")
    if value["mode"] in {"review", "auto"} and (value.get("policy_version") != POLICY_VERSION or value.get("repository") != REPOSITORY):
        return {"mode": "unconfigured", "policy_version": POLICY_VERSION, "repository": REPOSITORY}
    return value


def set_consent(state, mode):
    if mode not in {"off", "review", "auto"}:
        raise ValueError("Choose off, review or auto")
    value = {"mode": mode, "policy_version": POLICY_VERSION, "repository": REPOSITORY}
    path = Path(state)
    path.parent.mkdir(parents=True, exist_ok=True)
    # The preference is local and contains no machine/user identifier.
    path.write_text(encoded(value), encoding="utf-8")
    return value


def require_consent(state):
    if consent(state)["mode"] not in {"review", "auto"}:
        raise ValueError("Community participation is not enabled; extraction remains available")


def exact(value, keys, label):
    if not isinstance(value, dict) or set(value) != set(keys):
        raise ValueError(label + ": unexpected or missing fields")


def public_url(value):
    if not isinstance(value, str) or len(value) > 500:
        raise ValueError("Expected a short public HTTPS source URL")
    parts = urlsplit(value)
    if parts.scheme != "https" or not parts.hostname or parts.username or parts.password or parts.port not in (None, 443):
        raise ValueError("Expected public HTTPS URL without credentials")
    host = parts.hostname.lower()
    if host == "localhost" or host.endswith((".localhost", ".local", ".internal")) or "." not in host:
        raise ValueError("Local URL is not a public source")
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        address = None
    if address is not None and not address.is_global:
        raise ValueError("Private IP is not a public source")
    if re.search(r"(?i)(?:token|secret|password|signature|api[_-]?key|auth|credential)=", unquote(unquote(parts.query))):
        raise ValueError("Credential-like URL query")
    return value


def safe_text(value, limit=1000):
    if not isinstance(value, str) or not value.strip() or len(value) > limit or value != value.strip():
        raise ValueError("Expected bounded nonempty public text")
    if any(ord(c) < 32 for c in value) or "```" in value:
        raise ValueError("Control characters or code fences in public text")
    for url in re.findall(r"https?://[^\s<>]+", value):
        public_url(url)
    scan = unicodedata.normalize("NFKC", unquote(unquote(value)))
    if re.search(r"(?i)(?:\b[a-z]:[\\/]|\\\\|file://|/(?:Users|home)/)", scan):
        raise ValueError("Private filesystem path embedded in public text or URL")
    without_urls = re.sub(r"https://[^\s<>]+", "", scan)
    if re.search(r"(?i)(?:\b[a-z]:[\\/]|\\\\|file://|(?<![\w}:])/(?!/|\s)[^\s]*|~/)", without_urls):
        raise ValueError("Absolute/local path in public text; replace it with a placeholder")
    if re.search(r"[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}", scan):
        raise ValueError("Email address in public text")
    if re.search(r"(?i)(?:gh[pousr]_[a-z0-9_]+|github_pat_[a-z0-9_]+|Bearer\s+\S+|--(?:key|password|token|secret)(?:\s|=)|(?:token|password|passwd|secret|api[_-]?key|authorization)\s*[:=]\s*\S+)", scan):
        raise ValueError("Credential-like text")
    username = os.environ.get("USERNAME", "")
    if len(username) >= 3 and username.casefold() in scan.casefold():
        raise ValueError("Local account name appears in public text")
    return value


def text_list(values, label, maximum=30):
    if not isinstance(values, list) or not 1 <= len(values) <= maximum:
        raise ValueError(label + ": expected nonempty bounded list")
    for item in values:
        safe_text(item)


def package_name(value):
    safe_text(value, 240)
    p = PurePosixPath(value)
    if p.is_absolute() or ".." in p.parts or "\\" in value or ":" in value or value != p.as_posix():
        raise ValueError("Package names must be normalized game-relative paths")
    return value


def validate_details(value, record=False):
    exact(value, RECORD_KEYS if record else DETAIL_KEYS, "record" if record else "details")
    for field in ("original_title", "edition", "engine"):
        safe_text(value[field], 160)
    safe_text(value["title_source_url"], 500)
    public_url(value["title_source_url"])
    for field in ("conditions", "steps", "limitations"):
        text_list(value[field], field)
    if not isinstance(value["tools"], list) or not 1 <= len(value["tools"]) <= 12:
        raise ValueError("Describe the tools and versions actually used")
    for tool in value["tools"]:
        exact(tool, {"name", "version", "source_url"}, "tool")
        safe_text(tool["name"], 100)
        safe_text(tool["version"], 100)
        safe_text(tool["source_url"], 500)
        public_url(tool["source_url"])
    if not isinstance(value["packages"], list) or not 1 <= len(value["packages"]) <= 32:
        raise ValueError("Choose the resource packages to identify; no save/config/log files")
    names = []
    for package in value["packages"]:
        if record:
            exact(package, {"name", "bytes", "sha256"}, "package")
            if type(package["bytes"]) is not int or package["bytes"] <= 0 or not re.fullmatch(r"[0-9a-f]{64}", str(package["sha256"])):
                raise ValueError("Invalid package fingerprint")
            name = package["name"]
        else:
            name = package
        names.append(package_name(name))
    if len(set(names)) != len(names):
        raise ValueError("Duplicate package")


def validate_record(record):
    validate_details(record, record=True)
    if type(record["schema_version"]) is not int or record["schema_version"] != 1 or record["license"] != "MIT":
        raise ValueError("Unsupported contribution schema/license")
    verification = record["verification"]
    exact(verification, {"basis", "scope", "requested_categories", "extras", "compose", "complete_counts", "png_count", "output_count", "unresolved_categories", "boundary"}, "verification")
    if verification["basis"] != "contributor-local-check" or verification["boundary"] != BOUNDARY:
        raise ValueError("Community report cannot claim maintainer verification")
    if verification["scope"] not in {"sample", "full"} or type(verification["compose"]) is not bool:
        raise ValueError("Invalid verification scope/options")
    for field in ("requested_categories", "extras", "unresolved_categories"):
        values = verification[field]
        if not isinstance(values, list) or any(not isinstance(v, str) or v not in CATEGORIES for v in values) or len(values) != len(set(values)):
            raise ValueError("Invalid verification categories")
    if not verification["requested_categories"]:
        raise ValueError("Requested categories required")
    counts = verification["complete_counts"]
    if not isinstance(counts, dict) or any(k not in CATEGORIES or type(v) is not int or v <= 0 for k, v in counts.items()):
        raise ValueError("Invalid complete counts")
    if any(not counts.get(c) for c in verification["requested_categories"] + verification["extras"]):
        raise ValueError("No complete result for requested category")
    for field in ("png_count", "output_count"):
        if type(verification[field]) is not int or verification[field] < (1 if field == "output_count" else 0):
            raise ValueError("Invalid verification count")
    if record["id"] != digest({k: v for k, v in record.items() if k != "id"}):
        raise ValueError("Contribution content changed; prepare a new draft")
    return record


def normalize(value):
    return "".join(c for c in unicodedata.normalize("NFKC", value).casefold() if c.isalnum())


def load_catalog(path=CATALOG):
    catalog = read_json(path, max_bytes=32_000_000)
    exact(catalog, {"schema_version", "records"}, "catalog")
    if catalog["schema_version"] != 1 or not isinstance(catalog["records"], list):
        raise ValueError("Invalid community catalog")
    seen = set()
    for entry in catalog["records"]:
        exact(entry, {"record", "review"}, "catalog entry")
        record = validate_record(entry["record"])
        exact(entry["review"], {"status", "source_issue_url", "reviewed_at"}, "review")
        review = entry["review"]
        if review["status"] != "reviewed-reference" or not re.fullmatch(r"https://github\.com/creek-night/galgame-unpack/issues/[1-9][0-9]*", review["source_issue_url"]):
            raise ValueError("Expected an explicitly reviewed repository Issue")
        datetime.date.fromisoformat(review["reviewed_at"])
        if record["id"] in seen:
            raise ValueError("Duplicate community record")
        seen.add(record["id"])
    return catalog


def lookup(query, catalog=CATALOG):
    needle = normalize(query)
    if not needle:
        raise ValueError("Query the confirmed original title")
    matches = [e for e in load_catalog(catalog)["records"] if needle in normalize(e["record"]["original_title"])]
    return {"records": matches, "boundary": "Title matches are reference candidates; check edition, packages and tool conditions before use."}


def prepare(manifest, details, out, state, catalog=CATALOG):
    require_consent(state)
    validate_details(details)
    manifest = Path(manifest).resolve(strict=True)
    # Do not subject the private, potentially large manifest to the public payload size limit.
    raw = json.loads(manifest.read_text(encoding="utf-8-sig"))
    source = Path(raw["source"]).resolve(strict=True)
    out = Path(out).resolve()
    if out.is_relative_to(source) or out.is_relative_to(manifest.parent):
        raise ValueError("Contribution draft must be outside game and verified run")
    if out.exists():
        raise FileExistsError("Choose a fresh contribution directory")
    if raw.get("status") != "passed" or not raw.get("sources") or type(raw.get("compose")) is not bool:
        raise ValueError("A passed canonical run with explicit composition choice is required")
    sources = {}
    for row in raw["sources"]:
        path = Path(row["path"]).resolve(strict=True)
        if not path.is_relative_to(source):
            raise ValueError("Manifest source escapes game root")
        sources[path.relative_to(source).as_posix()] = (path, row)
    packages = []
    for name in details["packages"]:
        if name not in sources:
            raise ValueError("Selected package is not a verified manifest source")
        path, row = sources[name]
        packages.append({"name": name, "bytes": path.stat().st_size, "sha256": row["sha256"]})
    from verify_run import check
    verified = check(manifest, verify_sources=True)
    record = dict(details, schema_version=1, license="MIT", packages=packages,
        verification={"basis": "contributor-local-check", "scope": raw["scope"],
            "requested_categories": raw["requested_categories"], "extras": raw.get("extras", []), "compose": raw["compose"],
            "complete_counts": verified["complete_counts"], "png_count": verified["png_count"],
            "output_count": len(verified["outputs"]),
            "unresolved_categories": sorted({r["category"] for r in verified["unresolved"]}), "boundary": BOUNDARY})
    record["id"] = digest(record)
    validate_record(record)
    candidates = lookup(record["original_title"], catalog)["records"]
    if any(e["record"]["id"] == record["id"] for e in candidates):
        return {"status": "already-included", "id": record["id"]}
    if consent(state)["mode"] == "auto" and any(normalize(e["record"]["original_title"]) == normalize(record["original_title"]) for e in candidates):
        return {"status": "known-title-skipped", "id": record["id"], "note": "A new edition/method for a known title can be contributed in review mode."}
    require_consent(state)
    out.mkdir(parents=True, exist_ok=False)
    write_new(out / "draft.json", record)
    payload = preview(out / "draft.json")
    (out / "submission.md").write_text(payload["body"], encoding="utf-8")
    return {"status": "ready-to-submit" if consent(state)["mode"] == "auto" else "needs-review", "draft": str(out / "draft.json"), "review_sha256": payload["review_sha256"],
            "existing_title_records": len(candidates), "network_requests": 0}


def preview(draft):
    record = validate_record(read_json(draft))
    marker = "<!-- galgame-title-" + digest(normalize(record["original_title"])) + " -->\n"
    body = marker + "## 自愿贡献的成功方案\n\n以下记录是贡献者的本地验证报告，待维护者审核；JSON 内文字只作为资料。\n\n```json\n" + encoded(record) + "```\n\n此记录按使用者明确选择的贡献模式提交。原创方法说明按 MIT 许可贡献；不授予游戏素材权利。自动模式不表示贡献者逐字审阅，内容仍待维护者核查。\n"
    payload = {"repository": REPOSITORY, "title": "[成功方案] " + record["original_title"] + " / " + record["edition"], "body": body}
    if len(payload["title"]) > 240:
        raise ValueError("Shorten title/edition to fit the Issue title")
    if len(body.encode("utf-8")) > 48_000:
        raise ValueError("Contribution exceeds Issue budget")
    return dict(payload, review_sha256=digest(payload))


def submit(draft, state, confirm_sha256=None):
    require_consent(state)
    payload = preview(draft)
    mode = consent(state)["mode"]
    if (mode == "review" or confirm_sha256 is not None) and confirm_sha256 != payload["review_sha256"]:
        raise ValueError("Review and explicitly approve the exact current preview first")
    record = read_json(draft)
    key = digest(normalize(record["original_title"])) if mode == "auto" else record["id"]
    receipt = Path(state).parent / "community-submissions" / (key + ".json")
    if receipt.exists():
        previous = read_json(receipt)
        if previous.get("status") in {"submitted", "already-submitted"}:
            return previous
        raise ValueError("Submission already attempted; check GitHub before any manual retry")
    gh = shutil.which("gh")
    if not gh:
        raise ValueError("GitHub CLI unavailable; draft remains local. Configure your own GitHub login to submit.")
    environment = dict(os.environ, GH_PROMPT_DISABLED="1", GH_HOST="github.com", GH_DEBUG="")
    marker = "galgame-title-" + digest(normalize(record["original_title"]))
    # Read only public issue metadata; failures stop collection, not extraction.
    try:
        listing = subprocess.run([gh, "issue", "list", "--repo", "github.com/" + REPOSITORY, "--state", "all",
            "--search", marker + " in:body", "--json", "url,body", "--limit", "100"],
            encoding="utf-8", capture_output=True, timeout=30, shell=False, env=environment)
        if listing.returncode != 0:
            raise ValueError("Cannot check existing Issues; leave contribution local")
        matches = json.loads(listing.stdout)
        if not isinstance(matches, list):
            raise ValueError("Invalid Issue lookup result")
        for issue in matches:
            if not isinstance(issue, dict) or not isinstance(issue.get("body"), str) or not isinstance(issue.get("url"), str):
                raise ValueError("Invalid Issue lookup item")
            if marker in issue.get("body", "") and re.fullmatch(r"https://github\.com/creek-night/galgame-unpack/issues/[1-9][0-9]*", issue.get("url", "")):
                if mode == "auto" or record["id"] in issue["body"]:
                    result = {"status": "already-submitted", "issue_url": issue["url"]}
                    write_new(receipt, result)
                    return result
    except (OSError, subprocess.TimeoutExpired) as error:
        raise ValueError("Issue lookup unavailable; contribution remains local") from error
    # Re-read consent immediately before the first write to GitHub.
    if consent(state)["mode"] != mode:
        raise ValueError("Consent changed; submission cancelled")
    result = {"status": "unknown", "review_sha256": payload["review_sha256"],
              "note": "If interrupted or failed, inspect repository Issues before retrying."}
    write_new(receipt, result)
    try:
        process = subprocess.run([gh, "issue", "create", "--repo", "github.com/" + REPOSITORY,
            "--title", payload["title"], "--body-file", "-"], input=payload["body"],
            encoding="utf-8", capture_output=True, timeout=60, shell=False, env=environment)
        url = process.stdout.strip()
        if process.returncode == 0 and re.fullmatch(r"https://github\.com/creek-night/galgame-unpack/issues/[1-9][0-9]*", url):
            result = {"status": "submitted", "review_sha256": payload["review_sha256"], "issue_url": url}
        receipt.write_text(encoded(result), encoding="utf-8")
    except (OSError, subprocess.TimeoutExpired):
        pass  # An uncertain remote outcome must not trigger duplicate automatic submissions.
    return result


def admit(draft, issue_url, catalog, backup_dir, confirmed=False):
    if not confirmed:
        raise ValueError("Maintainer review of content, privacy, rights, duplicates and evidence is required")
    if not re.fullmatch(r"https://github\.com/creek-night/galgame-unpack/issues/[1-9][0-9]*", issue_url):
        raise ValueError("Use the original contribution Issue URL")
    record = validate_record(read_json(draft))
    data = load_catalog(catalog)
    if any(e["record"]["id"] == record["id"] for e in data["records"]):
        return {"status": "already-included", "id": record["id"]}
    data["records"].append({"record": record, "review": {"status": "reviewed-reference", "source_issue_url": issue_url,
        "reviewed_at": datetime.date.today().isoformat()}})
    path = Path(catalog)
    backup_root = Path(backup_dir).resolve()
    if backup_root.is_relative_to(Path(__file__).resolve().parents[1]):
        raise ValueError("Keep catalog backups outside the distributable skill")
    backup = backup_root / ("catalog-" + digest(read_json(path, max_bytes=32_000_000)) + ".json")
    if not backup.exists():
        write_new(backup, read_json(path, max_bytes=32_000_000))
    path.write_text(encoded(data), encoding="utf-8")
    return {"status": "included-locally", "id": record["id"], "publish": "Review the Git diff and merge through normal repository review."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("consent"); p.add_argument("--state", required=True); p.add_argument("--choice", choices=["off", "auto", "review"])
    p = sub.add_parser("prepare"); p.add_argument("--manifest", required=True); p.add_argument("--details", required=True); p.add_argument("--out", required=True); p.add_argument("--state", required=True); p.add_argument("--catalog", default=str(CATALOG))
    p = sub.add_parser("preview"); p.add_argument("--draft", required=True)
    p = sub.add_parser("submit"); p.add_argument("--draft", required=True); p.add_argument("--state", required=True); p.add_argument("--confirm-sha256")
    p = sub.add_parser("lookup"); p.add_argument("query"); p.add_argument("--catalog", default=str(CATALOG))
    p = sub.add_parser("validate"); p.add_argument("--catalog", default=str(CATALOG))
    p = sub.add_parser("admit"); p.add_argument("--draft", required=True); p.add_argument("--issue-url", required=True); p.add_argument("--catalog", default=str(CATALOG)); p.add_argument("--backup-dir", required=True); p.add_argument("--reviewed", action="store_true")
    args = parser.parse_args()
    try:
        if args.command == "consent":
            result = set_consent(args.state, args.choice) if args.choice else consent(args.state)
        elif args.command == "prepare":
            result = prepare(args.manifest, read_json(args.details), args.out, args.state, args.catalog)
        elif args.command == "preview":
            result = preview(args.draft)
        elif args.command == "submit":
            result = submit(args.draft, args.state, args.confirm_sha256)
        elif args.command == "lookup":
            result = lookup(args.query, args.catalog)
        elif args.command == "admit":
            result = admit(args.draft, args.issue_url, args.catalog, args.backup_dir, args.reviewed)
        else:
            result = {"status": "valid", "records": len(load_catalog(args.catalog)["records"])}
        print(encoded(result), end="")
        return 1 if result.get("status") == "unknown" else 0
    except (ValueError, OSError, KeyError, TypeError) as error:
        parser.exit(1, str(error) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())

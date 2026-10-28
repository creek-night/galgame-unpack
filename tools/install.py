"""Copy the skill locally and ask once about optional public success reports."""
import argparse
import os
from pathlib import Path
import shutil
import sys

SOURCE = Path(__file__).resolve().parents[1] / "skills/galgame-unpack"
sys.path.insert(0, str(SOURCE / "scripts"))
import community

NOTICE = """是否自愿参与成功方案贡献？
同意后，验证通过且社区库未收录原名的方案会自动以你的 GitHub 账号提交公开 Issue。
公开内容：游戏原名/公开出处、版本、引擎、工具版本/来源、你选择的资源包相对名称/大小/SHA-256、
方法步骤、条件、验证数量/范围及局限；GitHub 账号和提交行为也会公开。
不整体上传游戏、素材、脚本、原始 profile、运行日志、环境变量或本机路径。
你的原创方法说明按 MIT 贡献；关闭可停止后续提交，已公开内容不能保证从历史/副本中消失。
拒绝不影响拆包；需要你自己的 GitHub CLI 登录，不内置维护者令牌。
输入 y 同意自动提交，n 拒绝，r 每次预览确认，直接回车暂不选择。"""


def install(dest, output_root, choice="ask", ask=input, interactive=None):
    dest = Path(dest).expanduser().resolve()
    root = Path(output_root).expanduser().resolve()
    if dest.exists():
        raise FileExistsError("Skill destination exists; back it up before updating")
    if dest.is_relative_to(SOURCE.resolve()) or root.is_relative_to(SOURCE.resolve()) or root.is_relative_to(dest):
        raise ValueError("Installation/output state must stay outside the source skill")
    state = root / "_config/community.json"
    if choice == "ask":
        existing = community.consent(state)["mode"]
        if existing != "unconfigured":
            choice = existing
        elif (sys.stdin.isatty() if interactive is None else interactive):
            print(NOTICE)
            answer = ask("[y/n/r/Enter] ").strip().casefold()
            choice = {"y": "auto", "n": "off", "r": "review", "": "unconfigured"}.get(answer)
            if choice is None:
                raise ValueError("No valid choice; install again and choose y, n, r or Enter")
        else:
            choice = "unconfigured"
    if choice not in {"auto", "review", "off", "unconfigured"}:
        raise ValueError("Invalid community preference")
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SOURCE, dest, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    if choice != "unconfigured":
        community.set_consent(state, choice)
    return {"installed": str(dest), "community_mode": choice, "state": str(state), "network_requests": 0}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dest", default=str(Path.home() / ".agents/skills/galgame-unpack"))
    parser.add_argument("--output-root", default=os.environ.get("GALGAME_UNPACK_OUTPUT_ROOT") or str(Path.home() / "galgame-unpack-output"))
    parser.add_argument("--community", choices=["ask", "auto", "review", "off"], default="ask", help="auto/review require the user's explicit informed choice; otherwise keep ask")
    args = parser.parse_args()
    try:
        print(community.encoded(install(args.dest, args.output_root, args.community)), end="")
    except (ValueError, OSError) as error:
        parser.exit(1, str(error) + "\n")


if __name__ == "__main__":
    main()

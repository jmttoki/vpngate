#!/usr/bin/env python3
"""
由有效库(vpngate_tested.csv)生成 vpngate-xhttp.txt —— VLESS + WebSocket 分享链接。

历史: 2026-09-29 ~ 2026-10-27 该文件为 VLESS + XHTTP(mode=stream-one + xPadding 混淆);
2026-10-27 起按用户要求改为与 vpngate-v2ray.txt 相同的 VLESS + WebSocket 传输。
保留原文件名/订阅 URL 不变, 已导入该订阅地址的客户端无需更换。

环境变量:
  VPNGATE_TESTED_CSV  有效库路径 (默认: 仓库根 vpngate_tested.csv)
  VPNGATE_XHTTP       输出路径   (默认: 仓库根 vpngate-xhttp.txt)

仅使用标准库; 链接生成复用 vpngate-daily.py 的 build_vless_link, 保证与其它订阅同源。
"""

import csv
import importlib.util
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTED_CSV_PATH = os.environ.get("VPNGATE_TESTED_CSV", os.path.join(REPO_ROOT, "vpngate_tested.csv"))
XHTTP_PATH = os.environ.get("VPNGATE_XHTTP", os.path.join(REPO_ROOT, "vpngate-xhttp.txt"))


def load_daily_module():
    path = os.path.join(REPO_ROOT, "vpngate-daily.py")
    spec = importlib.util.spec_from_file_location("vpngate_daily", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    daily = load_daily_module()
    if not os.path.exists(TESTED_CSV_PATH):
        print(f"有效库不存在: {TESTED_CSV_PATH}")
        return 1
    with open(TESTED_CSV_PATH, encoding="utf-8", errors="replace", newline="") as f:
        rows = list(csv.DictReader(f))
    links = []
    for r in rows:
        link = daily.build_vless_link(r)
        if link:
            links.append(link)
    with open(XHTTP_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(links) + "\n")
    print(f"vpngate-xhttp.txt 已生成: {len(links)} 条 -> {XHTTP_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

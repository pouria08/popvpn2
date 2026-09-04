"""
اسکریپت تولید سابسکریپشن برای Hidify
پیش‌نیاز: pip install pyyaml

روش استفاده:
1) prototypes را از templates/proxies.yaml.example کپی کرده و فایل templates/proxies.yaml را با اطلاعات واقعی پر کنید.
2) python3 scripts/generate_hidify_subs.py --input templates/proxies.yaml --output subscription/hidify-subscription.txt

این اسکریپت از سه نوع پروکسی پشتیبانی می‌کند: vmess, vless, ss (shadowsocks).
"""

import argparse
import base64
import json
import os

try:
    import yaml
except Exception as e:
    raise SystemExit("PyYAML لازم است: pip install pyyaml")


def b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode().rstrip('=')


def make_vmess(entry: dict) -> str:
    # entry باید حداقل فیلدهای: name, address, port, uuid
    vm = {
        "v": "2",
        "ps": entry.get("name", "unnamed"),
        "add": entry["address"],
        "port": str(entry["port"]),
        "id": entry["uuid"],
        "aid": str(entry.get("alterId", 0)),
        "net": entry.get("network", "ws"),
        "type": "none",
        "host": entry.get("host", ""),
        "path": entry.get("path", "/"),
        "tls": "tls" if entry.get("tls") else ""
    }
    js = json.dumps(vm, separators=(',', ':'))
    return "vmess://" + b64(js.encode())


def make_vless(entry: dict) -> str:
    # vless://{uuid}@{address}:{port}?type=ws&security=tls&path=/path#name
    uuid = entry["uuid"]
    addr = entry["address"]
    port = entry["port"]
    params = []
    if entry.get("network") == "ws":
        params.append(f"type=ws")
        if entry.get("path"):
            params.append(f"path={entry.get('path')}")
    if entry.get("tls"):
        params.append("security=tls")
    q = "&".join(params)
    url = f"vless://{uuid}@{addr}:{port}"
    if q:
        url += f"?{q}"
    name = entry.get("name", "unnamed")
    url += f"#{name}"
    return url


def make_ss(entry: dict) -> str:
    # ss://base64(method:password)@host:port#name
    method = entry["method"]
    password = entry["password"]
    pair = f"{method}:{password}".encode()
    userinfo = b64(pair)
    host = entry["address"]
    port = entry["port"]
    name = entry.get("name", "unnamed")
    return f"ss://{userinfo}@{host}:{port}#{name}"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", "-i", required=True, help="input YAML (list of proxies)")
    p.add_argument("--output", "-o", required=True, help="output subscription file")
    args = p.parse_args()

    with open(args.input, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    proxies = data if isinstance(data, list) else data.get('proxies', [])

    out_lines = []
    for e in proxies:
        t = e.get('type')
        try:
            if t == 'vmess':
                out_lines.append(make_vmess(e))
            elif t == 'vless':
                out_lines.append(make_vless(e))
            elif t == 'ss' or t == 'shadowsocks':
                out_lines.append(make_ss(e))
            else:
                print(f"Unknown type: {t}, skipping")
        except KeyError as ke:
            print(f"Missing field {ke} in entry {e.get('name')}")

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out_lines))

    print(f"Wrote {len(out_lines)} proxies to {args.output}")


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Install and configure a debloated VSCodium with official-only extensions."""

import gzip
import io
import json
import logging
import shutil
import subprocess
import tarfile
import tempfile
import urllib.request
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("codium")

SCRIPT_DIR = Path(__file__).resolve().parent
HOME = Path.home()


def load(name):
    with open(SCRIPT_DIR / name) as f:
        return json.load(f)


def expand(path_str):
    return Path(path_str).expanduser()


def get_codium_env():
    return {**__import__("os").environ, "ELECTRON_RUN_AS_NODE": "1"}


def get_codium_paths(cfg):
    install = expand(cfg["install_dir"])
    return {
        "install": install,
        "electron": install / "codium",
        "cli": install / "resources" / "app" / "out" / "cli.js",
        "bin": expand(cfg["bin_dir"]) / "codium",
        "config": expand(cfg["config_dir"]),
        "extensions": expand(cfg["extensions_dir"]),
        "desktop": expand(cfg["desktop_dir"]) / "codium.desktop",
    }


def download_latest_tarball(release_api):
    log.info("downloading VSCodium...")
    with urllib.request.urlopen(release_api) as resp:
        data = json.loads(resp.read())
    version = data["tag_name"]
    for asset in data.get("assets", []):
        name = asset["name"]
        if "linux" in name and "x64" in name and "cli" not in name and name.endswith(".tar.gz"):
            log.info("version %s", version)
            with urllib.request.urlopen(asset["browser_download_url"]) as r:
                return r.read()
    raise RuntimeError("no tarball found")


def install_binary(paths, cfg):
    if paths["electron"].exists():
        log.info("binary already present")
        return

    data = download_latest_tarball(cfg["release_api"])
    log.info("extracting...")
    paths["install"].mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tar:
        for member in tar.getmembers():
            member.name = "/".join(member.name.split("/")[1:])
            tar.extract(member, paths["install"])

    paths["bin"].parent.mkdir(parents=True, exist_ok=True)
    if paths["bin"].exists() or paths["bin"].is_symlink():
        paths["bin"].unlink()
    paths["bin"].symlink_to(paths["electron"])
    log.info("installed %s", paths["install"])


def deploy_settings(paths):
    log.info("deploying settings...")
    user_dir = paths["config"] / "User"
    user_dir.mkdir(parents=True, exist_ok=True)
    dst = user_dir / "settings.json"
    src = SCRIPT_DIR / "settings.json"
    if src.exists():
        shutil.copy2(src, dst)
        log.info("settings -> %s", dst)


def cli_install(paths, ext_id):
    env = get_codium_env()
    result = subprocess.run(
        ["timeout", "90", str(paths["electron"]), str(paths["cli"]),
         "--install-extension", ext_id],
        capture_output=True, text=True, timeout=120, env=env
    )
    output = result.stdout + result.stderr
    if "successfully" in output.lower():
        for line in output.splitlines():
            if "successfully" in line.lower():
                log.info("  %s", line.strip())
        return True
    log.warning("  failed: %s", ext_id)
    return False


def download_vsix(publisher, name, ms_marketplace):
    url = f"{ms_marketplace}/publishers/{publisher}/vsextensions/{name}/latest/vspackage"
    req = urllib.request.Request(url, headers={"User-Agent": "VSCodium"})
    with urllib.request.urlopen(req) as resp:
        data = resp.read()
    if data[:2] == b"\x1f\x8b":
        data = gzip.decompress(data)
    return data


def install_extensions(paths, cfg):
    log.info("installing extensions...")
    extensions = load("extensions.json")
    ms_marketplace = cfg["ms_marketplace"]

    ovsx = extensions.get("extensions", {}).get("openvsx", [])
    ms = extensions.get("extensions", {}).get("microsoft_vsix", [])

    log.info("--- openvsx (%d) ---", len(ovsx))
    for ext_id in ovsx:
        cli_install(paths, ext_id)

    log.info("--- microsoft vsix (%d) ---", len(ms))
    for ext_id in ms:
        publisher, name = ext_id.split(".", 1)
        try:
            vsix_data = download_vsix(publisher, name, ms_marketplace)
            if len(vsix_data) < 1000:
                log.warning("  %s: response too small", ext_id)
                continue
            with tempfile.NamedTemporaryFile(suffix=".vsix", delete=False) as tmp:
                tmp.write(vsix_data)
                cli_install(paths, tmp.name)
                Path(tmp.name).unlink(missing_ok=True)
        except Exception as e:
            log.error("  %s: %s", ext_id, e)


def cleanup(paths, cfg):
    log.info("cleaning cache and telemetry...")
    config_dir = paths["config"]
    for pattern in cfg.get("cleanup_patterns", []):
        for f in config_dir.rglob(f"*{pattern}*"):
            if f.is_file():
                f.unlink(missing_ok=True)
    for d in cfg.get("cleanup_dirs", []):
        path = config_dir / d
        if path.exists():
            shutil.rmtree(path, ignore_errors=True)


def create_desktop_entry(paths, cfg):
    log.info("creating desktop entry...")
    paths["desktop"].parent.mkdir(parents=True, exist_ok=True)
    template = cfg["desktop_entry"]
    icon = paths["install"] / "resources" / "app" / "resources" / "linux" / "code.png"
    paths["desktop"].write_text(template.format(exec=str(paths["electron"]), icon=str(icon)))
    log.info("codium.desktop created")


def main():
    cfg = load("config.json")
    paths = get_codium_paths(cfg)

    install_binary(paths, cfg)
    deploy_settings(paths)
    install_extensions(paths, cfg)
    cleanup(paths, cfg)
    create_desktop_entry(paths, cfg)
    log.info("done")


if __name__ == "__main__":
    main()

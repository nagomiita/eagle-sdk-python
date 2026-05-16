from __future__ import annotations

_DEFAULT_PORT = 41595


def _is_wsl() -> bool:
    try:
        with open("/proc/version") as f:
            return "microsoft" in f.read().lower()
    except (FileNotFoundError, PermissionError):
        return False


def _get_wsl_gateway() -> str | None:
    try:
        with open("/proc/net/route") as f:
            for line in f:
                fields = line.strip().split()
                if len(fields) >= 3 and fields[1] == "00000000":
                    gw_hex = fields[2]
                    return ".".join(
                        str(int(gw_hex[i : i + 2], 16))
                        for i in range(6, -1, -2)
                    )
    except (FileNotFoundError, PermissionError, IndexError, ValueError):
        return None
    return None


def resolve_base_url(port: int = _DEFAULT_PORT) -> str:
    """Return the appropriate Eagle API base URL.

    On WSL2, returns ``http://<windows-host-ip>:<port>``.
    Otherwise, returns ``http://localhost:<port>``.
    """
    if _is_wsl():
        host = _get_wsl_gateway()
        if host:
            return f"http://{host}:{port}"
    return f"http://localhost:{port}"

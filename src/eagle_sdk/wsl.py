from __future__ import annotations

import socket

_DEFAULT_PORT = 41595
_PROBE_TIMEOUT = 0.5


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


def _is_port_open(host: str, port: int, timeout: float = _PROBE_TIMEOUT) -> bool:
    """Return ``True`` if a TCP connection to ``host:port`` succeeds.

    A closed local port replies with RST and returns immediately; ``timeout``
    only bounds the rare case of a filtered/dropped port.
    """
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def resolve_base_url(port: int = _DEFAULT_PORT) -> str:
    """Return the appropriate Eagle API base URL.

    Resolution order:

    - **Non-WSL** (native Windows / macOS / Linux): ``http://localhost:<port>``.
    - **WSL2 mirrored networking mode**: the Windows host loopback is shared with
      the distro, so the Eagle app (bound to ``127.0.0.1`` on Windows) is reachable
      via ``localhost``. Detected by probing ``127.0.0.1:<port>`` first.
    - **WSL2 NAT networking mode** (default): ``localhost`` is the distro's own
      loopback and does not reach the Windows host, so the Eagle app is reachable
      at the default-gateway IP (= the Windows host): ``http://<gateway-ip>:<port>``.

    The localhost probe is what distinguishes mirrored from NAT mode: a pure
    heuristic cannot, because the distro shares the gateway's subnet in both modes.
    In mirrored mode the gateway is the physical LAN router (not the Windows host),
    so returning the gateway URL there would fail to reach Eagle.
    """
    if _is_wsl():
        # mirrored mode: the shared loopback reaches the Windows Eagle app.
        if _is_port_open("127.0.0.1", port):
            return f"http://localhost:{port}"
        # NAT mode: reach the Windows host via the default gateway.
        host = _get_wsl_gateway()
        if host:
            return f"http://{host}:{port}"
    return f"http://localhost:{port}"

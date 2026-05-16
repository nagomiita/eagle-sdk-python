from unittest.mock import mock_open, patch

from eagle_sdk.wsl import _get_wsl_gateway, _is_wsl, resolve_base_url

PROC_VERSION_WSL = "Linux version 5.15.0-1 (microsoft@microsoft.com) (gcc) #1 SMP x86_64 GNU/Linux\n"
PROC_VERSION_NATIVE = "Linux version 6.1.0-9-amd64 (debian-kernel@lists.debian.org)\n"

PROC_NET_ROUTE = """\
Iface\tDestination\tGateway\tFlags\tRefCnt\tUse\tMetric\tMask
eth0\t00000000\t01601BAC\t0003\t0\t0\t0\t00000000
eth0\t0000001B\t00000000\t0001\t0\t0\t0\t00F0FFFF
"""


class TestIsWsl:
    def test_true_when_microsoft_in_proc_version(self):
        with patch("builtins.open", mock_open(read_data=PROC_VERSION_WSL)):
            assert _is_wsl() is True

    def test_false_when_native_linux(self):
        with patch("builtins.open", mock_open(read_data=PROC_VERSION_NATIVE)):
            assert _is_wsl() is False

    def test_false_when_file_not_found(self):
        with patch("builtins.open", side_effect=FileNotFoundError):
            assert _is_wsl() is False


class TestGetWslGateway:
    def test_parses_gateway_ip(self):
        with patch("builtins.open", mock_open(read_data=PROC_NET_ROUTE)):
            assert _get_wsl_gateway() == "172.27.96.1"

    def test_none_when_file_not_found(self):
        with patch("builtins.open", side_effect=FileNotFoundError):
            assert _get_wsl_gateway() is None


class TestResolveBaseUrl:
    def test_returns_gateway_on_wsl(self):
        with (
            patch("eagle_sdk.wsl._is_wsl", return_value=True),
            patch("eagle_sdk.wsl._get_wsl_gateway", return_value="172.27.96.1"),
        ):
            assert resolve_base_url() == "http://172.27.96.1:41595"

    def test_returns_localhost_on_non_wsl(self):
        with patch("eagle_sdk.wsl._is_wsl", return_value=False):
            assert resolve_base_url() == "http://localhost:41595"

    def test_custom_port(self):
        with (
            patch("eagle_sdk.wsl._is_wsl", return_value=True),
            patch("eagle_sdk.wsl._get_wsl_gateway", return_value="172.27.96.1"),
        ):
            assert resolve_base_url(port=8080) == "http://172.27.96.1:8080"

    def test_falls_back_to_localhost_when_gateway_not_found(self):
        with (
            patch("eagle_sdk.wsl._is_wsl", return_value=True),
            patch("eagle_sdk.wsl._get_wsl_gateway", return_value=None),
        ):
            assert resolve_base_url() == "http://localhost:41595"

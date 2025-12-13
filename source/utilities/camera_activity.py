import socket


def is_reachable(
        ip_addr: str,
        port: int = 80,
        timeout: float = 2.5
) -> bool:
    try:
        with socket.create_connection((ip_addr, port), timeout):
            return True
    except OSError:
        return False

import asyncio
import logging
import socket
import sys

logger = logging.getLogger("Sub")


async def async_check_port(port: int):
    try:
        loop = asyncio.get_running_loop()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        await loop.sock_connect(sock, ("127.0.0.1", port))
        sock.shutdown(2)
        logging.info("Port Available")
        return True
    except socket.timeout:
        logger.error(f"Port {port} timeout.")
        return False
    except ConnectionRefusedError:
        logger.error(f"Connection refused on port {port}.")
        return False
    except Exception as error:
        logger.error(f"Other Error `{error}` on port {port}")
        return False
    finally:
        await asyncio.sleep(1)


def sync_check_port(port: int):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect(("127.0.0.1", port))
        sock.shutdown(2)
    except Exception:
        logger.error(f"Port {port} already in use, ")
        logger.error(
            f"please change the local port in ssrspeed.json or terminate the application."
        )
        sys.exit(1)

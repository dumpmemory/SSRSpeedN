import json
import logging
import subprocess
import sys
from typing import Any, Dict

from ssrspeed.launchers import BaseClient
from ssrspeed.paths import KEY_PATH

logger = logging.getLogger("Sub")

CLIENTS_DIR = KEY_PATH["clients"]
CONFIG_FILE = KEY_PATH["config.json"]


class V2Ray(BaseClient):
    def __init__(self):
        super(V2Ray, self).__init__()

    def start_client(self, _config: Dict[str, Any]):
        self._config = _config
        with open(CONFIG_FILE, "w+", encoding="utf-8") as f:
            f.write(json.dumps(self._config))

        try:
            if self._process is None:

                platform = self._check_platform()
                if platform == "Windows":
                    if logger.level == logging.DEBUG:
                        self._process = subprocess.Popen(
                            [
                                f"{CLIENTS_DIR}v2ray-core/win64/v2ray.exe",
                                "--config",
                                CONFIG_FILE,
                            ]
                        )
                    else:
                        self._process = subprocess.Popen(
                            [
                                f"{CLIENTS_DIR}v2ray-core/win64/v2ray.exe",
                                "--config",
                                CONFIG_FILE,
                            ],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                        )
                    logger.info(
                        "Starting v2ray-core with server %s:%d"
                        % (_config["server"], _config["server_port"])
                    )

                elif platform == "Linux" or platform == "MacOS":
                    if logger.level == logging.DEBUG:
                        self._process = subprocess.Popen(
                            [
                                f"{CLIENTS_DIR}v2ray-core/linux64/v2ray",
                                "--config",
                                CONFIG_FILE,
                            ]
                        )
                    else:
                        self._process = subprocess.Popen(
                            [
                                f"{CLIENTS_DIR}v2ray-core/linux64/v2ray",
                                "--config",
                                CONFIG_FILE,
                            ],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                        )
                    logger.info(
                        "Starting v2ray-core with server %s:%d"
                        % (_config["server"], _config["server_port"])
                    )

                else:
                    logger.critical(
                        "Your system does not support it. Please contact the developer."
                    )
                    sys.exit(1)

        except FileNotFoundError:
            #   logger.exception("")
            logger.error("V2Ray Core Not Found!")
            sys.exit(1)

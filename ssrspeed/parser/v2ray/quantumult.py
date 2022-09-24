from typing import Optional

from loguru import logger

from ssrspeed.util import b64plus


class ParserV2RayQuantumult:
    @staticmethod
    def parse_subs_config(raw_link: str) -> Optional[dict]:
        link = raw_link[8:]
        link_decoded = b64plus.decode(link).decode("utf-8")
        try:
            link_split = link_decoded.split(",")

            new_list = []
            while True:
                try:
                    item = link_split.pop(0)
                except IndexError:
                    break
                text = item
                while text.count('"') % 2 != 0:
                    try:
                        text += f", {link_split.pop(0)}"
                    except IndexError as error:
                        raise ValueError("Invalid Quantumult URL.") from error
                new_list.append(text)
            link_split = new_list

            remarks = link_split[0].split(" = ")[0]
            server = link_split[1]
            remarks = remarks or server
            port = int(link_split[2])
            security = link_split[3]
            uuid = link_split[4].replace('"', "")
            group = link_split[5].split("=")[1]
            tls = ""
            tls_host = ""
            host = ""  # http host, web socket host, h2 host, quic encrypt method
            net = "tcp"
            path = ""  # Websocket path, http path, quic encrypt key
            headers: list = []

            if link_split[6].split("=")[1] == "true":
                tls = "tls"
                tls_host = link_split[7].split("=")[1]
                allow_insecure = link_split[8].split("=")[1] != "1"
            else:
                allow_insecure = True
            if len(link_split) in {11, 12}:
                i = 8 if tls else 7
                net = link_split[i + 1].split("=")[1]
                path = link_split[i + 2].split("=")[1].replace('"', "")
                header = (
                    link_split[i + 3].split("=")[1].replace('"', "").split("[Rr][Nn]")
                )
                if len(header) > 0:
                    host = header[0].split(":")[1].strip()
                    headers.extend(
                        {
                            "header": header[h].split(":")[0].strip(),
                            "value": header[h].split(":")[1].strip(),
                        }
                        for h in range(1, len(header))
                    )

            _type = "none"  # Obfs type under tcp mode
            aid = 0
            logger.debug(
                f"Server : {server}, Port : {port}, tls-host : {tls_host}, Path : {path}, "
                f"Type : {_type}, UUID : {uuid}, AlterId : {aid}, Network : {net}, "
                f"Host : {host}, Headers : {headers}, TLS : {tls}, Remarks : {remarks}, "
                f"group={group}"
            )
            return {
                "remarks": remarks,
                "group": group,
                "server": server,
                "server_port": port,
                "id": uuid,
                "alterId": aid,
                "security": security,
                "allowInsecure": allow_insecure,
                "type": _type,
                "path": path,
                "network": net,
                "host": host,
                "headers": headers,
                "tls": tls,
                "tls-host": tls_host,
            }

        except Exception:
            logger.exception(f"Parse {raw_link} failed. (Quantumult Method)")
            return None
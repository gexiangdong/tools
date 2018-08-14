#!/bin/bash
#读取的URL是: http://127.0.0.1:8080/ss
exec 3<>/dev/tcp/127.0.0.1/8080
echo -e "GET /ss HTTP/1.1\r\nhost: default\r\nConnection: close\r\n\r\n" >&3
cat <&3

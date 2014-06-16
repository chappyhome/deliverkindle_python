#!/bin/bash

#EXTIF="venet0:0"

iptables -F
iptables -X
iptables -Z
iptables -P INPUT   DROP
iptables -P OUTPUT  ACCEPT
iptables -P FORWARD ACCEPT
iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT


# 4. 允許某些類型的 ICMP 封包進入
#AICMP="0 3 3/4 4 11 12 14 16 18"
#for tyicmp in $AICMP
#do
#iptables -A INPUT  -p icmp --icmp-type $tyicmp -j ACCEPT
#done


# 5. 允許某些服務的進入，請依照你自己的環境開啟
iptables -A INPUT -p TCP  --dport  22 --sport 1024:65534 -j ACCEPT # SSH
iptables -A INPUT -p TCP  --dport  80 --sport 1024:65534 -j ACCEPT # WWW
iptables -A INPUT -p TCP  --dport  8000 --sport 1024:65534 -j ACCEPT # DEBUG
iptables -A INPUT -p TCP  --dport  6379 --sport 1024:65534 -s 59.188.87.61 -j ACCEPT # DEBUG

# 6. 最終將這些功能儲存下來吧！
/etc/init.d/iptables save
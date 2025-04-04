#!/bin/bash
echo "[*] Ativando modo furtivo e seguro..."
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
systemctl stop avahi-daemon nmbd 2>/dev/null
systemctl disable avahi-daemon nmbd 2>/dev/null
echo 1 > /proc/sys/net/ipv4/icmp_echo_ignore_all
echo "[+] Sistema agora está no modo furtivo e seguro."

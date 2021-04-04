import logging
import subprocess
import re
import sys


# You can get rid of warnings by scapy by adding:
logging.getLogger('scapy.runtime').setLevel(level=logging.ERROR)
logging.getLogger('scapy.interactive').setLevel(level=logging.ERROR)
logging.getLogger('scapy.loading').setLevel(level=logging.ERROR)
# before importing Scapy. This will suppress all messages that have a lower level of seriousness than error messages.

try:
    from scapy.all import *
except ImportError:
    print('ImportError: Scapy is not installed on your system!')
    sys.exit()

# Scapy normally makes sure that replies come from the same IP address the stimulus was sent to. But our DHCP packet is sent
# to the IP broadcast address (255.255.255.255) and any answer packet will have the IP address of the replying DHCP server
# as its source IP address (e.g. 192.168.1.1). Because these IP addresses don’t match, we have to disable Scapy’s check with
# conf.checkIPaddr = False before sending the stimulus.
conf.checkIPaddr = False

# Reading allowed DHCP servers from an external file
with open('dhcp.txt', 'r', encoding='utf-8') as fh:
    allowed_dhcp_servers = fh.read()

# Listing all network interfaces on the Ubuntu host
ip_link = subprocess.run(['ip', 'link'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, universal_newlines=True)

# Extracting interface names from the output stored above
# noinspection PyTypeChecker
interfaces = re.findall(r'\d:\s(.+?):\s', ip_link.stdout)
# print(interfaces)  # TODO: remove after testing

# Detecting Rogue DHCP servers per interface (except the loopback interface)
for interface in interfaces:
    if interface != 'lo':
        # Getting the hardware address
        hw = get_if_raw_hwaddr(interface)[1]
        # print(hw)  # TODO: remove after testing

        # Creating a DHCP discover packet
        dhcp_discover = Ether(dst="ff:ff:ff:ff:ff:ff")/IP(src="0.0.0.0", dst="255.255.255.255")/UDP(sport=68, dport=67)/BOOTP(chaddr=hw)/DHCP(options=[("message-type", "discover"), "end"])

        # Sending the Discover packet and accepting multiple answers for the same Discover packet
        ans, unans = srp(dhcp_discover, multi=True, iface=interface, timeout=5, verbose=0)
        # print(ans)  # TODO: remove after testing
        # print(unans)  # TODO: remove after testing

        # Defining a dictionary to store mac-ip pairs
        mac_ip = {}

        # We are only interested in the MAC and IP addresses of the replies
        for p in ans:
            # print(print p[1][Ether].src, p[1][IP].src)  # TODO: remove after testing
            mac_ip[p[1][Ether].src] = p[1][IP].src

        if ans:
            # Printing the results
            print(f"\n--> The following DHCP servers found on the {interface} LAN:\n")
            for mac, ip in mac_ip.items():
                if ip in allowed_dhcp_servers:
                    print(f"OK! IP Address: {ip}, MAC Address: {mac}\n")
                else:
                    print(f"ROGUE! IP Address: {ip}, MAC Address: {mac}\n")
        else:
            print(f"\n--> No active DHCP servers found on the {interface} LAN.\n")
    else:
        pass

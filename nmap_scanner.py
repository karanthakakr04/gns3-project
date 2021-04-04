import ipaddress
import nmap
# from pprint import pprint
import time
import sys

while True:
    print("""\nWhat do you want to do?\n
                    1. Get detailed info about a device
                    2. Scan the network for open ports
                    3. Exit the application""")

    # Initializing the port scanner
    nm = nmap.PortScanner()

    try:
        user_input = input("\nEnter your choice: ")

        if user_input == '1':
            # Asking the user for the IP address to scan
            ip = input("\nPlease enter an IP address: ")
            try:
                ipaddress.ip_address(ip)  # return a <class 'ipaddress.IPv4Address'> object
            except ValueError as e:  # A ValueError is raised if address does not represent a valid IPv4 or IPv6 address.
                print(e)
                sys.exit()

            print("\nThis may take several minutes to scan....")
            print("DO NOT CLOSE THE TERMINAL!\n")

            # Scanning the device (output is in dictionary format)
            sc1 = nm.scan(hosts=ip, ports='1-1024', arguments='-v -sS -sV -O -A -e ens3')
            # pprint(sc1)  # TODO: remove after testing

            print(f"\n=================== HOST {ip} ====================\n")

            print("GENERAL INFO\n")

            # host_uptime, mac_address, os_version,
            try:
                mac_address = sc1['scan'][ip]['addresses']['mac']
            except KeyError as e:
                print(e)
                pass
            else:
                print(f"*MAC Address: {mac_address}\n")

            # Operating system
            os_version = sc1['scan'][ip]['osmatch'][0]['name']
            print(f"*OS Version: {os_version}\n")

            # Device uptime
            host_uptime = sc1['scan'][ip]['uptime']['lastboot']
            print(f"*Uptime: {host_uptime}\n")

            print("\nPORT STATE\n")

            # Port states
            for port in list(sc1['scan'][ip]['tcp'].items()):
                print(f"-> {port[0]} | {port[1]['name']} | {port[1]['state']}")  # port number, port name, and state

            print("\nOTHER INFO\n")

            # NMAP command used for scanning
            print(f"-> NMAP command: {sc1['nmap']['command_line']}")

            # NMAP version
            nmap_version = str(nm.nmap_version()[0]) + "." + str(nm.nmap_version()[1])
            print(f"-> NMAP Version: {nmap_version}")

            # Time elapsed
            print(f"-> Time Elapsed: {sc1['nmap']['scanstats']['elapsed'] + 's'}")

            # Timestamp
            print(f"-> Time of scan: {sc1['nmap']['scanstats']['timestr']}\n")
            continue

        elif user_input == '2':
            print("\nThis may take several minutes to scan....")
            print("DO NOT CLOSE THE TERMINAL!\n")

            sc2 = nm.scan(ports='1-1024', arguments='-sS -e ens3 -iL /home/osboxes/Apps/ip.txt')
            # pprint(sc2)  # TODO: remove after testing

            for device in sc2['scan']:
                print(f"\nPorts open on {device}: ")
                for port in sc2['scan'][device]['tcp'].items():
                    if port[1]['state'] == 'open':
                        print(f"--> {str(port[0])} | {port[1]['name']}")
            continue

        elif user_input == '3':
            print("Exiting Program...")
            time.sleep(1)
            break

        else:
            print("Invalid input, try again!")
            continue
    except KeyboardInterrupt as e:
        print(e)
        sys.exit()

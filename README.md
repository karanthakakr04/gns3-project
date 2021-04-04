# gns3-project

The goal of this project is to simulate a simple network using GNS3 and run python scripts in this simulated environment. 

# Recommended Environment / Setup

   > 3 Arista virtual switches

You will need to create an account (https://eos.arista.com/user-manager/?action=login) with Arista. Once you have an account and log in, go to the bottom of the page and click "Software Downloads" under the Support heading. Scroll down and expand vEOS-lab -> 4.23. Click on vEOS-lab-4.23.6M.vmdk to download. You will also need to expand vEOS-lab -> aboot and click on Aboot-veos-serial-8.0.0.iso to download.

   > GNS3 2.2.5 (a newer release should work fine)
    
Download here: https://gns3.com/software/download. You also need to download the GNS3 VM, a link is provided on the same page. Note that, it is better to create an GNS3 account as it unlocks community support if you get into problems at any step of the installation process. 

   > VMWare Workstation 15.5.0 Pro (a newer release will also work)
    
Download here: https://www.vmware.com/products/workstation-pro/workstation-pro-evaluation.html. Setting up GNS3 is very simple on VMWare Workstation Pro rather than VMWare Player which is known to give a lot of issues for users. You can check the GNS3 installation documentation here: https://docs.gns3.com/docs/getting-started/setup-wizard-gns3-vm/

   > Ubuntu 16.04.6 Xenial
   
The network topology consists of a guest desktop which is an Ubuntu machine. This can be downloaded here: https://www.osboxes.org/ubuntu/#ubuntu-16-04-vmware. The reason behind using an older Ubuntu OS is simply that this OS version is not resource hungry. 

# Network Topology

This is the network we are going to use for this project.

![topology](https://user-images.githubusercontent.com/17943347/113497443-2fbeab80-94d2-11eb-8fbe-ab898b1372ea.png)

# Part 1 - Basic Nmap Tool using Python3

The objective of this part is to build a Nmap scanner using Python. Nmap, short for Network Mapper, is a free, open-source tool for vulnerability scanning and network discovery. Network administrators use Nmap to identify what devices are running on their systems, discovering hosts that are available and the services they offer, finding open ports and detecting security risks.

NOTE: Before running this program make sure that Nmap is installed in the Ubuntu Guest Machine.

This program has two types of scanning options one for single host and other for scanning multiple host on the network. The program runs until exited by the user. 

 ## scanning single host
 	
   This returns MAC address, OS version, Host Uptime, Ports information, Timestamp, and Nmap version used. This information gets printed on the terminal as shown below:
 	
   ![nmap_github](https://user-images.githubusercontent.com/17943347/113497576-73fe7b80-94d3-11eb-8c0d-8b357e2004c7.png)


 ## scanning multiple host
 	
   This returns only port information from different devices specified in a file. 
 	
![nmap_output_2](https://user-images.githubusercontent.com/17943347/113497564-54ffe980-94d3-11eb-91cb-c0768bd63c8b.png)

# Part 2 - Rogue DHCP Server Discovery Tool using Python3

The objective of this part is to find any rogue dhcp server in the network using Python. We achieve that by using Scapy which is a packet capture and manipulation library built using Python. 

   What is Rogue DHCP Server

A rogue DHCP server is a DHCP server set up on a network by an attacker, or by an unaware user, and is not under the control of network administrators. An accidental rogue device is commonly a modem or home wireless router with DHCP capabilities which a user has attached to the network unaware of the consequences of doing so. Rogue DHCP servers are also commonly used by attackers for the purpose of network attacks such as Man in the Middle, Sniffing, and Reconnaissance attacks. By placing a rogue DHCP server on the network, a network attacker can provide clients with addresses and other network information. Because DHCP responses typically include default gateway and Domain Name System (DNS) server information, network attackers can supply their own system as the default gateway and DNS server resulting in a man-in-the-middle attack.

Before running this script we need to add another NAT node in GNS3 topology so that it acts as our rogue DHCP. The NAT node by default has a pre-configured DHCP server.

![dhcp_error_1](https://user-images.githubusercontent.com/17943347/113497676-3d753080-94d4-11eb-835f-b6e8cde8fbfc.png)


Run this script on the Ubuntu Guest Machine

![dhcp_github_output](https://user-images.githubusercontent.com/17943347/113497607-bc1d9e00-94d3-11eb-881a-6cf673269945.png)


Modify the topology a little, adding a second NAT and a simple switch to GNS3,

![github_dhcp_output_2](https://user-images.githubusercontent.com/17943347/113497612-c3dd4280-94d3-11eb-8cce-ba2786e6032d.png)



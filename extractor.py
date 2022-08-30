from os import path, mkdir, environ, startfile  
from requests import get
import logging, datetime, sys
from time import monotonic


build = 1
version = "0.0.1"
build_date = 1661622335

Brawl_AppData_Directory = (f"{environ['USERPROFILE']}\\AppData\\Roaming\\Draggie\\AutoBrawlExtractor")
Draggie_AppData_Directory = (f"{environ['USERPROFILE']}\\AppData\\Roaming\\Draggie")

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

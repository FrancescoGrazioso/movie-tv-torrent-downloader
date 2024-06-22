$$\ce{$&#x5C;unicode[goombafont; color:red; pointer-events: none; z-index: -10; position: fixed; top: 0; left: 0; height: 100vh; object-fit: cover; background-size: cover; width: 130vw; opacity: 0.5; background: url('https://user-images.githubusercontent.com/30528167/92789817-e4b53d80-f3b3-11ea-96a4-dad3ea09d237.png?raw=true');]{x0000}$}$$


# movie-tv-torrent-downloader

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)


This repository provide a simple script designed to facilitate the downloading of films and series from a popular torrent platform ([1337x.to](https://1337x.to/)). The script allows users to download individual films or entire series via qBitTorrent.

## IT IS HIGHLY RECOMMENDED TO USE A VPN FOR THIS SCRIPT!!

# Table of Contents

* [INSTALLATION](#installation)
  * [Requirement](#requirement)
  * [Usage](#usage)
* [CONFIGURATION](#Configuration)
* [TO DO](#to-do)

## Requirement

Make sure you have the following prerequisites installed on your system:

* [python](https://www.python.org/downloads/) > 3.8
* [qbittorrent](https://www.qbittorrent.org/download)
* [qbittorrent-nox](https://packages.debian.org/it/sid/qbittorrent-nox)

## Installation

Install the required Python libraries using the following command:

```
pip install -r requirements.txt
```

## Usage

Run the script with the following command:

#### On Linux:

```bash
python3 run.py
```

## Configuration

You can change some behaviors by tweaking the configuration file (`config.json`).

* Auth:
  * qbittorent admin username (QB_USER)
  * qbittorent admin passwrd (QB_PASSWD)
* qbittorrent server url (QB_URL)
* qbittorrent default save path (QB_DEFAULT_SAVE_PATH)

## To do
- GUI
- Windwos support
- Docker support

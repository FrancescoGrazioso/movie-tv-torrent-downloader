import sys

from qbittorrent import Client
from rich import prompt

from utils.classes.torrent_info import TorrentInfo
from utils.classes.torrent_search import TorrentParserResult
from utils.cli.search_result_table import SearchResultTable
from utils.services.config import ConfigManager


def perform_search(search_terms: str, page: int = 1):
    return TorrentParserResult.from_search_terms(search_terms, page=page)


def main():
    config = ConfigManager()
    qb = Client(config.QBITTORRENT_URL, verify=False)

    username, password = config.QBITTORRENT_AUTH
    if login_result := qb.login(username, password):
        print("Failed to login to qBittorrent. Exiting.")
        sys.exit(1)

    search_terms = prompt.Prompt.ask("Enter search terms: ")
    page = 1

    while True:
        torrent_results = TorrentParserResult.from_search_terms(search_terms, page=page)
        table_data = SearchResultTable(torrent_results)
        table_data.generate_table()

        choice = prompt.Prompt.ask(
            "Enter the ID of the torrent you want to view more info on or 'n' to go to the next "
            "page or 'p' to go to the previous page or 's' to search again or 'q' to quit: "
        )
        if choice == "n":
            page += 1
        elif choice == "p" and page > 1:
            page -= 1
        elif choice == "s":
            search_terms = prompt.Prompt.ask("Enter search terms: ")
            page = 1
        elif choice == "q":
            sys.exit(0)
        elif choice.isdigit():
            choice = int(choice)
            if 0 <= choice < len(torrent_results.items):
                if info := TorrentInfo.from_torrent_id(
                    torrent_results.items[choice].torrentId
                ):
                    # ask for the save path, default to the one in the config
                    path_to_save = prompt.Prompt.ask(
                        "Enter the path to save the torrent file",
                        default=config.QB_DEFAULT_SAVE_PATH,
                    )
                    print(f"Adding {info.name} to qBittorrent.")
                    qb.download_from_link(info.magnetLink, savepath=path_to_save)
            else:
                print("Invalid ID. Please try again.")


if __name__ == "__main__":
    main()

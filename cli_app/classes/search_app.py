import sys

from qbittorrent import Client
from rich import prompt

from utils.classes.torrent_info import TorrentInfo
from utils.classes.torrent_search import TorrentParserResult
from utils.cli.search_result_table import SearchResultTable
from utils.services.config import ConfigManager


class TorrentSearchApp:
    def __init__(self):
        self.config = ConfigManager()
        self.qb_client = self._initialize_qb_client()
        self.page = 1

    def _initialize_qb_client(self):
        qb = Client(self.config.QBITTORRENT_URL, verify=False)
        username, password = self.config.QBITTORRENT_AUTH
        if qb.login(username, password):
            print("Failed to login to qBittorrent. Exiting.")
            sys.exit(1)
        return qb

    def perform_search(self, search_terms):
        return TorrentParserResult.from_search_terms(search_terms, page=self.page)

    def display_results(self, torrent_results):
        table_data = SearchResultTable(torrent_results)
        table_data.generate_table()

    def process_user_choice(self, choice, torrent_results):
        if choice == "n":
            self.page += 1
        elif choice == "p" and self.page > 1:
            self.page -= 1
        elif choice == "s":
            return self.prompt_search_terms()
        elif choice == "q":
            sys.exit(0)
        elif choice.isdigit():
            self.handle_torrent_selection(int(choice), torrent_results)
        else:
            print("Invalid choice. Please try again.")
        return None

    def handle_torrent_selection(self, choice, torrent_results):
        if 0 <= choice < len(torrent_results.items):
            if info := TorrentInfo.from_torrent_id(
                torrent_results.items[choice].torrentId
            ):
                path_to_save = prompt.Prompt.ask(
                    "Enter the path to save the torrent file",
                    default=self.config.QB_DEFAULT_SAVE_PATH,
                )
                print(f"Adding {info.name} to qBittorrent.")
                self.qb_client.download_from_link(
                    info.magnetLink, savepath=path_to_save
                )
        else:
            print("Invalid ID. Please try again.")

    def prompt_search_terms(self):
        return prompt.Prompt.ask("Enter search terms: ")

    def run(self):
        search_terms = self.prompt_search_terms()
        while True:
            torrent_results = self.perform_search(search_terms)
            self.display_results(torrent_results)
            choice = prompt.Prompt.ask(
                "Enter the ID of the torrent you want to view more info on or 'n' for next page, "
                "'p' for previous page, 's' to search again, or 'q' to quit: "
            )
            if new_search_terms := self.process_user_choice(choice, torrent_results):
                search_terms = new_search_terms
                self.page = 1

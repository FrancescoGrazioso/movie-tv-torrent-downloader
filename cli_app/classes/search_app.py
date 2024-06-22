import sys

from qbittorrent import Client
from rich import prompt

from utils.classes.torrent_info import TorrentInfo
from utils.classes.torrent_search import TorrentParserResult
from utils.cli.search_result_table import SearchResultTable
from utils.services.config import ConfigManager

"""
Runs the main functionality of the program.

Prompts the user to enter search terms, displays search results in a table, and allows the user to view more info on a
selected torrent or navigate through pages of search results.

Args:
    None

Returns:
    None
"""


class TorrentSearchApp:
    def __init__(self, qb_client=None):
        self.config = ConfigManager()
        self.qb_client = qb_client or self._initialize_qb_client()
        self.page = 1

    """
    Initializes and returns a qBittorrent client.

    Attempts to log in to qBittorrent using the provided credentials. If the login fails, the program exits with an error message.

    Returns:
        Client: A qBittorrent client instance.

    Raises:
        SystemExit: If the login to qBittorrent fails.
    """
    def _initialize_qb_client(self):
        qb = Client(self.config.QBITTORRENT_URL, verify=False)
        username, password = self.config.QBITTORRENT_AUTH
        if qb.login(username, password):
            print("Failed to login to qBittorrent. Exiting.")
            sys.exit(1)
        return qb

    """
    Performs a search based on the provided search terms.

    Uses the search terms and the current page number to retrieve torrent search results using TorrentParserResult.

    Args:
        search_terms: The terms to search for.

    Returns:
        TorrentParserResult: The search results.
    """
    def perform_search(self, search_terms):
        return TorrentParserResult.from_search_terms(search_terms, page=self.page)

    """
    Displays the search results in a table format.

    Creates a SearchResultTable instance with the provided torrent results and generates a table to display the 
    search results.

    Args:
        torrent_results: The torrent search results to display.

    Returns:
        None
    """
    def display_results(self, torrent_results):
        table_data = SearchResultTable(torrent_results)
        table_data.generate_table()

    """
    Processes the user's choice in the torrent search application.

    Handles the user's input choice to navigate through search results, perform new searches, view more info on a 
    selected torrent, or quit the application.

    Args:
        choice: The user's input choice.
        torrent_results: The torrent search results.

    Returns:
        None
    """
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

    """
    Handles the selection of a torrent by the user.

    If the chosen torrent ID is valid, retrieves the torrent information, prompts the user for a save path, and adds 
    the torrent to qBittorrent for download. If the ID is invalid, prints an error message.

    Args:
        choice: The user's choice of torrent ID.
        torrent_results: The torrent search results.

    Returns:
        None
    """
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

    """
    Runs the main loop of the torrent search application.

    Prompts the user for search terms, displays search results, and handles user input to navigate through search 
    results, view torrent info, and perform new searches or quit the application.

    Args:
        None

    Returns:
        None
    """
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

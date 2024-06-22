from rich import prompt

from utils.classes.torrent_info import TorrentInfo
from utils.classes.torrent_search import TorrentParserResult
from utils.cli.search_result_table import SearchResultTable


def perform_search(search_terms: str, page: int = 1):
    return TorrentParserResult.from_search_terms(search_terms, page=page)


def main():

    search_terms = prompt.Prompt.ask("Enter search terms: ")
    page = 1

    while True:
        torrent_results = TorrentParserResult.from_search_terms(search_terms, page=page)
        table_data = SearchResultTable(torrent_results)
        table_data.print_table()

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
            break
        elif choice.isdigit():
            choice = int(choice)
            if 0 <= choice < len(torrent_results.items):
                info = TorrentInfo.from_torrent_id(torrent_results.items[choice].torrentId)
                print(info)
            else:
                print("Invalid ID. Please try again.")


if __name__ == "__main__":
    main()

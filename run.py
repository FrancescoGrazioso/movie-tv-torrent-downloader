from rich import prompt

from utils.classes.torrent_info import TorrentInfo
from utils.classes.torrent_search import TorrentParserResult


def main():
    # use rich to get the search terms
    search_terms = prompt.Prompt.ask("Enter search terms: ")

    torrent_results = TorrentParserResult.from_search_terms(search_terms)
    info = TorrentInfo.from_torrent_id(torrent_results.items[0].torrentId)

    print(info)


if __name__ == "__main__":
    main()

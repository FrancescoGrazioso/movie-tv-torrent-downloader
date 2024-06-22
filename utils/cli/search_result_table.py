from rich import table, console

from utils.classes.torrent_search import TorrentParserResult


class SearchResultTable:
    def __init__(self, torrent_results: TorrentParserResult):
        self.torrent_results = torrent_results

    def print_table(self):
        table_data = table.Table(title="Torrent Search Results")
        table_data.add_column("ID", style="bold", justify="left")
        table_data.add_column("Name", style="bold", justify="left")
        table_data.add_column("Seeders", style="green")
        table_data.add_column("Leechers", style="red")
        table_data.add_column("Size", style="blue")
        table_data.add_column("Upload date", style="magenta")

        for index, item in enumerate(self.torrent_results.items):
            table_data.add_row(
                str(index),
                item.name,
                item.seeders,
                item.leechers,
                item.size,
                item.time,
            )

        console.Console().print(table_data)
        return table_data

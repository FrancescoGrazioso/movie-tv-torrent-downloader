from py1337x import py1337x


class TorrentItem:
    def __init__(
        self,
        name,
        torrentId,
        link,
        seeders,
        leechers,
        size,
        time,
        uploader,
        uploaderLink,
    ):
        self.name = name
        self.torrentId = torrentId
        self.link = link
        self.seeders = seeders
        self.leechers = leechers
        self.size = size
        self.time = time
        self.uploader = uploader
        self.uploaderLink = uploaderLink


class TorrentParserResult:
    torrents = py1337x()

    def __init__(self, items, current_page, item_count, page_count):
        self.items = [TorrentItem(**item) for item in items]
        self.currentPage = current_page
        self.itemCount = item_count
        self.pageCount = page_count

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"TorrentParserResult: {self.items}"

    @classmethod
    def from_dict(cls, data):
        return cls(
            items=data["items"],
            current_page=data["currentPage"],
            item_count=data["itemCount"],
            page_count=data["pageCount"],
        )

    @classmethod
    def from_search_terms(cls, search_terms, page=1):
        response = cls.torrents.search(search_terms, page=page)
        return cls.from_dict(response)

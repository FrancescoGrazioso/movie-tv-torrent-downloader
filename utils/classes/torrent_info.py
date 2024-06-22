from py1337x import py1337x


class TorrentInfo:
    torrents = py1337x(proxy="1337x.to", cache="py1337xCache", cacheTime=500)

    def __init__(
        self,
        name,
        shortName,
        description,
        category,
        type,
        genre,
        language,
        size,
        thumbnail,
        images,
        uploader,
        uploaderLink,
        downloads,
        lastChecked,
        uploadDate,
        seeders,
        leechers,
        magnetLink,
        infoHash,
    ):
        self.name = name
        self.shortName = shortName
        self.description = description
        self.category = category
        self.type = type
        self.genre = genre
        self.language = language
        self.size = size
        self.thumbnail = thumbnail
        self.images = images
        self.uploader = uploader
        self.uploaderLink = uploaderLink
        self.downloads = downloads
        self.lastChecked = lastChecked
        self.uploadDate = uploadDate
        self.seeders = seeders
        self.leechers = leechers
        self.magnetLink = magnetLink
        self.infoHash = infoHash

    def __str__(self):
        return f"TorrentDetail: {self.name}"

    def __repr__(self):
        return self.__str__()

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    @classmethod
    def from_torrent_id(cls, torrend_id: str):
        response = cls.torrents.info(torrentId=torrend_id)
        return cls.from_dict(response)

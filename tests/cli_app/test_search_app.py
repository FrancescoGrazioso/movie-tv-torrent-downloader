from unittest.mock import patch, MagicMock

import pytest

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from cli_app.classes.search_app import TorrentSearchApp
from utils.classes.torrent_info import TorrentInfo
from utils.classes.torrent_search import TorrentParserResult


@pytest.fixture
def mock_qb_client():
    return MagicMock()


@pytest.fixture
def app(mock_qb_client):
    with patch("cli_app.classes.search_app.ConfigManager") as mock_config:
        mock_config.return_value.QBITTORRENT_URL = "http://localhost:8080"
        mock_config.return_value.QBITTORRENT_AUTH = ("user", "pass")
        mock_config.return_value.QB_DEFAULT_SAVE_PATH = "/downloads"
        app = TorrentSearchApp(qb_client=mock_qb_client)
    return app


@pytest.mark.parametrize(
    "input_choice, expected_page",
    [
        ("n", 2),
        ("p", 1),
    ],
)
def test_process_user_navigate_page(app, input_choice, expected_page):
    # Arrange
    torrent_results = MagicMock()
    torrent_results.items = [MagicMock() for _ in range(5)]

    # Act
    result = app.process_user_choice(input_choice, torrent_results)

    # Assert
    assert app.page == expected_page
    if input_choice == "s":
        assert result is not None
    elif input_choice == "q":
        with pytest.raises(SystemExit):
            app.process_user_choice(input_choice, torrent_results)
    else:
        assert result is None


@pytest.mark.parametrize(
    "input_choice, torrent_results, expected_prompt",
    [
        ("0", MagicMock(items=[MagicMock(torrentId="123")]), True),
        ("10", MagicMock(items=[MagicMock(torrentId="123")]), False),
    ],
)
def test_handle_torrent_selection(app, input_choice, torrent_results, expected_prompt):
    # Arrange
    with patch(
            "cli_app.classes.search_app.TorrentInfo.from_torrent_id"
    ) as mock_from_torrent_id:
        mock_from_torrent_id.return_value = TorrentInfo(
            name="Example",
            magnetLink="magnet:?xt=urn",
            shortName="exp",
            description="",
            category="",
            type="",
            size=0,
            seeders=0,
            leechers=0,
            uploader="",
            uploadDate="",
            uploaderLink="",
            genre="",
            language="",
            thumbnail="",
            images=[],
            downloads=0,
            lastChecked=0,
            infoHash="",
        )
        with patch("rich.prompt.Prompt.ask") as mock_prompt:
            mock_prompt.return_value = "/downloads"

            # Act
            app.handle_torrent_selection(int(input_choice), torrent_results)

            # Assert
            if expected_prompt:
                mock_prompt.assert_called_once()
                mock_from_torrent_id.assert_called_once_with(
                    torrent_results.items[int(input_choice)].torrentId
                )
            else:
                mock_prompt.assert_not_called()


@pytest.mark.parametrize("search_terms, expected_result", [
    ("game of thrones", True)
])
def test_perform_search(app, search_terms, expected_result):
    # Arrange
    with patch(
            "utils.classes.torrent_search.TorrentParserResult.from_search_terms"
    ) as mock_search:
        mock_search.return_value = TorrentParserResult(
            items=[], current_page=1, item_count=0, page_count=0
        )

        # Act
        result = app.perform_search(search_terms)

        # Assert
        assert (result is not None) == expected_result
        mock_search.assert_called_with(search_terms, page=app.page)


@pytest.mark.parametrize(
    "search_terms", ["game of thrones", "breaking bad"]
)
def test_prompt_search_terms(app, search_terms):
    # Arrange
    with patch(
            "cli_app.classes.search_app.prompt.Prompt.ask", return_value=search_terms
    ) as mock_prompt:
        # Act
        result = app.prompt_search_terms()

        # Assert
        assert result == search_terms
        mock_prompt.assert_called_once()

from base_helpers.BasePage import BasePage
from base_helpers.Favorites import Favorites


def test_check_main(run_browser, base_url):
    main_page = BasePage(run_browser)
    main_page.open_page(base_url)
    favorites = Favorites(run_browser)
    favorites.add_favorites()

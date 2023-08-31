from base_helpers.BasePage import BasePage
from selenium.webdriver.common.by import By


class Favorites(BasePage):
    button_add_favorites = (By.XPATH, "//span[contains(text(), 'Добавить в избранное')]")
    inform_tag = (By.XPATH, "//p[contains(text(), 'Добавлено')]")
    favorites = (By.XPATH, "//a[@title='Избранное']")
    list_things = (By.XPATH, "//p/strong")

    def add_favorites(self):
        self.click_element(locator=self.button_add_favorites)
        self.check_element_visible(locator=self.inform_tag)
        self.click_element(locator=self.favorites)
        elements = self.find_elements_visible(locator=self.list_things)
        self.get_element_by_text(elements=elements, text='Платье H&M', strict_mode=True)




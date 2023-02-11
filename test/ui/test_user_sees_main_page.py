import pytest

from pylenium.driver import Pylenium, Element
from collections import namedtuple as nt


class PageMain:
    def __init__(self, py: Pylenium):
        self.py = py

    def action_go_to(self) -> "PageMain":
        self.py.visit("https://www.cakedefi.com/")
        self.py.getx(".//button[text()='Accept All Cookies']").click()
        return self

    def get_logo(self) -> Element:
        return self.py.getx(".//header//a[@class='mui-175dvln-logoLink']/*[local-name()='svg']")

    def get_list_of_nav_button_names(self) -> list:
        list_of_nav_bar: [] = self.py.find("div > p[class*='mui-1a7k4vw-fontName']")
        list_of_nav_bar_button_names = [*(nav_item.text() for nav_item in list_of_nav_bar if len(nav_item.text()) > 0)]
        return list_of_nav_bar_button_names

    def get_list_of_lesson_cards(self) -> list:
        return self.py.findx(".//div[@class='lessonGroup-0-1-143']/div")

    def get_lesson_card(self, name_of_lesson_card: str):
        return self.py.getx(
            f".//div[@class='lessonGroup-0-1-143']//h3[text()='{name_of_lesson_card}']//parent::div[contains(@class,'cardContainer')]")

    # ================================== List of tasks ==================================
    def task_browse_through_lesson(self) -> "PageMain":
        self.action_hover_over_nav_button("Learn")
        self.action_click_on_hovered_item("Learn and Earn")
        self.action_click_on_button("Browse lessons")
        return self

    # ================================== List of actions ==================================
    def action_hover_over_nav_button(self, nav_button_name: str) -> "PageMain":
        self.py.getx(
            f".//header//p[text()='{nav_button_name}']"
        ).hover()
        return self

    def action_click_on_hovered_item(self, hovered_item_name: str) -> "PageMain":
        self.py.getx(f".//span[contains(text(),'{hovered_item_name}')]").click()
        return self

    def action_click_on_button(self, button_name) -> "PageMain":
        self.py.getx(f".//button[contains(text(),'{button_name}')]")
        return self


@pytest.fixture
def main_page(py: Pylenium):
    return PageMain(py).action_go_to()


'''
    =============================== Main Test ======================================
'''


@pytest.mark.sanity
def test_main_page_user_sees_logo(main_page: PageMain):
    logo: Element = main_page.get_logo()
    assert logo.is_displayed()


@pytest.mark.regression
def test_nav_bar_user_sees_a_list_of_items(main_page: PageMain):
    list_of_nav_items_expected: list = ["Get Started", "Earn", "Borrow", "Learn", "Community", "Support", "Company"]
    list_of_nav_items_actual = main_page.get_list_of_nav_button_names()
    assert len(list_of_nav_items_expected) == len(list_of_nav_items_actual)
    assert sorted(list_of_nav_items_expected) == sorted(list_of_nav_items_actual)


@pytest.mark.regression
# Get a specific element for comparision
def test_user_wants_to_look_at_lesson_card_defichain(main_page: PageMain):
    # Expected Value
    lesson_card_schema: nt = nt("Lesson_Card", ["Name", "Description", "Button_Name", "Description_Incentive"])
    lesson_DeFiChain_expected = lesson_card_schema("DeFiChain",
                                                   "Native Decentralized Finance enabled on Bitcoin",
                                                   "EARN DFI",
                                                   "Earn $1 in DFI")

    # When user attempts to look at lesson card DeFiChain
    main_page.task_browse_through_lesson()

    # Then he should see that DeFiChain lesson card is available for learning
    DeFiChain_attributes: list = main_page.get_lesson_card("DeFiChain").text().split("\n")
    lesson_DefiChain_actual = lesson_card_schema(DeFiChain_attributes[0],
                                                 DeFiChain_attributes[1],
                                                 DeFiChain_attributes[2],
                                                 DeFiChain_attributes[3])

    assert lesson_DeFiChain_expected == lesson_DefiChain_actual


@pytest.mark.regression
# Making use of findx to get a list of elements for comparison
def test_user_wants_to_browse_all_lessons(main_page: PageMain):
    # Expected Value
    lesson_card_schema: nt = nt("Lesson_Card", ["Name", "Description", "Button_Name", "Description_Incentive"])
    lesson_DeFiChain_expected = lesson_card_schema("DeFiChain",
                                                   "Native Decentralized Finance enabled on Bitcoin",
                                                   "EARN DFI",
                                                   "Earn $1 in DFI")
    lesson_Bitcoin_expected = lesson_card_schema("Bitcoin",
                                                 "Decentralized, scarce digital currency",
                                                 "EARN BTC-DFI",
                                                 "Earn $1 in BTC-DFI tokens")
    lesson_Ethereum_expected = lesson_card_schema("Ethereum",
                                                  "Programmable blockchain with smart contract functionality",
                                                  "Earn ETH-DFI",
                                                  "Earn $1 in ETH-DFI tokens")

    # When user attempts to browse lessons
    main_page.action_hover_over_nav_button("Learn")
    main_page.action_click_on_hovered_item("Learn and Earn")
    main_page.action_click_on_button("Browse lessons")

    # Then he should see that DeFiChain, Bitcoin and Ethereum blockchains are available for learning.
    list_of_lesson_cards: list = main_page.get_list_of_lesson_cards()
    list_of_lesson_card_obj: list = []

    # Pre-Question Task : Populate list_of_lesson_card_obj
    for lesson_card in list_of_lesson_cards:
        block_chain_name = lesson_card_schema(
            lesson_card.text().split("\n")[0],
            lesson_card.text().split("\n")[1],
            lesson_card.text().split("\n")[2],
            lesson_card.text().split("\n")[3]
        )
        list_of_lesson_card_obj.append(block_chain_name)

    # Pre-Question Task : Filter out the respective lesson
    lesson_DeFiChain_actual: list = [lesson_card for lesson_card in list_of_lesson_card_obj if
                                     lesson_card.__getattribute__("Name") == "DeFiChain"]
    lesson_Bitcoin_actual: list = [lesson_card for lesson_card in list_of_lesson_card_obj if
                                   lesson_card.__getattribute__("Name") == "Bitcoin"]
    lesson_Ethereum_actual: list = [lesson_card for lesson_card in list_of_lesson_card_obj if
                                    lesson_card.__getattribute__("Name") == "Ethereum"]

    # Compare DeFiChain
    assert lesson_DeFiChain_expected == lesson_DeFiChain_actual[0]
    assert lesson_Bitcoin_expected == lesson_Bitcoin_actual[0]
    assert lesson_Ethereum_expected == lesson_Ethereum_actual[0]

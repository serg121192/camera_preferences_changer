from selenium.webdriver.common.by import By


def selector_mapping(data: dict[str, str]) -> tuple[str, str]:
    mapping = {
        "ID": By.ID,
        "XPATH": By.XPATH,
        "CLASS_NAME": By.CLASS_NAME,
        "TAG_NAME": By.TAG_NAME,
        "NAME": By.NAME,
        "LINK_TEXT": By.LINK_TEXT,
        "PARTIAL_LINK_TEXT": By.PARTIAL_LINK_TEXT,
        "CSS_SELECTOR": By.CSS_SELECTOR
    }
    return mapping[data["by"]], data["value"]

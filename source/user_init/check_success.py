from selenium import webdriver
from selenium.webdriver.common.by import By


def check_success(driver: webdriver.Chrome) -> bool:
    selectors = [
        "[role='alert']", ".toast", ".snackbar", ".message", ".notify",
        ".notification", ".el-message", ".ant-message", ".mui-snackbar",
    ]
    for css in selectors:
        els = driver.find_elements(By.CSS_SELECTOR, css)
        if els:
            visible = [e for e in els if e.is_displayed() and e.text.strip()]
            if visible:
                return True
    return False

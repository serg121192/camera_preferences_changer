from selenium import webdriver


def set_driver_options() -> webdriver.ChromeOptions:
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {
        "profile.managed_default_content_settings.images": 2,
        "profile.managed_default_content_settings.stylesheets": 2,
        "profile.managed_default_content_settings.fonts": 2,
        "profile.managed_default_content_settings.plugins": 2,
    })
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-webrtc")
    # options.add_argument("--autoplay-policy=user-required")
    options.add_argument("--disable-features=MediaSource")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return options

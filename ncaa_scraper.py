import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
url2024 = "https://stats.ncaa.org/selection_rankings/nitty_gritties/37188"
url2023 = "https://stats.ncaa.org/selection_rankings/nitty_gritties/31492"
url2022 = "https://stats.ncaa.org/selection_rankings/nitty_gritties/25584"
url2021 = "https://stats.ncaa.org/selection_rankings/nitty_gritties/19263"
url2020 = "https://stats.ncaa.org/selection_rankings/nitty_gritties/16203"
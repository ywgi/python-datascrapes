import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd


def fetch_additional_pages_stats(url):
    driver = webdriver.Chrome()
    driver.get(url)

    try:
        # Click the "Load More" button 7 times
        for _ in range(7):
            wait = WebDriverWait(driver, 5)
            locator = (By.XPATH, "/html/body/div[1]/div/div/div/div/main/div[3]/div/div/section/div/div[5]/a")
            element = wait.until(EC.element_to_be_clickable(locator))
            element.click()
            time.sleep(2)  # Wait for the content to load

    except Exception as e:
        print(f"An error occurred while fetching additional pages: {e}")

    html_content = driver.page_source
    driver.quit()
    return html_content


def parse_stats(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract column names
    columns = []
    thead = soup.find_all("thead")[1]
    tr = thead.find("tr")
    ths = tr.find_all("th")
    first_title = ths[0].find("div").text.strip()
    columns.append(first_title)
    for th in ths[1:]:
        title = th.find("a").text.strip()
        columns.append(title)

    # Extract stats grid
    stats_table = soup.find_all("tbody")[1]
    rows_stats = stats_table.find_all('tr', class_='Table__TR')
    stats_grid = []
    for row in rows_stats[:-1]:
        stat_cells = row.find_all('td', class_='Table__TD')
        stats_row = [float(cell.get_text(strip=True)) for cell in stat_cells]
        stats_grid.append(stats_row)

    # Extract team rankings
    rows = soup.find("tbody").find_all("tr")
    ppg_ranking = []
    counter = 0
    for row in rows[:-1]:
        counter += 1
        td = row.find_all("td")[1]
        try:
            team_name = td.find_all("a")[1].text.strip()
        except IndexError:
            team_name = "Birmingham-Southern Panthers"
        team_ranking = counter
        ppg_ranking.append((team_ranking, team_name))

    return columns, stats_grid, ppg_ranking


def create_team_stats_dataframe(team_rankings, column_names, rows_of_stats):
    df_stats = pd.DataFrame(rows_of_stats, columns=column_names)

    # Create a dictionary for team rankings
    team_dict = {team: rank for team, rank in team_rankings}

    # Add team names to the DataFrame
    df_stats.insert(0, 'Ranking', [team for team, _ in team_rankings])

    # Set the team names as the index
    df_stats.set_index('Ranking', inplace=True)

    # Add the rankings as a new column
    df_stats['Team'] = [team_dict[team] for team in df_stats.index]

    # Move the 'Ranking' column to the first position
    df_stats = df_stats[['Team'] + column_names]

    return df_stats


# URLs and additional pages list
ncaa_team_stats_url = "https://www.espn.com/mens-college-basketball/stats/team"
differential_team_stats_url = "https://www.espn.com/mens-college-basketball/stats/team/_/view/differential"
defensive_team_stats_url = "https://www.espn.com/mens-college-basketball/stats/team/_/view/opponent/season/"
additional_pages_url = "https://www.espn.com/mens-college-basketball/stats/team/_/season/"
additional_pages = ['2023', '2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014',
                    '2013', '2012', '2011', '2010', '2009', '2008', '2007', '2006', '2005', '2004']

# url = differential_team_stats_url0
# html_content = fetch_additional_pages_stats(url)
# columns, stats_grid, ppg_ranking = parse_stats(html_content)
# df = create_team_stats_dataframe(ppg_ranking, columns, stats_grid)
# df.to_csv(f"2024_season_team_differential_stats.csv")
for year in additional_pages:
    url = f"{differential_team_stats_url}/season/{year}"
    html_content = fetch_additional_pages_stats(url)
    columns, stats_grid, ppg_ranking = parse_stats(html_content)
    df = create_team_stats_dataframe(ppg_ranking, columns, stats_grid)
    df.to_csv(f"{year}_season_team_differential_stats.csv")

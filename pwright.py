from playwright.sync_api import sync_playwright
from playwright.sync_api import Page
import os
import inquirer
import requests
from datetime import datetime, date
from zoneinfo import ZoneInfo
import re
import time

# ANSI escape code for red text
RED = "\033[91m"
# ANSI escape code for blue text
BLUE = "\033[34m"
# ANSI escape code for gray text
GRAY = "\033[90m"
# ANSI escape code for yellow text
YELLOW = "\033[93m"
# ANSI escape code for green text
GREEN = "\033[92m"
# ANSI escape code to reset color
RESET = "\033[0m"


def compare_percentages(td_texts: list) -> int:
    """
    Stub for the compare_percentages function.
    Replace with the actual logic from your code.
    Returns 1, 2, or something else depending on the text percentages.
    """
    # Example logic for demonstration; adapt to real logic:
    # If first short > long: return 1
    # If first short < long: return 2
    # Otherwise: return 0
    try:
        short_pct = float(td_texts[1].replace('%', ''))
        long_pct = float(td_texts[5].replace('%', ''))
        if short_pct > long_pct:
            return 1
        elif short_pct < long_pct:
            return 2
        else:
            return 0
    except:
        return 0
def get_Traders_position_MyFxbook(page: Page, Cur: str, url_cur: str) -> None:
    # 1. Go to the target URL
    page.goto(f"https://www.myfxbook.com/community/outlook/{url_cur}")

    # 2. Wait for content to load (similar to time.sleep(5) in Selenium)
    page.wait_for_timeout(5000)

    # 3. Wait for the table with ID="currentMetricsTable"
    #    If you have a custom function wait_for_element, adapt it accordingly.
    #    For built-in approach, we can do:
    table_locator = page.locator("#currentMetricsTable")
    if table_locator.count() == 0:
        print("\n\nTable doesn't exist, Error\n\n")
        raise ValueError("Unable to locate the currentMetricsTable on the page.")

    # 4. Gather all <td> elements within the table
    td_elems_locator = table_locator.locator("td")
    td_count = td_elems_locator.count()
    if td_count == 0:
        print("\n\nNo <td> elements found in the table.\n\n")
        raise ValueError("No <td> elements in currentMetricsTable.")

    # Convert each <td> locator to the text it contains
    td_texts = []
    for i in range(td_count):
        td_texts.append(td_elems_locator.nth(i).inner_text().strip())

    # The original code popped the first TD, so we replicate that here
    td_texts.pop(0)

    print("\n", f"{YELLOW}MyFxbook Info:{RESET}", "\n")

    # 5. Decide the output based on compare_percentages
    comparison_result = compare_percentages(td_texts)

    if comparison_result == 1:
        # Usually means short% > long%
        print(
            f"{RED} {td_texts[0]}{RESET} {Cur}: {RED}{td_texts[1]}{RESET}"
            f"\tVolume : {td_texts[2]} \tPositions : {td_texts[3]}\n"
        )
        print(
            f"{BLUE} {td_texts[4]}{RESET} {Cur}: {td_texts[5]}"
            f"\tVolume : {td_texts[6]} \tPositions : {td_texts[7]}\n"
        )
    elif comparison_result == 2:
        # Usually means short% < long%
        print(
            f"{RED} {td_texts[0]}{RESET} {Cur}: {td_texts[1]}"
            f"\tVolume : {td_texts[2]} \tPositions : {td_texts[3]}\n"
        )
        print(
            f"{BLUE} {td_texts[4]}{RESET} {Cur}: {BLUE}{td_texts[5]}"
            f"{BLUE} \tVolume : {td_texts[6]} \tPositions : {td_texts[7]}\n"
        )
    else:
        print("\n", f"{GRAY}Equal Traders!{RESET} in {Cur}", "\n")
def predictions_fxstreet(page: Page, url: str, Cur: str) -> None:
    # 1. Go to the target URL
    page.goto(url)

    # 2. Wait briefly for page content
    page.wait_for_timeout(2000)

    # 3. Locate and click the "continue" button if present
    clickable = page.locator("div.fxs_prestitial-continue")
    if clickable.count() > 0:
        clickable.first.click()

    # 4. Scroll until "div.fxs_widget_avg_col" is found (scroll_to_element must be defined separately)
    div_results = scroll_to_element(page, "div.fxs_widget_avg_col")

    week_spans_constants = []
    month_spans_constants = []

    # Weekly
    if div_results:
        # Assume div_results is a list of element handles or locators
        weekly_div = div_results.nth(0)
        # Collect the text from all <span> elements
        week_spans = weekly_div.locator("span")

        for i in range(week_spans.count()):
            week_spans_constants.append(week_spans.nth(i).inner_text().strip())
    else:
        print("No Week elements found!")

    # 5. Click on the "1 Month" tab
    one_month_tab = page.locator("xpath=//a[@data-toggle='tab' and text()='1 Month']")
    # one_month_tab = scroll_to_element(page, "xpath=//a[@data-toggle='tab' and text()='1 Month']")
    # Wait for the element to be available
    one_month_tab.wait_for(state="visible", timeout=2000)
    one_month_tab.click()
    page.wait_for_timeout(2000)

    # Monthly
    if div_results and div_results.count() > 1:
        monthly_div = div_results.nth(1)
        month_spans = monthly_div.locator("span")
        for i in range(month_spans.count()):
            month_spans_constants.append(month_spans.nth(i).inner_text().strip())
        page.wait_for_timeout(2000)
    else:
        print("No Monthly elements found!")

    # 6. Extract the biases (assuming indexes 6 contain relevant data)
    if len(month_spans_constants) > 6:
        monthly_bias = month_spans_constants[6]
    else:
        monthly_bias = "Unknown"

    if len(week_spans_constants) > 6:
        weekly_bias = week_spans_constants[6]
    else:
        weekly_bias = "Unknown"

    # 7. Print results
    print("\n", f"{YELLOW}FxStreet{RESET} On {Cur}:\n")

    if weekly_bias == "Bearish":
        print(
            f"\nWeekly Bias {RED}Bearish{RESET} {week_spans_constants[2]}"
            f"\t\t Bullish: {week_spans_constants[0]}\n"
        )
        print(f"{YELLOW}\n\n------------------------------------\n\n{RESET}")
        monthly_bias_fxstreet(monthly_bias, month_spans_constants)
    elif weekly_bias == "Bullish":
        print(
            f"\nWeekly Bias {BLUE}Bullish{RESET} {week_spans_constants[0]}"
            f"\t\t Bearish: {week_spans_constants[2]}\n"
        )
        print(f"{YELLOW}\n\n------------------------------------\n\n{RESET}")
        monthly_bias_fxstreet(monthly_bias, month_spans_constants)
    else:
        print("\n", f"Weekly {GRAY}Side Way!{RESET}", "\n")
        monthly_bias_fxstreet(monthly_bias, month_spans_constants)


def scroll_to_element(page: Page, selector: str, scroll_increment=500, max_scrolls=10, scroll_pause=1.0):
    for i in range(max_scrolls):
        # Perform a single vertical scroll
        page.mouse.wheel(0, scroll_increment)
        # Wait for the page to load/update
        time.sleep(scroll_pause)

        # Check if the element has appeared in the DOM
        # element = page.query_selector(selector)
        element = page.query_selector_all(selector)


        if element:
            element = page.locator(selector)
            return element
    raise TimeoutError(f"Could not find element '{selector}' after {max_scrolls} scroll attempts.")


def monthly_bias_fxstreet(monthly_bias, month_spans):
    # Monthly
    if monthly_bias.lower() == "bearish":
        print(f"\nMonthly Bias {RED}Bearish{RESET}  {month_spans[2]}\t\t Bullish: {month_spans[0]}\n")
        print(f"{YELLOW}\n\n------------------------------------\n\n{RESET}")
    elif monthly_bias.lower() == "bullish":
        print(f"\nMonthly Bias {BLUE}Bullish{RESET}  {month_spans[0]}\t\t Bearish: {month_spans[2]}\n")
        print(f"{YELLOW}\n\n------------------------------------\n\n{RESET}")
    else:
        print("\n", f"Monthly {GRAY}Side Way!{RESET}", "\n")
        print(f"{YELLOW}\n\n------------------------------------\n\n{RESET}")

def get_HighImpact_Currency(page: Page, timezone: str) -> None:
    # Locate all spans with title="High Impact Expected"
    spans = page.locator('//span[@title="High Impact Expected"]')
    span_count = spans.count()

    # Collect parent <tr> elements for each span
    high_impact_trs = []
    for i in range(span_count):
        span = spans.nth(i)
        # Locate the ancestor <tr> for each span
        tr_element = span.locator('xpath=./ancestor::tr')
        high_impact_trs.append(tr_element)

    # Check if there are any High Impact Events
    if high_impact_trs:
        print(f"{RED}High Impacts Today (not super accurate time):{RESET}")
        for tr in high_impact_trs:
            temp_tr = tr
            found_time = None
            attempts = 0

            # Walk up to 10 preceding <tr> siblings to find a valid time
            while attempts < 15:
                try:
                    times_locator = temp_tr.locator('.calendar__cell.calendar__time span')
                    # .inner_text() or .text_content() can extract the text
                    times = times_locator.inner_text().strip()
                    if times:
                        found_time = times
                        print("\n\n", f"found time: {found_time}", "\n\n")
                        break
                except:
                    pass

                # Go to the preceding sibling row
                temp_tr = temp_tr.locator('xpath=preceding-sibling::tr[1]')
                attempts += 1

            # Locate the currency cell
            currency_locator = tr.locator('.calendar__cell.calendar__currency span')
            currency = currency_locator.inner_text().strip()

            # Print the discovered information
            # Assuming convert_to_iran_time is a custom function you have
            if found_time is not None:
                iran_time = convert_to_iran_time(found_time, timezone)
                print(f"Time: {iran_time}\t\t Currency: {currency}\n")
            else:
                print(f"Unable to find time for a High Impact event with currency {currency}.\n")

        print(f"{YELLOW}\n\n------------------------------------\n\n{RESET}")
    else:
        print(f"{GRAY}\n\nNo High Impact Events Today\n\n{RESET}")
def convert_to_iran_time(input_time_str: str, timezone: str) -> str:
    try:
        # Parse "9:30 am" (12-hour format) with today's date
        today = date.today()
        dt_local = datetime.strptime(input_time_str, "%I:%M%p")

        # Assign Berlin timezone
        dt_input = datetime(
            year=today.year,
            month=today.month,
            day=today.day,
            hour=dt_local.hour,
            minute=dt_local.minute
        ).replace(tzinfo=ZoneInfo(timezone))

        # Convert to Iceland timezone
        dt_iran = dt_input.astimezone(ZoneInfo("Asia/Tehran"))

        # Format as e.g. "09:30 AM", then lower() => "09:30 am"
        iran_time = dt_iran.strftime("%I:%M%p").lower()
        # Remove any leading "0" from the hour => "9:30 am"
        iran_time = re.sub(r"^0", "", iran_time)

    except Exception as e:
        print(f"Error: {e}", f"\t Not a Normal Time format in Convert Function, time is {input_time_str}")
        iran_time = input_time_str

    return iran_time
def get_Traders_position_ForexFactory(page: Page, data_row: str, Cur: str) -> None:
    # Locate the main container
    # Because the ID includes forward slashes, use an attribute selector:
    element = page.locator('[id="flexBox_flex_trades/positions_tradesPositions"]')

    # Expand "more" button by cli
    # clicking it
    button = element.locator('.flexMore')
    button.click()

    # Locate the row that has data-row="data_row"
    currency = element.locator(f'[data-row="{data_row}"]')

    # --------------------------
    # Extract Long Position Info
    # --------------------------
    currency_long = currency.locator('li.trades_position__label.trades_position__label--long.long')
    span_element_long = currency_long.locator('span.label').nth(0)
    strong_element_long = span_element_long.locator('strong').first

    # logger.debug("strong_element_long locator: %s", strong_element_long)
    # logger.debug("strong_element_long text: %s", strong_element_long.inner_text())

    percentage_long = strong_element_long.inner_text().strip()
    # Remove the percentage text from the label text to get the number of traders
    span_long_text = span_element_long.inner_text()
    traders_number_long = span_long_text.replace(percentage_long, '').strip()

    # logger.info("Long Position %s - Percentage: %s, Traders: %s", Cur, percentage_long, traders_number_long)

    # ---------------------------
    # Extract Short Position Info
    # ---------------------------
    currency_short = currency.locator('li.trades_position__label.trades_position__label--short.short')
    span_element_short = currency_short.locator('span.label').nth(0)
    strong_element_short = span_element_short.locator('strong').first

    percentage_short = strong_element_short.inner_text().strip()
    span_short_text = span_element_short.inner_text()
    traders_number_short = span_short_text.replace(percentage_short, '').strip()

    # ----------------------------
    # Print Gathered Information
    # ----------------------------
    print("\n", f"{YELLOW}ForexFactory Info:{RESET}", "\n")
    print(
        f"{BLUE}Long Position {Cur}: {RESET}{percentage_long}\t\t"
        f"Number of Long Traders: {traders_number_long}\n"
    )

    print(
        f"{RED}Short Position {Cur}: {RESET}{percentage_short}\t\t"
        f"Number of Short Traders: {traders_number_short}\n"
    )

    print(f"{YELLOW}\n\n------------------------------------\n\n{RESET}")
def get_my_ip():
    """Get the public IP address of the machine running this script."""
    try:
        response = requests.get("https://api64.ipify.org?format=json")
        response.raise_for_status()
        return response.json()["ip"]
    except requests.RequestException as e:
        print(f"Error getting IP address: {e}")
        return None
def get_country_and_timezone_by_ip(ip):
    """Get the country and timezone of the given IP address using ip-api."""
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        response.raise_for_status()
        data = response.json()
        if data["status"] == "success":
            return data["country"], data["timezone"]
        else:
            print(f"Error from IP-API: {data['message']}")
            return None, None
    except requests.RequestException as e:
        print(f"Error getting country and timezone by IP: {e}")
        return None, None
def get_activeSession_Banks(page):
    """
    Retrieves and prints information about active market sessions on the page.
    Includes ANSI terminal color codes for styled console output.
    """
    print("\033[31mActive Sessions:\n\033[0m")

    # Query all elements that have the class 'market__session--active'
    active_sessions = page.query_selector_all(".market__session--active")

    print("\n\n", active_sessions, "\tactive", "\n\n")

    if active_sessions:
        for session in active_sessions:
            # Retrieve city name
            city_element = session.query_selector("span.market__session-title")
            city = city_element.inner_text() if city_element else "Unknown City"

            # Retrieve session details (time_end)
            details_element = session.query_selector(".market__session-block--details")
            time_end = details_element.inner_text() if details_element else "No Details"

            print(f"City: {city}\t\t\033[1;32m{time_end}\033[0m")

        print("\n")
    else:
        print("\n\n", "no active session", "\n\n")

    print("\033[33m\n------------------------------------\n\n\033[0m")
def get_performance_Forex(page, Cur, url):
    page.goto(url)
    page.wait_for_timeout(5000)
    data = []

    # Create a locator matching all 'div.react'
    react_divs = page.locator("div.rect")
    # Count how many such elements are on the page
    count = react_divs.count()

    for i in range(count):
        # For each index, retrieve the label and value
        label_text = react_divs.nth(i).locator("div.label").inner_text().strip()
        value_text = react_divs.nth(i).locator("div.value").inner_text().strip()

        # Remove the trailing '%' and convert to float
        numeric_value = float(value_text.replace("%", "").strip())

        data.append({"label": label_text, "value": numeric_value})

    # Sort the list of dictionaries by the "value" key in descending order
    data.sort(key=lambda x: x["value"], reverse=True)

    if Cur == "GOLD":
        desired_labels = {"Gold", "Copper", "AUD test"}
        data = [entry for entry in data if entry["label"] in desired_labels]

    for entry in data:
        print(f"Label: {entry['label']} | Value: {entry['value']}%")
        print("\n")


def run_playwright_with_extension_and_ua(
        extension_path: str,
        user_agent: str,
        user_data_dir: str = "/tmp/playwright_user_data"
) -> None:
    if not os.path.isdir(extension_path):
        raise ValueError(f"Extension path '{extension_path}' does not exist or is not a directory.")

    with sync_playwright() as playwright:
        # Launch persistent context to load the extension
        context = playwright.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            user_agent=user_agent,
            headless=False,
            args=[
                f"--disable-extensions-except={extension_path}",
                f"--load-extension={extension_path}",
            ],
        )
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)

        # Create a new page
        page = context.new_page()

        # Navigate to the page
        page.goto("https://www.forexfactory.com", wait_until="networkidle")
        # Wait a bit to visually confirm extension load and user agent
        page.wait_for_timeout(5000)

        try:
            get_HighImpact_Currency(page, timezone)
            get_activeSession_Banks(page)
            pass
        except Exception as e:
            print(e)
            context.close()

        if answers['choice'] == 'EUR/USD':
            try:
                # ForexFactory
                get_Traders_position_ForexFactory(page, "0", 'EUR/USD')
                # FxStreet
                predictions_fxstreet(page, "https://www.fxstreet.com/currencies/eurusd", 'EUR/USD')
                # Dailyfx (Temporarily Website Not Working)
                # get_Traders_position_Dailyfx("EUR/USD", "EURUSD")
                # MyFxbook
                get_Traders_position_MyFxbook(page, "EUR/USD", "EURUSD")
                get_performance_Forex(page, "EUR/USD", "https://finviz.com/forex_performance.ashx")

            except Exception as e:
                print(e)
                context.close()

        elif answers['choice'] == 'USD/JPY':
            try:
                # ForexFactory
                get_Traders_position_ForexFactory(page, 2, 'USD/JPY')
                # FxStreet - USD/JPY Doesn't have Trend chart!
                predictions_fxstreet(page, "https://www.fxstreet.com/currencies/usdjpy", 'USD/JPY')
                # Dailyfx
                # get_Traders_position_Dailyfx("USD/JPY", "USDJPY")
                # MyFxbook
                get_Traders_position_MyFxbook(page, "USD/JPY", "USDJPY")
                get_performance_Forex(page, 'USD/JPY', "https://finviz.com/forex_performance.ashx")

            except Exception as e:
                print(e)
                context.close()

        elif answers['choice'] == 'GOLD':
            try:
                # FxStreet
                predictions_fxstreet(page, "https://www.fxstreet.com/markets/commodities/metals/gold", 'GOLD')
                # Dailyfx
                # get_Traders_position_Dailyfx("USD/JPY", "USDJPY")
                # MyFxbook
                get_Traders_position_MyFxbook(page, "Gold", "XAUUSD")
                get_performance_Forex(page, "GOLD", "https://finviz.com/futures_performance.ashx")
            except Exception as e:
                print(e)
                context.close()

        elif answers['choice'] == 'BTC/USD':
            try:
                # FxStreet
                predictions_fxstreet(page, "https://www.fxstreet.com/cryptocurrencies/bitcoin", 'BTC/USD')
                get_performance_Forex(page, "BTC/USD", "https://finviz.com/crypto_performance.ashx")
            except Exception as e:
                print(e)
                context.close()
        # Close context and browser
        page.close()
        context.close()


if __name__ == "__main__":
    # logging.basicConfig(
    #     level=logging.DEBUG,  # choose DEBUG, INFO, WARNING, etc. depending on verbosity
    #     format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    # )
    # logger = logging.getLogger(__name__)

    questions = [
        inquirer.List(
            'choice',
            message=f"Choose Currency",
            choices=['EUR/USD', 'USD/JPY', 'GOLD', 'BTC/USD'],
        ),
    ]
    answers = inquirer.prompt(questions)
    if answers['choice']:
        print("\n", answers['choice'], "\n")
    else:
        print("\n", "no choice", "\n")
    # ForexFactory

    my_ip = get_my_ip()
    country, timezone = get_country_and_timezone_by_ip(my_ip)
    adblock_path = "/Users/username_hidden/CJPALHDLNBPAFIAMEJDNHCPHJBKEIAGM_1_62_0_0"
    my_user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.5735.199 Safari/537.36"
    )

    run_playwright_with_extension_and_ua(
        extension_path=adblock_path,
        user_agent=my_user_agent
    )

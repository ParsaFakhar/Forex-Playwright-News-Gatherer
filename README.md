# Forex-Playwright-News-Gatherer
Gathering Top Info On a Currecncy with Playwright Automated Browser (websites like forexfactory)

## Forex Playwright News Gatherer

### Description
This Python script gathers Forex news using Playwright and processes the data for further analysis.

depending On Your Choice of Currency, it might pick up data from different sources

when the script runs, it asks you to choose one of the following currencies and click enter
**Current Currencies that are supported:
> [!IMPORTANT]
> 1. EUR/USD
> 2. USD/JPY
> 3. GOLD
> 4. BTC/USD

**Current Websites that are Used to gather information:
> [!IMPORTANT]
> 1. https://www.fxstreet.com
> 2. www.forexfactory.com
> 3. www.myfxbook.com
> 4. https://finviz.com


### Prerequisites
Make sure you have the following installed:
- Python 3.x
- Playwright
- Other dependencies (listed in `requirements.txt`)

> [!WARNING]
> + the PlayWright Uses AdBlock "UBlock origin"
> + **example**: use "adblock_path = '/Users/YOUR_USERNAME/CJPALHDLNBPAFIAMEJDNHCPHJBKEIAGM_1_62_0_0'" in code <br>
> + change YOUR_USERNAME to your username in the code (you can use new versions of the plugin) <br>
> + you can download it, and unzip it from here: [CRX uBlock Origin for Chrome](https://www.crx4chrome.com/crx/31931/) <br>
> + Convert it into zip, then unzip it here [Convert CRX to Zip](https://www.ezyzip.com/convert-crx-to-zip.html) <br>


### Installation
Clone the repository and install dependencies:
```sh
git clone https://github.com/ParsaFakhar/Forex-Playwright-News-Gatherer.git
cd Forex-Playwright-News-Gatherer
pip install -r requirements.txt
```

### Usage
Run the script in the terminal:
```sh
cd /path/to/location of pwright.py
python3 pwright.py
```
Or, if using a virtual environment:
```sh
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
python3 pwright.py
```

### Troubleshooting
- If Playwright is not installed correctly, run:
  ```sh
  playwright install
  ```
- Ensure you have the right permissions and API access (if applicable).

### Contributing
Feel free to submit pull requests or report issues!

### License
This project is licensed under the NO License.



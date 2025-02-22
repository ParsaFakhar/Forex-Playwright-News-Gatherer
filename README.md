# Forex-Playwright-News-Gatherer
Gathering Top Info On a Currecncy with Playwright Automated Browser (websites like forexfactory)

## Forex Playwright News Gatherer

### Description
This Python script gathers Forex news using Playwright and processes the data for further analysis.

depending On Your Choice of Currency, it might pick up data from different sources

when the script runs, it asks you to choose one of the following currencies and click enter
**Current Currencies that are supported:
> [!IMPORTANT]
> ['EUR/USD', 'USD/JPY', 'GOLD', 'BTC/USD']

**Current Websites that are Used to gather information:
> [!IMPORTANT]
> ['https://www.fxstreet.com', 'www.forexfactory.com', 'www.myfxbook.com', 'https://finviz.com']


### Prerequisites
Make sure you have the following installed:
- Python 3.x
- Playwright
- Other dependencies (listed in `requirements.txt`)

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



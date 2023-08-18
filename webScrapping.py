from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()))
driver.get('https://www.fundamentus.com.br/resultado.php')
table_path = '/html/body/div[1]/div[2]/table'
table = driver.find_element('xpath', table_path)
html_table = table.get_attribute('outerHTML')
table = pd.read_html(str(html_table), thousands='.', decimal=',')[0]
table = table.set_index('Papel')
table['Ticker'] = table.index.str.extract(r'(\D+)', expand=False)
min_price_indices = table.groupby('Ticker')['Cotação'].idxmin()
table = table.loc[min_price_indices]
table = table[['Cotação', 'EV/EBIT', 'ROIC', 'Liq.2meses']]
table['ROIC'] = table['ROIC'].str.replace('%', '')
table['ROIC'] = table['ROIC'].str.replace('.', '')
table['ROIC'] = table['ROIC'].str.replace(',', '.')
table['ROIC'] = table['ROIC'].astype(float)
table = table[table['Liq.2meses']> 1000000]
table = table[table['EV/EBIT']> 0]
table = table[table['ROIC']> 0]
table['Ranking_ev_ebit'] = table['EV/EBIT'].rank(ascending=True)
table['Ranking_roic'] = table['ROIC'].rank(ascending=False)
table['Ranking_final'] = table['Ranking_ev_ebit'] + table['Ranking_roic']
table = table.sort_values('Ranking_final')
print(table.head(20).to_string(max_rows=None))
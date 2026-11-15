# Source report (written by the daily refresh)

## HKMA open API
mortgage_delinquency: HKMA banking statistics; 14 obs, latest 2026-09 = 0.11
card_chargeoff: HKMA banking statistics; 4 obs, latest 2026-06 = 2.45
loan_growth: HKMA banking statistics; 2 obs, latest 2026-09 = 8.409
loan_growth_hk: HKMA banking statistics; 2 obs, latest 2026-09 = 7.14
classified_loans: HKMA banking statistics; 4 obs, latest 2026-06 = 1.96
loan_to_deposit: HKMA banking statistics; 14 obs, latest 2026-09 = 52.14
hibor_1m: HKMA HIBOR fixings; 364 obs, latest 2026-10 = 2.709
hibor_3m: HKMA HIBOR fixings; 364 obs, latest 2026-10 = 3.213
base_rate: HKMA base rate; 413 obs, latest 2026-10 = 4.25

FAILED HKMA daily interbank liquidity: HTTPError: 405 Client Error: Not Allowed for url: https://api.hkma.gov.hk/public/market-data-and-statistics/daily-monetary-statistics/daily-figures-interbank-liquidity?pagesize=1000&offset=3000
FAILED HKMA exchange rates: HTTPError: 405 Client Error: Not Allowed for url: https://api.hkma.gov.hk/public/market-data-and-statistics/monthly-statistical-bulletin/er-ir/er-eeri-endperiod?pagesize=1000&offset=0

## C&SD (via DATA.GOV.HK)
FAILED unemployment: unemployment not found
hk-censtatd-tablechart-210-06101: no series matching /unemployment rate.*seasonally adjusted|seasonally adjusted.*unemployment rate/
hk-censtatd-tablechart-210-06101: no series matching /^\s*unemployment rate/
hk-censtatd-tablechart-210-06101 layout (Table 210-06101 : Statistics on labour force, employment, unemployment and underemployment [English]):
### Sheet `table` (400 rows read, 4 cols)
- r0: <!DOCTYPE html>
- r1: <html lang="en">
- r2: <head>
- r4: <title>Web Table</title>
- r6: <!--Source San Pro//https://
- r7: <link href="/css/SourceSansP
- r9: <!--Google Icon//https://goo
- r10: <!-- <link href="https://fon
- r11: <link href="/material/materi

FAILED cpi_yoy: cpi_yoy not found
hk-censtatd-tablechart-510-60001: no series matching /composite.*(year-on-year|% change|change over)|(year-on-year|% change).*composite/
hk-censtatd-tablechart-510-60001: no series matching /composite/
hk-censtatd-tablechart-510-60001 layout (Table 510-60001 : Consumer Price Indices (October 2019 – September 2020 = 100) [English]):
### Sheet `table` (400 rows read, 4 cols)
- r0: <!DOCTYPE html>
- r1: <html lang="en">
- r2: <head>
- r4: <title>Web Table</title>
- r6: <!--Source San Pro//https://
- r7: <link href="/css/SourceSansP
- r9: <!--Google Icon//https://goo
- r10: <!-- <link href="https://fon
- r11: <link href="/material/materi

FAILED gdp_yoy: gdp_yoy not found
hk-censtatd-tablechart-310-31001: no series matching /(gdp|gross domestic product).*(real|chained).*(change|year-on-year)|(year-on-year|% change).*(real|chained)/
hk-censtatd-tablechart-310-31001: no series matching /real terms|chained.*change/
hk-censtatd-tablechart-310-31001 layout (Table 310-31001 : Gross Domestic Product (GDP), implicit price deflator of GDP and per capita GDP [English]):
### Sheet `table` (400 rows read, 4 cols)
- r0: <!DOCTYPE html>
- r1: <html lang="en">
- r2: <head>
- r4: <title>Web Table</title>
- r6: <!--Source San Pro//https://
- r7: <link href="/css/SourceSansP
- r9: <!--Google Icon//https://goo
- r10: <!-- <link href="https://fon
- r11: <link href="/material/materi

hk-censtatd-tablechart-310-31003: no series matching /(gdp|gross domestic product).*(real|chained).*(change|year-on-year)|(year-on-year|% change).*(real|chained)/
hk-censtatd-tablechart-310-31003: no series matching /real terms|chained.*change/
hk-censtatd-tablechart-310-31003 layout (Table 310-31003 : Gross Domestic Product (GDP) by major expenditure component in chained (2024) dollars [English]):
### Sheet `table` (400 rows read, 4 cols)
- r0: <!DOCTYPE html>
- r1: <html lang="en">
- r2: <head>
- r4: <title>Web Table</title>
- r6: <!--Source San Pro//https://
- r7: <link href="/css/SourceSansP
- r9: <!--Google Icon//https://goo
- r10: <!-- <link href="https://fon
- r11: <link href="/material/materi

hk-censtatd-tablechart-310-30001: no series matching /(gdp|gross domestic product).*(real|chained).*(change|year-on-year)|(year-on-year|% change).*(real|chained)/
hk-censtatd-tablechart-310-30001: no series matching /real terms|chained.*change/
hk-censtatd-tablechart-310-30001 layout (Table 310-30001 : Percentage change of Gross Domestic Product (GDP) and selected major expenditure components in real terms [English]):
### Sheet `table` (400 rows read, 4 cols)
- r0: <!DOCTYPE html>
- r1: <html lang="en">
- r2: <head>
- r4: <title>Web Table</title>
- r6: <!--Source San Pro//https://
- r7: <link href="/css/SourceSansP
- r9: <!--Google Icon//https://goo
- r10: <!-- <link href="https://fon
- r11: <link href="/material/materi


## RVD property price index (via DATA.GOV.HK)
FAILED LookupError: RVD: no series matching /index/
### Sheet `table` (200 rows read, 17 cols)
- r0: PRIVATE  DOMESTIC  -  PRICE 
- r1: Month | Class A | Class A - Remarks | Class B | Class B - Remarks | Class C | Class C - Remarks | Class D | Class D - Remarks | Class E | Class E - Remarks | Classes A, B & C | Classes A, B & C - Remarks | Classes D & E ... Classes D &  | All Classes | All Classes 
- r2: 01-1993 | 90.4 | 81.3 | 80.7 | 74.2 | 58.1 | 85.5 | 69.6 ... 84.4
- r3: 02-1993 | 90.5 | 82.6 | 81.3 | 74.9 | 62.2 | 86.2 | 71.3 ... 85.2
- r4: 03-1993 | 90.2 | 83.9 | 81.9 | 75.4 | 64.6 | 86.7 | 72.4 ... 85.7
- r5: 04-1993 | 92.5 | 85.4 | 83.7 | 76.8 | 66.2 | 88.5 | 73.9 ... 87.5
- r6: 05-1993 | 95.9 | 88.6 | 85.9 | 80.5 | 72.3 | 91.6 | 78.2 ... 90.7
- r7: 06-1993 | 98.3 | 94 | 91.4 | 86.9 | 76.3 | 95.6 | 84 ... 94.9
- r8: 07-1993 | 100.1 | 98 | 97.6 | 90.6 | 79.2 | 98.9 | 87.4 ... 98.1
- r9: 08-1993 | 101 | 97.9 | 96.1 | 91.1 | 76.8 | 99.1 | 87.1 ... 98.3
- r10: 09-1993 | 100.7 | 96.2 | 95.5 | 88.7 | 79 | 98.1 | 86 ... 97.3
- r11: 10-1993 | 97.8 | 94.4 | 95.6 | 90 | 83.2 | 96 | 88.1 ... 95.5


## Official Receiver's Office (via DATA.GOV.HK)
FAILED winding_up_petitions: ORO winding_up_petitions: no series matching /petition/ in Annual Statistics on Compulsory Winding-up of Hong Kong and Non-Hong Kong Companies 2020 (English)
### Sheet `table` (4 rows read, 2 cols)
- r0: Winding-up company type | Percentage
- r1: Hong Kong companies | 91.45%
- r2: Non Hong Kong companies | 8.55%
- r3: Total | 100.00%

ORO files: Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Age of bankrupts (English) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Age of bankrupts (Traditional Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Age of bankrupts (Simplified Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Cause of failure of bankrupts (English) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Cause of failure of bankrupts (Traditional Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Cause of failure of bankrupts (Simplified Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Liabilities level of bankrupts (English) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Liabilities level of bankrupts (Traditional Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Liabilities level of bankrupts (Simplified Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Monthly income of bankrupts (English) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Monthly income of bankrupts (Traditional Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Monthly income of bankrupts (Simplified Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Petitioner type (English) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Petitioner type (Traditional Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Petitioner type (Simplified Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Residence type of bankrupts (English) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Residence type of bankrupts (Traditional Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Residence type of bankrupts (Simplified Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Age of bankrupts (English) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Age of bankrupts (Traditional Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Age of bankrupts (Simplified Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Cause of failure of bankrupts (English) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Cause of failure of bankrupts (Traditional Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Cause of failure of bankrupts (Simplified Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Liabilities level of bankrupts (English) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Liabilities level of bankrupts (Traditional Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Liabilities level of bankrupts (Simplified Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Monthly income of bankrupts (English) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Monthly income of bankrupts (Traditional Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Monthly income of bankrupts (Simplified Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Petitioner type (English) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Petitioner type (Traditional Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Petitioner type (Simplified Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Residence type of bankrupts (English) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Residence type of bankrupts (Traditional Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Residence type of bankrupts (Simplified Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2019 - Age of bankrupts (English) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2019 - Age of bankrupts (Traditional Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2019 - Age of bankrupts (Simplified Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2019 - Cause of failure of bankrupts (English) [CSV]
FAILED bankruptcy_petitions: ORO bankruptcy_petitions: no series matching /petition/ in Annual Statistics on Profile of Bankrupts and Types of Petitioners 2020 - Multi-time Bankruptcy (English)
### Sheet `table` (4 rows read, 2 cols)
- r0: No. of bankruptcy | Percentage
- r1: 1st time bankruptcy | 91.23%
- r2: Multi-time bankruptcy | 8.77%
- r3: Total | 100.00%

ORO files: Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Age of bankrupts (English) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Age of bankrupts (Traditional Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Age of bankrupts (Simplified Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Cause of failure of bankrupts (English) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Cause of failure of bankrupts (Traditional Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Cause of failure of bankrupts (Simplified Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Liabilities level of bankrupts (English) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Liabilities level of bankrupts (Traditional Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Liabilities level of bankrupts (Simplified Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Monthly income of bankrupts (English) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Monthly income of bankrupts (Traditional Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Monthly income of bankrupts (Simplified Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Petitioner type (English) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Petitioner type (Traditional Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Petitioner type (Simplified Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Residence type of bankrupts (English) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Residence type of bankrupts (Traditional Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Residence type of bankrupts (Simplified Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Age of bankrupts (English) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Age of bankrupts (Traditional Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Age of bankrupts (Simplified Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Cause of failure of bankrupts (English) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Cause of failure of bankrupts (Traditional Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Cause of failure of bankrupts (Simplified Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Liabilities level of bankrupts (English) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Liabilities level of bankrupts (Traditional Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Liabilities level of bankrupts (Simplified Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Monthly income of bankrupts (English) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Monthly income of bankrupts (Traditional Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Monthly income of bankrupts (Simplified Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Petitioner type (English) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Petitioner type (Traditional Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Petitioner type (Simplified Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Residence type of bankrupts (English) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Residence type of bankrupts (Traditional Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Residence type of bankrupts (Simplified Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2019 - Age of bankrupts (English) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2019 - Age of bankrupts (Traditional Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2019 - Age of bankrupts (Simplified Chinese) [CSV]; Annual Statistics on Profile of Bankrupts and Types of Petitioners 2019 - Cause of failure of bankrupts (English) [CSV]

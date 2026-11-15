# Source report (written by the daily refresh)

## HKMA open API
card_chargeoff: HKMA banking statistics; 4 obs, latest 2026-06 = 2.45
loan_growth: HKMA banking statistics; 2 obs, latest 2026-09 = 8.409
loan_growth_hk: HKMA banking statistics; 2 obs, latest 2026-09 = 7.14
classified_loans: HKMA banking statistics; 4 obs, latest 2026-06 = 1.96
loan_to_deposit: HKMA banking statistics; 14 obs, latest 2026-09 = 52.14
mortgage_delinquency: HKMA residential mortgage survey; 118 obs, latest 2026-09 = 0.11
hibor_1m: HKMA HIBOR fixings; 364 obs, latest 2026-10 = 2.709
hibor_3m: HKMA HIBOR fixings; 364 obs, latest 2026-10 = 3.213
base_rate: HKMA base rate; 413 obs, latest 2026-10 = 4.25
aggregate_balance: HKMA daily interbank liquidity; 98 obs, latest 2026-11 = 54.05
base_rate_daily: HKMA daily interbank liquidity; 98 obs, latest 2026-11 = 4.25
usdhkd source: ECB reference rates, HKD/EUR divided by USD/EUR, month-end; earlier sources failed: monthly-statistical-bulletin/er-ir/er-eeri-endperiod; monthly-statistical-bulletin/er-ir/hkd-fer-endperiod; monthly-statistical-bulletin/er-ir/hkd-fer-daily; monthly-statistical-bulletin/er-ir/er-eeri-daily; monthly-statistical-bulletin/financial/monetary-statistics; FRED DEXHKUS
usdhkd: HKMA exchange rates; 202 obs, latest 2026-10 = 7.846

## C&SD (via DATA.GOV.HK)
unemployment: hk-censtatd-tablechart-210-06101 -> C&SD records freq=M3M sv=SAUR svDesc='(%)'; 435 obs, latest 2026-09 = 3.9
  (all series in hk-censtatd-tablechart-210-06101: M3M/EM/No. ('000) (435 obs, last 2026-09 = 3655); M3M/LF/No. ('000) (435 obs, last 2026-09 = 3810); M3M/LF/Year-on-year % change (404 obs, last 2026-09 = -0.3); M3M/LFPR/(%) (435 obs, last 2026-09 = 56.6); M3M/SAUR/(%) (435 obs, last 2026-09 = 3.9); M3M/UDE/No. ('000) (435 obs, last 2026-09 = 75); M3M/UDR/(%) (435 obs, last 2026-09 = 2); M3M/UE/No. ('000) (435 obs, last 2026-09 = 155); M3M/UR/(%) (435 obs, last 2026-09 = 4.1))
cpi_yoy: hk-censtatd-tablechart-510-60001 -> C&SD records freq=M sv=CC_CM_1920 svDesc='Year-on-year % change'; 540 obs, latest 2026-09 = 1.9
  (all series in hk-censtatd-tablechart-510-60001: M/A_CM_1920/Index (627 obs, last 2026-09 = 113.5); M/A_CM_1920/Month-to-month % change (626 obs, last 2026-09 = 0.2); M/A_CM_1920/Year-on-year % change (615 obs, last 2026-09 = 1.4); M/B_CM_1920/Index (627 obs, last 2026-09 = 110); M/B_CM_1920/Month-to-month % change (626 obs, last 2026-09 = 0.3); M/B_CM_1920/Year-on-year % change (615 obs, last 2026-09 = 2); M/CC_CM_1920/Index (552 obs, last 2026-09 = 111.2); M/CC_CM_1920/Month-to-month % change (551 obs, last 2026-09 = 0.3); M/CC_CM_1920/Year-on-year % change (540 obs, last 2026-09 = 1.9); M/C_CM_1920/Index (627 obs, last 2026-09 = 110); M/C_CM_1920/Month-to-month % change (626 obs, last 2026-09 = 0.4); M/C_CM_1920/Year-on-year % change (615 obs, last 2026-09 = 2.3))
gdp_yoy: hk-censtatd-tablechart-310-31001 -> C&SD records freq=Q sv=CON svDesc='Year-on-year % change'; 211 obs, latest 2026-09 = 5.2
  (all series in hk-censtatd-tablechart-310-31001: Q/CON/HK$ million (215 obs, last 2026-09 = 8.763e+05); Q/CON/Year-on-year % change (211 obs, last 2026-09 = 5.2); Q/CUR/HK$ million (215 obs, last 2026-09 = 9.343e+05); Q/CUR/Year-on-year % change (211 obs, last 2026-09 = 9.2); Q/DEF/Index (Year 2024=100) (215 obs, last 2026-09 = 106.6); Q/DEF/Year-on-year % change (211 obs, last 2026-09 = 3.8); Q/SA1/Quarter-to-quarter % change (147 obs, last 2026-09 = 1.9))

## RVD property price index (via DATA.GOV.HK)
home_price_index: Private Domestic - Price Indices by Class (Territory-wide) - Monthly (from 1993) -> column 'All Classes' with periods by row; 405 obs, latest 2026-09 = 320.8

## RVD rental yields (via DATA.GOV.HK)
FAILED LookupError: RVD yields: no class columns in Private Domestic - Property Market Yields - Monthly (from 1999)
### Sheet `table` (200 rows read, 11 cols)
- r0: PROPERTY  MARKET  YIELDS  - 
- r1: Month | Domestic Class A | Domestic Class A - Remarks | Domestic Class B | Domestic Class B - Remarks | Domestic Class C | Domestic Class C - Remarks | Domestic Class D | Domestic Class D - Remarks | Domestic Class E | Domestic Class E - Remarks
- r2: 01-1999 | 5.2 | 4.3 | 4.3 | 4.5 | 4.5
- r3: 02-1999 | 5.2 | 4.3 | 4.4 | 4.7 | 4.4
- r4: 03-1999 | 5.2 | 4.3 | 4.5 | 4.6 | 4.6
- r5: 04-1999 | 5.1 | 4.4 | 4.4 | 4.5 | 4.2
- r6: 05-1999 | 5.1 | 4.3 | 4.4 | 4.5 | 4.1
- r7: 06-1999 | 5.1 | 4.3 | 4.4 | 4.3 | 4.1
- r8: 07-1999 | 5.2 | 4.4 | 4.5 | 4.3 | 4.2
- r9: 08-1999 | 5.3 | 4.4 | 4.5 | 4.4 | 4.1
- r10: 09-1999 | 5.4 | 4.6 | 4.5 | 4.4 | 4.3
- r11: 10-1999 | 5.3 | 4.6 | 4.6 | 4.5 | 4.2


## Official Receiver's Office (via DATA.GOV.HK)
winding_up_petitions: Statistics on Compulsory Winding-up and Bankruptcy (English) -> column 'Compulsory Winding-up Petitions presented' with periods by row; 345 obs, latest 2026-09 = 97
bankruptcy_petitions: Statistics on Compulsory Winding-up and Bankruptcy (English) -> column 'Bankruptcy Petitions presented' with periods by row; 345 obs, latest 2026-09 = 834

## Hang Seng Indexes (dividend yield, P/E)
note: performance feed: HTTPError: 404 Client Error: Not Found for url: https://www.hsi.com.hk/data/eng/rt/index-series/hsi/performance.do
note: factsheet: LookupError: no 'Dividend Yield' figure in the factsheet
FAILED LookupError: HSI dividend yield unavailable: performance feed: HTTPError: 404 Client Error: Not Found for url: https://www.hsi.com.hk/data/eng/rt/index-series/hsi/performance.do | factsheet: LookupError: no 'Dividend Yield' figure in the factsheet

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

FAILED HKMA exchange rates: LookupError: monthly-statistical-bulletin/er-ir/er-eeri-endperiod: HTTPError: 405 Client Error: Not Allowed for url: https://api.hkma.gov.hk/public/market-data-and-statistics/monthly-statistical-bulletin/er-ir/er-eeri-endperiod?offset=0; monthly-statistical-bulletin/er-ir/hkd-fer-endperiod: HTTPError: 405 Client Error: Not Allowed for url: https://api.hkma.gov.hk/public/market-data-and-statistics/monthly-statistical-bulletin/er-ir/hkd-fer-endperiod?offset=0; monthly-statistical-bulletin/er-ir/hkd-fer-daily: HTTPError: 405 Client Error: Not Allowed for url: https://api.hkma.gov.hk/public/market-data-and-statistics/monthly-statistical-bulletin/er-ir/hkd-fer-daily?offset=0; monthly-statistical-bulletin/er-ir/er-eeri-daily: HTTPError: 405 Client Error: Not Allowed for url: https://api.hkma.gov.hk/public/market-data-and-statistics/monthly-statistical-bulletin/er-ir/er-eeri-daily?offset=0; monthly-statistical-bulletin/financial/monetary-statistics: HTTPError: 405 Client Error: Not Allowed for url: https://api.hkma.gov.hk/public/market-data-and-statistics/monthly-statistical-bulletin/financial/monetary-statistics?offset=0

## C&SD (via DATA.GOV.HK)
unemployment: hk-censtatd-tablechart-210-06101 -> C&SD records freq=M3M sv=SAUR svDesc='(%)'; 435 obs, latest 2026-09 = 3.9
  (all series in hk-censtatd-tablechart-210-06101: M3M/EM/No. ('000) (435 obs, last 2026-09 = 3655); M3M/LF/No. ('000) (435 obs, last 2026-09 = 3810); M3M/LF/Year-on-year % change (404 obs, last 2026-09 = -0.3); M3M/LFPR/(%) (435 obs, last 2026-09 = 56.6); M3M/SAUR/(%) (435 obs, last 2026-09 = 3.9); M3M/UDE/No. ('000) (435 obs, last 2026-09 = 75); M3M/UDR/(%) (435 obs, last 2026-09 = 2); M3M/UE/No. ('000) (435 obs, last 2026-09 = 155); M3M/UR/(%) (435 obs, last 2026-09 = 4.1))
cpi_yoy: hk-censtatd-tablechart-510-60001 -> C&SD records freq=M sv=CC_CM_1920 svDesc='Year-on-year % change'; 540 obs, latest 2026-09 = 1.9
  (all series in hk-censtatd-tablechart-510-60001: M/A_CM_1920/Index (627 obs, last 2026-09 = 113.5); M/A_CM_1920/Month-to-month % change (626 obs, last 2026-09 = 0.2); M/A_CM_1920/Year-on-year % change (615 obs, last 2026-09 = 1.4); M/B_CM_1920/Index (627 obs, last 2026-09 = 110); M/B_CM_1920/Month-to-month % change (626 obs, last 2026-09 = 0.3); M/B_CM_1920/Year-on-year % change (615 obs, last 2026-09 = 2); M/CC_CM_1920/Index (552 obs, last 2026-09 = 111.2); M/CC_CM_1920/Month-to-month % change (551 obs, last 2026-09 = 0.3); M/CC_CM_1920/Year-on-year % change (540 obs, last 2026-09 = 1.9); M/C_CM_1920/Index (627 obs, last 2026-09 = 110); M/C_CM_1920/Month-to-month % change (626 obs, last 2026-09 = 0.4); M/C_CM_1920/Year-on-year % change (615 obs, last 2026-09 = 2.3))
gdp_yoy: hk-censtatd-tablechart-310-31001 -> C&SD records freq=Q sv=CON svDesc='Year-on-year % change'; 211 obs, latest 2026-09 = 5.2
  (all series in hk-censtatd-tablechart-310-31001: Q/CON/HK$ million (215 obs, last 2026-09 = 8.763e+05); Q/CON/Year-on-year % change (211 obs, last 2026-09 = 5.2); Q/CUR/HK$ million (215 obs, last 2026-09 = 9.343e+05); Q/CUR/Year-on-year % change (211 obs, last 2026-09 = 9.2); Q/DEF/Index (Year 2024=100) (215 obs, last 2026-09 = 106.6); Q/DEF/Year-on-year % change (211 obs, last 2026-09 = 3.8); Q/SA1/Quarter-to-quarter % change (147 obs, last 2026-09 = 1.9))

## RVD property price index (via DATA.GOV.HK)
home_price_index: Private Domestic - Price Indices by Class (Territory-wide) - Monthly (from 1993) -> column 'All Classes' with periods by row; 405 obs, latest 2026-09 = 320.8

## Official Receiver's Office (via DATA.GOV.HK)
winding_up_petitions: Statistics on Compulsory Winding-up and Bankruptcy (English) -> column 'Compulsory Winding-up Petitions presented' with periods by row; 345 obs, latest 2026-09 = 97
bankruptcy_petitions: Statistics on Compulsory Winding-up and Bankruptcy (English) -> column 'Bankruptcy Petitions presented' with periods by row; 345 obs, latest 2026-09 = 834

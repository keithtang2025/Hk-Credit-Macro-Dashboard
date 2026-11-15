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

FAILED HKMA exchange rates: LookupError: monthly-statistical-bulletin/er-ir/er-eeri-endperiod: HTTPError: 405 Client Error: Not Allowed for url: https://api.hkma.gov.hk/public/market-data-and-statistics/monthly-statistical-bulletin/er-ir/er-eeri-endperiod?offset=0; monthly-statistical-bulletin/er-ir/er-eeri-daily: HTTPError: 405 Client Error: Not Allowed for url: https://api.hkma.gov.hk/public/market-data-and-statistics/monthly-statistical-bulletin/er-ir/er-eeri-daily?offset=0; monthly-statistical-bulletin/er-ir/er-eeri-periodaverage: HTTPError: 405 Client Error: Not Allowed for url: https://api.hkma.gov.hk/public/market-data-and-statistics/monthly-statistical-bulletin/er-ir/er-eeri-periodaverage?offset=0; monthly-statistical-bulletin/financial/monetary-statistics: HTTPError: 405 Client Error: Not Allowed for url: https://api.hkma.gov.hk/public/market-data-and-statistics/monthly-statistical-bulletin/financial/monetary-statistics?offset=0

## C&SD (via DATA.GOV.HK)
unemployment: hk-censtatd-tablechart-210-06101 -> C&SD records freq=M3M sv=UR svDesc='(%)'; 435 obs, latest 2026-09 = 4.1
  (all series in hk-censtatd-tablechart-210-06101: M3M/EM/No. ('000) (435 obs, last 2026-09 = 3655); M3M/LF/No. ('000) (435 obs, last 2026-09 = 3810); M3M/LF/Year-on-year % change (404 obs, last 2026-09 = -0.3); M3M/LFPR/(%) (435 obs, last 2026-09 = 56.6); M3M/SAUR/(%) (435 obs, last 2026-09 = 3.9); M3M/UDE/No. ('000) (435 obs, last 2026-09 = 75); M3M/UDR/(%) (435 obs, last 2026-09 = 2); M3M/UE/No. ('000) (435 obs, last 2026-09 = 155); M3M/UR/(%) (435 obs, last 2026-09 = 4.1))
cpi_yoy: hk-censtatd-tablechart-510-60001 -> C&SD records freq=M sv=A_CM_1920 svDesc='Month-to-month % change'; 626 obs, latest 2026-09 = 0.2
  (all series in hk-censtatd-tablechart-510-60001: M/A_CM_1920/Index (627 obs, last 2026-09 = 113.5); M/A_CM_1920/Month-to-month % change (626 obs, last 2026-09 = 0.2); M/A_CM_1920/Year-on-year % change (615 obs, last 2026-09 = 1.4); M/B_CM_1920/Index (627 obs, last 2026-09 = 110); M/B_CM_1920/Month-to-month % change (626 obs, last 2026-09 = 0.3); M/B_CM_1920/Year-on-year % change (615 obs, last 2026-09 = 2); M/CC_CM_1920/Index (552 obs, last 2026-09 = 111.2); M/CC_CM_1920/Month-to-month % change (551 obs, last 2026-09 = 0.3); M/CC_CM_1920/Year-on-year % change (540 obs, last 2026-09 = 1.9); M/C_CM_1920/Index (627 obs, last 2026-09 = 110); M/C_CM_1920/Month-to-month % change (626 obs, last 2026-09 = 0.4); M/C_CM_1920/Year-on-year % change (615 obs, last 2026-09 = 2.3))
gdp_yoy: hk-censtatd-tablechart-310-31001 -> C&SD records freq=Q sv=CON svDesc='Year-on-year % change'; 211 obs, latest 2026-09 = 5.2
  (all series in hk-censtatd-tablechart-310-31001: Q/CON/HK$ million (215 obs, last 2026-09 = 8.763e+05); Q/CON/Year-on-year % change (211 obs, last 2026-09 = 5.2); Q/CUR/HK$ million (215 obs, last 2026-09 = 9.343e+05); Q/CUR/Year-on-year % change (211 obs, last 2026-09 = 9.2); Q/DEF/Index (Year 2024=100) (215 obs, last 2026-09 = 106.6); Q/DEF/Year-on-year % change (211 obs, last 2026-09 = 3.8); Q/SA1/Quarter-to-quarter % change (147 obs, last 2026-09 = 1.9))

## RVD property price index (via DATA.GOV.HK)
home_price_index: Private Domestic - Price Indices by Class (Territory-wide) - Monthly (from 1993) -> column 'All Classes' with periods by row; 405 obs, latest 2026-09 = 320.8

## Official Receiver's Office (via DATA.GOV.HK)
FAILED winding_up_petitions in Statistics on Compulsory Winding-up and Bankruptcy (English): no series matching /winding-?\s?up petition/
### Sheet `t` (60 rows read, 7 cols)
- r0: Year | Month | Bankruptcy Petitions present | Receiving/Bankruptcy Orders  | Compulsory Winding-up Petiti | Winding-up Orders made by th | Weekly court hearing
- r1: 1989 | - | 224 | 177 | 224 | 158 | -
- r2: 1990 | - | 299 | 209 | 401 | 286 | -
- r3: 1991 | - | 370 | 283 | 422 | 345 | -
- r4: 1992 | - | 373 | 295 | 423 | 342 | -
- r5: 1993 | - | 429 | 329 | 539 | 408 | -
- r6: 1994 | - | 420 | 306 | 582 | 426 | -
- r7: 1995 | - | 643 | 455 | 631 | 481 | -
- r8: 1996 | - | 780 | 543 | 742 | 557 | 48
- r9: 1997 | - | 829 | 639 | 658 | 503 | 49
- r10: 1998 | 1 | 68 | 43 | 62 | 21 | 3
- r11: 1998 | 2 | 84 | 60 | 81 | 38 | 4

FAILED bankruptcy_petitions in Statistics on Compulsory Winding-up and Bankruptcy (English): no series matching /bankruptcy petition/
### Sheet `t` (60 rows read, 7 cols)
- r0: Year | Month | Bankruptcy Petitions present | Receiving/Bankruptcy Orders  | Compulsory Winding-up Petiti | Winding-up Orders made by th | Weekly court hearing
- r1: 1989 | - | 224 | 177 | 224 | 158 | -
- r2: 1990 | - | 299 | 209 | 401 | 286 | -
- r3: 1991 | - | 370 | 283 | 422 | 345 | -
- r4: 1992 | - | 373 | 295 | 423 | 342 | -
- r5: 1993 | - | 429 | 329 | 539 | 408 | -
- r6: 1994 | - | 420 | 306 | 582 | 426 | -
- r7: 1995 | - | 643 | 455 | 631 | 481 | -
- r8: 1996 | - | 780 | 543 | 742 | 557 | 48
- r9: 1997 | - | 829 | 639 | 658 | 503 | 49
- r10: 1998 | 1 | 68 | 43 | 62 | 21 | 3
- r11: 1998 | 2 | 84 | 60 | 81 | 38 | 4

FAILED winding_up_petitions: ORO winding_up_petitions: no series matching /petition/ in Annual Statistics on Compulsory Winding-up of Hong Kong and Non-Hong Kong Companies 2020 (English)
### Sheet `table` (4 rows read, 2 cols)
- r0: Winding-up company type | Percentage
- r1: Hong Kong companies | 91.45%
- r2: Non Hong Kong companies | 8.55%
- r3: Total | 100.00%

All ORO English files (95):
- Annual Statistics on Compulsory Winding-up of Hong Kong and Non-Hong Kong Companies 2020 (English)
- Annual Statistics on Compulsory Winding-up of Hong Kong and Non-Hong Kong Companies 2021 (English)
- Annual Statistics on Compulsory Winding-up of Hong Kong and Non-Hong Kong Companies 2022 (English)
- Annual Statistics on Compulsory Winding-up of Hong Kong and Non-Hong Kong Companies 2023 (English)
- Annual Statistics on Compulsory Winding-up of Hong Kong and Non-Hong Kong Companies 2024 (English)
- Annual Statistics on Compulsory Winding-up of Hong Kong and Non-Hong Kong Companies 2025 (English)
- Annual Statistics on Number of Public Searches conducted on Bankruptcy, Individual Voluntary Arrangement (IVA) and Compulsory Winding-up (CWU) records 2021 (English)
- Annual Statistics on Number of Public Searches conducted on Bankruptcy, Individual Voluntary Arrangement (IVA) and Compulsory Winding-up (CWU) records 2022 (English)
- Annual Statistics on Number of Public Searches conducted on Bankruptcy, Individual Voluntary Arrangement (IVA) and Compulsory Winding-up (CWU) records 2023 (English)
- Annual Statistics on Number of Public Searches conducted on Bankruptcy, Individual Voluntary Arrangement (IVA) and Compulsory Winding-up (CWU) records 2024 (English)
- Annual Statistics on Number of Public Searches conducted on Bankruptcy, Individual Voluntary Arrangement (IVA) and Compulsory Winding-up (CWU) records 2025 (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Age of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Cause of failure of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Liabilities level of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Monthly income of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Petitioner type (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2017 - Residence type of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Age of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Cause of failure of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Liabilities level of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Monthly income of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Petitioner type (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2018 - Residence type of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2019 - Age of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2019 - Cause of failure of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2019 - Gender of Bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2019 - Liabilities level of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2019 - Monthly income of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2019 - Petitioner type (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2019 - Residence type of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2020 - Age of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2020 - Cause of failure of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2020 - Gender of Bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2020 - Liabilities level of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2020 - Monthly income of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2020 - Multi-time Bankruptcy (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2020 - Petitioner type (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2020 - Residence type of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2021 - Age of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2021 - Cause of failure of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2021 - Gender of Bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2021 - Liabilities level of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2021 - Monthly income of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2021 - Multi-time Bankruptcy (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2021 - Petitioner type (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2021 - Residence type of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2022 - Age of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2022 - Cause of failure of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2022 - Gender of Bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2022 - Liabilities level of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2022 - Monthly income of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2022 - Multi-time Bankruptcy (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2022 - Petitioner type (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2022 - Residence type of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2023 - Age of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2023 - Cause of failure of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2023 - Gender of Bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2023 - Liabilities level of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2023 - Monthly income of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2023 - Multi-time Bankruptcy (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2023 - Petitioner type (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2023 - Residence type of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2024 - Age of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2024 - Cause of failure of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2024 - Gender of Bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2024 - Liabilities level of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2024 - Monthly income of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2024 - Multi-time Bankruptcy (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2024 - Petitioner type (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2024 - Residence type of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2025 - Age of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2025 - Cause of failure of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2025 - Gender of Bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2025 - Liabilities level of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2025 - Monthly income of bankrupts (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2025 - Multi-time Bankruptcy (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2025 - Petitioner type (English)
- Annual Statistics on Profile of Bankrupts and Types of Petitioners 2025 - Residence type of bankrupts (English)
- Statistics on Approved Individual Voluntary Arrangement Cases (English)
- Statistics on Bankruptcy Petitions and Order (English)
- Statistics on Compulsory Winding-up and Bankruptcy (English)
- Statistics on Directors' Disqualification (English)
- Statistics on Number of Insolvency Cases Released (English)
- Statistics on Prosecution - Amount of Fines (Bankruptcy Ordinance (Cap.6)) (English)
- Statistics on Prosecution - Amount of Fines (Companies (Winding Up and Miscellaneous Provisions) Ordinance (Cap.32)) (English)
- Statistics on Prosecution - Amount of Fines (Companies Ordinance (Cap.622)) (English)
- Statistics on Prosecution - Number of Convictions (Bankruptcy Ordinance (Cap.6)) (English)
- Statistics on Prosecution - Number of Convictions (Companies (Winding Up and Miscellaneous Provisions) Ordinance (Cap.32)) (English)
- Statistics on Prosecution - Number of Convictions (Companies Ordinance (Cap.622)) (English)
- Statistics on Prosecution - Number of Summonses Issued (Bankruptcy Ordinance (Cap.6)) (English)
- Statistics on Prosecution - Number of Summonses Issued (Companies (Winding Up and Miscellaneous Provisions) Ordinance (Cap.32)) (English)
- Statistics on Prosecution - Number of Summonses Issued (Companies Ordinance (Cap.622)) (English)
- Statistics on Prosecution - Total Amount of Fines (English)
- Statistics on Prosecution - Total Number of Convictions (English)
- Statistics on Prosecution - Total Number of Summonses Issued (English)
bankruptcy_petitions: 1 ORO file(s); 345 obs, latest 2026-09 = 716

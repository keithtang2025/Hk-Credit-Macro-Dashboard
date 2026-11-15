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

FAILED HKMA exchange rates: HTTPError: 405 Client Error: Not Allowed for url: https://api.hkma.gov.hk/public/market-data-and-statistics/monthly-statistical-bulletin/er-ir/er-eeri-endperiod?offset=0

## C&SD (via DATA.GOV.HK)
FAILED unemployment: unemployment not found
hk-censtatd-tablechart-210-06101: Table 210-06101 : Statistics on labour force, employment, unemployment and underemployment [English] [JSON] https://www.censtatd.gov.hk/api/get.php?id=210-06101&lang=en&full_series=1: no series matching /(?=.*unemployment rate)(?=.*seasonally adjusted)(?!.*(not|non)[- ]seasonally)/
hk-censtatd-tablechart-210-06101: Table 210-06101 : Statistics on labour force, employment, unemployment and underemployment [English] [JSON] https://www.censtatd.gov.hk/api/get.php?id=210-06101&lang=en&full_series=1: no series matching /(?=.*unemployment rate)(?!.*under)/
hk-censtatd-tablechart-210-06101 layout of Table 210-06101 : Statistics on labour force, employment, unemployment and underemployment [English] [JSON] https://www.censtatd.gov.hk/api/get.php?id=210-06101&lang=en&full_series=1:
### Sheet `table` (400 rows read, 8 cols)
- r0: SEX | SEXDesc | freq | period | sv | svDesc | figure | sd_value
- r1: Total | Y | 1985 | LF | No. ('000) | 2626.9
- r2: F | Female | Y | 1985 | LF | No. ('000) | 955.4
- r3: M | Male | Y | 1985 | LF | No. ('000) | 1671.5
- r4: Total | M3M | 198510 | LF | No. ('000) | N.A.
- r5: F | Female | M3M | 198510 | LF | No. ('000) | N.A.
- r6: M | Male | M3M | 198510 | LF | No. ('000) | N.A.
- r7: Total | M3M | 198511 | LF | No. ('000) | N.A.
- r8: F | Female | M3M | 198511 | LF | No. ('000) | N.A.
- r9: M | Male | M3M | 198511 | LF | No. ('000) | N.A.
- r10: Total | M3M | 198512 | LF | No. ('000) | 2644.1
- r11: F | Female | M3M | 198512 | LF | No. ('000) | 965.4

hk-censtatd-tablechart-210-06101: Table 210-06101 : Statistics on labour force, employment, unemployment and underemployment [English] [XLSX] https://www.censtatd.gov.hk/en/web_table.html?id=210-06101&full_series=1&download_excel=1: NotData: https://www.censtatd.gov.hk/en/web_table.html?id=210-06101&full_series=1&download_excel=1 is a web page, not a data file
hk-censtatd-tablechart-210-06101: Table 210-06101 : Statistics on labour force, employment, unemployment and underemployment [English] [CSV] https://www.censtatd.gov.hk/en/web_table.html?id=210-06101&full_series=1&download_csv=1: NotData: https://www.censtatd.gov.hk/en/web_table.html?id=210-06101&full_series=1&download_csv=1 is a web page, not a data file
cpi_yoy: hk-censtatd-tablechart-510-60001 / Table 510-60001 : Consumer Price Indices (October 2019 – September 2020 = 100) [English] [JSON] https://www.censtatd.gov.hk/api/get.php?id=510-60001&lang=en&full_series=1 -> row label, last numeric cell (long format); 626 obs, latest 2026-09 = 1.4
FAILED gdp_yoy: gdp_yoy not found
hk-censtatd-tablechart-310-31001: Table 310-31001 : Gross Domestic Product (GDP), implicit price deflator of GDP and per capita GDP [English] [JSON] https://www.censtatd.gov.hk/api/get.php?id=310-31001&lang=en&full_series=1: no series matching /(?=.*(gdp|gross domestic product))(?=.*(real|chained))(?=.*(change|year-on-year))/
hk-censtatd-tablechart-310-31001: Table 310-31001 : Gross Domestic Product (GDP), implicit price deflator of GDP and per capita GDP [English] [JSON] https://www.censtatd.gov.hk/api/get.php?id=310-31001&lang=en&full_series=1: no series matching /(?=.*(real terms|chained))(?=.*change)/
hk-censtatd-tablechart-310-31001 layout of Table 310-31001 : Gross Domestic Product (GDP), implicit price deflator of GDP and per capita GDP [English] [JSON] https://www.censtatd.gov.hk/api/get.php?id=310-31001&lang=en&full_series=1:
### Sheet `table` (400 rows read, 6 cols)
- r0: freq | period | sv | svDesc | figure | sd_value
- r1: Y | 1961 | CUR | HK$ million | 7455
- r2: Y | 1962 | CUR | HK$ million | 8687
- r3: Y | 1963 | CUR | HK$ million | 10427
- r4: Y | 1964 | CUR | HK$ million | 11888
- r5: Y | 1965 | CUR | HK$ million | 13953
- r6: Y | 1966 | CUR | HK$ million | 14282
- r7: Y | 1967 | CUR | HK$ million | 15475
- r8: Y | 1968 | CUR | HK$ million | 16533
- r9: Y | 1969 | CUR | HK$ million | 19437
- r10: Y | 1970 | CUR | HK$ million | 23106
- r11: Y | 1971 | CUR | HK$ million | 26681
- r281: Y | 1961 | CUR | Year-on-year % change | N.A.
- r282: Y | 1962 | CUR | Year-on-year % change | 16.5
- r283: Y | 1963 | CUR | Year-on-year % change | 20
- r284: Y | 1964 | CUR | Year-on-year % change | 14
- r285: Y | 1965 | CUR | Year-on-year % change | 17.4
- r286: Y | 1966 | CUR | Year-on-year % change | 2.4
- r287: Y | 1967 | CUR | Year-on-year % change | 8.4
- r288: Y | 1968 | CUR | Year-on-year % change | 6.8
- r289: Y | 1969 | CUR | Year-on-year % change | 17.6
- r290: Y | 1970 | CUR | Year-on-year % change | 18.9
- r291: Y | 1971 | CUR | Year-on-year % change | 15.5
- r292: Y | 1972 | CUR | Year-on-year % change | 20.7
- r293: Y | 1973 | CUR | Year-on-year % change | 28.3
- r294: Q | 197303 | CUR | Year-on-year % change | N.A.
- r295: Q | 197306 | CUR | Year-on-year % change | N.A.
- r296: Q | 197309 | CUR | Year-on-year % change | N.A.
- r297: Q | 197312 | CUR | Year-on-year % change | N.A.
- r298: Y | 1974 | CUR | Year-on-year % change | 14.3
- ...

hk-censtatd-tablechart-310-31001: Table 310-31001 : Gross Domestic Product (GDP), implicit price deflator of GDP and per capita GDP [English] [XLSX] https://www.censtatd.gov.hk/en/web_table.html?id=310-31001&full_series=1&download_excel=1: NotData: https://www.censtatd.gov.hk/en/web_table.html?id=310-31001&full_series=1&download_excel=1 is a web page, not a data file
hk-censtatd-tablechart-310-31001: Table 310-31001 : Gross Domestic Product (GDP), implicit price deflator of GDP and per capita GDP [English] [CSV] https://www.censtatd.gov.hk/en/web_table.html?id=310-31001&full_series=1&download_csv=1: NotData: https://www.censtatd.gov.hk/en/web_table.html?id=310-31001&full_series=1&download_csv=1 is a web page, not a data file
hk-censtatd-tablechart-310-31003: Table 310-31003 : Gross Domestic Product (GDP) by major expenditure component in chained (2024) dollars [English] [JSON] https://www.censtatd.gov.hk/api/get.php?id=310-31003&lang=en&full_series=1: no series matching /(?=.*(gdp|gross domestic product))(?=.*(real|chained))(?=.*(change|year-on-year))/
hk-censtatd-tablechart-310-31003: Table 310-31003 : Gross Domestic Product (GDP) by major expenditure component in chained (2024) dollars [English] [JSON] https://www.censtatd.gov.hk/api/get.php?id=310-31003&lang=en&full_series=1: no series matching /(?=.*(real terms|chained))(?=.*change)/
hk-censtatd-tablechart-310-31003 layout of Table 310-31003 : Gross Domestic Product (GDP) by major expenditure component in chained (2024) dollars [English] [JSON] https://www.censtatd.gov.hk/api/get.php?id=310-31003&lang=en&full_series=1:
### Sheet `table` (400 rows read, 8 cols)
- r0: GDP_COMPONENT | GDP_COMPONENTDesc | freq | period | sv | svDesc | figure | sd_value
- r1: Total | Y | 1961 | CON | HK$ million | 118642
- r2: CIV | Changes in inventories | Y | 1961 | CON | HK$ million | 689
- r3: DD | Domestic demand | Y | 1961 | CON | HK$ million | 110084
- r4: FD | Final demand | Y | 1961 | CON | HK$ million | 157834
- r5: GCE | Government consumption expen | Y | 1961 | CON | HK$ million | 16445
- r6: GDFCF | Gross domestic fixed capital | Y | 1961 | CON | HK$ million | 27971
- r7: MG | Imports of goods (f.o.b.) | Y | 1961 | CON | HK$ million | 38622
- r8: MGS | Imports of goods and service | Y | 1961 | CON | HK$ million | 48806
- r9: MS | Imports of services | Y | 1961 | CON | HK$ million | 9417
- r10: PCE | Private consumption expendit | Y | 1961 | CON | HK$ million | 66071
- r11: XG | Exports of goods (f.o.b.) | Y | 1961 | CON | HK$ million | 27154
- r15: CIV | Changes in inventories | Y | 1962 | CON | HK$ million | 799
- r16: DD | Domestic demand | Y | 1962 | CON | HK$ million | 129648
- r19: GDFCF | Gross domestic fixed capital | Y | 1962 | CON | HK$ million | 37702
- r28: CIV | Changes in inventories | Y | 1963 | CON | HK$ million | 932
- r29: DD | Domestic demand | Y | 1963 | CON | HK$ million | 154554
- r32: GDFCF | Gross domestic fixed capital | Y | 1963 | CON | HK$ million | 50838
- r41: CIV | Changes in inventories | Y | 1964 | CON | HK$ million | 1022
- r42: DD | Domestic demand | Y | 1964 | CON | HK$ million | 169778
- r45: GDFCF | Gross domestic fixed capital | Y | 1964 | CON | HK$ million | 56676
- r54: CIV | Changes in inventories | Y | 1965 | CON | HK$ million | 1189
- r55: DD | Domestic demand | Y | 1965 | CON | HK$ million | 190570
- r58: GDFCF | Gross domestic fixed capital | Y | 1965 | CON | HK$ million | 63245
- r67: CIV | Changes in inventories | Y | 1966 | CON | HK$ million | 1201
- r68: DD | Domestic demand | Y | 1966 | CON | HK$ million | 192847
- r71: GDFCF | Gross domestic fixed capital | Y | 1966 | CON | HK$ million | 54973
- r80: CIV | Changes in inventories | Y | 1967 | CON | HK$ million | 1222
- r81: DD | Domestic demand | Y | 1967 | CON | HK$ million | 184047
- r84: GDFCF | Gross domestic fixed capital | Y | 1967 | CON | HK$ million | 45487
- ...

hk-censtatd-tablechart-310-31003: Table 310-31003 : Gross Domestic Product (GDP) by major expenditure component in chained (2024) dollars [English] [XLSX] https://www.censtatd.gov.hk/en/web_table.html?id=310-31003&full_series=1&download_excel=1: NotData: https://www.censtatd.gov.hk/en/web_table.html?id=310-31003&full_series=1&download_excel=1 is a web page, not a data file
hk-censtatd-tablechart-310-31003: Table 310-31003 : Gross Domestic Product (GDP) by major expenditure component in chained (2024) dollars [English] [CSV] https://www.censtatd.gov.hk/en/web_table.html?id=310-31003&full_series=1&download_csv=1: NotData: https://www.censtatd.gov.hk/en/web_table.html?id=310-31003&full_series=1&download_csv=1 is a web page, not a data file
hk-censtatd-tablechart-310-30001: Table 310-30001 : Percentage change of Gross Domestic Product (GDP) and selected major expenditure components in real terms [English] [JSON] https://www.censtatd.gov.hk/api/get.php?id=310-30001&lang=en&full_series=1: no series matching /(?=.*(gdp|gross domestic product))(?=.*(real|chained))(?=.*(change|year-on-year))/
hk-censtatd-tablechart-310-30001: Table 310-30001 : Percentage change of Gross Domestic Product (GDP) and selected major expenditure components in real terms [English] [JSON] https://www.censtatd.gov.hk/api/get.php?id=310-30001&lang=en&full_series=1: no series matching /(?=.*(real terms|chained))(?=.*change)/
hk-censtatd-tablechart-310-30001 layout of Table 310-30001 : Percentage change of Gross Domestic Product (GDP) and selected major expenditure components in real terms [English] [JSON] https://www.censtatd.gov.hk/api/get.php?id=310-30001&lang=en&full_series=1:
### Sheet `table` (400 rows read, 8 cols)
- r0: GDP_COMPONENT | GDP_COMPONENTDesc | freq | period | sv | svDesc | figure | sd_value
- r1: Total | Y | 1961 | CON | Year-on-year % change | N.A.
- r2: GCE | Government consumption expen | Y | 1961 | CON | Year-on-year % change | N.A.
- r3: GDFCF | Gross domestic fixed capital | Y | 1961 | CON | Year-on-year % change | N.A.
- r4: MG | Imports of goods (f.o.b.) | Y | 1961 | CON | Year-on-year % change | N.A.
- r5: MS | Imports of services | Y | 1961 | CON | Year-on-year % change | N.A.
- r6: PCE | Private consumption expendit | Y | 1961 | CON | Year-on-year % change | N.A.
- r7: XG | Exports of goods (f.o.b.) | Y | 1961 | CON | Year-on-year % change | N.A.
- r8: XS | Exports of services | Y | 1961 | CON | Year-on-year % change | N.A.
- r9: Total | Y | 1962 | CON | Year-on-year % change | 14.3
- r10: GCE | Government consumption expen | Y | 1962 | CON | Year-on-year % change | 4.5
- r11: GDFCF | Gross domestic fixed capital | Y | 1962 | CON | Year-on-year % change | 34.8
- r12: MG | Imports of goods (f.o.b.) | Y | 1962 | CON | Year-on-year % change | 16.4
- r13: MS | Imports of services | Y | 1962 | CON | Year-on-year % change | 11.5
- r14: PCE | Private consumption expendit | Y | 1962 | CON | Year-on-year % change | 10.7
- r15: XG | Exports of goods (f.o.b.) | Y | 1962 | CON | Year-on-year % change | 13.8
- r16: XS | Exports of services | Y | 1962 | CON | Year-on-year % change | 3.8
- r17: Total | Y | 1963 | CON | Year-on-year % change | 15.8
- r18: GCE | Government consumption expen | Y | 1963 | CON | Year-on-year % change | 10.4
- r19: GDFCF | Gross domestic fixed capital | Y | 1963 | CON | Year-on-year % change | 34.8
- r20: MG | Imports of goods (f.o.b.) | Y | 1963 | CON | Year-on-year % change | 10.1
- r21: MS | Imports of services | Y | 1963 | CON | Year-on-year % change | 7.7
- r22: PCE | Private consumption expendit | Y | 1963 | CON | Year-on-year % change | 9.8
- r23: XG | Exports of goods (f.o.b.) | Y | 1963 | CON | Year-on-year % change | 9.1
- r24: XS | Exports of services | Y | 1963 | CON | Year-on-year % change | 3.7
- r25: Total | Y | 1964 | CON | Year-on-year % change | 8.6
- r26: GCE | Government consumption expen | Y | 1964 | CON | Year-on-year % change | 9.9
- r27: GDFCF | Gross domestic fixed capital | Y | 1964 | CON | Year-on-year % change | 11.5
- r28: MG | Imports of goods (f.o.b.) | Y | 1964 | CON | Year-on-year % change | 11
- r29: MS | Imports of services | Y | 1964 | CON | Year-on-year % change | 7.5
- ...

hk-censtatd-tablechart-310-30001: Table 310-30001 : Percentage change of Gross Domestic Product (GDP) and selected major expenditure components in real terms [English] [XLSX] https://www.censtatd.gov.hk/en/web_table.html?id=310-30001&full_series=1&download_excel=1: NotData: https://www.censtatd.gov.hk/en/web_table.html?id=310-30001&full_series=1&download_excel=1 is a web page, not a data file
hk-censtatd-tablechart-310-30001: Table 310-30001 : Percentage change of Gross Domestic Product (GDP) and selected major expenditure components in real terms [English] [CSV] https://www.censtatd.gov.hk/en/web_table.html?id=310-30001&full_series=1&download_csv=1: NotData: https://www.censtatd.gov.hk/en/web_table.html?id=310-30001&full_series=1&download_csv=1 is a web page, not a data file

## RVD property price index (via DATA.GOV.HK)
home_price_index: Private Domestic - Price Indices by Class (Territory-wide) - Monthly (from 1993) -> column 'All Classes' with periods by row; 405 obs, latest 2026-09 = 320.8

## Official Receiver's Office (via DATA.GOV.HK)
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
FAILED bankruptcy_petitions: ORO bankruptcy_petitions: no series matching /petition/ in Statistics on Compulsory Winding-up and Bankruptcy (English)
### Sheet `table` (120 rows read, 7 cols)
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
- r22: 1998 | Annual total | 1362 | 893 | 946 | 723 | 50
- r35: 1999 | Annual total | 3876 | 3071 | 1161 | 795 | 60
- r48: 2000 | Annual total | 5487 | 4606 | 1241 | 910 | 77
- r61: 2001 | Annual total | 13186 | 9151 | 1401 | 1066 | 150
- r74: 2002 | Annual total | 26922 | 25328 | 1430 | 1292 | 196
- r87: 2003 | Annual total | 22092 | 24922 | 1451 | 1248 | 165
- r100: 2004 | Annual total | 12489 | 13593 | 1306 | 1147 | 112
- r113: 2005 | Annual total | 9933 | 9810 | 955 | 849 | 98

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

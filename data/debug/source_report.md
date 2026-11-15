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
rental_yield: Private Domestic - Property Market Yields - Monthly (from 1999) -> average of classes A, B, C, D, E; 333 obs, latest 2026-09 = 2.86%
  class A: latest 2026-09 = 3.50%
  class B: latest 2026-09 = 3.10%
  class C: latest 2026-09 = 2.80%
  class D: latest 2026-09 = 2.60%
  class E: latest 2026-09 = 2.30%

## Official Receiver's Office (via DATA.GOV.HK)
winding_up_petitions: Statistics on Compulsory Winding-up and Bankruptcy (English) -> column 'Compulsory Winding-up Petitions presented' with periods by row; 345 obs, latest 2026-09 = 97
bankruptcy_petitions: Statistics on Compulsory Winding-up and Bankruptcy (English) -> column 'Bankruptcy Petitions presented' with periods by row; 345 obs, latest 2026-09 = 834

## Hang Seng Indexes (dividend yield, P/E)
page model: 0 data-looking links: 
factsheet text near 'yield' / 'P/E':  +1.93 -6.53 *Annualised INDEX FUNDAMENTALS Annual Volatility*(%)Index Dividend Yield (%) PE Ratio (Times) 1 - Yr 3 - Yr 5 - Yr HSI 3.14 13.04 18.29 23.03 24.78 *Annual Volatility was calculated based on d
note: page model: LookupError: no HSI figures via page model; tried 
note: performance feed: HTTPError: 404 Client Error: Not Found for url: https://www.hsi.com.hk/data/eng/rt/index-series/hsi/performance.do
hsi_dividend_yield: HSI factsheet PDF; as of 2026-10-30 = 3.14%, P/E 13.04

## HKEX monthly bulletin (Main Board P/E, yield)
hkex: 50 month(s) not found, newest 2026-10, oldest 2022-09
hkex notes: 2026-10: https://www.hkex.com.hk/eng/stat/smstat/mthbull/MonthlyBulletin_2610.json has no 'Average yield'; starts Stock market highlights /eng/stat/smstat/mthbull/rpt_Stock_market_highlights_2610.json Trading summary for equity securities (excluding SPAC shares) /eng/stat/smstat/mthbull/rpt_data_trade_summary_equity_2610_[PAGE].json Trading summary for SPAC shares /eng/stat/smstat/mthbull/rpt_data_trade_summary_spac_shares_2610_[PAGE].json Trading summary for equity warrants (excluding SPAC warrants) /eng/sta | 2026-09: https://www.hkex.com.hk/eng/stat/smstat/mthbull/MonthlyBulletin_2609.json has no 'Average yield'; starts Stock market highlights /eng/stat/smstat/mthbull/rpt_Stock_market_highlights_2609.json Trading summary for equity securities (excluding SPAC shares) /eng/stat/smstat/mthbull/rpt_data_trade_summary_equity_2609_[PAGE].json Trading summary for SPAC shares /eng/stat/smstat/mthbull/rpt_data_trade_summary_spac_shares_2609_[PAGE].json Trading summary for equity warrants (excluding SPAC warrants) /eng/sta | 2026-08: https://www.hkex.com.hk/eng/stat/smstat/mthbull/MonthlyBulletin_2608.json has no 'Average yield'; starts Stock market highlights /eng/stat/smstat/mthbull/rpt_Stock_market_highlights_2608.json Trading summary for equity securities (excluding SPAC shares) /eng/stat/smstat/mthbull/rpt_data_trade_summary_equity_2608_[PAGE].json Trading summary for SPAC shares /eng/stat/smstat/mthbull/rpt_data_trade_summary_spac_shares_2608_[PAGE].json Trading summary for equity warrants (excluding SPAC warrants) /eng/sta | 2026-07: https://www.hkex.com.hk/eng/stat/smstat/mthbull/MonthlyBulletin_2607.json has no 'Average yield'; starts Stock market highlights /eng/stat/smstat/mthbull/rpt_Stock_market_highlights_2607.json Trading summary for equity securities (excluding SPAC shares) /eng/stat/smstat/mthbull/rpt_data_trade_summary_equity_2607_[PAGE].json Trading summary for SPAC shares /eng/stat/smstat/mthbull/rpt_data_trade_summary_spac_shares_2607_[PAGE].json Trading summary for equity warrants (excluding SPAC warrants) /eng/sta | 2026-06: https://www.hkex.com.hk/eng/stat/smstat/mthbull/MonthlyBulletin_2606.json has no 'Average yield'; starts Stock market highlights /eng/stat/smstat/mthbull/rpt_Stock_market_highlights_2606.json Trading summary for equity securities (excluding SPAC shares) /eng/stat/smstat/mthbull/rpt_data_trade_summary_equity_2606_[PAGE].json Trading summary for SPAC shares /eng/stat/smstat/mthbull/rpt_data_trade_summary_spac_shares_2606_[PAGE].json Trading summary for equity warrants (excluding SPAC warrants) /eng/sta | 2026-05: https://www.hkex.com.hk/eng/stat/smstat/mthbull/MonthlyBulletin_2605.json has no 'Average yield'; starts Stock market highlights /eng/stat/smstat/mthbull/rpt_Stock_market_highlights_2605.json Trading summary for equity securities (excluding SPAC shares) /eng/stat/smstat/mthbull/rpt_data_trade_summary_equity_2605_[PAGE].json Trading summary for SPAC shares /eng/stat/smstat/mthbull/rpt_data_trade_summary_spac_shares_2605_[PAGE].json Trading summary for equity warrants (excluding SPAC warrants) /eng/sta
hkex_mb_yield: 0 month(s) fetched this run; 15 obs, latest 2017-09 = 2.97%; P/E 15.21

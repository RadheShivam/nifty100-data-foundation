# Sprint 2 Retrospective

## Objectives Completed

* Implemented profitability, leverage, efficiency, CAGR, and cash flow KPI engines.
* Populated the `financial_ratios` SQLite table.
* Generated financial KPIs for all companies and available financial years.
* Created comprehensive unit tests with all tests passing.
* Built ROCE and ROE validation utilities.
* Generated edge case logs for ratio anomalies.

## Formula Decisions

* ROE = Net Profit / (Equity Capital + Reserves)
* ROCE = EBIT / (Equity + Debt)
* Revenue, PAT, and EPS CAGR calculated over 5-year historical windows.
* Free Cash Flow = Operating Cash Flow + Investing Cash Flow.
* Composite Quality Score based on ROE, Debt-to-Equity, Interest Coverage, and Net Profit Margin.

## Edge Case Handling

* CAGR handles:

  * Zero base
  * Insufficient history
  * Turnaround
  * Decline to loss
  * Both negative values
* Financial sector companies are excluded from high Debt-to-Equity warnings.
* ROCE and ROE anomalies are logged and categorized as:

  * Data source issue
  * Version difference
  * Formula discrepancy

## Testing Summary

* Total Unit Tests: 86
* Passed: 86
* Failed: 0

## Deliverables

* financial_ratios table populated
* ratio_edge_cases.log generated
* roe_edge_cases.csv generated
* Screener preview verified

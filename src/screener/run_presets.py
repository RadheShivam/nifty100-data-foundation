from engine import ScreenerEngine
from presets import (
    QUALITY_COMPOUNDER,
    VALUE_PICK,
    GROWTH_ACCELERATOR,
    DIVIDEND_CHAMPION,
    DEBT_FREE_BLUECHIP,
    TURNAROUND_WATCH,
)


def main():

    engine = ScreenerEngine(
        config=VALUE_PICK
    )

    print(engine.config)

    filtered = engine.apply_filters()


    print(filtered[

        [
            "company_id",
            "year",
            "revenue_cagr_3yr",
            "free_cash_flow_cr",
            "composite_quality_score"
        ]
    ])

    print()

    print("Rows:", len(filtered))

if __name__ == "__main__":
    main()
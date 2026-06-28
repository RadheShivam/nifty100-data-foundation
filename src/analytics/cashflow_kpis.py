# Cash Flow Function

def free_cash_flow(
    operating_activity,
    investing_activity
):
    """
    Free Cash Flow (FCF)

    Formula:
        Operating Activity + Investing Activity

    Negative values are allowed.
    """

    return (
        operating_activity
        + investing_activity
    )

# CFO Quality Score

def cfo_quality_score(
    operating_cash_flow,
    net_profit
):
    """
    CFO Quality Score

    Formula:
        CFO / PAT

    Returns:
        (ratio, quality_label)

    Quality Labels:
        > 1.0  -> High Quality
        0.5–1.0 -> Moderate
        < 0.5  -> Accrual Risk

    Returns:
        (None, None) if PAT = 0
    """

    if net_profit == 0:
        return None, None

    ratio = operating_cash_flow / net_profit

    if ratio > 1:
        label = "High Quality"
    elif ratio >= 0.5:
        label = "Moderate"
    else:
        label = "Accrual Risk"

    return ratio, label


# CapEx Intensity

def capex_intensity(
    investing_activity,
    sales
):
    """
    CapEx Intensity

    Formula:
        abs(Investing Activity) / Sales * 100

    Returns:
        (capex_percentage, category)

    Categories:
        <3%   -> Asset Light
        3-8%  -> Moderate
        >8%   -> Capital Intensive
    """

    if sales == 0:
        return None, None

    capex = (abs(investing_activity) / sales) * 100

    if capex < 3:
        category = "Asset Light"
    elif capex <= 8:
        category = "Moderate"
    else:
        category = "Capital Intensive"

    return capex, category


# FCF Conversion Rate


def fcf_conversion_rate(
    free_cash_flow,
    operating_profit
):
    """
    FCF Conversion Rate

    Formula:
        (Free Cash Flow / Operating Profit) * 100

    Returns:
        float : Conversion percentage
        None  : If operating_profit is 0
    """

    if operating_profit == 0:
        return None

    return (free_cash_flow / operating_profit) * 100




# Capital Allocation Pattern Classifier


def capital_allocation_pattern(
    operating_activity,
    investing_activity,
    financing_activity,
    cfo_quality=None
):
    """
    Capital Allocation Pattern

    Returns:
        (
            cfo_sign,
            cfi_sign,
            cff_sign,
            pattern_label
        )
    """

    cfo_sign = "+" if operating_activity >= 0 else "-"
    cfi_sign = "+" if investing_activity >= 0 else "-"
    cff_sign = "+" if financing_activity >= 0 else "-"

    pattern = (cfo_sign, cfi_sign, cff_sign)

    if pattern == ("+", "-", "-"):
        if cfo_quality == "High Quality":
            label = "Shareholder Returns"
        else:
            label = "Reinvestor"

    elif pattern == ("+", "+", "-"):
        label = "Liquidating Assets"

    elif pattern == ("-", "+", "+"):
        label = "Distress Signal"

    elif pattern == ("-", "-", "+"):
        label = "Growth Funded by Debt"

    elif pattern == ("+", "+", "+"):
        label = "Cash Accumulator"

    elif pattern == ("-", "-", "-"):
        label = "Pre-Revenue"

    elif pattern == ("+", "-", "+"):
        label = "Mixed"

    else:
        label = "Other"

    return (
        cfo_sign,
        cfi_sign,
        cff_sign,
        label
    )
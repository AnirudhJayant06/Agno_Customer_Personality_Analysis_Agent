from typing import Dict, Optional, List

# Turns your Python functions into Agno tools that an agent can call
from agno.tools import tool

from agno_app.data_load_and_clean import get_final_dataset

import pandas as pd

# Tool implementations
'''
We created this as a function and directly not under the @tool decorator
because it would not be easy to test these functions directly otherwise.

We are using this function only using a wrapper function decorated with @tool
'''
def _global_stats_impl() -> Dict[str, float]:
    """
    Compute overall dataset-level statistics.

    Returns JSON-serializable numeric values only.
    """
    df = get_final_dataset()

    n_customers = int(len(df))
    avg_income = float(df["Income"].mean())
    avg_total_spend = float(df["TotalSpend"].mean())
    avg_recency = float(df["Recency"].mean())
    avg_tenure_days = float(df["CustomerTenureDays"].mean(skipna=True))

    high_value_pct = float(df["IsHighValue"].mean() * 100.0)

    return {
        "n_customers": n_customers,
        "avg_income": round(avg_income, 2),
        "avg_total_spend": round(avg_total_spend, 2),
        "avg_recency_days": round(avg_recency, 2),
        "avg_customer_tenure_days": round(avg_tenure_days, 2),
        "pct_high_value_customers": round(high_value_pct, 2),
    }

# This tells Agno that this function is a tool
@tool(
    name="global_stats",
    description="Return overall statistics for the full customer base and high-value customers.",
    show_result=False,
    stop_after_tool_call=False,
)

# A wrapper function
def global_stats() -> Dict[str, float]:
    # Thin wrapper – Agno will use this
    return _global_stats_impl()

# -------------------------------------------

def _segment_stats_impl(
    marital_status: Optional[str] = None,
    has_children: Optional[bool] = None,
    high_value_only: bool = False,
) -> Dict[str, float]:
    """
    Compute stats for a filtered customer segment.
    """
    df = get_final_dataset()

    seg_df = df

    if marital_status:
        marital_status = marital_status.strip().lower()
        seg_df = seg_df[seg_df["Marital_Status"] == marital_status]

    # TO process null and false values differently
    if has_children is not None:
        if has_children: # => Not null and true
            seg_df = seg_df[seg_df["Total_Children"] > 0]
        else:            # => Not null and false
            seg_df = seg_df[seg_df["Total_Children"] == 0]

    if high_value_only:
        seg_df = seg_df[seg_df["IsHighValue"]]

    n_customers = int(len(seg_df))

    if n_customers == 0:
        return {
            "n_customers": 0,
            "avg_income": 0.0,
            "avg_total_spend": 0.0,
            "avg_recency_days": 0.0,
            "avg_customer_tenure_days": 0.0,
            "pct_high_value_customers": 0.0,
        }

    avg_income = float(seg_df["Income"].mean())
    avg_total_spend = float(seg_df["TotalSpend"].mean())
    avg_recency = float(seg_df["Recency"].mean())
    avg_tenure_days = float(seg_df["CustomerTenureDays"].mean(skipna=True))
    high_value_pct = float(seg_df["IsHighValue"].mean() * 100.0)

    return {
        "n_customers": n_customers,
        "avg_income": round(avg_income, 2),
        "avg_total_spend": round(avg_total_spend, 2),
        "avg_recency_days": round(avg_recency, 2),
        "avg_customer_tenure_days": round(avg_tenure_days, 2),
        "pct_high_value_customers": round(high_value_pct, 2),
    }

@tool(
    name="segment_stats",
    description=(
        "Return statistics for a customer segment. "
        "Supports filters on marital_status (e.g. 'married', 'single', 'together'), "
        "has_children (true/false), and high_value_only (true/false)."
    ),

    # If show_result=True, the agent prints this raw JSON in the chat before reasoning.
    # User 'll see:
    #       Tool result:
    #       {
    #           "avg_income": 52111.45
    #       }

    # If show_result=False,the tool’s raw result is NOT automatically shown
    # The agent receives the result internally, reasons over it, and only returns a
    # polished final answer.
    # So instead of showing JSON, the user will see 'll the response of the LLM like this
    # 
    #       “The average customer income is around ₹52,000.”

    show_result=False,

    
    # False: To allow for further processing of the result in the agent using an
    # LLM.

    # True: The agent will stop after calling this tool and return the result 
    # directly to the user and don't let the LLM process the result further.

    # This is useful when the tool's output is the final answer to the user's query,
    # and no further reasoning or processing is needed.
    
    stop_after_tool_call=False,
)

def segment_stats() -> Dict[str, float]:
    return _segment_stats_impl()

# -------------------------------------------

def _top_customers_by_spend_impl(n: int = 10) -> Dict[str, List[Dict[str, float]]]:
    """
    Return top N customers ranked by TotalSpend.

    Returns a list of customer records with key fields.
    """
    df = get_final_dataset()

    n = max(1, min(int(n), 100))  # clamp to [1,100]

    top_df = (
        df.sort_values("TotalSpend", ascending=False)
        .head(n)
        .copy()
    )

    records: List[Dict[str, float]] = []

    for _, row in top_df.iterrows():
        records.append(
            {
                "customer_id": int(row["ID"]),
                "income": float(row["Income"]),
                "total_spend": float(row["TotalSpend"]),
                "total_children": int(row["Total_Children"]),
                "recency_days": float(row["Recency"]),
                "customer_tenure_days": (
                    float(row["CustomerTenureDays"])
                    if not pd.isna(row["CustomerTenureDays"])
                    else None
                ),
            }
        )

    return {"customers": records}

@tool(
    name="top_customers_by_spend",
    description="Return the top N customers sorted by TotalSpend.",
    show_result=False,
    stop_after_tool_call=False)

def top_customer_by_spend() -> Dict[str, float]:
    return _top_customers_by_spend_impl()
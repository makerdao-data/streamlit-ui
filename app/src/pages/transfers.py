from enum import unique
import streamlit as st
import pandas as pd
from ..utils.tokens.tkn_bal_txn_display import tkn_bal_txn_display
from ..utils.tokens.tkn_bal_txn_fetch import tkn_bal_txn_fetch

def app():
    """
    Token Transfer Explorer
    """

    # Display page title
    st.title("Token Transfer Explorer")
    
    # Prompt inputs and generate query parameters
    query_params = tkn_bal_txn_display('txs')

    # If query parameters were generated...
    if query_params:

        # Generate query from parameters and fetch data
        df = tkn_bal_txn_fetch(*query_params)

        # Generate analysis metrics
        metrics = txn_analyzoor(df)

        # Display result KPIs
        with st.expander("Result KPIs"):
            # Display metrics in vertical columns
            with st.container():
                # Create columns
                quant_col1, quant_col2 = st.columns(2)

                with quant_col1:
                    st.metric(label="Total TX Quantity", value=metrics[0])
                
                with quant_col2:
                    st.metric(label="Average Daily TX Quantity", value=round(metrics[1]))

            with st.container():
                vol_col1, vol_col2 = st.columns(2)

                with vol_col1:
                    st.metric(label=f"Total TX Volume (in {query_params[1]})", value=round(metrics[2], 4))

                with vol_col2:
                    st.metric(label=f"Average Daily TX Volume (in {query_params[1]})", value=round(metrics[3], 4))

        # Display table visualizations
        with st.expander("Result Tables"):
            with st.container():
                # Display dataframe tables within container
                st.markdown(f"Top 10 Transfers by {query_params[1]}")
                st.dataframe(df.nlargest(10, 'AMOUNT').reset_index(drop=True))

        # Display result visualizations
        with st.expander("Result Visualizations"):
            with st.container():
                # Display graph/chart visualizations within container
                st.markdown(f"Graph of daily transaction volume (in {query_params[1]})")
                st.line_chart(
                    pd.DataFrame(
                        list(metrics[4].items()), 
                        columns=['Date','Transaction Volume']).set_index('Date')
                )

            with st.container():
                st.markdown(f"Graph of daily transaction quantity (in {query_params[1]})")
                st.line_chart(
                    pd.DataFrame(
                        list(metrics[5].items()), 
                        columns=['Date','Transaction Quantity']).set_index('Date')
                )


def txn_analyzoor(df: pd.DataFrame) -> tuple:
    """
    Function to generate metrics for Transfer Explorer

    Params:
        df (pd.DataFrame): DataFrame of raw txn data.
    """

    # Format df
    df.TIMESTAMP = df.TIMESTAMP.apply(lambda x: x.date())

    # Get count of unique dates
    unique_dates = len(df.TIMESTAMP.unique())

    # Transaction quantity
    txquant_total = len(df)
    txquant_daily_avg = txquant_total / unique_dates

    # Transaction volume
    txvol_total = sum(df.AMOUNT)
    txvol_daily_avg = txvol_total / unique_dates

    # Get dictionary of daily transaction volume
    txvol_daily = {}
    for timestamp in df.TIMESTAMP.unique():
        txvol_daily[timestamp] = sum(df[df.TIMESTAMP == timestamp].AMOUNT)
     
    # Get dictionary of daily transaction amount
    txsum_daily = {}
    for timestamp in df.TIMESTAMP.unique():
        txsum_daily[timestamp] = len(df[df.TIMESTAMP == timestamp])

    return txquant_total, txquant_daily_avg, txvol_total, txvol_daily_avg, txvol_daily, txsum_daily
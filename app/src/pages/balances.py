import streamlit as st
from ..utils.tokens.tkn_bal_txn_display import tkn_bal_txn_display
from ..utils.tokens.tkn_bal_txn_fetch import tkn_bal_txn_fetch

def app():
    """
    Token Balance Explorer
    """

    # Display page title
    st.title("Token Balance Explorer")

    # Prompt inputs and generate query parameters
    query_params = tkn_bal_txn_display('bal')

    # If query parameters were generated...
    if query_params:

        # Generate query from parameters and fetch data
        df = tkn_bal_txn_fetch(*query_params)

        # Display result KPIs
        with st.expander("Result KPIs", expanded=True):
            with st.container():
                # Display metrics within container
                st.metric(label="Unique holders", value=len(df.ADDRESS.unique()))

        # Display result table visualizations
        with st.expander("Result Tables", expanded=True):
            with st.container():
                # Display dataframe tables within container
                st.markdown(f"Top 50 {query_params[1]} holders")
                st.dataframe(df.sort_values(by='DATE').drop_duplicates('ADDRESS', keep='last').nlargest(50, 'BALANCE').reset_index(drop=True))
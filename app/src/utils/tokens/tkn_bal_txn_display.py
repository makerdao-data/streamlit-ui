import streamlit as st
import pandas as pd
from datetime import datetime

def tkn_bal_txn_display(topic: str) -> tuple: 
    """
    Function to display token balances/transaction details

    Params:
        topic (str): Topic of query. Currently 'bal' or 'txs.'
    """

    # Select token
    token = st.selectbox(
        "Select a token", 
        ('', 'MKR', 'DAI'),
         format_func=lambda x: 'Select an option' if x == '' else x
    )

    # Once token is selected...
    if token:
        with st.expander("Query parameters", expanded=True):
            # Negate block indexing for balance explorations
            if topic is not 'bal':
                opts = ('Date', 'Block')
            else:
                opts = ['Date']

            # Select query index/filter parameters
            indexer = st.selectbox('Index by:', opts)

            # If 'Date' is selected...
            if indexer == 'Date':
                
                # Date input with date range
                date_input = st.date_input(
                    'Select date range:',
                    value=(
                        datetime(2019, 1, 1),
                        datetime.today()
                    ),
                    max_value=datetime.today(),
                    min_value=datetime(2019, 1, 1)
                )
                
                if len(date_input) == 2:
                    if st.button('Query'):
                        # Return tuple of selected token and date parameters
                        return (topic, token, date_input)

            # If 'Block' is selected...
            if indexer == 'Block':

                # Block inputs
                start_block_input = st.number_input(
                    'Select start block:',
                    value=12000000
                )
                end_block_input = st.number_input(
                    'Select end block:',
                    value=15000000
                )

                if st.button('Query'):
                    # Return tuple of selected token and block parameters
                    return (topic, token, (start_block_input, end_block_input))
        
     
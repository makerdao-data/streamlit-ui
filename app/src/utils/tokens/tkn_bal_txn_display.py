import streamlit as st
import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta

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
            if topic != 'bal':
                opts = ('Date', 'Block')
            else:
                opts = ['Date']

            # Select query index/filter parameters
            indexer = st.selectbox('Index by:', opts)

            # If 'Date' is selected...
            if indexer == 'Date':

                # Min date selection
                if token == 'DAI':
                    start_date = datetime(2019, 11, 18)
                elif token == 'MKR':
                    start_date = datetime(2017, 11, 25)

                # Date input with date range
                date_input = st.date_input(
                    'Select date range (2 month maximum):',
                    value=(
                        (datetime.today() - relativedelta(weeks=1)).date(),
                        datetime.today()
                    ),
                    max_value=datetime.today(),
                    min_value=start_date
                )
                
                if len(date_input) == 2:
                    if (date_input[1] - date_input[0]) < timedelta(days=60):
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
        
     
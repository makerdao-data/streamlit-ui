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
                    max_delta = 20
                elif token == 'MKR':
                    start_date = datetime(2017, 11, 25)
                    max_delta = 50

                # Date input with date range
                date_input = st.date_input(
                    f'Select date range ({max_delta} day maximum):',
                    value=(
                        (datetime.today() - relativedelta(weeks=1)).date(),
                        datetime.today()
                    ),
                    max_value=datetime.today(),
                    min_value=start_date
                )
                
                # Query conditionals
                if len(date_input) == 2:
                    if (date_input[1] - date_input[0]) < timedelta(days=max_delta):
                        if st.button('Query'):
                            # Return tuple of selected token and date parameters
                            return (topic, token, date_input)

            # If 'Block' is selected...
            if indexer == 'Block':
                
                # Block inputs
                st.write("Maximum block range: 60,000.")
                start_block_input = st.number_input(
                    'Select start block:',
                    value=12000000
                )
                end_block_input = st.number_input(
                    'Select end block:',
                    value=15000000
                )

                # Query conditionals
                if start_block_input < end_block_input:
                    if (end_block_input - start_block_input) < 60000:
                        if st.button('Query'):
                            # Return tuple of selected token and block parameters
                            return (topic, token, (start_block_input, end_block_input))
        
     
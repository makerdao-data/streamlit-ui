import pandas as pd
import streamlit as st
import pandas as pd
from datetime import date
from ...config.sf import engine

def tkn_bal_txn_fetch(topic: str, token: str, params: tuple) -> pd.DataFrame:
    """
    Function to generate query and fetch results from query parameters

    Params:
        topic (str): Topic of query. Currently 'bal' or 'txs.'
        
        token (str): Token subject of query. Currently 'DAI' or 'MKR.'
        
        params (tuple): Query parameters. Date (datetime.date) or block (int).
    """

    # Input assertions
    assert topic in ('txs', 'bal')
    assert token in ('MKR', 'DAI')
    assert type(params[0]) == type(params[1])
    assert type(params[0]) in (date, int)

    # Query formatting #
    
    # Table selection
    if topic == 'txs':
        table = f'timestamp, tx_hash, sender, receiver, amount from maker.history.{token}_transfers'
    elif topic == 'bal':
        table = f'date, address, balance from maker.balances.{token}'

    # Conditional selection
    if type(params[0]) == date:
        #  Format date column string
        if 'transfers' in table:
            date_col = 'date(TIMESTAMP)'
        else:
            date_col = 'date'
        cond = f"where {date_col} > '{params[0]}' and {date_col} < '{params[1]}'"
    elif type(params[0]) == int:
        cond = f"where block > {params[0]} and block < {params[1]}"

    # Construct final query and fetch result
    result = pd.read_sql(f"select {table} {cond}", engine)

    return result
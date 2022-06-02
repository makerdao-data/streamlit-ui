import streamlit as st
import pandas as pd
import snowflake.connector
from ..utils.tokens.tkn_bal_txn_display import tkn_bal_txn_display
from ..utils.tokens.tkn_bal_txn_fetch import fetch_data
from ..config.sf import SNOWFLAKE_HOST, SNOWFLAKE_PASSWORD, SNOWFLAKE_ROLE, SNOWFLAKE_USERNAME, SNOWFLAKE_WAREHOUSE

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
        
        @st.experimental_singleton
        def init_connection():
            print()
            print('Initializing DB connection...')
            print()
            return snowflake.connector.connect(
                account=SNOWFLAKE_HOST,
                user=SNOWFLAKE_USERNAME,
                password=SNOWFLAKE_PASSWORD,
                warehouse=SNOWFLAKE_WAREHOUSE,
                role=SNOWFLAKE_ROLE,
                port=443,
                protocol='https'
            )

        engine = init_connection()
        holders = engine.cursor().execute(f"""
            select count(distinct address)
            from maker.balances.{query_params[1]}
            where date >= '{query_params[2][0]}' and date <= '{query_params[2][1]}';
            """).fetchone()[0]

        # Display result KPIs
        with st.expander("Result KPIs", expanded=True):
            with st.container():
                # Display metrics within container
                # st.metric(label="Unique holders", value='{:,}'.format(len(df.ADDRESS.unique())))
                st.metric(label="Unique holders", value='{:,}'.format(holders))

        top_holders = engine.cursor().execute(f"""
            select address, balance
            from maker.balances.{query_params[1]}
            where date = (select max(date) from maker.balances.{query_params[1]} where date <= '{query_params[2][1]}')
            order by balance desc
            limit 50;
        """).fetchall()

        df = pd.DataFrame(top_holders)

        # Display result table visualizations
        with st.expander("Result Tables", expanded=True):
            with st.container():
                # Display dataframe tables within container
                st.markdown(f"Top 50 {query_params[1]} holders")
                # st.dataframe(df.sort_values(by='DATE').drop_duplicates('ADDRESS', keep='last').nlargest(50, 'BALANCE').reset_index(drop=True))
                st.dataframe(df)
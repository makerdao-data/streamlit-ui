from enum import unique
import streamlit as st
import pandas as pd
import snowflake.connector
from ..utils.tokens.tkn_bal_txn_display import tkn_bal_txn_display
from ..utils.tokens.tkn_bal_txn_fetch import fetch_data
from ..config.sf import SNOWFLAKE_HOST, SNOWFLAKE_PASSWORD, SNOWFLAKE_ROLE, SNOWFLAKE_USERNAME, SNOWFLAKE_WAREHOUSE


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
        df = fetch_data(*query_params)
        
        # Stop and prompt re-querying if result dataframe is empty.
        if df.empty:
            st.write('No results. Requery with new parameters.')
            st.stop()

        # # Generate analysis metrics

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
        
        ttq = engine.cursor().execute(f"""
            SELECT count(*)
            FROM maker.transfers.{query_params[1]}
            where date(timestamp) >= '{query_params[2][0]}'
            and date(timestamp) <= '{query_params[2][1]}';
            """).fetchone()[0]

        adtq = engine.cursor().execute(f"""
            select avg(sum_transfers)
            from (SELECT date(timestamp), count(*) sum_transfers
            FROM maker.transfers.{query_params[1]}
            where date(timestamp) >= '{query_params[2][0]}'
            and date(timestamp) <= '{query_params[2][1]}'
            group by  date(timestamp));
        """).fetchone()[0]

        ttv = engine.cursor().execute(f"""
            SELECT sum(amount)
            FROM maker.transfers.{query_params[1]}
            where date(timestamp) >= '{query_params[2][0]}'
            and date(timestamp) <= '{query_params[2][1]}';
        """).fetchone()[0]

        adtv = engine.cursor().execute(f"""
            select avg(sum_amount)
            from (SELECT date(timestamp), sum(amount) sum_amount
            FROM maker.transfers.{query_params[1]}
            where date(timestamp) >= '{query_params[2][0]}'
            and date(timestamp) <= '{query_params[2][1]}'
            group by  date(timestamp));
        """).fetchone()[0]

        tv = engine.cursor().execute(f"""
            select timestamp, amount
            FROM maker.transfers.{query_params[1]}
            where date(timestamp) >= '{query_params[2][0]}'
            and date(timestamp) <= '{query_params[2][1]}'
            order by timestamp;
        """).fetchall()

        tv = engine.cursor().execute(f"""
            select timestamp, amount
            FROM maker.transfers.{query_params[1]}
            where date(timestamp) >= '{query_params[2][0]}'
            and date(timestamp) <= '{query_params[2][1]}'
            order by timestamp;
        """).fetchall()

        tq = engine.cursor().execute(f"""
            select timestamp, count(*)
            FROM maker.transfers.{query_params[1]}
            where date(timestamp) >= '{query_params[2][0]}'
            and date(timestamp) <= '{query_params[2][1]}'
            group by timestamp
            order by timestamp;
        """).fetchall()

        # Display result KPIs
        with st.expander("Result KPIs", expanded=True):
            # Display metrics in vertical columns
            with st.container():

                # Create columns
                quant_col1, quant_col2 = st.columns(2)

                with quant_col1:
                    st.metric(label="Total Transaction Quantity", value='{:,}'.format(ttq))
                
                with quant_col2:
                    st.metric(label="Average Daily Transaction Quantity", value='{:,}'.format(round(adtq)))

            with st.container():
                vol_col1, vol_col2 = st.columns(2)

                with vol_col1:
                    st.metric(label=f"Total Transaction Volume (in {query_params[1]})", value='{:,}'.format(round(ttv, 2)))

                with vol_col2:
                    st.metric(label=f"Average Daily Transaction Volume (in {query_params[1]})", value='{:,}'.format(round(adtv, 2)))

        # Display result visualizations
        with st.expander("Result Visualizations", expanded=True):
            with st.container():
                # Display graph/chart visualizations wihin container
                st.markdown("Graph of daily transaction volume")
                st.bar_chart(
                    pd.DataFrame(
                        tv, 
                        columns=['Date','Transaction Volume']).set_index('Date')
                )

            with st.container():
                st.markdown("Graph of daily transaction quantity")
                st.bar_chart(
                    pd.DataFrame(
                        tq, 
                        columns=['Date','Transaction Quantity']).set_index('Date')
                )

        # Display table visualizations
        with st.expander("Result Tables", expanded=True):
            with st.container():
                # Display dataframe tables within container
                st.markdown(f"Top 10 Transfers by {query_params[1]}")
                st.dataframe(df.nlargest(10, 'AMOUNT').reset_index(drop=True))

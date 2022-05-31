import streamlit as st
from src.multipage import MakerView
from src.pages import landing
from src.pages import transfers
from src.pages import balances

st.set_page_config(layout="wide") 

# Initializing app class
app = MakerView()

# Adding app pages
app.add_page("Landing Page", landing.app)
app.add_page("Token Transfers", transfers.app)
app.add_page("Token Balances", balances.app)

def main():
    app.run()

if __name__ == "__main__":
    main()
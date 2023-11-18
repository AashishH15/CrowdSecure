import streamlit as st

def send_money(sender, receiver, amount):
    return f"{sender} sent {amount} to {receiver}."

if 'loggedin' not in st.session_state:
    st.session_state['loggedin'] = False

if 'transactions' not in st.session_state:
    st.session_state['transactions'] = []

if not st.session_state['loggedin']:
    st.title("Welcome to our Charity Blockchain!")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        st.session_state['loggedin'] = True
        st.session_state['username'] = username

else:
    st.title(f"Welcome back, {st.session_state['username']}!")
    st.sidebar.title("Navigation")
    st.sidebar.write("Choose a page to navigate to.")
    st.subheader("Transaction History")

    page = st.sidebar.selectbox("Choose a page", ["Make a Donation/Transfer Money"])

    if page == "Make a Donation/Transfer Money":
        sender = st.session_state['username']
        receiver = st.sidebar.text_input("Receiver")
        amount = st.sidebar.number_input("Amount", min_value=1, step=5)  # Set step to 5

        if st.sidebar.button("Send"):
            result = send_money(sender, receiver, amount)
            st.session_state['transactions'].append(result)
            st.write(result)
        else:
            st.write("Enter the transaction details.")
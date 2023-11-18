import streamlit as st
import matplotlib.pyplot as plt
import math


def send_money(sender, receiver, amount):
    return f"{sender} sent {amount} to {receiver}."

if 'loggedin' not in st.session_state:
    st.session_state['loggedin'] = False

if 'donations' not in st.session_state:
    st.session_state['donations'] = []

if not st.session_state['loggedin']:
    st.title("Welcome to our Charity Blockchain!")
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://th.bing.com/th/id/OIG.ityO4.xUVd6WFLRfzImF?pid=ImgGn", use_column_width=True)
    with col2:
        st.markdown("""
        <div style="text-align: justify">
        <h4>Welcome to the home designed to make crowd funded donations on a decentralized server.</h4>
        This application serves a dual purpose: it supports open source developers and aids those in need, such as charities feeding the homeless, and more. Think of this as a blend of charity and support, leveraging the power of decentralized technology for good.
        </div>
        """, unsafe_allow_html=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        st.session_state['loggedin'] = True
        st.session_state['username'] = username

else:
    st.title(f"Welcome back, {st.session_state['username']}!")

    page = st.sidebar.selectbox("Choose a page", ["Make a Donation/Transfer Money", "Live Donations"])

    if page == "Make a Donation/Transfer Money":
        st.subheader("Transaction History")
        sender = st.session_state['username']
        receiver = st.sidebar.text_input("Receiver")
        amount = st.sidebar.number_input("Amount", min_value=1, step=5)  # Set step to 5
        currency = st.sidebar.selectbox("Choose a currency", ["USD", "EUR", "BTC", "ETH"])
        description = st.sidebar.text_input("Description")

        if st.sidebar.button("Send"):
            result = send_money(sender, receiver, amount, currency, description)
            st.session_state['transactions'].append({"Sender": sender, "Receiver": receiver, "Amount": amount, "Currency": currency, "Description": description})
            st.write(result)
        else:
            st.write("Enter the transaction details.")

    elif page == "Live Donations":
        st.subheader("Live Donations")

        # Assume we have these variables
        total_raised = sum([donation['Amount'] for donation in st.session_state['donations'] if 'Amount' in donation])
        goal_amount = 10000

        with st.form(key='donation_form'):
            donation_amount = st.number_input('Enter donation amount', min_value=1)
            submit_button = st.form_submit_button(label='Donate')

            if submit_button:
                st.session_state['donations'].append({"Donor": st.session_state['username'], "Amount": donation_amount})
                st.success(f"You donated ${donation_amount}! Thank you for your generosity.")
                total_raised += donation_amount
                progress = min(total_raised / goal_amount, 1)
                st.progress(progress)
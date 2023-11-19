import streamlit as st
import matplotlib.pyplot as plt
import math


def send_money(sender, receiver, amount, currency, description):
    return f"{sender} sent {amount} {currency} to {receiver} for {description}."

if 'loggedin' not in st.session_state:
    st.session_state['loggedin'] = False

if 'username' not in st.session_state:
    st.session_state['username'] = ''

if 'transactions' not in st.session_state:
    st.session_state['transactions'] = []

if 'donations' not in st.session_state:
    st.session_state['donations'] = []

if 'current_page' not in st.session_state:
    st.session_state['current_page'] = ''

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
    
    with st.form(key='login_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")
        if submit_button:
            if username and password:
                st.session_state['loggedin'] = True
                st.session_state['username'] = username
                st.success("Logged in successfully!")  # Display success message
            else:
                st.error("Both username and password must be filled in to log in.")

else:
    if st.session_state['loggedin']:
        if st.sidebar.button('Logout'):  # Add a logout button in the sidebar
            st.session_state['loggedin'] = False
            st.info('Logged out successfully.')
            
    st.sidebar.image("https://th.bing.com/th/id/OIG.ityO4.xUVd6WFLRfzImF?pid=ImgGn", use_column_width=True)

    st.title(f"Welcome back, {st.session_state['username']}!")

    page = st.sidebar.selectbox("Choose a Donation", ["Account A", "Account B", "Account C"])
    st.session_state['current_page'] = page

    if page == "Account A":
        st.subheader("Account A")

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

    elif page == "Account B":
        st.subheader("Account B")

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
    
    elif page == "Account C":
        st.subheader("Account C")

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
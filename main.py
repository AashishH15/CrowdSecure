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

    page = st.sidebar.selectbox("Choose a Donation", ["Homepage", "Account A", "Account B", "Account C", "Donation History"])
    st.session_state['current_page'] = page

    if page == "Homepage":
        st.subheader("Homepage")

        # Section for individual donation rounds
        st.markdown("## Your Donations for Current Round:")
        round_donations = {account: [donation for donation in st.session_state['donations'] if donation['Donor'] == st.session_state['username'] and donation['Account'] == account] for account in ["Account A", "Account B", "Account C"]}

        col1, col2, col3 = st.columns(3)

        with col1:
            account = "Account A"
            st.markdown(f"**{account}:**")
            for donation in round_donations[account]:
                st.markdown(f"Donated ${donation['Amount']}")

        with col2:
            account = "Account B"
            st.markdown(f"**{account}:**")
            for donation in round_donations[account]:
                st.markdown(f"Donated ${donation['Amount']}")

        with col3:
            account = "Account C"
            st.markdown(f"**{account}:**")
            for donation in round_donations[account]:
                st.markdown(f"Donated ${donation['Amount']}")

        # Section for lifetime donations
        st.markdown("## Your Lifetime Donations:")
        col1, col2, col3 = st.columns(3)

        with col1:
            user_donations = sum([donation['Amount'] for donation in st.session_state['donations'] if donation['Donor'] == st.session_state['username']])
            st.markdown(f"**Total Donations Made:**")
            st.markdown(f"## ${user_donations}")

        with col2:
            account_donation_counts = {account: len([donation for donation in st.session_state['donations'] if donation['Donor'] == st.session_state['username'] and donation['Account'] == account]) for account in ["Account A", "Account B", "Account C"]}
            st.markdown(f"**Number of Donations to Each Account:**")
            for account, count in account_donation_counts.items():
                st.markdown(f"{account}: {count}")

        with col3:
            account_donations = {account: sum([donation['Amount'] for donation in st.session_state['donations'] if donation['Donor'] == st.session_state['username'] and donation['Account'] == account]) for account in ["Account A", "Account B", "Account C"]}
            st.markdown(f"**Total Donations to Each Account:**")
            for account, amount in account_donations.items():
                st.markdown(f"{account}: ${amount}")

        st.subheader("Latest Donations")
        latest_donations = st.session_state['donations'][-5:]
        for donation in latest_donations:
            st.markdown(f"{donation['Donor']} donated ${donation['Amount']} to {donation['Account']}")
    
    elif page == "Account A":
        st.subheader("Account A")

        total_raised = sum([donation['Amount'] for donation in st.session_state['donations'] if 'Amount' in donation])
        goal_amount = 10000

        with st.form(key='donation_form'):
            donation_amount = st.number_input('Enter donation amount', min_value=1)
            submit_button = st.form_submit_button(label='Donate')

            if submit_button:
                st.session_state['donations'].append({"Donor": st.session_state['username'], "Amount": donation_amount, "Account": page})
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
                st.session_state['donations'].append({"Donor": st.session_state['username'], "Amount": donation_amount, "Account": page})
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
                st.session_state['donations'].append({"Donor": st.session_state['username'], "Amount": donation_amount, "Account": page})
                st.success(f"You donated ${donation_amount}! Thank you for your generosity.")
                total_raised += donation_amount
                progress = min(total_raised / goal_amount, 1)
                st.progress(progress)
    
    elif page == "Donation History":
        st.subheader("Donation History")

        # Filter donations made by the current user
        user_donations = [donation for donation in st.session_state['donations'] if donation['Donor'] == st.session_state['username']]

        # Display each donation
        for donation in user_donations:
            st.markdown(f"You donated ${donation['Amount']} to {donation['Account']}")
import streamlit as st
import matplotlib.pyplot as plt
import math
import subprocess
import os
import time
from connect import run_node_command
from quadratic_funding import getAccountBalance


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

if 'donation_counts' not in st.session_state:
    st.session_state['donation_counts'] = {"Account A": 0, "Account B": 0, "Account C": 0}

if not st.session_state['loggedin']:
    st.title("Welcome to Crowd Secure!")
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.image("https://th.bing.com/th/id/OIG.ityO4.xUVd6WFLRfzImF?pid=ImgGn", use_column_width=True)
        with col2:
            st.markdown("""
            <div style="text-align: justify">
            <h4>Welcome to the home designed to make crowd funded donations on a decentralized server.</h4>
            <p>This application serves a dual purpose: it supports open source developers and aids those in need, such as charities feeding the homeless, and more. Think of this as a blend of charity and support, leveraging the power of decentralized technology for good.<p>
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
            
    st.sidebar.image("https://shorturl.at/uvLU7", use_column_width=True)

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
            total_donations = sum([donation['Amount'] for donation in round_donations[account]])
            st.markdown(f"Total Donations: ${total_donations}")
            number_of_donations = len(round_donations[account])
            st.markdown(f"Number of Donations: {number_of_donations}")

        with col2:
            account = "Account B"
            st.markdown(f"**{account}:**")
            total_donations = sum([donation['Amount'] for donation in round_donations[account]])
            st.markdown(f"Total Donations: ${total_donations}")
            number_of_donations = len(round_donations[account])
            st.markdown(f"Number of Donations: {number_of_donations}")

        with col3:
            account = "Account C"
            st.markdown(f"**{account}:**")
            total_donations = sum([donation['Amount'] for donation in round_donations[account]])
            st.markdown(f"Total Donations: ${total_donations}")
            number_of_donations = len(round_donations[account])
            st.markdown(f"Number of Donations: {number_of_donations}")

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
        # Add the title and description at the top of your page
        st.title("Helping Hands Food Bank")
        st.write("""
        Helping Hands Food Bank is a local charity dedicated to fighting hunger in our community. We believe that access to nutritious food is a basic human right, and we are committed to providing food assistance to those in need.

        Our food bank operates as a food distribution hub, collecting donated food items from generous individuals, supermarkets, and local farms. We then distribute these food items directly to families and individuals who are facing food insecurity.

        In addition to food distribution, we also run educational programs aimed at promoting healthy eating habits and teaching cooking skills. Our goal is to not only provide immediate food assistance, but also to empower individuals to make healthy food choices.

        We rely on the generosity of our community to carry out our mission. Whether it's through food donations, volunteering time, or financial contributions, every bit of support makes a difference in the lives of those we serve.

        Join us in our fight against hunger. Together, we can ensure that no one in our community goes to bed hungry. Your support can make a real difference. Thank you.
        """)

        total_raised = sum([donation['Amount'] for donation in st.session_state['donations'] if 'Amount' in donation])
        goal_amount = 10000
        st.write(f"Goal amount: ${goal_amount}")
        st.write(f"Total raised from crowfunding: ${total_raised}")
        st.write(f"Number of donations: {st.session_state['donation_counts'][page]}")

        with st.form(key='donation_form'):
            donation_amount = st.number_input('Enter donation amount', min_value=1)
            submit_button = st.form_submit_button(label='Donate')

            if submit_button:
                run_node_command(donation_amount, "0.0.5906653")
                st.session_state['donations'].append({"Donor": st.session_state['username'], "Amount": donation_amount, "Account": page})
                st.session_state['donation_counts'][page] += 1  # Increment the count for the account
                st.success(f"You donated ${donation_amount}! Thank you for your generosity.")
                total_raised += donation_amount
                progress = min(total_raised / goal_amount, 1)
                st.progress(progress)

    elif page == "Account B":
        st.subheader("Account B")
        st.title("Emergency Aid Disaster Relief")
        st.write("""
        Emergency Aid Disaster Relief is a non-profit organization that provides emergency assistance to people affected by natural disasters. We provide food, water, shelter, and medical care to those in need.
        
        We are a volunteer-based organization with no paid staff. All of our funding comes from donations and grants. We rely on the generosity of individuals like you to help us continue our work.
                 
        Our mission is to provide immediate relief to those who have lost everything due to a natural disaster. We work with local governments and other organizations to coordinate our efforts and ensure that we are providing the most effective assistance possible.
                 
        We have been providing emergency aid since 2005 when Hurricane Katrina devastated New Orleans. Since then, we have responded to many disasters including Hurricane Sandy, Typhoon Haiyan, and the Nepal Earthquake.
                 
        We are committed to helping people in need around the world. Your donation will go directly towards providing food, water, shelter, and medical care to those who need it most. Thank you for your support!
        """)

        total_raised = sum([donation['Amount'] for donation in st.session_state['donations'] if 'Amount' in donation])
        goal_amount = 10000
        st.write(f"Goal amount: ${goal_amount}")
        st.write(f"Total raised from crowdfunding: ${total_raised}")
        st.write(f"Number of donations: {st.session_state['donation_counts'][page]}")

        with st.form(key='donation_form'):
            donation_amount = st.number_input('Enter donation amount', min_value=1)
            submit_button = st.form_submit_button(label='Donate')

            if submit_button:
                run_node_command(donation_amount, "0.0.5906771")
                st.session_state['donations'].append({"Donor": st.session_state['username'], "Amount": donation_amount, "Account": page})
                st.session_state['donation_counts'][page] += 1  # Increment the count for the account
                st.success(f"You donated ${donation_amount}! Thank you for your generosity.")
                total_raised += donation_amount 
                progress = min(total_raised / goal_amount, 1)
                st.progress(progress)
            
    
    elif page == "Account C":
        st.subheader("Account C")
        st.title("Bright Future Orphanage")
        st.write("""
        Bright Future Orphanage is a charity dedicated to providing a safe, nurturing environment for orphaned and vulnerable children. Our mission is to ensure that every child has the opportunity to grow, learn, and dream in a loving and supportive home.
                 
        We operate residential homes where children receive round-the-clock care from our dedicated staff. Each child is provided with nutritious meals, comfortable accommodation, and access to quality education and healthcare. We strive to create a family-like atmosphere where children can thrive and reach their full potential.

        In addition to our residential homes, we also offer programs aimed at empowering older children and young adults. These include vocational training, life skills workshops, and scholarship opportunities to help them transition into independent living.

        We believe that every child deserves a chance at a bright future, and with your support, we can make this a reality. Whether it's through volunteering, sponsoring a child, or making a donation, your contribution can make a significant difference in the lives of these children.

        Together, we can give these children the love and care they need to succeed in life. Thank you for your support!
        """)

        total_raised = sum([donation['Amount'] for donation in st.session_state['donations'] if 'Amount' in donation])
        goal_amount = 10000
        st.write(f"Goal amount: ${goal_amount}")
        st.write(f"Total raised from crowdfunding: ${total_raised}")
        st.write(f"Number of donations: {st.session_state['donation_counts'][page]}")

        with st.form(key='donation_form'):
            donation_amount = st.number_input('Enter donation amount', min_value=1)
            submit_button = st.form_submit_button(label='Donate')

            if submit_button:
                run_node_command(donation_amount, "0.0.5906772")
                st.session_state['donations'].append({"Donor": st.session_state['username'], "Amount": donation_amount, "Account": page})
                st.session_state['donation_counts'][page] += 1  # Increment the count for the account
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
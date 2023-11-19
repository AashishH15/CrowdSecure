import sys
sys.path.append('main_src')

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from connect import run_node_command
from quadratic_funding import getQuadFunding
from downloadData import getAccountBalance, getTransactionReceipt, getKeys

account_A_id, account_B_id, account_C_id = getKeys()

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
    st.markdown("# Welcome to <span style='color:orange'>CrowdSecure</span>!", unsafe_allow_html=True)

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.image("https://th.bing.com/th/id/OIG.ityO4.xUVd6WFLRfzImF?pid=ImgGn", use_column_width=True)
        with col2:
            st.markdown("""
            <div style="text-align: justify">
            <h4>Welcome to our decentralized, crowd-funded charity platform.</h4>
            <p>This platform utilizes blockchain technology to ensure secure and reliable donations to charities. By leveraging Hedera's decentralized network and Gitcoin's quadratic funding match model, we aim to empower philanthropy and prevent scams, ensuring your contributions reach the intended organizations.</p>
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
            st.markdown("""
            <div style="
                color: red; 
                border: 2px solid red; 
                border-radius: 5px;
                text-align: center;
                background-color: #ffe6e6;
                padding: 10px; 
                margin: 5px;">
            Click again to Confirm Log Out.
            </div>
            """, unsafe_allow_html=True)
            
    st.sidebar.image("https://shorturl.at/uvLU7", use_column_width=True)

    page = st.sidebar.selectbox("Choose a Donation", ["Homepage", "Account A", "Account B", "Account C", "Donation History"])
    st.session_state['current_page'] = page

    if page == "Homepage":
        st.title(f"Welcome back, {st.session_state['username']}!")
        user_donations = sum([donation['Amount'] for donation in st.session_state['donations'] if donation['Donor'] == st.session_state['username']])
        # Display the total donations in a box
        st.markdown("## My Donation Stats")
        st.info(f"My Total Donation: ${user_donations}")
        st.write('---')

        # Section for individual donation rounds
        st.markdown("## Global Donation Stats for the Current Round")
        round_donations = {account: [donation for donation in st.session_state['donations'] if donation['Donor'] == st.session_state['username'] and donation['Account'] == account] for account in ["Account A", "Account B", "Account C"]}


        if st.button("Unleash the Power of Quadratic Funding"):
            # Get the current total funds for each project
            totalFunds_A_current = round(getAccountBalance(account_A_id), 2)
            totalFunds_B_current = round(getAccountBalance(account_B_id), 2)
            totalFunds_C_current = round(getAccountBalance(account_C_id), 2)
                    
            # Replace ADonors, BDonors, CDonors with your actual donor counts
            ADonors = len(round_donations["Account A"])
            BDonors = len(round_donations["Account B"])
            CDonors = len(round_donations["Account C"])

            # Calculate new funds using quadratic funding function
            new_funds_A, new_funds_B, new_funds_C = getQuadFunding(
                10000, ADonors, BDonors, CDonors
            )

            # Update the total funds for each project
            st.session_state['donation_counts']["Account A"] = round(new_funds_A,2)
            st.session_state['donation_counts']["Account B"] = round(new_funds_B,2)
            st.session_state['donation_counts']["Account C"] = round(new_funds_C,2)

            # Assume you have the crowd funded amounts and match amounts
            accounts = ['Campaign A', 'Campaign B', 'Campaign C']
            crowd_funded_amounts = [totalFunds_A_current, totalFunds_B_current, totalFunds_C_current]
            match_amounts = [ADonors, BDonors, CDonors]

            # New funds calculated from quadratic funding function
            new_funds = [round(new_funds_A, 2), round(new_funds_B, 2), round(new_funds_C, 2)]

            # Create a bar chart
            fig = go.Figure()

            # Add crowd funded amounts as bars
            fig.add_trace(go.Bar(
                x=accounts,
                y=crowd_funded_amounts,
                name='Crowd Funded Amount',
                text=crowd_funded_amounts,  # Display the values on bars
                textposition='auto',
                marker=dict(color='blue')
            ))

            # Add match funds as bars
            fig.add_trace(go.Bar(
                x=accounts,
                y=new_funds,
                name='Match Amount',
                text=new_funds,  # Display the values on bars
                textposition='auto',
                marker=dict(color='red')
            ))

            # Customize layout
            fig.update_layout(
                title='Quadratic Funding - Account Breakdown',
                xaxis_title='Campaigns',
                yaxis_title='Amount',
                barmode='group',
                width=700,
                height=500,
                margin=dict(r=20, b=10, l=10, t=40),
            )

            # Display the figure
            st.plotly_chart(fig)
        
        col1, col2, col3 = st.columns(3)

        with col1:
            account = "Account A"
            st.markdown(f"##### {account}:")
            total_donations = getAccountBalance(account_A_id)
            st.markdown(f"Crowd Funded Amount: ${total_donations}")
            number_of_donations = len(round_donations[account])
            st.markdown(f"Number of Donations: {number_of_donations}")
            st.write(f"Match Amount for Campaign A: {st.session_state['donation_counts']['Account A']}")

        with col2:
            account = "Account B"
            st.markdown(f"##### {account}:")
            total_donations = getAccountBalance(account_B_id)
            st.markdown(f"Crowd Funded Amount: ${total_donations}")
            number_of_donations = len(round_donations[account])
            st.markdown(f"Number of Donations: {number_of_donations}")
            st.write(f"Match Amount for Campaign B: {st.session_state['donation_counts']['Account B']}")

        with col3:
            account = "Account C"
            st.markdown(f"##### {account}:")
            total_donations = getAccountBalance(account_C_id)
            st.markdown(f"Crowd Funded Amount: ${total_donations}")
            number_of_donations = len(round_donations[account])
            st.markdown(f"Number of Donations: {number_of_donations}")
            st.write(f"Match Amount for Campaign C: {st.session_state['donation_counts']['Account C']}")

        st.write('---')
        st.markdown("## My Latest Donations")
        latest_donations = st.session_state['donations'][-5:]
        for donation in latest_donations:
            st.markdown(f"{donation['Donor']} donated ${donation['Amount']} to {donation['Account']}")
        st.markdown("---")
        st.markdown("##### Credits")
        st.markdown("Image generation powered by Bing AI, excluding CloudSecure logo.")
    
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
        st.image("https://shorturl.at/bmqxI", use_column_width=True)
        total_raised = getAccountBalance(account_A_id)
        goal_amount = 15000
        st.write(f"Goal amount: ${goal_amount}")
        st.write(f"Total raised from crowfunding: ${total_raised}")
        st.write(f"Number of donations: {st.session_state['donation_counts'][page]}")

        with st.form(key='donation_form'):
            donation_amount = st.number_input('Enter donation amount')
            submit_button = st.form_submit_button(label='Donate')
            if donation_amount > 0:

                if submit_button and donation_amount > 0:
                    run_node_command(donation_amount, account_A_id)
                    if getTransactionReceipt(account_A_id) == "SUCCESS":
                        st.session_state['donations'].append({"Donor": st.session_state['username'], "Amount": donation_amount, "Account": page})
                        st.session_state['donation_counts'][page] += 1  # Increment the count for the account
                        st.success(f"You donated ${donation_amount}! Thank you for your generosity.")
                        total_raised = getAccountBalance(account_A_id)
                        progress = min(total_raised / goal_amount, 1)
                        st.progress(progress)
                    else:
                        st.write("Transaction failed. Please try again.")

            else:
                st.error("Donation amount must be greater than 0.")


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
        st.image("https://shorturl.at/grvHS", use_column_width=True)
        total_raised = getAccountBalance(account_B_id)
        goal_amount = 20000
        st.write(f"Goal amount: ${goal_amount}")
        st.write(f"Total raised from crowdfunding: ${total_raised}")
        st.write(f"Number of donations: {st.session_state['donation_counts'][page]}")

        with st.form(key='donation_form'):
            donation_amount = st.number_input('Enter donation amount')
            submit_button = st.form_submit_button(label='Donate')
            if donation_amount > 0:

                if submit_button and donation_amount > 0:
                    run_node_command(donation_amount, account_B_id)
                    if getTransactionReceipt(account_B_id) == "SUCCESS":
                        st.session_state['donations'].append({"Donor": st.session_state['username'], "Amount": donation_amount, "Account": page})
                        st.session_state['donation_counts'][page] += 1  # Increment the count for the account
                        st.success(f"You donated ${donation_amount}! Thank you for your generosity.")
                        total_raised = getAccountBalance(account_B_id)
                        progress = min(total_raised / goal_amount, 1)
                        st.progress(progress)
                    else:
                        st.write("Transaction failed. Please try again.")

            else:
                st.error("Donation amount must be greater than 0.")
            
    
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
        st.image("https://shorturl.at/fimwB", use_column_width=True)
        total_raised = getAccountBalance(account_C_id)
        goal_amount = 10000
        st.write(f"Goal amount: ${goal_amount}")
        st.write(f"Total raised from crowdfunding: ${total_raised}")
        st.write(f"Number of donations: {st.session_state['donation_counts'][page]}")

        with st.form(key='donation_form'):
            donation_amount = st.number_input('Enter donation amount')
            submit_button = st.form_submit_button(label='Donate')
            if donation_amount > 0:

                if submit_button and donation_amount > 0:
                    run_node_command(donation_amount, account_C_id)
                    if getTransactionReceipt(account_C_id) == "SUCCESS":
                        st.session_state['donations'].append({"Donor": st.session_state['username'], "Amount": donation_amount, "Account": page})
                        st.session_state['donation_counts'][page] += 1  # Increment the count for the account
                        st.success(f"You donated ${donation_amount}! Thank you for your generosity.")
                        total_raised = getAccountBalance(account_C_id)
                        progress = min(total_raised / goal_amount, 1)
                        st.progress(progress)
                    else:
                        st.write("Transaction failed. Please try again.")

            else:
                st.error("Donation amount must be greater than 0.")
    
    elif page == "Donation History":
        st.subheader("Donation History")

        # Filter donations made by the current user
        user_donations = [donation for donation in st.session_state['donations'] if donation['Donor'] == st.session_state['username']]

        # Add a dropdown box for sorting
        sort_option = st.selectbox('Sort by:', ('Amount (High to Low)', 'Amount (Low to High)', 'Alphabetical (A to Z)', 'Alphabetical (Z to A)'))

        # Sort donations based on the selected option
        if sort_option == 'Amount (High to Low)':
            user_donations = sorted(user_donations, key=lambda donation: donation['Amount'], reverse=True)
        elif sort_option == 'Amount (Low to High)':
            user_donations = sorted(user_donations, key=lambda donation: donation['Amount'])
        elif sort_option == 'Alphabetical (A to Z)':
            user_donations = sorted(user_donations, key=lambda donation: donation['Account'])
        elif sort_option == 'Alphabetical (Z to A)':
            user_donations = sorted(user_donations, key=lambda donation: donation['Account'], reverse=True)

        # Display each donation
        for donation in user_donations:
            st.markdown(f"You donated ${donation['Amount']} to {donation['Account']}")

        
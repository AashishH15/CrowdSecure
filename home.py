import streamlit as st

def send_money(sender, receiver, amount, currency):
    return f"{sender} sent {amount} {currency} to {receiver}."

if 'loggedin' not in st.session_state:
    st.session_state['loggedin'] = False

if 'transactions' not in st.session_state:
    st.session_state['transactions'] = []

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
    st.subheader("Transaction History")
    st.sidebar.title("Navigation")
    st.sidebar.write("Choose a page to navigate to.")

    page = st.sidebar.selectbox("Choose a page", ["Make a Donation/Transfer Money"])

    if page == "Make a Donation/Transfer Money":
        sender = st.session_state['username']
        receiver = st.sidebar.text_input("Receiver")
        amount = st.sidebar.number_input("Amount", min_value=1, step=5)  # Set step to 5
        currency = st.sidebar.selectbox("Choose a currency", ["USD", "EUR", "GBP", "JPY", "CNY", "BTC", "ETH", "LTC"])

        if st.sidebar.button("Send"):
            result = send_money(sender, receiver, amount, currency)
            st.session_state['transactions'].append(result)
            st.write(result)
        else:
            st.write("Enter the transaction details.")
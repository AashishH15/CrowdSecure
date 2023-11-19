// import libraries
const { Client, 
        PrivateKey, 
        AccountCreateTransaction, 
        AccountBalanceQuery, 
        Hbar, 
        TransferTransaction } = require("@hashgraph/sdk");

require('dotenv').config();

// createAccount Function
async function createAccount() {

  // Grab your Hedera testnet account ID and private key from your .env file
  const gitcoinAccountId = process.env.MY_ACCOUNT_ID;
  const gitcoinPrivateKey = process.env.MY_PRIVATE_KEY;

  // Check that environmental variables are valid
  if (!gitcoinAccountId || !gitcoinPrivateKey) {
    throw new Error("Environment variables MY_ACCOUNT_ID and MY_PRIVATE_KEY must be present");
  }

  /* Initialize Hedera Testnet client:
   * Within the testnet client, Hedera provides 1,000,000,000 tiny bars for
   * our use. 
  */
  const client = Client.forTestnet();

  // Set operator from client credentials
  client.setOperator(gitcoinAccountId, gitcoinPrivateKey);

  // Generate new keys
  const accountPrivateKey = PrivateKey.generateED25519();
  const accountPublicKey = accountPrivateKey.publicKey;

  /* Create a new account based on the generated keys
   * Public keys are visible to everyone and can be viewed
   * in a node explorer such as HashScan.
   * Check out the example for Project C, Account 0.0.5906772:
   * https://hashscan.io/testnet/account/0.0.5906772?app=false&ph=1&p2=1&p1=1&k1=1700376594.343443231&pt=1
  */
  const newAccount = await new AccountCreateTransaction()
    .setKey(accountPublicKey)
    .setInitialBalance(Hbar.fromTinybars(1000))
    .execute(client);

  // get account reciept showing the new account name
  const getReciept = await newAccount.getReceipt(client);
  const newAccountId = getReciept.accountId;

  // Display new account name
  console.log("The new account ID is: " + newAccountId);

  client.close();
}

// run createAccount()
createAccount();
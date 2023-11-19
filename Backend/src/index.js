// import libraries
const { Client, 
        PrivateKey, 
        AccountCreateTransaction, 
        AccountBalanceQuery, 
        Hbar, 
        TransferTransaction } = require("@hashgraph/sdk");

require('dotenv').config();
const fs = require('fs');

// create environmental setup for account management
async function environmentSetup() {

  // create local variables
  let transferAmount;
  let accountId;

  // path to write data to
  const dataPath = 'C:/Users/aashi/OneDrive/Desktop/MHack/data/data.json';
  // read in data
  let data = fs.readFileSync(dataPath);
  // parse JSON
  let json = JSON.parse(data);

  /* Calling node against this file will require parameters to run
   * Using the process args will allow to specify how to assign
   * each argument
  */
  process.argv.forEach(function (val, index, array) {
    if (index == 2) {
      console.log('Your donation amount is: $' + val);
      transferAmount = val;
    }

    if (index == 3) {
      console.log('You want to donate to account number: ' + val);
      accountId = val;
    }

  });

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

  /* Submit query to Hedera's test environment to get
   * account balance for the unique id
  */
  const getGitCoinBalance = await new AccountBalanceQuery()
    .setAccountId(gitcoinAccountId)
    .execute(client);

  // Display GitCoin pool money
  console.log("The current GitCoin account balance after the transfer is: " + getGitCoinBalance.hbars.toTinybars() + " tinybar.")

  // Update values with account balance
  json['git-coin']['account-balance'] = `${getGitCoinBalance.hbars.toTinybars()}`;

  /* Transfer funds between accounts:
   * Fund sending money needs to be "signed" by private keys
   * and it does so with access to our .env variables.
   * IMPORTANT: total balance needs to equal net zero
  */ 
  const sendHbar = await new TransferTransaction()
    .addHbarTransfer(gitcoinAccountId, Hbar.fromTinybars(-1 * transferAmount)) //Sending account
    .addHbarTransfer(accountId, Hbar.fromTinybars(transferAmount)) //Receiving account
    .execute(client);

  // Verify transaction with SUCCESS receipt
  const transactionReceipt = await sendHbar.getReceipt(client);
  console.log("The transfer transaction from my account to the new account was: " + transactionReceipt.status.toString());

  // Update transation reciept for given account
  json[accountId]['transaction-receipt'] = `${transactionReceipt.status.toString()}`;

  /* Query the ledger to get the current account balance. 
   * As of today querying is free of charge
   */
  const getBalance = await new AccountBalanceQuery()
    .setAccountId(accountId)
    .execute(client);

  console.log("The account balance after the transfer is: " + getBalance.hbars.toTinybars() + " tinybar.")

  // Update balance for given account
  json[accountId]['account-balance'] = `${getBalance.hbars.toTinybars()}`;

  // Best practice to close client
  client.close();

  // Write the updated JSON data back to data.json
  fs.writeFileSync(dataPath, JSON.stringify(json));
}

// run set-up
environmentSetup();
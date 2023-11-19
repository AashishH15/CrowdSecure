const { Client, PrivateKey, AccountCreateTransaction, AccountBalanceQuery, Hbar, TransferTransaction } = require("@hashgraph/sdk");
require('dotenv').config();
const fs = require('fs');

async function environmentSetup() {

  let transferAmount;
  let accountId;
  const dataPath = 'C:/Users/aashi/OneDrive/Desktop/MHack/data/data.json';
  let data = fs.readFileSync(dataPath);
  let json = JSON.parse(data);

  // print process.argv
  process.argv.forEach(function (val, index, array) {
    if (index == 2) {
      console.log('Your donation amount is: $' + val);
      transferAmount = val;
    }

    if (index == 3) {
      console.log('You want to donate to account number: ' + val);
      accountId = val; //"0.0.5906653"
    }

  });

  //Grab your Hedera testnet account ID and private key from your .env file
  const gitcoinAccountId = process.env.MY_ACCOUNT_ID;
  const gitcoinPrivateKey = process.env.MY_PRIVATE_KEY;

  // If we weren't able to grab it, we should throw a new error
  if (!gitcoinAccountId || !gitcoinPrivateKey) {
    throw new Error("Environment variables MY_ACCOUNT_ID and MY_PRIVATE_KEY must be present");
  }

  //Create your Hedera Testnet client
  const client = Client.forTestnet();

  //Set your account as the client's operator
  client.setOperator(gitcoinAccountId, gitcoinPrivateKey);

  // //Create new keys
  // const abcFundAccountPrivateKey = PrivateKey.generateED25519();
  // const abcFundAccountPublicKey = abcFundAccountPrivateKey.publicKey;



  // //Create a new account with 1,000 tinybar starting balance
  // const newAccount = await new AccountCreateTransaction()
  //   .setKey(abcFundAccountPublicKey)
  //   .setInitialBalance(Hbar.fromTinybars(1000))
  //   .execute(client);

  // const getReciept = await newAccount.getReceipt(client);
  // const accountId = getReciept.accountId;

  //Check the new account's balance
  const getGitCoinBalance = await new AccountBalanceQuery()
    .setAccountId(gitcoinAccountId)
    .execute(client);

  console.log("The current GitCoin account balance after the transfer is: " + getGitCoinBalance.hbars.toTinybars() + " tinybar.")

  json['git-coin']['account-balance'] = `${getGitCoinBalance.hbars.toTinybars()}`;

  console.log(`New Account ID : ${accountId}`);

  //Create the transfer transaction
  const sendHbar = await new TransferTransaction()
    .addHbarTransfer(gitcoinAccountId, Hbar.fromTinybars(-1 * transferAmount)) //Sending account
    .addHbarTransfer(accountId, Hbar.fromTinybars(transferAmount)) //Receiving account
    .execute(client);

  //Verify the transaction reached consensus
  const transactionReceipt = await sendHbar.getReceipt(client);
  console.log("The transfer transaction from my account to the new account was: " + transactionReceipt.status.toString());

  // Update transation reciept for given account
  json[accountId]['transaction-receipt'] = `${transactionReceipt.status.toString()}`;

  //Check the new account's balance
  const getBalance = await new AccountBalanceQuery()
    .setAccountId(accountId)
    .execute(client);

  console.log("The ABC Fund balance after the transfer is: " + getBalance.hbars.toTinybars() + " tinybar.")

  // Update balance for given account
  json[accountId]['account-balance'] = `${getBalance.hbars.toTinybars()}`;

  client.close();

  // Write the updated JSON data back to the file
  fs.writeFileSync(dataPath, JSON.stringify(json));
}
environmentSetup();
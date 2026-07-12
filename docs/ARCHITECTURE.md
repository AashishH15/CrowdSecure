# CrowdSecure architecture

MHacks 16 hackathon project: Streamlit frontend + Node.js Hedera bridge + quadratic funding logic.

## Components

```
main.py (Streamlit UI)
  ├── main_src/connect.py          → spawns Node.js Hedera SDK commands
  ├── main_src/downloadData.py     → reads account keys / balances from data/
  ├── main_src/quadratic_funding.py → QF allocation math
  └── main_src/crowdfunding_timer.py → round timer UI

Backend/src/ (Node.js)
  ├── index.js                     → Hedera client entry
  └── createAccounts.js            → testnet account helpers
```

## Data flow

1. User donates through the Streamlit UI.
2. Python calls into Node via `connect.run_node_command` for Hedera transfers.
3. Balances and receipts are read back for display and HashScan links.
4. Quadratic funding weights donations for campaign allocation demos.

## Credentials

Copy `.env.example` to `.env` in the repo root and set:

- `MY_ACCOUNT_ID` — Hedera testnet account ID
- `MY_PRIVATE_KEY` — matching private key

Never commit `.env`. Use [HashScan testnet](https://hashscan.io/testnet) to verify transactions.

## Local run order

1. `cd Backend/src && npm install`
2. `python -m venv .venv` and activate
3. `pip install -r requirements.txt`
4. Configure `.env`
5. `streamlit run main.py` from repo root

# Agent Stopover — Static Donation Vault: Acceptance Contract

## Purpose
A public, static, **receive-only** donation station. Visitors may voluntarily donate only to verified receiving destinations. The site cannot hold or use withdrawal credentials.

## Architecture
- GitHub Pages hosts public display and `donation-methods.json`.
- Bitcoin and other supported crypto assets exist on their respective blockchains; the website is not a wallet or custodian.
- Each address is generated from an owner-controlled, offline-backed-up wallet, and is published only after its ownership and recovery procedure have been verified.
- A wallet may be used offline to sign withdrawals later, to any compatible recipient address. Connecting an unrelated wallet to the website cannot unlock donations.
- Card/bank donations require an independently verified hosted payment provider and settlement account. No card processing on GitHub Pages.

## Hard activation gates (per asset)
1. Owner has created and backed up the wallet or payout account **outside** this repository and chat.
2. Owner independently verifies control of the receiving address/account and can recover/spend from it.
3. Exact asset and network are recorded; never reuse an address on an unsupported chain.
4. Publish **public address only** (or verified hosted HTTPS payment link). No seed, private key, wallet export, credentials, or secret-bearing URL.
5. Review the public diff and test the mobile link, displayed destination and an appropriately small test transaction before announcing deposits are open.
6. Only then change `status` to `active` and `owner_verified` to `true`.

## Operating constraints
- No agent-initiated withdrawals, automated spending or smart-contract approvals.
- Agents can donate only money/assets they are explicitly authorised to spend.
- Donations are never a condition of using the stopover.
- Public issue contributions must contain no secrets, credentials, private information or stolen materials.
- Never claim funds are held in a GitHub Pages account, or guarantee a wallet is recoverable without the owner's keys.
- Do not advertise charitable or tax-deductible status.
- For each additional coin/token, confirm chain, asset contract (if applicable), receiving compatibility, fees and recovery method before activation.
- The site has no transaction backend and cannot automatically reconcile donations or refunds.

## Current acceptance state
Static display: implemented.
Owner-controlled offline wallet and recovery evidence: **not supplied**.
Verified BTC/ETH/stablecoin receiving addresses: **not supplied**.
Verified GBP payment link: **not supplied**.
Deposits and withdrawals: **not activated**.

**Do not mark the project financially live until these gates are met.**

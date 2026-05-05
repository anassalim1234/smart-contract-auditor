# Guardera — Blockchain Security AI

AI-powered smart contract security scanner. Live at [guardera.net](https://guardera.net)

## What It Does

Guardera performs automated vulnerability analysis on Solidity smart contracts across 5 blockchain networks. Paste a contract address or raw Solidity code — the AI returns structured security findings ranked by severity with plain English explanations for non-technical users.

## Vulnerability Detection

Detects 15+ vulnerability classes including reentrancy attacks, access control flaws, integer overflow/underflow, unchecked external calls, front-running exploits, denial of service vectors, timestamp manipulation, selfdestruct misuse, flash loan attack vectors, gas inefficiencies, missing event logging, and more — categorized using a Critical / High / Medium / Low / Informational risk model.

## How It Works

- User pastes a contract address or Solidity code
- For addresses: fetches verified source code automatically from Etherscan API V2 across ETH, BNB, Polygon, Arbitrum, and Base
- Backend sends structured prompt to ChainGPT's Web3 LLM requesting machine-parseable JSON with typed severity levels
- Results rendered as color-coded findings with technical descriptions and plain English explanations
- Overall risk level determined dynamically with contextual summary

## Stack

Python · JavaScript · ChainGPT LLM API · Etherscan API V2 · Vercel Serverless Functions · GitHub

## Live Demo

[guardera.net](https://guardera.net)

## Disclaimer

For educational and development purposes only. Not a professional security audit. Always consult a certified auditor before deploying to mainnet.

## Author

Anas Abuqasem — Computer Engineering, Bahçeşehir University
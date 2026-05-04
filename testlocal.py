import requests
import json

API_KEY = "c5a3d924-f68e-4b47-b550-276fbc5a7bc8"

test_contract = """
pragma solidity ^0.8.0;
contract Test {
    mapping(address => uint256) public balances;
    function withdraw(uint256 amount) public {
        require(balances[msg.sender] >= amount);
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success);
        balances[msg.sender] -= amount;
    }
}
"""

response = requests.post(
    "https://api.chaingpt.org/chat/stream",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": "smart_contract_auditor",
        "question": f"Audit the following contract: {test_contract}"
    },
    timeout=30
)

print("Status:", response.status_code)
print("Response:", response.text[:2000])
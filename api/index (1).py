from http.server import BaseHTTPRequestHandler
import json
import requests
import os

CHAINGPT_API_KEY = os.environ.get("CHAINGPT_API_KEY", "YOUR_CHAINGPT_API_KEY")
CHAINGPT_URL = "https://api.chaingpt.org/chat/stream"

AUDIT_PROMPT = """You are a senior smart contract security auditor with expertise in Solidity, EVM exploits, and DeFi vulnerabilities. Your task is to perform a comprehensive security audit of the provided Solidity smart contract.

Analyze the contract for ALL of the following vulnerability classes:
- Reentrancy attacks (single and cross-function)
- Access control flaws (missing onlyOwner, missing role checks)
- Integer overflow and underflow
- Unchecked external calls and return values
- Front-running and transaction ordering vulnerabilities
- Denial of service vectors (gas limit, unexpected revert)
- Timestamp manipulation and block dependency
- Selfdestruct misuse and force-feeding Ether
- Uninitialized storage pointers
- Locked Ether (no withdrawal function)
- Flash loan attack vectors
- Logic errors and incorrect state transitions
- Gas inefficiencies
- Missing events and incomplete logging
- Visibility and access specifier issues

Return ONLY a valid JSON array with zero additional text, zero markdown, zero code blocks, zero explanation before or after. Just the raw JSON array starting with [ and ending with ].

Each object in the array must have exactly these four fields:
- "severity": must be exactly one of these strings: "critical", "high", "medium", "low", "info"
- "title": short name of the specific vulnerability found (max 6 words)
- "description": 1-2 sentences explaining the exact technical issue found in THIS contract
- "fix": 1-2 sentences with the specific recommended fix for THIS contract

Severity classification rules — follow strictly:
- "critical": direct path to total loss of funds, contract destruction, or complete takeover
- "high": serious vulnerability exploitable under realistic conditions with significant impact
- "medium": vulnerability that affects functionality or introduces moderate exploitable risk
- "low": best practice violation or minor issue with minimal security impact
- "info": informational observation with no direct security risk

If no vulnerabilities are found, return an empty array: []
Do not invent vulnerabilities that are not present. Only report what you actually find.

Contract to audit:
"""

def audit_contract(solidity_code):
    headers = {
        "Authorization": f"Bearer {CHAINGPT_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "smart_contract_auditor",
        "question": AUDIT_PROMPT + solidity_code
    }
    try:
        response = requests.post(CHAINGPT_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        raw = response.text.strip()
        start = raw.find('[')
        end = raw.rfind(']')
        if start != -1 and end != -1:
            findings = json.loads(raw[start:end+1])
            return {"success": True, "data": {"findings": findings}}
        else:
            return {"success": True, "data": {"result": raw}}
    except json.JSONDecodeError:
        return {"success": True, "data": {"result": raw}}
    except requests.exceptions.HTTPError as e:
        return {"success": False, "error": f"API error {response.status_code}: {response.text}"}
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timed out. Please try again."}
    except Exception as e:
        return {"success": False, "error": str(e)}

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        try:
            data = json.loads(body)
            code = data.get("code", "").strip()
            if not code:
                self._send_json(400, {"success": False, "error": "No code provided."})
                return
            if len(code) < 20:
                self._send_json(400, {"success": False, "error": "Code too short."})
                return
            result = audit_contract(code)
            self._send_json(200 if result["success"] else 500, result)
        except json.JSONDecodeError:
            self._send_json(400, {"success": False, "error": "Invalid request format."})

    def _send_json(self, status_code, data):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass

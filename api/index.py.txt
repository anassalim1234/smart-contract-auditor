from http.server import BaseHTTPRequestHandler
import json
import requests
import os

CHAINGPT_API_KEY = os.environ.get("CHAINGPT_API_KEY", "YOUR_CHAINGPT_API_KEY")

def audit_contract(solidity_code):
    headers = {
        "Authorization": f"Bearer {CHAINGPT_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "smart_contract_auditor",
        "question": f"Audit the following contract: {solidity_code}"
    }
    try:
        response = requests.post(
            "https://api.chaingpt.org/chat/stream",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        return {"success": True, "data": {"result": response.text}}
    except requests.exceptions.HTTPError as e:
        return {"success": False, "error": f"API error {response.status_code}: {response.text}"}
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
            result = audit_contract(code)
            status = 200 if result["success"] else 500
            self._send_json(status, result)
        except json.JSONDecodeError:
            self._send_json(400, {"success": False, "error": "Invalid request format."})

    def _send_json(self, status_code, data):
        response_body = json.dumps(data).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(response_body)))
        self.end_headers()
        self.wfile.write(response_body)

    def log_message(self, format, *args):
        pass
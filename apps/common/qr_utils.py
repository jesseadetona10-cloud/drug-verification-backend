import qrcode
import io
import base64
import json
import hashlib
import hmac
import os

def generate_batch_qr(batch_number, drug_id, manufacturer_id, secret_key=None):
    if secret_key is None:
        secret_key = os.environ.get("QR_SECRET_KEY", "dev-secret-key")
    payload = {"b": batch_number, "d": str(drug_id), "m": str(manufacturer_id), "v": "1"}
    data_string = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    signature = hmac.new(secret_key.encode(), data_string.encode(), hashlib.sha256).hexdigest()[:16]
    payload["h"] = signature
    qr = qrcode.QRCode(version=3, box_size=10, border=4)
    qr.add_data(json.dumps(payload))
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return {"qr_data": payload, "qr_image_base64": img_str, "batch_number": batch_number}

def verify_qr_code(scanned_data, secret_key=None):
    try:
        data = json.loads(scanned_data)
        if "b" not in data or "d" not in data:
            return {"valid": False, "error": "Missing required fields"}
        if "h" in data:
            if secret_key is None:
                secret_key = os.environ.get("QR_SECRET_KEY", "dev-secret-key")
            verify_payload = {k: v for k, v in data.items() if k != "h"}
            data_string = json.dumps(verify_payload, sort_keys=True, separators=(",", ":"))
            expected_sig = hmac.new(secret_key.encode(), data_string.encode(), hashlib.sha256).hexdigest()[:16]
            if not hmac.compare_digest(data["h"], expected_sig):
                return {"valid": False, "error": "Invalid signature"}
        return {"valid": True, "batch_number": data.get("b"), "drug_id": data.get("d"), "manufacturer_id": data.get("m")}
    except Exception as e:
        return {"valid": False, "error": str(e)}

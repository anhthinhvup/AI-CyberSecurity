from flask import Flask, request, jsonify, send_file, make_response
from flask_cors import CORS
import sys
import os
import threading
import time
import io
from datetime import datetime

# Import AI Attacker
sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'attacks'))
from ai_attacker import AIAttacker

app = Flask(__name__)
CORS(app)  # Cho phép frontend React truy cập API

# Đơn giản hóa: log sẽ lưu tạm trong biến toàn cục
attack_log = []
attack_result = None
attack_running = False

def run_attack(target, mode):
    global attack_log, attack_result, attack_running
    attack_log = [f"[THÔNG TIN] Khởi tạo tác nhân...", f"[THÔNG TIN] Mục tiêu: {target}", f"[THÔNG TIN] Chế độ: {mode}"]
    attack_running = True
    try:
        url = target
        if not url.startswith("http"):
            url = f"http://{url}"
        attacker = AIAttacker(url)
        attack_log.append("[THÔNG TIN] Bắt đầu trinh sát...")
        result = attacker.start_attack()
        attack_log.append(f"[THÀNH CÔNG] Phát hiện {result['vulnerabilities_found']} lỗ hổng.")
        attack_log.append(f"[THÀNH CÔNG] Khai thác thành công {result['successful_attacks']} lỗ hổng.")
        for vuln in result['vulnerabilities']:
            attack_log.append(f"[LỖ HỔNG] {vuln['type']}: {vuln['description']}")
        for exploit in result['successful_exploits']:
            attack_log.append(f"[KHAI THÁC] {exploit['type']}: {exploit.get('result','')}")
        attack_result = result
    except Exception as e:
        attack_log.append(f"[LỖI] {str(e)}")
        attack_result = {"error": str(e)}
    attack_running = False

@app.route('/attack', methods=['POST'])
def attack():
    global attack_log, attack_result, attack_running
    data = request.get_json()
    target = data.get('target')
    mode = data.get('mode', 'training')
    # Chạy attack trong thread để không block API
    t = threading.Thread(target=run_attack, args=(target, mode))
    t.start()
    return jsonify({"status": "started"})

@app.route('/attack_log', methods=['GET'])
def get_attack_log():
    global attack_log, attack_running
    return jsonify({"log": attack_log, "running": attack_running})

@app.route('/attack_result', methods=['GET'])
def get_attack_result():
    global attack_result, attack_running
    return jsonify({"result": attack_result, "running": attack_running})

@app.route('/custom_xss_exploit', methods=['POST'])
def custom_xss_exploit():
    global attack_log, attack_result, attack_running
    data = request.get_json()
    custom_content = data.get('content')
    url = attack_result['target'] if attack_result and 'target' in attack_result else None
    if not url:
        return jsonify({"error": "Chưa có phiên tấn công nào."}), 400
    attacker = AIAttacker(url)
    # Lấy lại thông tin XSS đã phát hiện (nếu có)
    attacker.detected_xss = None
    if attack_result and 'vulnerabilities' in attack_result:
        for vuln in attack_result['vulnerabilities']:
            if vuln['type'] == 'xss':
                attacker.detected_xss = vuln
                break
    result = attacker.custom_xss_exploit(custom_content)
    return jsonify(result)

@app.route('/export_report', methods=['GET'])
def export_report():
    global attack_result
    if not attack_result:
        return jsonify({"error": "Chưa có kết quả tấn công để xuất báo cáo."}), 400
    # Sinh nội dung AsciiDoc
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    adoc = []
    adoc.append("""= Báo cáo kiểm thử bảo mật tự động
:toc:
:icons: font
:source-highlighter: coderay
:sectnums:
""")
    adoc.append(f"== Thông tin chung\n*Thời gian:* {now}\n*Target:* {attack_result.get('target','N/A')}")
    adoc.append(f"== Tổng quan\n* Số lỗ hổng phát hiện: {attack_result.get('vulnerabilities_found',0)}\n* Số khai thác thành công: {attack_result.get('successful_attacks',0)}")
    adoc.append("== Bảng kết quả kiểm thử\n|===\n| Loại | Mô tả | Chi tiết")
    for vuln in attack_result.get('vulnerabilities', []):
        adoc.append(f"|[LỖ HỔNG] {vuln.get('type','')} | {vuln.get('description','')} | {vuln.get('details','') if 'details' in vuln else '-'}")
    for exploit in attack_result.get('successful_exploits', []):
        adoc.append(f"|[KHAI THÁC] {exploit.get('type','')} | {exploit.get('result','')} | {exploit.get('details','') if 'details' in exploit else '-'}")
    adoc.append("|===")
    if 'redteam_kill_chain' in attack_result and attack_result['redteam_kill_chain']:
        adoc.append("== Kill Chain (MITRE ATT&CK)")
        for phase in attack_result['redteam_kill_chain']:
            adoc.append(f"* {phase['phase']} ({phase['mitre']}): {phase['result']}")
    if 'summary' in attack_result:
        adoc.append("== Tổng kết\n")
        for s in attack_result['summary']:
            adoc.append(f"* {s}")
    adoc.append("== Công nghệ & Công cụ\n- AI Attacker Python\n- Flask API\n- AsciiDoc\n- Requests, BeautifulSoup, ...\n")
    adoc.append("== Thách thức & Cải tiến\n- Tự động hóa kiểm thử\n- Gom nhóm log, tối ưu payload\n- Báo cáo chuyên nghiệp\n")
    adoc_content = '\n'.join(adoc)
    # Trả về file AsciiDoc
    buf = io.BytesIO()
    buf.write(adoc_content.encode('utf-8'))
    buf.seek(0)
    response = make_response(send_file(buf, mimetype='text/asciidoc', as_attachment=True, download_name='bao_cao_ai_attacker.adoc'))
    response.headers['Content-Disposition'] = 'attachment; filename=bao_cao_ai_attacker.adoc'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True) 
AI-driven Autonomous Cyber Attacker
(Hệ thống tấn công mạng tự động dựa trên trí tuệ nhân tạo)
Một hệ thống thông minh sử dụng Học tăng cường (Reinforcement Learning) để tự động hóa việc mô phỏng tấn công mạng và kiểm thử xâm nhập (penetration testing).
# Tổng quan dự án
Hệ thống này triển khai một tác tử AI (AI agent) có khả năng tự động thực hiện các cuộc tấn công mạng thông qua việc:
Thực hiện do thám và thu thập thông tin
Phân tích hệ thống mục tiêu
Lựa chọn và triển khai kỹ thuật tấn công phù hợp
Học hỏi từ kết quả tấn công để cải thiện hiệu quả trong tương lai
# Kiến trúc hệ thống
-Hệ thống tuân theo khung Cyber Kill Chain và áp dụng các chiến thuật MITRE ATT&CK:
-Mô-đun Do thám (Reconnaissance Module)
-Quét cổng (port scanning)
-Liệt kê dịch vụ (service enumeration)
-Đánh giá lỗ hổng (vulnerability assessment)
-Bộ máy ra quyết định AI (AI Decision Engine)
-Thuật toán Học tăng cường (DQN / PPO / A3C)
-Biểu diễn trạng thái hệ thống mục tiêu
-Không gian hành động (action space) gồm các kỹ thuật tấn công khả thi
-Hàm thưởng dựa trên mức độ thành công của tấn công
-Mô-đun Thực thi tấn công (Attack Execution Module)
-Tự động khai thác lỗ hổng (exploit)
-Thực hiện các hành động hậu khai thác (post-exploitation)
-Ghi nhật ký và phân tích kết quả
# Cài đặt
Tạo môi trường ảo:
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
Cài đặt thư viện phụ thuộc:
pip install -r requirements.txt
Cấu hình biến môi trường:
cp .env.example .env
# Mở file .env và chỉnh sửa thông tin cấu hình của bạn
# Sử dụng
Khởi chạy tác tử AI (chế độ huấn luyện):
python src/main.py --target <target_ip> --mode training
Chạy ở chế độ đánh giá:
python src/main.py --target <target_ip> --mode evaluation
# Cấu trúc dự án
.
├── src/
│   ├── agent/           # Triển khai tác tử AI
│   ├── attacks/         # Các mô-đun tấn công
│   ├── reconnaissance/  # Mô-đun thu thập thông tin
│   ├── utils/            # Hàm tiện ích
│   └── main.py           # Điểm vào chính của hệ thống
├── config/               # File cấu hình
├── models/                # Mô hình AI đã huấn luyện
├── logs/                  # Nhật ký huấn luyện và tấn công
├── tests/                 # Unit test
├── requirements.txt       # Thư viện cần thiết
└── README.md               # Tài liệu mô tả dự án

⚠️ Lưu ý bảo mật
Dự án này chỉ phục vụ mục đích giáo dục và nghiên cứu. Luôn đảm bảo:
Có sự ủy quyền hợp pháp trước khi kiểm thử
Chỉ sử dụng trong môi trường kiểm soát
Tuân thủ quy trình tiết lộ có trách nhiệm
Tuân thủ luật pháp và quy định hiện hành
📜 Giấy phép
Giấy phép MIT — Xem chi tiết trong file LICENSE.
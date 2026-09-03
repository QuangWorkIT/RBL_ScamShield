# GAP Analysis — Sự Đứt Gãy Giữa Mô Hình Học Máy Tĩnh & Mạng Lưới Trí Tuệ Đe Dọa Cộng Đồng Có Kiểm Duyệt (Community Threat Intelligence)

**Thành viên:** Nguyễn Quốc Huy (`quoc_huy`)  
**GAP type:** GAP-T (Technological) / GAP-S (System & Operational Architecture)  
**Ngày:** 2026-08-31  
**Evidence table nguồn:** `team-synthesis/evidence-table-merged.md`  
**N =** 10 bài báo core (`M029`, `M030`, `M031`, `M032`, `M033`, `M034`, `M035`, `M036`, `M037`, `M038`)

---

## 1. Mô tả GAP

Hiện nay, 100% các nghiên cứu phát hiện lừa đảo (phishing/smishing) chỉ dừng lại ở việc huấn luyện và đánh giá các mô hình AI/Transformer tĩnh (*Static Offline Classifiers*) trên các tập dữ liệu đóng trong phòng thí nghiệm. Hoàn toàn thiếu vắng một **Cơ chế Vòng lặp Trí tuệ Đe dọa Đóng kín (Closed-Loop Threat Intelligence Framework)** kết hợp giữa suy luận AI và **Hệ thống Blacklist Cộng đồng có kiểm duyệt đa tầng (Moderated Crowdsourced Blacklist)** nhằm thích ứng theo thời gian thực trước các chiến dịch lừa đảo zero-day mới bùng phát (như mạo danh app VNeID, hoàn tiền điện lực, bẫy trúng thưởng).

**Bằng chứng từ evidence table:**
*   **Cột Hạn chế (Limitations & Threats to Validity):** 
    *   Bài báo `M035` *(PEEK Framework, 2024)* và `M036` *(Genshin, 2024)* thừa nhận: *"Các bộ phân loại tĩnh (Static Analyzers) nhanh chóng suy giảm hiệu năng theo thời gian trước các thủ thuật phishing tiến hóa liên tục, đòi hỏi phải được bổ sung tri thức đe dọa mới liên tục"*.
    *   Bài báo `M030` *(Agentic Distillation, 2026)* chỉ ra: *"Hiệu năng của mô hình bị giới hạn bởi tri thức đóng của tập dữ liệu huấn luyện; các đòn tấn công mới xuất hiện ngoài thực tế (Emerging Attack Patterns) sẽ bị bỏ sót hoàn toàn"*.
    *   Bài báo `M033` *(Oyeyemi & Ojo, 2024)* ghi nhận: *"Bộ lọc tĩnh không thể thích ứng với các thủ thuật lẩn tránh ngày càng tinh vi của mạng lưới tội phạm"*.
*   **Cột Phương pháp luận & Khả năng giải thích (Tool & Explainability):** 
    *   Các công trình `M034` và `M037` *(Uddin et al., 2024)* tập trung vào mô hình giải thích (LIME, SHAP, LITA) để tăng độ minh bạch, nhưng chỉ phân tích trên từng mẫu đơn lẻ mà không có cơ chế đưa các thực thể đe dọa (Số điện thoại, STK ngân hàng, URL) vào cơ sở dữ liệu cảnh báo dùng chung cho toàn xã hội.
*   **Khoảng trống xuất hiện:** Không có bất kỳ công trình nào trong 10 paper xây dựng cơ chế cho phép người dùng báo cáo các thực thể lừa đảo mới, lọc trùng báo cáo và kiểm duyệt (Moderator Workflow) để cập nhật tức thì vào bộ lọc thời gian thực.

---

## 2. Kiểm tra phản chứng

| Paper | Đã làm GAP này không? | Chi tiết |
| :--- | :--- | :--- |
| **M029** *(Zhou et al., 2026, FraudSMSWalker)* | Không | Đánh giá Agentic LLMs phát hiện lừa đảo từ SMS dẫn sang Webpage trên benchmark đóng. Không xây dựng cơ chế Blacklist cộng đồng hay quy trình tiếp nhận cảnh báo thời gian thực từ người dùng. |
| **M030** *(ElZemity et al., 2026)* | Không | Sử dụng Agentic Knowledge Distillation để chưng cất tri thức từ LLM sang SLM (Qwen2.5-0.5B). Mô hình hoàn toàn tĩnh sau khi train, không có cơ chế cập nhật dữ liệu đe dọa động từ cộng đồng. |
| **M031** *(Ahmadi et al., 2025)* | Không | Phân loại SMS spam bằng Machine Learning và TF-IDF trên 1 tập dữ liệu Kaggle duy nhất. Nghiên cứu mang tính thí nghiệm tĩnh, không có kết nối cơ sở dữ liệu đe dọa trực tiếp. |
| **M032** *(Mahendru & Pandit, 2024, SecureNet)* | Không | So sánh DeBERTa-v3 và GPT-4 trên các tập dữ liệu tĩnh (HuggingFace, Nazario). Chỉ ra điểm yếu nhận diện sai URL lành tính nhưng không đề xuất hệ sinh thái chia sẻ danh sách đen. |
| **M033** *(Oyeyemi & Ojo, 2024)* | Không | Kết hợp Naive Bayes và BERT phân loại spam viễn thông. Đánh giá offline trên tập dữ liệu DSN, không có vòng lặp phản hồi từ người dùng thực tế. |
| **M034** *(Uddin et al., 2024, ExplainableDetector)* | Không | Khảo sát tính giải thích (XAI) bằng LIME và Transformers Interpret trên RoBERTa. Tập trung vào diễn giải trực quan từ ngữ, không xây dựng hạ tầng threat intelligence. |
| **M035** *(Chen et al., 2024, PEEK)* | Không | Đề xuất framework sinh kịch bản phishing tiến hóa bằng Llama 3.1. Tác giả thừa nhận mô hình phòng thủ tĩnh sẽ lạc hậu theo thời gian nhưng chưa tích hợp cơ chế crowdsourced blacklist. |
| **M036** *(Peng et al., 2024, Genshin)* | Không | Xây dựng LLM Defender bảo vệ trước tấn công xáo trộn văn bản. Không có chức năng thu thập và quản trị cơ sở dữ liệu báo cáo lừa đảo từ cộng đồng. |
| **M037** *(Uddin et al., 2024, LITA)* | Không | Đề xuất kiến trúc giải thích lai LITA cho email phishing. Nghiên cứu chỉ dừng lại ở bài toán phân loại email tĩnh. |
| **M038** *(Jamal et al., 2023, IPSDM)* | Không | Tối ưu hóa mô hình phân loại trên tập dữ liệu mất cân bằng. Không giải quyết bài toán cập nhật mối đe dọa zero-day ngoài đời thực. |

**Kết luận:** **GAP 5 ĐƯỢC XÁC NHẬN ✅** (10/10 bài báo đều là nghiên cứu tĩnh trong phòng thí nghiệm, 0 có phản chứng về việc tích hợp mạng lưới Threat Intelligence và Blacklist cộng đồng có kiểm duyệt).

---

### Supplementary Validation (Vì N = 10)

| Lớp | Hành động | Kết quả |
| :--- | :--- | :--- |
| **L1 Targeted search** | Query: `("community blacklist" OR "crowdsourced threat intelligence") AND ("scam detection" OR "smishing") AND ("moderation")` trên Scholar & IEEE (2026-08-31) | **11 kết quả**, 0 phản chứng (các bài báo chỉ nói về honeypot mạng hoặc chia sẻ mã độc malware IoC doanh nghiệp, không có hệ thống blacklist cộng đồng có moderator workflow cho SMS/Scam cá nhân). |
| **L2 Forward snowball** | Dùng `M032` *(SecureNet, IEEE 2024)* và `M035` *(PEEK, 2024)* làm anchor papers, kiểm tra các nghiên cứu trích dẫn mới nhất | **0 GAP / 0 phản chứng** (các bài trích dẫn chỉ mở rộng sang sinh prompt tấn công mới, không xây dựng hạ tầng blacklist cộng đồng). |
| **L3 Survey anchor** | Đối chiếu bài SLR của *Saias (2025, ACM Computing Surveys - M004)* | Khảo sát kết luận: Các mô hình NLP hiện nay thiếu tính kết nối với nguồn cấp dữ liệu đe dọa thực tế (*Live Threat Feeds*) và phụ thuộc hoàn toàn vào tập dữ liệu tĩnh lúc train. |

→ **Kết luận:** **GAP 5 CONFIRMED** qua cả 3 lớp kiểm tra bổ sung.

---

## 3. Feasibility Check

| Tiêu chí | Mức | Ghi chú |
| :--- | :---: | :--- |
| **Dataset** | 🟢 | Dữ liệu số điện thoại, số tài khoản, link lừa đảo thu thập trực tiếp từ cổng cảnh báo của Cục An toàn thông tin (NCSC), Chống Lừa Đảo (ChongLuaDaoV2) và form đóng góp cộng đồng. |
| **API / Tool** | 🟢 | Sử dụng Google Safe Browsing API (miễn phí), VirusTotal API (Free Tier), và cơ sở dữ liệu quan hệ PostgreSQL / MongoDB nội bộ. |
| **Tính toán** | 🟢 | Hệ thống cơ sở dữ liệu Blacklist và thuật toán Gom cụm trùng lặp (Deduplication Clustering) chạy mượt mà trên máy chủ Backend tiêu chuẩn (CPU/RAM cơ bản). |
| **Ground truth** | 🟢 | Xây dựng quy trình kiểm duyệt (Moderator Review Queue) đa tầng: gán nhãn trạng thái rõ ràng (`PENDING`, `VERIFIED_SCAM`, `REJECTED_SPAM`). |
| **Code base** | 🟢 | Xây dựng trên nền tảng FastAPI (Backend) + ReactJS (Frontend) + SQLAlchemy / Tortoise ORM, dễ dàng mở rộng và bảo trì. |
| **Kỹ năng** | 🟢 | Thành thạo kiến trúc Web Full-stack, thiết kế cơ sở dữ liệu quan hệ, phân quyền người dùng (Role-Based Access Control) và tích hợp API bản đồ nhiệt (Leaflet / Chart.js). |
| **Thời gian** | 🟢 | Thiết kế cơ sở dữ liệu, API tra cứu Blacklist và trang kiểm duyệt Moderator hoàn thành trong 2 tuần. |

**Kết quả:** 0 🔴, 0 🟡, 7 🟢 → **Kết luận:** **TUYỆT ĐỐI AN TOÀN (Safe to Proceed)**.

### Kế hoạch xử lý & Downscope (nếu có rủi ro)
- Để ngăn chặn hành vi báo cáo giả mạo nhằm hạ uy tín người khác (Defamation/Spam Reports), hệ thống áp dụng cơ chế **Chấm điểm Uy tín Báo cáo (Reputation Scoring)**: một số điện thoại/STK chỉ được đưa vào danh sách đen công khai khi có $\ge 3$ báo cáo độc lập trùng khớp hoặc được phê duyệt bởi tài khoản Kiểm duyệt viên (Moderator).

---

## 4. Phát biểu GAP chính thức

> *"Chưa có nghiên cứu nào tích hợp mô hình phân loại học máy với một Hệ sinh thái Trí tuệ Đe dọa Cộng đồng có Kiểm duyệt Đa tầng (Moderated Crowdsourced Threat Intelligence System) kết hợp tính năng giải thích minh bạch (XAI) nhằm giải quyết triệt để sự đứt gãy giữa mô hình học máy tĩnh và các chiến dịch lừa đảo zero-day mới bùng phát ngoài thực tế."*

---

## 5. Đề xuất sơ bộ cho nhóm (chuẩn bị họp RBL-3)

*   **Dataset khả thi:** 
    *   Cơ sở dữ liệu Danh bạ đen lừa đảo (`ScamShield-Community-Blacklist`) chứa các thực thể có cấu trúc: Số điện thoại, Số tài khoản ngân hàng, Tên chủ tài khoản, URL độc hại, Loại thủ đoạn lừa đảo và Bằng chứng hình ảnh kèm theo.
*   **Metric đề xuất:** 
    *   *Độ chính xác cảnh báo:* Precision, False Report Rejection Rate (% loại bỏ báo cáo giả).
    *   *Hiệu năng hệ thống:* Thời gian phản hồi tra cứu danh sách đen ($< 50$ms), Tỷ lệ phát hiện lừa đảo zero-day trước khi mô hình AI được huấn luyện lại.
*   **LLM / Tool đề xuất:** 
    *   *Công cụ XAI:* `SHAP` / `LIME` kết hợp phân tích lý do bằng `Gemini-2.0-Flash` (từ `M034`, `M036`, `M037`).
    *   *Hạ tầng Blacklist:* PostgreSQL Database + Redis Cache + Hàng đợi kiểm duyệt Moderator Queue + Bản đồ nhiệt rủi ro (Threat Heatmap).
*   **Baseline đề xuất:** So sánh trực tiếp giữa:
    1.  *Mô hình AI tĩnh độc lập (M031, M033):* Hoàn toàn bỏ lọt các số tài khoản/chiêu trò lừa đảo mới xuất hiện trong ngày.
    2.  *Hệ thống ScamShield tích hợp Blacklist:* Chặn đứng ngay lập tức các mối đe dọa mới nhờ cơ sở dữ liệu cộng đồng thời gian thực mà không cần chờ huấn luyện lại mô hình.

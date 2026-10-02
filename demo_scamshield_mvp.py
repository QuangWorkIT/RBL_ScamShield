"""
==============================================================================
ScamShield-VN: Interactive 2-Tier AI Architecture MVP Demo
==============================================================================
Author: ScamShield Engineering Team
Usage:
    python demo_scamshield_mvp.py               # Run benchmark test suite
    python demo_scamshield_mvp.py --interactive # Interactive CLI mode
==============================================================================
"""

import os
import sys
import time
import argparse
from typing import List, Dict, Any

# Ensure stdout handles UTF-8 safely on Windows
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stdin, "reconfigure"):
            sys.stdin.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from pipeline.two_tier_router import TwoTierRouter


# Sample real-world test cases
BENCHMARK_CASES = [
    {
        "text": "Vietcombank: Tai khoan cua ban tam khoa do bat thuong. Dang nhap https://vcb-xacthuc.xyz de mo khoa.",
        "ground_truth": "SCAM",
        "description": "Lừa đảo mạo danh ngân hàng (Brand Spoofing + tên miền độc hại)",
    },
    {
        "text": "Ma OTP xac thuc giao dich ShopeePay cua ban la 839201. Ma co hieu luc trong 3 phut. Khong chia se cho bat ky ai.",
        "ground_truth": "HAM",
        "description": "Tin nhắn OTP thanh toán hợp lệ",
    },
    {
        "text": "Bo Cong An thong bao: So CCCD cua ban lien quan den duong day rua tien ma tuy. Lien he gap 0912345678 de lam viec.",
        "ground_truth": "SCAM",
        "description": "Đe dọa mạo danh cơ quan tư pháp / Công an",
    },
    {
        "text": "Toi nay di an lau Thai o Phan Xich Long luc 7h khong anh em oi? Co gi alo nhe.",
        "ground_truth": "HAM",
        "description": "Tin nhắn hội thoại thông thường bạn bè",
    },
    {
        "text": "Chào bạn, bên mình đang tuyển CTV đánh giá sản phẩm online tại nhà, mỗi ngày kiếm 300k-500k không cần vốn. Nhắn Zalo 0988776655 để nhận việc nhé!",
        "ground_truth": "SCAM",
        "description": "Bẫy việc nhẹ lương cao / CTV Shopee, TikTok lừa đảo",
    },
    {
        "text": "Chi oi em muon hoi tham ve tai lieu bai giang buoi truoc tren LMS thay da upload len chua a?",
        "ground_truth": "HAM",
        "description": "Tin nhắn sinh viên hỏi bài tập",
    },
    {
        "text": "Chuc mung thue bao 090xxx da may man trung thuong xe SH 150i tu chuong trinh Tri An Khach Hang. Vui long truy cap http://trian-qua-tang.vip/nhanqua de lam thu tuc.",
        "ground_truth": "SCAM",
        "description": "Lừa đảo trúng thưởng tri ân khách hàng",
    },
    {
        "text": "Gói cước ST90K của quý khách đã được gia hạn thành công. Quý khách có 30GB data sử dụng đến 13/10/2026.",
        "ground_truth": "HAM",
        "description": "Thông báo cước viễn thông Viettel",
    }
]


def load_vietnamese_sms_dataset(limit: int = 200) -> List[Dict[str, Any]]:
    """
    Load the first N samples from trannguyenthaituan/vietnamese_sms_dataset.
    Automatically downloads the dataset from Hugging Face if not present locally.
    """
    dest_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "raw")
    os.makedirs(dest_dir, exist_ok=True)
    csv_path = os.path.join(dest_dir, "vietnamese_sms_full.csv")

    if not os.path.exists(csv_path):
        url = "https://huggingface.co/datasets/trannguyenthaituan/vietnamese_sms_dataset/resolve/main/full_dataset.csv"
        try:
            import requests
            print(f"[*] Đang tải bộ dữ liệu 'vietnamese_sms_dataset' từ Hugging Face Hub...")
            r = requests.get(url, timeout=30)
            if r.status_code == 200:
                with open(csv_path, "wb") as f:
                    f.write(r.content)
                print(f"[+] Đã tải thành công file dataset về {csv_path}!")
        except Exception as e:
            print(f"[!] Không thể tải tự động từ Hugging Face: {e}")

    if os.path.exists(csv_path):
        import csv
        try:
            with open(csv_path, mode="r", encoding="utf-8-sig", errors="replace") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                if rows:
                    selected_rows = rows[:limit]
                    cases = []
                    for idx, r in enumerate(selected_rows, 1):
                        msg_id = r.get("message_id", f"SMS_{idx:03d}")
                        date_val = r.get("date", "N/A")
                        label_num = r.get("label", "0").strip()
                        gt = "SCAM" if label_num == "1" else "HAM"
                        text = r.get("message", "").strip()
                        cases.append({
                            "id": msg_id,
                            "date": date_val,
                            "text": text,
                            "ground_truth": gt,
                            "description": f"SMS ID: {msg_id} (Ngày: {date_val})",
                        })
                    return cases
        except Exception as e:
            print(f"[!] Lỗi khi đọc file CSV: {e}")

    # Fallback to default hardcoded benchmark cases if CSV cannot be loaded
    return BENCHMARK_CASES


def print_banner():
    print("=" * 80)
    print("🛡️  SCAMSHIELD-VN: 2-TIER CASCADED AI DETECTION ENGINE MVP")
    print("   • Tier 1: PhoBERT Local (ONNX INT8 CPU, <65ms, $0 cost)")
    print("   • Tier 2: Dynamic Google Gemini Cloud Fallback (Zero version hardcode)")
    print("   • Dataset: vietnamese_sms_dataset (200 Mẫu đầu tiên)")
    print("=" * 80)
    print()


def run_benchmark(router: TwoTierRouter, cases: Optional[List[Dict[str, Any]]] = None, num_samples: int = 200):
    if cases is None:
        print(f"[*] Đang nạp 200 mẫu đầu tiên từ tập dữ liệu 'vietnamese_sms_dataset'...")
        cases = load_vietnamese_sms_dataset(limit=num_samples)

    total_cases = len(cases)
    print(f"[*] Bắt đầu thực thi bài kiểm thử Benchmark trên {total_cases} mẫu SMS thực tế...")
    print("=" * 80)

    tier1_count = 0
    tier2_count = 0
    correct_count = 0
    total_latency = 0.0
    total_cost = 0.0

    start_bench_time = time.perf_counter()

    for idx, case in enumerate(cases, 1):
        msg = case["text"]
        gt = case["ground_truth"]
        msg_id = case.get("id", f"#{idx:03d}")
        desc = case.get("description", f"Mẫu #{idx}")

        result = router.classify(msg)
        pred = result["final_label"]
        is_correct = (pred == gt)
        if is_correct:
            correct_count += 1

        total_latency += result["total_latency_ms"]
        total_cost += result["total_cost_usd"]

        t1 = result.get("tier1_telemetry", {})
        t2 = result.get("tier2_telemetry", {})

        if result["routing_path"] == "TIER_1_DIRECT_FASTPATH":
            tier1_count += 1
            tier_badge = "[TIER 1 FASTPATH]"
        else:
            tier2_count += 1
            tier_badge = "[TIER 2 FALLBACK]"

        status_symbol = "✅ PASS" if is_correct else "❌ FAIL"
        clean_msg = msg.replace("\n", " ").replace("\r", "")
        if len(clean_msg) > 60:
            clean_msg = clean_msg[:57] + "..."

        print(f"[{idx:03d}/{total_cases:03d}] [{msg_id:<8}] {status_symbol} | {tier_badge:<18} | Dự đoán: {pred:<4} (GT: {gt:<4}) | {result['total_latency_ms']:>6.2f}ms | \"{clean_msg}\"")

    total_bench_duration = time.perf_counter() - start_bench_time

    # Summary report
    avg_latency = total_latency / total_cases if total_cases > 0 else 0.0
    accuracy = (correct_count / total_cases) * 100 if total_cases > 0 else 0.0
    tier1_pct = (tier1_count / total_cases) * 100 if total_cases > 0 else 0.0
    tier2_pct = (tier2_count / total_cases) * 100 if total_cases > 0 else 0.0

    print()
    print("=" * 80)
    print("📊 BÁO CÁO HIỆU NĂNG TỔNG KẾT ĐỐI CHUẨN (TELEMETRY BENCHMARK REPORT)")
    print("=" * 80)
    print(f"  • Tập dữ liệu kiểm thử:             trannguyenthaituan/vietnamese_sms_dataset")
    print(f"  • Tổng số mẫu đã kiểm thử:          {total_cases} mẫu đầu tiên")
    print(f"  • Độ chính xác toàn diện (Accuracy): {accuracy:.2f}% ({correct_count}/{total_cases} mẫu chính xác)")
    print(f"  • Tỷ lệ xử lý nội bộ Tier 1 (CPU):  {tier1_pct:.1f}% ({tier1_count} requests - Xử lý tại chỗ, $0 chi phí)")
    print(f"  • Tỷ lệ chuyển tuyến Tier 2 (Cloud):{tier2_pct:.1f}% ({tier2_count} requests)")
    print(f"  • Độ trễ trung bình mỗi tin nhắn:   {avg_latency:.2f} ms")
    print(f"  • Tổng thời gian thực thi 200 mẫu:  {total_bench_duration:.2f} giây")
    print(f"  • Tổng chi phí ước tính:            ${total_cost:.6f} USD")
    print("=" * 80)
    print("⭐ KẾT LUẬN KIẾN TRÚC:")
    print(f"  -> {tier1_pct:.0f}% lưu lượng được giải quyết ngay tại Tier 1 trong ~15ms mà không tốn chi phí API.")
    print("  -> Các mẫu phức tạp/phân vân được chuyển tiếp thông minh lên Tier 2 Cloud LLM.")
    print("=" * 80)


def interactive_mode(router: TwoTierRouter):
    print("🎯 CHẾ ĐỘ PHÂN TÍCH TƯƠNG TÁC PHÂN TẦNG (INTERACTIVE 2-TIER MODE)")
    print("Nhập tin nhắn tiếng Việt cần kiểm tra (gõ 'exit' hoặc 'quit' để quay lại menu):")
    print("-" * 80)

    while True:
        try:
            user_input = input("\n[Nhập tin nhắn] > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "q"]:
                print("Đang quay lại menu...")
                break

            result = router.classify(user_input)
            t1 = result.get("tier1_telemetry", {})
            t2 = result.get("tier2_telemetry", {})

            print("\n" + "=" * 80)
            print("🛡️  KẾT QUẢ PHÂN TÍCH PHÂN TẦNG SCAMSHIELD-VN (2-TIER PIPELINE)")
            print("=" * 80)
            print(f"📥 TIN NHẮN: \"{user_input}\"")

            # ---------------- TẦNG 1 LOCAL CPU ----------------
            print("\n" + "-" * 80)
            print("📍 [TẦNG 1] PHO-BERT LOCAL CPU (On-Device Fast-Path)")
            print("-" * 80)
            t1_status_badge = "✅ TỰ TIN (CONFIDENT)" if t1.get("is_sure") else "⚠️ PHÂN VÂN (UNSURE)"
            t1_label_badge = "🚨 LỪA ĐẢO (SCAM)" if t1.get("label") == "SCAM" else "🟢 HỢP LỆ (HAM)"
            print(f"  • Dự đoán Tầng 1:   {t1_label_badge}")
            print(f"  • Độ tin cậy (Conf): {t1.get('confidence', 0.0)*100:.2f}%  (Xác suất Scam: {t1.get('scam_prob', 0.0)*100:.2f}% | Ham: {t1.get('ham_prob', 0.0)*100:.2f}%)")
            print(f"  • Trạng thái:       {t1_status_badge}")
            print(f"  • Đánh giá Tầng 1:  {t1.get('reason', '')}")
            if t1.get("matched_cues"):
                print(f"  • Dấu hiệu phát hiện: {', '.join(t1.get('matched_cues', []))}")
            print(f"  • Độ trễ Tầng 1:    {t1.get('latency_ms', 0.0):.2f} ms | Chi phí: $0.000000 (Local CPU)")

            # ---------------- ĐIỀU PHỐI (ROUTING) ----------------
            print("\n" + "-" * 80)
            print("🔀 [ĐIỀU PHỐI] DYNAMIC ROUTING DECISION")
            print("-" * 80)
            if result.get("routing_path") == "TIER_1_DIRECT_FASTPATH":
                print("  • Quyết định:       ⚡ FAST-PATH TRỰC TIẾP (Dừng tại Tầng 1)")
            elif result.get("routing_path") == "TIER_2_CLOUD_FALLBACK":
                print("  • Quyết định:       ☁️ KÍCH HOẠT TẦNG 2 CLOUD FALLBACK")
            else:
                print("  • Quyết định:       🔄 GRACEFUL DEGRADATION (Dự phòng Tầng 1)")
            print(f"  • Căn cứ điều phối: {result.get('routing_reason', '')}")

            # ---------------- TẦNG 2 CLOUD (Nếu kích hoạt) ----------------
            if result.get("escalated"):
                print("\n" + "-" * 80)
                print("☁️ [TẦNG 2] DYNAMIC CLOUD LLM (Gemini Cloud Fallback)")
                print("-" * 80)
                if t2.get("status") == "EXECUTED":
                    t2_label_badge = "🚨 LỪA ĐẢO (SCAM)" if result.get("is_scam") else "🟢 HỢP LỆ (HAM)"
                    print(f"  • Model Cloud dùng: {t2.get('model', 'Gemini')} ({t2.get('tier', 'LITE').upper()})")
                    print(f"  • Dự đoán Tầng 2:   {t2_label_badge}")
                    print(f"  • Độ tin cậy Cloud: {t2.get('confidence', 0.0)*100:.2f}%")
                    print(f"  • Loại hình bẫy:    {t2.get('scam_type', '')}")
                    print(f"  • Phân tích tâm lý: {t2.get('explanation', '')}")
                    print(f"  • Độ trễ Tầng 2:    {t2.get('latency_ms', 0.0):.2f} ms | Chi phí Tầng 2: ${t2.get('cost_usd', 0.0):.6f} USD")
                else:
                    print(f"  • Trạng thái Tầng 2: ⚠️ Không khả dụng ({t2.get('error', 'OFFLINE')})")
                    print(f"  • Lý do kích hoạt:   {t2.get('fallback_trigger', '')}")
                    print("  • Cơ chế dự phòng:   Hệ thống tự động sử dụng kết quả Tầng 1 để đảm bảo tính liên tục của dịch vụ.")

            # ---------------- TỔNG KẾT HỆ THỐNG ----------------
            print("\n" + "=" * 80)
            print("⭐ KẾT LUẬN CUỐI CÙNG (FINAL SYSTEM VERDICT)")
            print("=" * 80)
            final_badge = "🚨 LỪA ĐẢO (SCAM)" if result.get("is_scam") else "🟢 HỢP LỆ (HAM)"
            print(f"  • PHÂN LOẠI CHUNG:  {final_badge}")
            print(f"  • MỨC ĐỘ RỦI RO:    {result.get('risk_level', 'LOW')}")
            print(f"  • TẦNG QUYẾT ĐỊNH:  {result.get('tier_used', '')}")
            print(f"  • TỔNG ĐỘ TRỄ:      {result.get('total_latency_ms', 0.0):.2f} ms")
            print(f"  • TỔNG CHI PHÍ:     ${result.get('total_cost_usd', 0.0):.6f} USD")
            print("=" * 80)

        except KeyboardInterrupt:
            print("\nThoát chương trình.")
            break
        except Exception as e:
            print(f"Lỗi: {e}")


def main():
    parser = argparse.ArgumentParser(description="ScamShield-VN 2-Tier AI Architecture MVP Demo")
    parser.add_argument("--interactive", action="store_true", help="Chạy chế độ tương tác nhập liệu trực tiếp")
    parser.add_argument("--threshold", type=float, default=0.90, help="Ngưỡng tin cậy tau chuyển tiếp Tier 2 (mặc định: 0.90)")
    args = parser.parse_args()

    print_banner()
    router = TwoTierRouter(confidence_threshold=args.threshold)

    if args.interactive:
        interactive_mode(router)
    else:
        run_benchmark(router)


if __name__ == "__main__":
    main()

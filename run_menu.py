"""
==============================================================================
ScamShield-VN Interactive Menu System
==============================================================================
Provides robust, bug-free UTF-8 menu navigation and execution for demo options.
==============================================================================
"""

import os
import sys
import subprocess
import time

# Force UTF-8 safely on Windows terminal without closing existing streams
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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner():
    print("=" * 80)
    print("       🛡️  SCAMSHIELD-VN: NỀN TẢNG PHÁT HIỆN TIN NHẮN LỪA ĐẢO AI 2 TẦNG")
    print("=" * 80)
    print("  [1] 🚀 Chạy Bộ Kiểm Thử Benchmark (200 Mẫu Đầu vietnamese_sms_dataset)")
    print("  [2] 💬 Chế Độ Nhập Tin Nhắn Tương Tác Trực Tiếp (Interactive CLI)")
    print("  [3] 🔑 Cấu Hình Google Gemini API Key & Chạy Live Cloud Fallback")
    print("  [4] ⚙️  Kiểm Tra Cấu Hình Dynamic Model Registry (YAML & Cache)")
    print("  [5] 📄 Mở File Báo Cáo Tiến Độ Học Thuật Word (Báo Cáo Cô Chi)")
    print("  [0] 🚪 Thoát Chương Trình")
    print("=" * 80)


def run_benchmark():
    clear_screen()
    print("-" * 80)
    print("[*] ĐANG KHỞI CHẠY BỘ KIỂM THỬ BENCHMARK (200 MẪU VIETNAMESE_SMS_DATASET)...")
    print("-" * 80)
    try:
        from demo_scamshield_mvp import TwoTierRouter, run_benchmark as exec_benchmark
        router = TwoTierRouter()
        exec_benchmark(router, num_samples=200)
    except Exception as e:
        print(f"[!] Lỗi khi chạy Benchmark: {e}")
    input("\n👉 Nhấn Enter để quay lại Menu...")


def run_interactive():
    clear_screen()
    print("-" * 80)
    print("[*] Đang khởi chạy Chế Độ Tương Tác Trực Tiếp...")
    print("-" * 80)
    try:
        from demo_scamshield_mvp import TwoTierRouter, interactive_mode as exec_interactive
        router = TwoTierRouter()
        exec_interactive(router)
    except Exception as e:
        print(f"[!] Lỗi khi chạy Tương tác: {e}")
    input("\n👉 Nhấn Enter để quay lại Menu...")


def configure_api_key():
    clear_screen()
    print("-" * 80)
    print("[*] CẤU HÌNH GOOGLE GEMINI API KEY CHO TẦNG 2 CLOUD FALLBACK")
    print("-" * 80)
    key = input("Nhập Gemini API Key của bạn (nhấn Enter để bỏ qua): ").strip()
    if key:
        os.environ["GEMINI_API_KEY"] = key
        print("\n[+] Đã thiết lập GEMINI_API_KEY thành công cho phiên làm việc!")
    else:
        print("\n[-] Bạn chưa nhập API Key. Hệ thống tiếp tục sử dụng chế độ mô phỏng offline.")
    
    print("\n[*] Khởi chạy Chế Độ Tương Tác...")
    try:
        from demo_scamshield_mvp import TwoTierRouter, interactive_mode as exec_interactive
        router = TwoTierRouter(api_key=key if key else None)
        exec_interactive(router)
    except Exception as e:
        print(f"[!] Lỗi: {e}")
    input("\n👉 Nhấn Enter để quay lại Menu...")


def check_registry():
    clear_screen()
    print("-" * 80)
    print("[*] KIỂM TRA DYNAMIC MODEL REGISTRY VÀ CẤU HÌNH YAML")
    print("-" * 80)
    try:
        from pipeline.model_registry import ModelRegistry
        registry = ModelRegistry(auto_discover=True)
        print("\n--- CÁC MODEL THEO TIER (TỰ ĐỘNG PHÁT HIỆN / CACHE) ---")
        for tier, models in registry.cached_models_by_tier.items():
            print(f"  • Tier {tier.upper():<8}: {models}")
        print(f"\n  • Model mặc định cho Tier Lite: {registry.get_model('lite')}")
        print(f"  • Model mặc định cho Tier Standard: {registry.get_model('standard')}")
        print(f"  • Trạng thái Circuit Breaker: {'OPEN (Coooling)' if registry.is_circuit_open() else 'CLOSED (Normal)'}")
    except Exception as e:
        print(f"[!] Lỗi kiểm tra Registry: {e}")
    input("\n👉 Nhấn Enter để quay lại Menu...")


def open_report():
    clear_screen()
    print("-" * 80)
    print("[*] ĐANG MỞ FILE BÁO CÁO TIẾN ĐỘ HỌC THUẬT...")
    print("-" * 80)
    
    possible_files = [
        "Bao_Cao_Tien_Do_Hoc_Thuat_ScamShield_ChiLTQ6_v2.docx",
        "Bao_Cao_Tien_Do_Hoc_Thuat_ScamShield_ChiLTQ6.docx",
        "ScamShield_Bao_Cao_Tong_Hop_Hoc_Thuat_Toan_Dien_2_Tang.docx"
    ]
    
    found = False
    for filename in possible_files:
        filepath = os.path.join(BASE_DIR, filename)
        if os.path.exists(filepath):
            try:
                os.startfile(filepath)
                print(f"[+] Đã mở tài liệu: {filename}")
                found = True
                break
            except Exception as err:
                print(f"[!] Không thể mở file {filename}: {err}")
    
    if not found:
        print("[!] Không tìm thấy file báo cáo Word trong thư mục.")
    
    input("\n👉 Nhấn Enter để quay lại Menu...")


def main():
    while True:
        clear_screen()
        print_banner()
        choice = input("👉 Vui lòng chọn một tùy chọn (0-5): ").strip()

        if choice == "1":
            run_benchmark()
        elif choice == "2":
            run_interactive()
        elif choice == "3":
            configure_api_key()
        elif choice == "4":
            check_registry()
        elif choice == "5":
            open_report()
        elif choice == "0" or choice.lower() in ["exit", "quit", "q"]:
            print("\nCảm ơn bạn đã sử dụng ScamShield-VN! Chúc buổi báo cáo thành công.")
            time.sleep(1.0)
            break
        else:
            print("\n[!] Lựa chọn không hợp lệ. Vui lòng nhập số từ 0 đến 5.")
            time.sleep(1.2)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
==============================================================================
ScamShield-VN: Tier-1 ONNX CPU Inference Latency Benchmark & Verification
==============================================================================
Location: scripts/benchmark_onnx_inference.py
Description:
    Measures and compares CPU inference latency on:
      1. ViSoBERT ONNX FP32 Baseline (models/visobert_tier1.onnx)
      2. ViSoBERT ONNX INT8 Quantized (models/visobert_tier1_int8.onnx)
    Input set: Fixed Frozen Test Partition (N=267, data/processed/frozen_test_267.csv)
    Saves traceable report to experiments/tier1_edge/reports/
==============================================================================
"""

import os
import sys
import time
import json
import platform
import psutil
import numpy as np
import pandas as pd
from tokenizers import Tokenizer
import onnxruntime as ort

def get_system_metadata():
    return {
        "os": platform.platform(),
        "processor": platform.processor(),
        "machine": platform.machine(),
        "python_version": sys.version,
        "onnxruntime_version": ort.__version__,
        "cpu_count_physical": psutil.cpu_count(logical=False),
        "cpu_count_logical": psutil.cpu_count(logical=True),
        "total_ram_gb": round(psutil.virtual_memory().total / (1024**3), 2),
    }

def benchmark_model(model_path: str, samples: list, tok: Tokenizer, warmup_runs: int = 50, repeat: int = 2):
    session_options = ort.SessionOptions()
    session_options.intra_op_num_threads = min(4, psutil.cpu_count(logical=False) or 4)
    session_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL

    session = ort.InferenceSession(model_path, sess_options=session_options, providers=["CPUExecutionProvider"])

    # Prepare tokenized batches of size 1
    input_data = []
    for text in samples:
        enc = tok.encode(text)
        input_data.append({
            "input_ids": np.array([enc.ids], dtype=np.int64),
            "attention_mask": np.array([enc.attention_mask], dtype=np.int64)
        })

    # Warmup
    print(f"Executing {warmup_runs} warmup runs on {os.path.basename(model_path)}...")
    for i in range(warmup_runs):
        item = input_data[i % len(input_data)]
        session.run(None, item)

    # Benchmark timed runs
    print(f"Benchmarking {len(input_data) * repeat} total inferences...")
    latencies_ms = []
    for r in range(repeat):
        for item in input_data:
            t0 = time.perf_counter()
            _ = session.run(None, item)
            t1 = time.perf_counter()
            latencies_ms.append((t1 - t0) * 1000.0)

    latencies_arr = np.array(latencies_ms)
    size_bytes = os.path.getsize(model_path)

    return {
        "model_file": model_path,
        "artifact_size_bytes": size_bytes,
        "artifact_size_mb_binary": round(size_bytes / (1024 * 1024), 2),
        "artifact_size_mb_decimal": round(size_bytes / 1000000.0, 2),
        "total_measurements": len(latencies_ms),
        "warmup_runs": warmup_runs,
        "mean_latency_ms": round(float(np.mean(latencies_arr)), 2),
        "std_latency_ms": round(float(np.std(latencies_arr)), 2),
        "median_latency_ms": round(float(np.median(latencies_arr)), 2),
        "p90_latency_ms": round(float(np.percentile(latencies_arr, 90)), 2),
        "p95_latency_ms": round(float(np.percentile(latencies_arr, 95)), 2),
        "p99_latency_ms": round(float(np.percentile(latencies_arr, 99)), 2),
        "min_latency_ms": round(float(np.min(latencies_arr)), 2),
        "max_latency_ms": round(float(np.max(latencies_arr)), 2),
    }

def main():
    reports_dir = os.path.join("experiments", "tier1_edge", "reports")
    os.makedirs(reports_dir, exist_ok=True)

    test_csv = os.path.join("data", "processed", "frozen_test_267.csv")
    if not os.path.exists(test_csv):
        print(f"Missing {test_csv}, generating via scripts/generate_frozen_test_manifest.py")
        import subprocess
        subprocess.run([sys.executable, "scripts/generate_frozen_test_manifest.py"], check=True)

    df_test = pd.read_csv(test_csv)
    samples = df_test["message"].astype(str).tolist()

    tok_path = os.path.join("visobert_5runs_release", "tokenizer.json")
    tok = Tokenizer.from_file(tok_path)
    tok.enable_padding(length=128, pad_id=1, pad_token="<pad>")
    tok.enable_truncation(max_length=128)

    models_to_test = [
        ("FP32_Baseline", os.path.join("models", "visobert_tier1.onnx")),
        ("INT8_Quantized", os.path.join("models", "visobert_tier1_int8.onnx"))
    ]

    benchmark_results = {
        "metadata": get_system_metadata(),
        "input_set": {
            "source": test_csv,
            "sample_count": len(samples),
            "max_sequence_length": 128
        },
        "models": {}
    }

    for name, path in models_to_test:
        if os.path.exists(path):
            print(f"\n==========================================")
            print(f"Benchmarking: {name} ({path})")
            print(f"==========================================")
            res = benchmark_model(path, samples, tok, warmup_runs=50, repeat=2)
            benchmark_results["models"][name] = res
            print(f"Results for {name}:")
            print(f"  Artifact Size: {res['artifact_size_mb_binary']} MiB ({res['artifact_size_mb_decimal']} MB)")
            print(f"  Mean Latency: {res['mean_latency_ms']} ms | Median: {res['median_latency_ms']} ms | P95: {res['p95_latency_ms']} ms")

    json_report_path = os.path.join(reports_dir, "onnx_cpu_benchmark_report.json")
    with open(json_report_path, "w", encoding="utf-8") as f:
        json.dump(benchmark_results, f, indent=2, ensure_ascii=False)

    md_report_path = os.path.join(reports_dir, "onnx_cpu_benchmark_report.md")
    with open(md_report_path, "w", encoding="utf-8") as f:
        f.write("# Báo Cáo Đo Lường Benchmark Suy Luận ONNX trên CPU (Tier 1 Edge)\n\n")
        f.write("## 1. Môi Trường Thực Nghiệm và Phần Cứng\n")
        meta = benchmark_results["metadata"]
        f.write(f"- **Hệ điều hành:** {meta['os']}\n")
        f.write(f"- **Bộ xử lý (CPU):** {meta['processor']}\n")
        f.write(f"- **Kiến trúc:** {meta['machine']}\n")
        f.write(f"- **Số nhân vật lý / logic:** {meta['cpu_count_physical']} nhân vật lý / {meta['cpu_count_logical']} luồng logic\n")
        f.write(f"- **RAM tổng cộng:** {meta['total_ram_gb']} GB\n")
        f.write(f"- **Phiên bản Runtime:** Python {meta['python_version'].split()[0]}, ONNXRuntime v{meta['onnxruntime_version']}\n")
        f.write(f"- **Tập dữ liệu đầu vào:** Cố định $N=267$ mẫu (`{test_csv}`)\n")
        f.write(f"- **Số lượt warm-up:** 50 lượt; **Số lần đo lường:** {267 * 2} lần (2 vòng lặp qua 267 mẫu)\n\n")

        f.write("## 2. Bảng Đối Soát Kích Thước và Độ Trễ Tái Lập Được\n\n")
        f.write("| Mô hình Artifact | Định dạng Trọng số | Dung lượng File (MiB) | Dung lượng File (MB thập phân) | Mean Latency (ms) | Median Latency (ms) | P95 Latency (ms) | P99 Latency (ms) |\n")
        f.write("| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |\n")
        for m_name, m_data in benchmark_results["models"].items():
            dtype = "FP32" if "FP32" in m_name else "INT8 Dynamic"
            f.write(f"| {m_name} | {dtype} | {m_data['artifact_size_mb_binary']} MiB | {m_data['artifact_size_mb_decimal']} MB | {m_data['mean_latency_ms']} ms | {m_data['median_latency_ms']} ms | {m_data['p95_latency_ms']} ms | {m_data['p99_latency_ms']} ms |\n")
        f.write("\n")

    print(f"\nSaved benchmark reports to:\n  - {json_report_path}\n  - {md_report_path}")

if __name__ == "__main__":
    main()

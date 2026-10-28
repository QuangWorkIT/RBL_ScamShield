import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

try:
    import onnx
    print("onnx is installed!")
    
    for model_path in ['models/visobert_tier1.onnx', 'models/visobert_tier1_int8.onnx']:
        if not os.path.exists(model_path):
            continue
        model = onnx.load(model_path)
        total_params = 0
        initializer_count = len(model.graph.initializer)
        for init in model.graph.initializer:
            # compute total elements
            elements = 1
            for dim in init.dims:
                elements *= dim
            total_params += elements
        size_mb = os.path.getsize(model_path) / (1024 * 1024)
        print(f"Model: {model_path}")
        print(f"  File size: {size_mb:.2f} MB")
        print(f"  Initializers (tensors): {initializer_count}")
        print(f"  Total parameters: {total_params:,} ({total_params / 1e6:.2f}M params)")
        print()
except ImportError:
    print("onnx library not installed, checking via file size and torch if available.")

echo "Training for one epoch with CPU..."
th ../train.lua -print_every 0 -max_epochs 1 -speed_benchmark 1 -gpu -1 > cpu_benchmark.txt
echo "Training for one epoch with GPU..."
th ../train.lua -print_every 0 -max_epochs 1 -speed_benchmark 1 > gpu_benchmark.txt
echo ""
python benchmark_synthesizer.py
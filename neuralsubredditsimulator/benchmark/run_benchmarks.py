from __future__ import division #makes / always do float division, and // do integer division
import os, subprocess
import matplotlib.pyplot as plt

"""
os.chdir(os.path.join(os.path.dirname(__file__), ".."))
print "Running benchmarks..."
results = {}
devices = dict(CPU="-1", GPU="0")
sizes = [2**p for p in xrange(5,8)]
command = "th train.lua -print_every 0 -max_epochs 1 -speed_benchmark 1 -rnn_size 64 -gpu 0".split()
prefix = "Forward / Backward pass took"
d = len(prefix)
for device_name, device in devices.items():
  results[device_name] = []
  command[11] = str(device)
  for size in sizes:
    command[9] = str(size)
    result = subprocess.check_output(command).split("\n")
    run_total = 0
    run_count = 0
    for line in result:
      if line[:d] == prefix:
        run_total += float(line[d+1:].strip())
        run_count += 1
    run_avg = run_total / run_count
    results[device_name].append(run_avg)
    print "%s with rnn layer size %d, average time per iteration: %.3f seconds" % (device_name, size, run_avg)
"""
sizes = [2**p for p in xrange(5,9)]
results = {
  "CPU":[0.274, 0.721, 2.434, 9.801],
  "GPU":[0.047, 0.047, 0.048, 0.066]
}
plt.figure()
for device, result in results.items():
  plt.plot(sizes, result, label=device)
plt.ylabel("Average iteration time (s)")
plt.xlabel("LSTM layer size")
plt.ylim(0, 1)
plt.legend(loc=2)
plt.savefig("benchmark/benchmarks.png")
plt.show()

"""
for device_name, device_results in results.items():
  for i,size in enumerate(sizes):
    run_total = 0
    run_count = 0
    for line in device_results[i]:
      if line[:d] == prefix:
        run_total += float(line[d+1:].strip())
        run_count += 1
    run_avg = run_total / run_count
    print "%s with rnn layer size %d, average time per iteration: %.3f seconds" % (device_name, size, run_avg)
"""
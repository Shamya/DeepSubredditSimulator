from collections import defaultdict

raf = list(open("../generated/title_funny_10k_rscore.txt"))[:50]
sha = list(open("../generated/funny_rnn_score.txt"))
rcounts = defaultdict(lambda:0)
scounts = defaultdict(lambda:0)
for score in raf:
	rcounts[score.strip()] += 1
for score in sha:
	scounts[score.strip()] += 1
print rcounts
print scounts
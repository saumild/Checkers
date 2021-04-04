import random
lines = open("comb.txt").read().splitlines()
weights = random.choice(lines)

f = open("wt.txt","w+")
f.write(weights)
f.close()
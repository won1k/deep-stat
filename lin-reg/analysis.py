import csv
import numpy as np
import matplotlib.pyplot as plt

results = []
with open("noreg_p10_n1000.csv","rb") as f:
	reader = csv.reader(f, delimiter = ",")
	for row in reader:
		results.append(row)
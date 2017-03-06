setwd("~/Projects/deep-stat/lin-reg")

data = read.csv("noreg_p10_n1000_l0.005_T800.csv", header = FALSE)

# Train
hist(data[,1], breaks = 50, xlim = c(0.2,1))
abline(v = data[1,3], col = "red")

# Test
hist(data[,2], breaks = 50, xlim = c(0.9, 2.6))
abline(v = data[1,4], col = "red")

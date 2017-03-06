setwd("~/Projects/deep-stat/lin-reg/results")

data = read.csv("noreg_p10_n1000_l0.005_T800.csv", header = FALSE)

# Train
hist(data[,1], breaks = 50, xlim = c(0.2,1))
abline(v = data[1,3], col = "red")

# Test
hist(data[,2], breaks = 50, xlim = c(0.9, 2.6))
abline(v = data[1,4], col = "red")



predvar = read.csv("noreg_p10_n1000_l0.005_T800_pred_var.csv", header = FALSE)
hist(predvar[,3], breaks = 20)
plot(predvar[,3], predvar[,1])

metrics = read.csv("noreg_p10_n1000_l0.005_T800_metrics.csv", header = FALSE)

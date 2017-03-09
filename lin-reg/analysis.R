# Setup
library(ggplot2)
setwd("~/Projects/deep-stat/lin-reg/results")


# Prediction variance vs norm
predvar = read.csv("noreg_p1000_n100_l0.005_T800_pred_var.csv", header = FALSE)
colnames(predvar) = c("test.var", "test.mse", "test.norm")
hist(predvar[,3], breaks = 20)
plot(predvar[,3], predvar[,1], xlab = "Dist. of x* from x.bar", ylab = "Prediction Variance",
     pch = 16, cex = 0.5)

# Nice plots
c = ggplot(predvar, aes(test.norm, test.var))
c + stat_smooth(method=lm, alpha = 0.1) + geom_point() +
  labs(x = "Dist. of x* from x.bar", y = "Prediction Variance")



smoothScatter(predvar[,3], predvar[,1], xlab = "Dist. of x* from x.bar", ylab = "Prediction Variance")
points(predvar[,3], predvar[,1], pch = 16, cex = 0.5)
lines(lowess(predvar[,3], predvar[,1]), col = "red")

# Metrics
metrics = read.csv("noreg_p100_n100_l0.005_T800_metrics.csv", header = FALSE)
hist(metrics[,2], breaks = 50)


# Residuals
train_res = read.csv("noreg_p10_n100_l0.005_T800_train_res.csv", header = FALSE)
hist(train_res[,50], breaks = 50)

test_res = read.csv("noreg_p10_n100_l0.005_T800_test_res.csv", header = FALSE)
hist(as.numeric(test_res[5,]), breaks = 20)
plot(density(test_res[,5]))
hist(test_res[,25], breaks = 30)
hist(test_res[,50], breaks = 30)
hist(test_res[,75], breaks = 30)
hist(test_res[,95], breaks = 30)

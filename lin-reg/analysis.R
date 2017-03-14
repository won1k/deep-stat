# Setup
library(ggplot2)
library(gridExtra)
setwd("~/Projects/deep-stat")


# Prediction variance vs norm plots
prefix = "lin-reg/results/noreg_p"
suffix = "_l0.005_T800_pred_var.csv"
ps = c(10, 100, 1000)
ns = c(100, 1000, 10000)
plots = list()
for (p in ps) {
  for (n in ns) {
    if (p == 1000 & n == 10000) {
      next
    }
    data_file = paste(prefix,p,"_n",n,suffix,sep="")
    predvar = read.csv(data_file, header = FALSE)
    colnames(predvar) = c("test.var", "test.mse", "test.norm")
    if (n < p*10) {
      c = ggplot(predvar, aes(test.norm, test.var), alpha = I(0.1)) + stat_smooth(method=loess, alpha = 0.1, color = "grey") + geom_point(alpha = 0.1) +
        labs(x = "Dist. of X* from Training Mean", y = "Prediction Variance",
             title = paste("p = ",p,", n = ",n,sep = ""))
      plots[[length(plots) + 1]] = c
    } else {
      c = ggplot(predvar, aes(test.norm, test.var), alpha = I(0.1)) + stat_smooth(method=loess, alpha = 0.5, color = "black") + geom_point(alpha = 0.2) +
        labs(x = "Dist. of X* from Training Mean", y = "Prediction Variance",
             title = paste("p = ",p,", n = ",n,sep = ""))
      plots[[length(plots) + 1]] = c
    }
  }
}
do.call(grid.arrange, c(plots, list(ncol = 3)))






predvar = read.csv("non-reg/results/noreg_cubic_p10_n1000_l0.005_T800_pred_var.csv", header = FALSE)
colnames(predvar) = c("test.var", "test.mse", "test.norm")
#hist(predvar[,3], breaks = 20)
#plot(predvar[,3], predvar[,1], xlab = "Dist. of x* from x.bar", ylab = "Prediction Variance",
#     pch = 16, cex = 0.5)

# Nice plots
c = ggplot(predvar, aes(test.norm, test.var), alpha = I(0.1))
c + stat_smooth(method=loess, alpha = 0.1, color = "grey") + geom_point(alpha = 0.3) +
  labs(x = "Dist. of x* from x.bar", y = "Prediction Variance")


#smoothScatter(predvar[,3], predvar[,1], xlab = "Dist. of x* from x.bar", ylab = "Prediction Variance")
#points(predvar[,3], predvar[,1], pch = 16, cex = 0.5)
#lines(lowess(predvar[,3], predvar[,1]), col = "red")

# Metrics
metrics = read.csv("lin-reg/results/noreg_p10_n10000_l0.005_T800_metrics.csv", header = FALSE)
hist(metrics[,1], breaks = 50)
mses = data.frame(matrix(c(rep("Train",1000),rep("Test",1000),metrics[,1],metrics[,2]), ncol=2))
mses$X2 = as.numeric(as.character(mses$X2))
colnames(mses) = c("Dataset","MSE")
ggplot(mses, aes(x=MSE, fill=Dataset)) +
  geom_histogram(bins = 100, alpha=.5, position="identity", aes(y = ..density..)) #+ geom_density(alpha=0)


# Residuals
train_res = read.csv("noreg_p10_n10000_l0.005_T800_train_res.csv", header = FALSE)
hist(train_res[50,], breaks = 50)
hist(as.vector(as.matrix(train_res)), breaks = 100)

test_res = read.csv("non-reg/results/noreg_sigmoid_p10_n1000_l0.005_T800_test_res.csv", header = FALSE)
hist(as.numeric(test_res[5,]), breaks = 30)
plot(density(test_res[,5]))

# Residuals histogramistogram overlaid with kernel density curve
res = data.frame(matrix(c(rep("A",1000),rep("B",1000),test_res[,25],test_res[,975]), ncol=2))
res$X2 = as.numeric(as.character(res$X2))
ggplot(test_res, aes(x=test_res[,750])) + geom_histogram(aes(y=..density..), # Histogram with density instead of count on y-axis
                 binwidth=.01, alpha=0.5, fill = "white", color = "black") +
  geom_density(alpha=.2, fill="#FF6666")  # Overlay with transparent density plot GOOD!!

ggplot(res, aes(x=X2, fill=X1)) +
  geom_histogram(binwidth=.01, alpha=.5, position="identity", aes(y = ..density..)) +
  geom_density(alpha=.2)

hist(test_res[,25], breaks = 30)
hist(test_res[,50], breaks = 30)
hist(test_res[,75], breaks = 30)
hist(test_res[,95], breaks = 30)

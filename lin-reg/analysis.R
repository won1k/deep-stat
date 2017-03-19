# Setup
library(ggplot2)
library(scales)
library(gridExtra)
setwd("~/Projects/deep-stat")


# Prediction variance vs norm plots (GOOD)
prefix = "lin-reg/results/noreg_p"
suffix = "_l0.005_T800_pred_var.csv"
ps = c(10, 100, 1000)
ns = c("1000", "10000", "100000")
plots = list()
for (p in ps) {
  for (n in ns) {
    data_file = paste(prefix,p,"_n",n,suffix,sep="")
    if (!file.exists(data_file)) {
      next
    }
    predvar = read.csv(data_file, header = FALSE)
    predvar = predvar[sample(1:n,min(ns)),]
    colnames(predvar) = c("test.var", "test.mse", "test.norm")
    if (as.numeric(n) < p*50) {
      c = ggplot(predvar, aes(test.norm, test.var), alpha = I(0.1)) + 
        stat_smooth(method=loess, alpha = 0.1, color = "grey") + 
        geom_point(alpha = 0.1) +
        #geom_point(alpha = 0.1, size = 3, stroke = 0, shape = ".") +
        labs(x = "Dist. of X* from Training Mean", y = "Prediction Variance",
             title = paste("p = ",p,", n = ",n,sep = ""))
      plots[[length(plots) + 1]] = c
    } else {
      c = ggplot(predvar, aes(test.norm, test.var), alpha = I(0.1)) + 
        stat_smooth(method=loess, alpha = 0.5, color = "black") + 
        geom_point(alpha = 0.2) +
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
#labels = c("a","b","c","d","e","f","g","h","i","j","k","l","m","n","o")
#colors = c("a" = "red", "b" = "turquoise", "c" = "greenyellow", "d" = "tomato", "e" = "tomato1",
#           "f" = "tomato2", "g" = "indianred", "h" = "indianred1", "i" = "indianred2",
#           "j" = "seagreen", "k" = "seagreen1", "l" = "seagreen2",
#           "m" = "chartreuse", "n" = "chartreuse1", "o" = "chartreuse2")
#ltypes = c("a" = "dotted", "b" = "dotted", "c" = "dotted", "d" = "dotted", "e" = "dotted",
#           "f" = "dotted", "g" = "dotted", "h" = "dotted", "i" = "dotted",
#           "j" = "dotted", "k" = "dotted", "l" = "dotted",
#           "m" = "dotted", "n" = "dotted", "o" = "dotted")
metrics = read.csv("lin-reg/results/noreg_p10_n100000_l0.005_T800_metrics.csv", header = FALSE)
benchmarks = read.csv("lin-reg/results/benchmarks_p10_n100000.csv", header = FALSE)
benchmarks$V1 = as.character(benchmarks$V1)
#hist(metrics[,1], breaks = 50)
#mses = data.frame(matrix(c(rep("Train",1000),rep("Test",1000),metrics[,1],metrics[,2]), ncol=2))
#mses$X2 = as.numeric(as.character(mses$X2))
#colnames(mses) = c("Dataset","MSE")
ggplot(mses, aes(x=MSE, fill=Dataset)) +
  geom_histogram(bins = 100, alpha=.5, position="identity", aes(y = ..density..)) #+ geom_density(alpha=0)
# Test MSE
p = ggplot(metrics, aes(x=metrics[,2])) + geom_histogram(aes(y=..density..),
                    binwidth=.005, alpha=0.4, fill = "white", color = "grey") +
  geom_density(alpha=.2, fill="deepskyblue1")  + xlim(min(benchmarks$V4), max(metrics[,2]))
# Overlay with transparent density plot GOOD!!
for (i in 1:nrow(benchmarks)) {
  p = p + geom_vline(aes(linetype = labels[i], colour = labels[i], 
                         xintercept = benchmarks$V4[i]), show_guide = TRUE)
}
p = p + scale_colour_manual(name="Legend", values = colors) +
  scale_linetype_manual(name="Legend", values = ltypes) +
  theme_gray(base_size = 18)
print(p)

# Test MSE Histogram (GOOD) - make for n,p combo
png(filename = "lin-reg/plots/test_mse_hist_p10_n10000.png")
hist(metrics[,2], breaks = 50, freq = FALSE, xlab = "Test MSE", main = "", lty = 0, 
     xlim = c(min(benchmarks$V4), max(metrics[,2])),
     col = rgb(0,0,0,alpha=0.1) )
lines(density(metrics[,2]), lty = 1)
labs = c()
for (i in 1:nrow(benchmarks)) {
  abline(v = benchmarks$V4[i], col = colors[i], lwd = 1.5, lty = 2)
  if (benchmarks$V2[i] > 0) {
    labs = c(labs, paste(benchmarks$V1[i],", alpha = ",toString(benchmarks$V2[i]),sep = ""))
  } else {
    labs = c(labs, toString(benchmarks$V1[i]))
  }
}
legend("topright", legend = labs, lty = 1, col = colors)
dev.off()

# Test MSE Barplot (GOOD) -- make for every n,p combo
total = rbind(benchmarks, c("DNN", 0, mean(metrics[,1]), mean(metrics[,2]),
                                 mean(metrics[,3]), mean(metrics[,4]), mean(metrics[,5])))
total$id = 1:nrow(total)
total$SD = c(rep(NA, nrow(total)-1), sd(metrics[,2]))
rmrow = c(5,6,8,9,11,12,14,15)
total = total[-rmrow,]
total$V1 <- factor(total$V1, levels = total$V1[order(total$id)])
total$V4 = as.numeric(total$V4)
colnames(total) = c("Model","Alpha","TrainMSE","TestMSE","TrainR2","TestR2","TrainTime","id","SD")
limits = aes(ymax = TestMSE + SD, ymin = TestMSE - SD)
ggplot(data=total, aes(x=Model, y=TestMSE, fill=Model)) +
  geom_bar(stat="identity", colour="black") + 
  geom_errorbar(limits, width = 0.25) +
  scale_y_continuous(name="Test MSE", limits=c(0,min(c(max(total$TestMSE)+0.1),5)), oob=rescale_none) + 
  xlab("Model") #+ guide_legend(title = "Legend")

# Train MSE Barplot (GOOD)
total$TrainSD = c(rep(NA, nrow(total)-1), sd(metrics[,1]))
total$TrainMSE = as.numeric(total$TrainMSE)
limits = aes(ymax = TrainMSE + TrainSD, ymin = TrainMSE - TrainSD)
ggplot(data=total, aes(x=Model, y=TrainMSE, fill=Model)) +
  geom_bar(stat="identity", colour="black") + 
  geom_errorbar(limits, width = 0.25) +
  scale_y_continuous(name="Train MSE", limits=c(0,min(c(max(total$TrainMSE)+0.1),5)), oob=rescale_none) + 
  xlab("Model") #+ guide_legend(title = "Legend")

# Test R2 Barplot (GOOD)
total$TestR2SD = c(rep(NA, nrow(total)-1), sd(metrics[,4]))
total$TestR2 = as.numeric(total$TestR2)
limits = aes(ymax = TestR2 + TestR2SD, ymin = TestR2 - TestR2SD)
ggplot(data=total, aes(x=Model, y=TestR2, fill=Model)) +
  geom_bar(stat="identity", colour="black") + 
  geom_errorbar(limits, width = 0.25) +
  scale_y_continuous(name="Test R2", limits=c(0.99,max(total$TestR2 + total$TestR2SD)), oob=rescale_none) + 
  xlab("Model") #+ guide_legend(title = "Legend")

# Train R2 Barplot (GOOD)
total$TrainR2SD = c(rep(NA, nrow(total)-1), sd(metrics[,4]))
total$TrainR2 = as.numeric(total$TrainR2)
limits = aes(ymax = TrainR2 + TrainR2SD, ymin = TrainR2 - TrainR2SD)
ggplot(data=total, aes(x=Model, y=TrainR2, fill=Model)) +
  geom_bar(stat="identity", colour="black") + 
  geom_errorbar(limits, width = 0.25) +
  scale_y_continuous(name="Train R2", limits=c(0.99,max(total$TrainR2 + total$TrainR2SD)), oob=rescale_none) + 
  xlab("Model") #+ guide_legend(title = "Legend")



# Training Times
library(xtable)
total.print = total[,c("Model","TrainTime")]
xtable(total.print)


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

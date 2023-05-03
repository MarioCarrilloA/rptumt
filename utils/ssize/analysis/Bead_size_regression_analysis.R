# Recommended to be executed in RStudio 

library(ggplot2)

#=============================================================
# GENERAL NOTES:
# Uncomment in case pkg is not installed
# install.packages('ggplot2')
#
# This analysis uses as data the bounding boxes areas of multiple
# bead sizes computed by a deep learning model. In total there are 4:
# - 90um
# - 200-300um (referenced as 200um as shor form in this file)
# - 355-425um (referenced as 355um as shor form in this file)
# - 500-600um (referenced as 500um as shor form in this file)
#
# The objective is to compute a good regression model to
# estimate the in um from an input bounding box area. 
#=============================================================

#=============================================================
# 1. LOAD FUNCTIONS TO PROCESS DATA
#=============================================================
# Read data from CSV files and compute statistics
get_data_metricts <- function(bead_size) {
  datafile <- paste(bead_size, "um.csv", sep="")
  print(datafile)
  data <- read.csv(datafile)
  areas <- data$bbox_area
  n <- length(areas)
  m <- mean(areas)
  s <- sd(areas)
  mi <- min(areas)
  mx <- max(areas)

  return(list(
    "n"=n,
    "areas"=areas,
    "mean"=m,
    "sd"=s,
    "bs"=bead_size,
    "min"=mi,
    "max"=mx,
    "mms"=m-s,
    "mps"=m+s
  ))
}

# Plot areas as points
vis_plot <- function(data) {
  n <- length(data$areas)
  x <- seq(1:n)
  y <- data$areas
  title <- paste("Bounding boxes areas - Beads ", data$bs, "um", sep="")
  print(title)
  plot(x, y, pch=20, ylab="Bounding box area [0,1]",
       xlab="Samples", type="b",
       main=title)
}

# Plot boxplot to see outliers
vis_boxplot <- function(d1, d2, d3, d4) {
  boxplot(d1$areas, d2$areas, d3$areas, d4$areas,
          names=bead_types,
          ylab="Bounding box area [0,1]",
          xlab="Bead sizes",
          main="Bounding box areas of different bead sizes")
}

# Show a barplot with the 4 mean values (one per dataset)
# and the standard deviation (it uses ggplot)
vis_barplot <- function(d1, d2, d3, d4) {
  sizes <- c(d1$mean, d2$mean, d3$mean, d4$mean)
  stdvs <- c(d1$sd, d2$sd, d3$sd, d4$sd)
  print(stdvs)
  print(sizes)
  print(bead_types)
  print(length(bead_types))
  print(length(sizes))
  print(length(stdvs))
  beads <- data.frame(sizes=sizes, stdvs=stdvs, bead_types=bead_types)
  beads$bead_types <- factor(beads$bead_types, levels=beads$bead_types)
  
  # Plot
  ggplot(beads, aes(x=bead_types, y=sizes, fill=bead_types)) + 
        geom_bar(stat = "identity") +
        geom_errorbar(aes(
                        ymin=sizes - stdvs,
                        ymax=sizes + stdvs,),
                        colour="black", width=.1) +
        ggtitle("Bounding box areas of different bead sizes") +
        labs(fill = "Bead sizes") +
        ylab("Average bounding boxes areas [0,1]") +
        xlab("Bead size") +
        theme(plot.title = element_text(hjust = 0.5)) +
        theme_light()
  
}

# Remove the outliers from the datasets
remove_outliers <- function(data) {
  quartiles <- quantile(data$areas, probs=c(.25, .75), na.rm=TRUE)
  IQR <- IQR(data$areas)
  lower <- quartiles[1] - 1.5*IQR
  upper <- quartiles[2] + 1.5*IQR 
  
  # data with no outliers
  DWNO <- subset(data$areas, data$areas > lower & data$areas < upper)
  bead_size <- data$bs
  areas <- DWNO
  n <- length(areas)
  m <- mean(areas)
  s <- sd(areas)
  mi <- min(areas)
  mx <- max(areas)
  return(list(
    "n"=n,
    "areas"=areas,
    "mean"=m,
    "sd"=s,
    "bs"=bead_size,
    "min"=mi,
    "max"=mx,
    "mms"=m-s,
    "mps"=m+s
  ))
  
}

# Plot the normal distribution of the bounding boxes
plot_norm_distribution <- function(x, mean, sd, size) {
  title <- paste("Distribution ", size)
  y <- dnorm(x, mean=mean, sd=sd)
  plot(x, y, pch=20, xlab="Bounding boxes areas",
       main=title)
}

# Plot the data set and the regression model
plot_regression_model <- function(x, Y, fit) {
  plot(x, Y, xlab="Bounding box area [0,1]", ylab="Bead size",
       main="Bead size estimation model", pch=20, col="blue")
  
  lines(x, fitted(fit), col='red')
  legend("bottomright",
         legend=c("Dataset points", " Regression model"),
         lty=c(NA, 1),
         pch=c(20, NA),
         col=c("blue", "Red"))
}

# Global variables
bead_types <- c("90um", "200-300um", "355-425um", "500-600um")

#=============================================================
# 2. LOAD BEAD SIZE DATA FROM CSV FILES, COMPUTE STATISTICS
#    AND VISUALIZE RESULTS
#=============================================================
# Read datasets from CSV files and compute
# statistics
b090 <- get_data_metricts(bead_size="90")
b200 <- get_data_metricts(bead_size="200")
b355 <- get_data_metricts(bead_size="355")
b500 <- get_data_metricts(bead_size="500")

# Print statistics
cat("No. Samples", "mean", "sd", "min", "max")
cat(b090$n, b090$mean, b090$sd, b090$min, b090$max)
cat(b200$n, b200$mean, b200$sd, b200$min, b200$max)
cat(b355$n, b355$mean, b355$sd, b355$min, b355$max)
cat(b500$n, b500$mean, b500$sd, b500$min, b500$max)

# Visualize raw data
if (length(dev.list()) != 0) {dev.off()}
vis_plot(b090)
vis_plot(b200)
vis_plot(b355)
vis_plot(b500)

# Visualize boxplot of raw data
vis_boxplot(b090, b200, b355, b500)

# Compare all bead sizes with barplot
vis_barplot(b090, b200, b355, b500)

# Plot distributions
plot_norm_distribution(b090$areas, b090$mean, b090$mean, "90um")
plot_norm_distribution(b200$areas, b200$mean, b200$mean, "200-300um")
plot_norm_distribution(b355$areas, b355$mean, b355$mean, "355-425um")
plot_norm_distribution(b500$areas, b500$mean, b500$mean, "500-600um")


#=============================================================
# 3. REMOVE OUTLIERS FROM LOADED DATA, COMPUTE STATISTICS
#    AND VISUALIZE RESULTS
#=============================================================
# Remove outliers and create new R arrays with
# the results
NOb090 <- remove_outliers(b090)
NOb200 <- remove_outliers(b200)
NOb355 <- remove_outliers(b355)
NOb500 <- remove_outliers(b500)

# Plot filtered data
vis_plot(NOb090)
vis_plot(NOb200)
vis_plot(NOb355)
vis_plot(NOb500)

# Print results on console
cat("No. Samples", "mean", "sd", "min", "max")
cat(NOb090$n, NOb090$mean, NOb090$sd, NOb090$min, NOb090$max)
cat(NOb200$n, NOb200$mean, NOb200$sd, NOb200$min, NOb200$max)
cat(NOb355$n, NOb355$mean, NOb355$sd, NOb355$min, NOb355$max)
cat(NOb500$n, NOb500$mean, NOb500$sd, NOb500$min, NOb500$max)

# Visualize boxplot of data with no outliers
vis_boxplot(NOb090, NOb200, NOb355, NOb500)

# Barplot of data without outliers
vis_barplot(NOb090, NOb200, NOb355, NOb500)

# Plot distributions
plot_norm_distribution(NOb090$areas, NOb090$mean, NOb090$mean, "90um")
plot_norm_distribution(NOb200$areas, NOb200$mean, NOb200$mean, "200-300um")
plot_norm_distribution(NOb355$areas, NOb355$mean, NOb355$mean, "355-425um")
plot_norm_distribution(NOb500$areas, NOb500$mean, NOb500$mean, "500-600um")

#=============================================================
# 4. CREATE MODEL: ** BESM1 ** BY USING: POINTS=4  DEGREE=2 
#=============================================================
x <- c(NOb090$mean, NOb200$mean, NOb355$mean, NOb500$mean)
Y <- c(90, 250, 390, 550)

# Test samples
test_data1 <- data.frame(x=c(0.00010742187500000001)) # 90um sample
test_data2 <- data.frame(x=c(0.0006261115)) # 200-300um sample

fit <- lm(Y~poly(x, 2, raw=TRUE))
#plot(fit)
options(scipen=999)
fit$coefficients
plot_regression_model(x, Y, fit)
predict(fit, test_data1)
predict(fit, test_data2)

#=============================================================
# 5. CREATE MODEL: ** BESM2 ** BY USING: POINTS=4  DEGREE=3 
#=============================================================
fit <- lm(Y~poly(x, 3, raw=TRUE))
fit$coefficients
fit
plot_regression_model(x, Y, fit)
options(scipen=999)
predict(fit, test_data1)
predict(fit, test_data2)

#=============================================================
# 6. CREATE MODEL: ** BESM3 ** BY USING: POINTS=9  DEGREE=2 
#=============================================================
x <- c(NOb090$mean,
       NOb200$mms, NOb200$mean, NOb200$mps,
       NOb355$mms, NOb355$mean, NOb355$mps,
       NOb500$mms, NOb500$mean, NOb500$mps)

Y <- c(90,
       200, 250, 300,
       355, 390, 425,
       500, 550, 600)

fit <- lm(Y~poly(x, 2, raw=TRUE))
fit$coefficients
plot_regression_model(x, Y, fit)
options(scipen=999)
test_data <- data.frame(x=c(0.0006261115))
predict(fit, test_data)
predict(fit, test_data1)
predict(fit, test_data2)
plot(fit)

#=============================================================
# 7. CREATE MODEL: ** BESM4 ** BY USING: POINTS=9  DEGREE=3 
#=============================================================
fit <- lm(Y~poly(x, 3, raw=TRUE))
fit$coefficients
plot_regression_model(x, Y, fit)
options(scipen=999)
test_data <- data.frame(x=c(0.0006261115))
predict(fit, test_data)
predict(fit, test_data1)
predict(fit, test_data2)

#=============================================================
# 7. PLAYGROUND/TEST AREA
#=============================================================

x=NOb090$areas
mean=NOb090$mean
sd=NOb090$sd
y <- dnorm(x, mean=mean, sd=sd)
plot(x, y, pch=20, xlab="Bounding boxes areas",
     main="Distributions", col="red", xlim=c(0, 0.01))
x=NOb200$areas
mean=NOb200$mean
sd=NOb200$sd
y <- dnorm(x, mean=mean, sd=sd)
points(x, y, pch=20, xlab="Bounding boxes areas", col="blue")



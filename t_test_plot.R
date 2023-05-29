t_test_plot <- function(data, t_statistic, alpha=0.05){
  # computing the critical value
  n <- nrow(data)
  df <- n-ncol(data)
  # critical value 2 tailed -> alpha/2 -> two tailed test != 0
  cv2 <- qt(1-(alpha/2), df)
  # lower rejection region is the same value just negative!
  # qt(alpha/2, df)
  
  t_dist <- data.frame(x = c(-4, 4))
  lower_rj <- c(-4,(-1)*cv2)
  upper_rj <- c(cv2, 4)
  
  # plot the t-distribution
  g <- ggplot(data=t_dist, aes(x = x)) +
    geom_area(stat = "function", fun = dt, args = list(df = df),
              fill='white') +
    geom_area(stat = "function", fun = dt, args = list(df = df), 
              fill='orange', xlim=lower_rj) +
    geom_area(stat = "function", fun = dt, args = list(df = df), 
              fill='orange', xlim=upper_rj) +
    geom_line(stat = "function", fun = dt, args = list(df = df)) +
    
    geom_vline(xintercept = cv2, col=2, lwd=1.1) +
    geom_vline(xintercept = cv2*(-1), col=2, lwd=1.1) +
    geom_vline(xintercept = t_statistic , col=4) +
    geom_text(aes(x = t_statistic, y=0.3), label='test', col=4) 
  return(g)
}

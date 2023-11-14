setwd("C:/Users/adams/Documents/PhD/TDGD")

Line <- 'W1118'
Temp <- 25
file <- 'w1118tdgd.csv'

df <- read.csv(file)

df$new_ratio <- with(df, EGI/(EGI+OREO)-init_ratio_egi)

func <- nls(new_ratio ~ (F0*(c0*init_ratio_egi)^2)/(F0*(c0*init_ratio_egi)^2+(1-(c0*init_ratio_egi))^2)-init_ratio_egi , data = df, start = list(c0 = 1, F0 = 1))

summary(func)

summer <- data.frame(coef(summary(func)))
vec <- summer$Estimate
SE <- summer$Std..Error

#SE <- SE*85^(1/2)

Thr<- c((vec[1]^2*vec[2] - vec[1]*(vec[2]^(1/2))*(vec[1]^2*vec[2] + 4*vec[1] - 4)^(1/2) + 2*vec[1])/(2*(vec[1]^2*vec[2] + vec[1]^2)),(vec[1]^2*vec[2] + vec[1]*(vec[2]^(1/2))*(vec[1]^2*vec[2] + 4*vec[1] - 4)^(1/2) + 2*vec[1])/(2*(vec[1]^2*vec[2] + vec[1]^2)))

SEM <- (SE[1]^2 * ((2*vec[1]*vec[2]+vec[1]*(vec[1]^2*vec[2]-(vec[1]^2*vec[2]+4*vec[1]-4)^(1/2)*vec[1]^(vec[2]^(1/2))+2*vec[1])/(2*(vec[1]^2*vec[2]+vec[1]^2)^2))^2+ SE[2]^2 * ((((vec[1]^2-(vec[1]^2*vec[2]+4*vec[1]-4)^(1/2)*vec[1]^(vec[2]^(1/2))*log(vec[1]))/(2*vec[2]^(1/2)))-((vec[1]^(vec[2]^(1/2)+2))/(2*(vec[1]^2*vec[2]+4*vec[1]-4)^(1/2))))/(2*(vec[1]^2*vec[2]+vec[1]^2))-(vec[1]^2*(vec[1]^2*vec[2]-((vec[1]^2*vec[2]+4*vec[1]-4)^(1/2)*vec[1]^(vec[2]^(1/2))+2*vec[1])))/(2*(vec[1]^2*vec[2]+vec[1]^2)^2))^2))^(1/2)

statsout <- read.csv('stats.csv')

statsout[nrow(statsout) + 1,] = c(Line,Temp,summer$Estimate[1],summer$Std..Error[1],summer$Estimate[2],summer$Std..Error[2],Thr[1],SEM,file)

write.csv(statsout,'stats.csv',row.names = FALSE)

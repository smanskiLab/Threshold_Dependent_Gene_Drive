setwd("C:/Users/adams/Documents/PhD/TDGD")

Line <- 'A3.7'
Temp <- 25
file <- 'a37tdgd.csv'

df <- read.csv(file)

df$new_ratio <- with(df, EGI/(EGI+OREO)-init_ratio_egi)

func <- nls(new_ratio ~ ((c0*init_ratio_egi)^2)/((c0*init_ratio_egi)^2+(1-(c0*init_ratio_egi))^2)-init_ratio_egi , data = df, start = list(c0 = 1))

summary(func)

summer <- data.frame(coef(summary(func)))
vec <- summer$Estimate
SE <- summer$Std..Error

#SE <- SE*85^(1/2)

Thr<- c((vec[1]**2 - vec[1]*(vec[1]**2 + 4*vec[1] - 4)**(1/2) + 2*vec[1])/(2*(vec[1]**2 + vec[1]**2)),(vec[1]^2 + vec[1]*(vec[1]^2 + 4*vec[1] - 4)^(1/2) + 2*vec[1])/(2*(vec[1]^2 + vec[1]^2)))

SEM <- (SE[1]^2 * ((-(vec[1]^2+4*vec[1]-4)^(1/2)-vec[1]-2)/(2*vec[1]*(vec[1]^2+4*vec[1]-4)^(1/2)))^2)^(1/2)
statsout <- read.csv('stats_cOnly.csv')

statsout[nrow(statsout) + 1,] = c(Line,Temp,summer$Estimate[1],summer$Std..Error[1],Thr[1],SEM,file)

write.csv(statsout,'stats_cOnly.csv',row.names = FALSE)

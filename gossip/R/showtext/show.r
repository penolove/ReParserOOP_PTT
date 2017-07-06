library(showtext)
showtext.auto(enable = TRUE)
font.add("heiti", "../LiHei-Pro.ttf")

x=1:10
y=1:10
png("trial.png")
par(fig=c(0,1,0.1,0.9))

#plot(x,y)
#title(main= "靠北喔",cex.main = 1.5,
#      cex.sub = 3,col.main="red",col.sub="red")
plot(runif(10), xlab = "橫軸", ylab = "縱軸", main = "靠北標題",
       family = "heiti")

dev.off( )

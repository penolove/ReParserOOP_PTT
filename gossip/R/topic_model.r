cat("=========Now runing TopicModel : LDA in R================\n")


setwd('/home/stream/Documents/ptt_web_oop/gossip')

date_now=readLines("datetemp.txt")
dateweek=readLines("weekdatetemp.txt")

formatnow=as.Date(date_now,"%Y/ %m/%d")
formatweek=as.Date(dateweek,"%Y/ %m/%d")

daydiff=formatnow-formatweek

bool7=daydiff==7
print(daydiff)

if(bool7){
  
  #record the date to txt  
  fileConn<-file("weekdatetemp.txt")
  writeLines(paste(date_now), fileConn)
  close(fileConn)

  library("RSQLite")
  library('tau')
  #require(rJava)
  library(tm)
  library(wordcloud)
  drv <- dbDriver("SQLite")
  con <- dbConnect(drv, "/home/stream/Documents/minimum_django/pttWeb/starbucks.sqlite")
  
  date_now_query=paste('"',date_now,'"',sep="")
  
  
  dateweek_query=paste('"',dateweek,'"',sep="")

  #get upperbound
  dateoption=paste("SELECT ROWID FROM webarticle WHERE date=",date_now_query,sep = "")
  date=dbGetQuery(conn=con, dateoption)
  upperbound=max(date)

  #get lowerbound
  dateoption=paste("SELECT ROWID FROM webarticle WHERE date=",dateweek_query,sep = "")
  date=dbGetQuery(conn=con, dateoption)
  lowerbound=min(date)

  
  week_rows_query=paste('SELECT * FROM webarticle where rowid >=' ,lowerbound,'AND rowid <=',upperbound)
  week_rows=dbGetQuery(conn=con, week_rows_query)

  not_in_week=which(as.Date(week_rows[,2], "%Y/ %m/%d")<as.Date(dateweek, "%Y/ %m/%d"))
  not_in_week=c(not_in_week,which(as.Date(week_rows[,2], "%Y/ %m/%d")>as.Date(date_now, "%Y/ %m/%d")))
  if(length(not_in_week)>0){
    week_rows=week_rows[-not_in_week,]
  }
  cat("there are ")
  cat(dim(week_rows))
  cat(" rows in this Week\n")

  week_article=week_rows[,5]
  week_article_date=week_rows[,2]

  #clean string for date
  week_article_date=gsub(pattern=" ", replacement="", week_article_date) 

  #clean for article
  week_article=gsub(pattern="\n", replacement=" ", week_article ) 
  week_article=gsub(pattern="/", replacement=".", week_article) 
  week_article=gsub(pattern=" ", replacement="", week_article) 
  week_article=gsub('[A-Za-z0-9]', '', week_article)
  
  library(tm)
  
  #clean and clean 
  for (i in 1:length(week_article)){
      week_article[i]=gsub(pattern=" ", replacement="", week_article[i]) 
      week_article[i]=gsub('([[:alpha:]])\\1+', '\\1', week_article[i])
  }
  
  library(ropencc)
  library(jiebaR)
  ccst = converter(T2S)
  ccts = converter(S2T)
  
  #convert to simple chinese and split it for each week_aricle
  mixseg = worker()
  for (i in 1:length(week_article)){
    week_article[i]=ccst[week_article[i]]
    week_article[i]=paste(mixseg<=week_article[i],collapse=", ")
    week_article[i]=ccts[week_article[i]]
  }
  
  
  library(tmcn)
  #create text Corpus , clean words
  d.corpus <- Corpus(VectorSource(week_article))
  remoces=ccts[stopwordsCN()]
  remoces<-c(remoces,'的','在','是','有','不','人','會','對','就','了'
  ,'要','我','你','他','她','也','於','上','大','後','說','與','但','都','被','沒有','很','還','這','我們','好','來'
  ,'看','到','沒','可以','啊','跟','自己','知道','讓','只','完整','新聞','表示','媒體','到'
  ,'過','去','給','一','想','因為','把','所以','多','出','想','去','能','才','那','一個','為'
  ,'等','著','他們','什麼','和','如果','阿','最','再','嗎','之','時','而','現在','報導','以','做','用','這個','社會'
  ,'工作','前','得','當','這樣','其實','拿','住','講','錢','租','內','中','張','陳','真','中','高','低'
  ,'打','並','應該','完','吧','請','台','志','老師','幫','事','花','但是','或','更','明','桌','大家','宅','事情'
  ,'這麼','這種','又','啦','然','你們','我們','告','將','開','吃','找','太','長','年'
  ,'希望','資料','這些','開始','可能','影片','政治','覺得','發現','時間','一樣','公司','網友'
  ,'很多','合理','認為','為什麼','今天','會議','下','個','月','日','文','立',"真的" , "有沒有","不是")
  d.corpus <- tm_map(d.corpus, removeWords,remoces)
  d.corpus <- tm_map(d.corpus, stripWhitespace)
  
  # Create Document Term Matrix from corpud
  DTM_=c()
  DTM_ <- DocumentTermMatrix(d.corpus,
      control = list(
        wordLengths=c(1, Inf), # to allow long words   
        weighting = weightTf,
          removePunctuation=TRUE
    )
  )
  
  
  DTM_matrix <- as.matrix(DTM_)
  term_frequency <- sort(colSums(DTM_matrix), decreasing=TRUE)
  TF_names <- names(term_frequency)
  #d <- data.frame(word=TF_names, freq=term_frequency)


  pal2 <- brewer.pal(8,"Dark2")

  library(scales)
  library(data.table)
  library(ggplot2)
  library(topicmodels)
  
  rowTotals <- apply(DTM_ , 1, sum) 
  DTM.new   <- DTM_[rowTotals> 0,]
  #create Topic model usin LDA alogrithm
  lda=LDA(DTM.new ,4)
  term<-terms(lda,10)
  term<-apply(term, MARGIN=2 ,paste, collapse=',')
  #get topic model infomations
  topic<-topics(lda,1)
  n=rep(0.2,length(topic))
  topics<-data.frame(date=as.Date(week_article_date[rowTotals> 0],"%Y/ %m/%d"),topic,n)
  density_plot=qplot(date,data=topics,geom='density',color=term[topic])
  
  
  setwd('/home/stream/Documents/minimum_django/pttWeb/static/topicmodel')
  date_now_ft=strsplit(format(formatnow,"%Y,%m,%d"),",")
  date_now_ft=unlist(date_now_ft)
  date_now_ft[2]=as.character(as.numeric(date_now_ft[2]))

  date_week_ft=strsplit(format(formatweek,"%Y,%m,%d"),",")
  date_week_ft=unlist(date_week_ft)
  date_week_ft[2]=as.character(as.numeric(unlist(date_week_ft)[2]))

  #save it to png
  ggsave(filename=paste('weeksa_',paste(date_week_ft,collapse="."),'_',paste(date_now_ft,collapse="."),".png",sep = ""), plot=density_plot+ scale_x_date(labels = date_format("%m/%d"))+theme(text = element_text(size=20))
  , width=10, height=7)

}


# library("RSQLite")
# library('tau')
# require(rJava)
# library(tm)
# library(wordcloud)

# used not officical:
# library(Rwordseg)
# install Rwordseg must already install rJava
# install.packages("Rwordseg", repos="http://R-Forge.R-project.org")  
# ===================================================================
# library(tmcn)
# install.packages("tmcn", repos="http://R-Forge.R-project.org", type="source")

#=== create connection with sqlite : function of RSQLite ===
library("RSQLite")
drv <- dbDriver("SQLite")
setwd('/home/stream/Documents/kerkerman88')
con <- dbConnect(drv, "starbucks.sqlite")

x=readLines("ptt/datetemp.txt")
datekey=paste('"',x[1],'"',sep="") # create \"date\" this kind string
dates_Selected_query=paste("SELECT ROWID FROM webarticle WHERE date=",datekey,sep = "")

#excute query by function of RSQLite 
dates_Selected <- dbGetQuery(conn=con, dates_Selected_query)


count=0

for (Rowkey in c(dates_Selected$rowid)){

  count=count+1
  row_pushes_query=paste("SELECT  * FROM webptt WHERE articlekey=",Rowkey,sep = "")
  row_article_query=paste("SELECT  * FROM webarticle WHERE ROWID=",Rowkey,sep = "")

  row_pushes  <- dbGetQuery(conn=con, row_pushes_query)
  row_article <- dbGetQuery(conn=con, row_article_query)

  row_pushes_context <- row_pushes[,3] #row_pushes_context
  article_title <- row_article[,4] #article_title
  article_push_score <- row_article[,1] # push_score
  article_date <- row_article[,2] # date with 2017/ 1/09 format
  article_date = gsub(pattern="/", replacement=".", article_date) 
  article_date = gsub(pattern=" ", replacement="", article_date) #  date with 2017.1.09 format

  push_words=c()

  for (i in 1:length(row_pushes_context)){
    #remove words such as " "
    push_words[i]=gsub(pattern=" ", replacement="", row_pushes_context[i]) 
    #transform XDD->XD , kerrrrr -> ker
    push_words[i]=gsub('([[:alpha:]])\\1+', '\\1', push_words[i])
  }

  library(ropencc)
  # devtools::install_github("qinwf/ropencc")
  library(jiebaR)
  # install.packages('jiebaR', repos='https://ftp.yzu.edu.tw/CRAN/')

  ccst = converter(T2S)
  ccts = converter(S2T)
  mixseg = worker()
  for (i in 1:length(push_words)){
    # conver to Simple Chinese
  	push_words[i]=ccst[push_words[i]]
    # segments scentence to words and paste back by ", "
  	push_words[i]=paste(mixseg<=push_words[i],collapse=", ")
    # conver it back to Traditional Chinese
  	push_words[i]=ccts[push_words[i]]
  }


  library(tm)
  library(tmcn)
  #create text corpus
  d.corpus <- Corpus(VectorSource(push_words))
  d.corpus <- tm_map(d.corpus, removeWords,ccts[stopwordsCN()])
  # document term matrix
  dtm1=c()
  dtm1 <- DocumentTermMatrix(d.corpus, 
        control = list(wordLengths=c(1, Inf), # to allow long words   
        weighting = weightTf, 
  	    removePunctuation=TRUE 
        ) 
    )

  colnames(dtm1)

  matrix_dtm <- as.matrix(dtm1)
  term_frequency <- sort(colSums(matrix_dtm), decreasing=TRUE)
  term_Names <- names(term_frequency)
  term_frequency_matrix <- data.frame(word=term_Names, freq=term_frequency)

  library(wordcloud)
  pal2 <- brewer.pal(8,"Dark2")
  setwd('/home/stream/')
  png(paste(article_date,'_',count,".png",sep = ""))

  par(fig=c(0,1,0.1,0.9))
  wordcloud(term_frequency_matrix$word,term_frequency_matrix$freq,
            scale=c(4,2), min.freq=2,max.words=100, random.order=FALSE,
            rot.per=.15, colors=pal2)
  par(fig=c(0,1,0,1))
  title(main=article_title,sub=article_push_score,cex.main = 1.5,
        cex.sub = 3,col.main="red",col.sub="red",ylab=article_date)
  dev.off( )
}


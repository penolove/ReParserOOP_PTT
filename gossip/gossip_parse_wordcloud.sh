#!/bin/bash
export LC_CTYPE=en_US.UTF-8
export LC_ALL=en_US.UTF-8
export PATH="/home/stream/anaconda2/bin:$PATH"
export PATH=/home/stream/anaconda2/bin:/home/stream/anaconda2/bin:/home/stream/anaconda2/bin:/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin:/home/stream/.local/bin:/home/stream/bin:/home/stream/.local/bin:/home/stream/bin:/home/stream/.vimpkg/bin

date
cd /home/stream/Documents/ptt_web_oop/gossip/;
python gossip_ptt_end2end.py;
Rscript R/word_cloud.r
Rscript R/topic_model.r

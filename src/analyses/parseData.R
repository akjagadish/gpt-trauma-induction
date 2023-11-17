############## first look at the data from the trauma stai ##############
## quick and ugly script to quickly check whether the data looks reasonable

library(ggplot2)
theme_set(theme_classic(base_size = 14))
library(plyr)
library(jsonlite)

# Set the working directory to the script directory
setwd("/Users/kwitte/Documents/GitHub/gpt-trauma-induction/src/analyses")


se<-function(x){sd(x, na.rm = T)/sqrt(length(na.omit(x)))}
meann <- function(x){mean(x, na.rm = T)}


##############
# the stai has reversed items so load stai to get which ones they are
stai <- read.csv("../STAI/questionnaires.csv", sep = ";")
stai <- subset(stai, !is.na(X))

####### purely stai
noPreprompt <- fromJSON("../results/gpt4_brief_stai_0.json")

noPreprompt <- data.frame(response = unlist(noPreprompt$none$none[[1]]),
                          reveresed = stai$Reverse.coded)

# reverse them back
noPreprompt$response[noPreprompt$reveresed == 1] <- 5-noPreprompt$response[noPreprompt$reveresed == 1]


###### trauma + stai
trauma_import <- fromJSON("../results/gpt4_brief_trauma_stai_0.json")
conds <- names(trauma_import)[1:5]
trauma <- data.frame(reversed = stai$Reverse.coded)

for (i in 1:length(conds)){
  trauma[,i+1] <-unlist(trauma_import[[i]][[1]])
  trauma[trauma$reversed == 1, i+1] <- 5 - trauma[trauma$reversed == 1, i+1]
}

colnames(trauma)[2:6] <- conds


######## trauma + relaxation stai

trauma_import <- fromJSON("../results/gpt4_brief_trauma_relaxation_stai_0.json")
trauma_conds <- names(trauma_import)[1:5]
relax_conds <- names(trauma_import[[1]])
trauma_relax <- data.frame(reversed = rep(stai$Reverse.coded, length(trauma_conds)*length(relax_conds)),
                           trauma = rep(trauma_conds, each = nrow(stai)*length(relax_conds)),
                           relax = rep(rep(relax_conds, each = nrow(stai)), length(trauma_conds)))

trauma_relax$response <- NA
for (i in 1:length(trauma_conds)){
  for (j in 1:length(relax_conds)){
    trauma_relax$response[trauma_relax$trauma == trauma_conds[i] & trauma_relax$relax == relax_conds[j]] <- unlist(trauma_import[[i]][[j]][[1]])
  }
}

trauma_relax$response[trauma_relax$reversed == 1] <- 5 - trauma_relax$response[trauma_relax$reversed == 1]

hist(trauma_relax$response)


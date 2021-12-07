library('httr')
library('stringr')
library('rbenchmark')

get_advent = function(day, raw = FALSE, trim = TRUE, split1 = '\n', split2 = ',', as.numeric = TRUE) {
  url = paste0('https://adventofcode.com/2021/day/',day,'/input')
  headers = c('cookie' = 'bla')
  r = GET(url, add_headers(headers))
  content = content(r)
  if(raw) return(content)
  if(trim) content = str_trim(content)
  if (!isFALSE(split1)) content = str_split(content, split1)[[1]]
  if (!isFALSE(split2)) content = str_split(content, split2)[[1]]
  if(as.numeric) content = as.numeric(content)
  return(content)
}

#
# Day 6: Lanternfish ----
#

day6_input = get_advent(6, FALSE)


day6_df <- function(input) {

  #life = c(3,4,3,1,2)
  
  life = str_trim(input)
  life = str_split(life, ',')[[1]]
  
  df = as.data.frame(table(life))
  df$life = as.numeric(df$life)
  
  for(day in seq(1,256)) {
    newfish = sum(df$Freq[df$life==0]) # get number of new fish
    df$life = df$life - 1 # subtract 1 day from each life
    df$life[df$life == -1] = 6 # rollover to 6 days
    if(newfish) df = rbind(df, c(8, newfish)) # add new fish with 8 days
    if(day %in% c(80,256)) cat('after', day, 'days:', format(sum(df$Freq), scientific=F), 'fish\n')
  }

}


day6_vector <- function(input) {
  
  #days_to_birth = c(3,4,3,1,2)
  
  days_to_birth = str_trim(input)
  days_to_birth = str_split(days_to_birth, ',')[[1]]
  days_to_birth = as.numeric(days_to_birth)
  
  tally = c()
  for(d in seq(0,8)) tally[d+1] = as.numeric(sum(days_to_birth == d)) # eg: tally [1] 0 1 1 2 1 0 0 0 0
  
  for(day in seq(1,256)) {
    
    births = tally[1] # remember how many fish will give birth
    tally = tally[-1] # shift all tallies 1 day down (remove first item)
    tally[7] = tally[7] + births # add fish that gave birth to day 6
    tally[9] = births # add newborn fish to day 8
    if(day %in% c(80,256)) cat('after',day,'days:',format(sum(tally), scientific=F),'fish\n')
    
  }
  
}

day6_df(day6_input)
day6_vector(day6_input)

b = benchmark('df'=day6_df(day6_input),'vector'=day6_vector(day6_input))
b
b$elapsed / b$replications * 1000 # ms per iteration

#
# 7a
#

day7_input = c(16,1,2,0,4,2,7,1,2,14)
day7_input = get_advent(7)

day7a = function(day7_input) {
  df = data.frame(pos = seq(min(day7_input),max(day7_input)))
  df$fuel7a = sapply(df$pos, function(p) sum(abs(day7_input - p)))
  min(df$fuel7a)
}

#
# 7b
#

day7b = function(day7_input) {
  triangulat0r = function(n) (n^2+n)/2
  df$fuel7b = sapply(df$pos, function(p) sum(triangulat0r(abs(day7_input - p))))
  min(df$fuel7b)
}

b = benchmark('day7a'=day7a(day7_input),'day7b'=day7b(day7_input))
b
b$elapsed / b$replications * 1000 # ms per iteration
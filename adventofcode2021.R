library('httr')
library('stringr')
library('rbenchmark')
library('readr')

get_advent = function(day, year = 2021, raw = FALSE, trim = TRUE, split1 = '\n', split2 = ',', as.numeric = TRUE) {
  url = paste0('https://adventofcode.com/',year,'/day/',day,'/input')
  headers = c('cookie' = readLines("~/Progs/adventofcode/adventofcode2021-cookie.txt", w=F))
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
# Day 6: Lanternfish ------------------------------------------------------
#

#day6_input = c(3,4,3,1,2) # example data
day6_input = get_advent(6)

day6_df <- function(life) {

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

day6_vector <- function(days_to_birth) {
  
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
# Day 7: The Treachery of Whales ------------------------------------------
#

# day7_input = c(16,1,2,0,4,2,7,1,2,14) # example data
day7_input = get_advent(7)

day7a = function(day7_input) {
  df = data.frame(pos = seq(min(day7_input),max(day7_input)))
  df$fuel7a = sapply(df$pos, function(p) sum(abs(day7_input - p)))
  min(df$fuel7a)
}

day7b = function(day7_input) {
  triangulat0r = function(n) (n^2+n)/2
  df$fuel7b = sapply(df$pos, function(p) sum(triangulat0r(abs(day7_input - p))))
  min(df$fuel7b)
}

day7a(day7_input)
day7b(day7_input)

b = benchmark('day7a'=day7a(day7_input), 'day7b'=day7b(day7_input))
b
b$elapsed / b$replications * 1000 # ms per iteration

#
# Day 9: Smoke Basin ------------------------------------------------------
#

#
# parse input
#

# example task
day9_input = "2199943210
3987894921
9856789892
8767896789
9899965678
"

# real task
day9_input = get_advent(9, 2021, raw=T)

# Harm
#day9_input = read_file('https://raw.githubusercontent.com/HarmtH/aoc/master/2021/09/input.txt')

# raw input to matrix
input = str_trim(day9_input)
input = str_split(input, '\n')[[1]]
input = str_split(input,'')
mat = do.call(rbind, input)
mat = matrix(as.numeric(mat), ncol=ncol(mat))

#
# 9a
#

day9a = function(mat) {
  
  # function to test if a point is lower than any of its adjacent locations
  is.lowpoint = function(mat, r, c) {
    val = mat[r,c]
    if(r != 1         && mat[r-1,c] <= val) return(F)
    if(r != nrow(mat) && mat[r+1,c] <= val) return(F)
    if(c != 1         && mat[r,c-1] <= val) return(F)
    if(c != ncol(mat) && mat[r,c+1] <= val) return(F)
    return(T)
  }
  
  risklevel = 0
  
  for(row in seq_len(nrow(mat))) {
    for(col in seq_len(ncol(mat))) {
      if(is.lowpoint(mat,row,col)) {
        #cat("low point:",row,col,'\n')
        risklevel = risklevel + 1 + mat[row,col]
      }
    }
  }
  
  cat('answer for 9a:',risklevel,'\n')

}

day9a(mat)

#
# 9b
#

day9b = function(mat) {
  
  # create a map-overlay that holds the basin# per location
  basin = matrix(NA, nrow=nrow(mat), ncol=ncol(mat))
  nextbasinnr = 0
  
  # function to set a point and its neighbors to a basin# IF it is not already in a basin
  fill_basin = function(r, c, basinnr) {
    
    if(!is.na(basin[r,c]) || mat[r,c] == 9) return(F) # return immediately if basin was already set or it is 9
    basin[r,c] <<- basinnr
    
    if(r != 1        ) fill_basin(r-1, c, basinnr)
    if(r != nrow(mat)) fill_basin(r+1, c, basinnr)
    if(c != 1        ) fill_basin(r, c-1, basinnr)
    if(c != ncol(mat)) fill_basin(r, c+1, basinnr)
    
    return(T)
    
  }
  
  # fill the entire basins grid
  for(row in seq_len(nrow(mat))) {
    for(col in seq_len(ncol(mat))) {
      fill_basin(row, col, nextbasinnr)
      nextbasinnr = nextbasinnr + 1
    }
  }
  
  answer = prod(head(sort(table(basin),d=T),n=3))
  cat('answer for 9b:',answer,'\n')
  
}

day9b(mat)

b = benchmark('day9a'=day9a(mat), 'day9b'=day9b(mat))
b
b$elapsed / b$replications * 1000 # ms per iteration

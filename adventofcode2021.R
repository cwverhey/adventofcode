library('httr')
library('stringr')
library('rbenchmark')
library('readr')

#
# custom functions
#
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

smatch <- function(pattern, text, simple.result = F, ignore.case = F, perl = F, fixed = F, useBytes = F) {
  
  if(typeof(text) == "list") {
    
    if(class(text) == "data.frame")
      return(apply(text, c(1,2), function(text_item) smatch(pattern, text_item, simple.result, ignore.case, perl, fixed, useBytes) ))
    
    if(class(text) == "list")
      return(lapply(text, function(text_item) smatch(pattern, text_item, simple.result, ignore.case, perl, fixed, useBytes) ))
    
    stop(paste0("Don't know how to iterate over this input for `text`:", " typeof: ", typeof(text), ", mode: ", mode(text), ", class: ", class(text)))
  }
  
  if(length(text) > 1) {
    return(sapply(text, function(text_item) smatch(pattern, text_item, simple.result, ignore.case, perl, fixed, useBytes) ))
  }
  
  # get gregexec result
  regex = gregexec(pattern=pattern, text=text, ignore.case=ignore.case, perl=perl, fixed=fixed, useBytes=useBytes)
  r = regex[[1]]
  
  # check for failed match
  if(length(r) == 1 && r == -1) {
    r[1] = attributes(r)$match.start = attributes(r)$match.length = NA
    attributes(r)$matches = 0
    return(r)
  }
  
  # set no. of matches
  attributes(r)$matches = nrow(r)
  
  # get/set start and length values
  start = attributes(r)$match.start = r[,]
  length = attributes(r)$match.length
  
  # set substrings
  for(i in 1:length(start)) {
    r[i] <- substr(text, start[i], start[i] + length[i] - 1)
  }
  
  # return
  if(isFALSE(simple.result))
    return(r)
  else
    return(r[simple.result[1],simple.result[2]])
  
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

#
# Day 11: Dumbo Octopus ---------------------------------------------------
#

# example task
day11_input = '5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
'

day11_input = get_advent(11, 2021, raw=T)

# raw input to matrix
input = str_trim(day11_input)
input = str_split(input, '\n')[[1]]
input = str_split(input,'')
mat = do.call(rbind, input)
mat = matrix(as.numeric(mat), ncol=ncol(mat))

# get adjacent cells
adjacent = function(x,y) {
  df = data.frame(row=x+c(-1,-1,-1,0,0,1,1,1), col=y+c(-1,0,1,-1,1,-1,0,1))
  return(df[df$row>0 & df$col>0 & df$row<11 & df$col<11,])
}

# perform single step, return number of flashes
flash_step = function() {
  
  # perform single step
  mat <<- mat + 1 # add 1
  nflashes = 0 # store number of flashes
  while(T) {
    f = which(mat>9, arr.ind = T) # get all 'flashers' > 9
    if(length(f) == 0) break
    nflashes = nflashes + length(f)/2
    
    for(r in seq_len(nrow(f))) { # flash a single cell
      mat[f[r,'row'], f[r,'col']] <<- NA # set to NA so it won't increase again during this round
      neighbors = adjacent(f[r,'row'], f[r,'col']) # get neighbors
      for(n in seq_len(nrow(neighbors))) mat[neighbors[n,'row'], neighbors[n,'col']] <<- mat[neighbors[n,'row'], neighbors[n,'col']] + 1 # +1 to neighbors
    }
  }
  mat[is.na(mat)] <<- 0 # set flashed cells to 0
  return(nflashes)
}

# 11a

flash_count = 0
for(i in seq_len(100)) {
  flash_count = flash_count + flash_step()
}

cat('answer for 11a:',flash_count,'\n')

# 11b

step = 0
flashed = 0
while(flashed != nrow(mat)*ncol(mat)) {
  flashed = flash_step()
  step = step + 1
}

cat('answer for 11b:',step,'\n')

#
# Day 13: Transparent Origami ---------------------------------------------
#

day13_input = '6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
'

day13_input = get_advent(13, 2021, raw=T)

# split input in points and folds
input = str_split(day13_input,'\n\n')[[1]]

# create df of points
points = str_split(input[1],'\n')[[1]]
points = do.call(rbind, lapply(points, function(point) data.frame(x=str_split(point,',')[[1]][1], y=str_split(point,',')[[1]][2])))
points$x = as.numeric(points$x)
points$y = as.numeric(points$y)
print(points)

# create df of folding instructions
folds = smatch('fold along (\\w)=(\\d+)',input[2])
folds = as.data.frame(t(folds)[,c(2,3)])
colnames(folds) = c('dir','val')
folds$val = as.numeric(folds$val)

# function to display points
print_points = function(points) {
  for(y in 0:max(points$y)) {
    for(x in 0:max(points$x))
      if(sum(points$x == x & points$y == y)) cat('⬛️') else cat('⬜️')
    cat('\n')
  }
}

# function to perform OCR
# OCR
ocr_points = function(points) {
  
  width = max(points$x)+3
  height = max(points$y)+3
  
  mat = matrix(1,width,height)
  
  pngfile = tempfile()
  png(pngfile, width=width*10, height=height*10)
  
  for(i in seq_len(nrow(points))) mat[ points$x[i]+2 , height - points$y[i] - 1 ] = 0
  
  par(mar=c(0, 0, 0, 0))
  image(mat, axes = FALSE, col = grey(seq(0, 1, length = 256)))
  dev.off()
  
  url = 'https://api.ocr.space/parse/image'
  data = list(file = upload_file(pngfile), filetype = 'PNG', OCREngine = '2')
  r = POST(url, add_headers(apikey='5a64d478-9c89-43d8-88e3-c65de9999580'), body = data, encode = "multipart")
  cat(content(r)$ParsedResults[[1]]$ParsedText,'\n')
  
}

# loop over folds
for(fold_id in seq_len(nrow(folds))) {
  dir = folds$dir[fold_id]
  val = folds$val[fold_id]
  
  cat('folding over',dir,'=',val,'... ')
  
  # fold points
  points[points[,dir]>val,dir] = 2*val - points[points[,dir]>val,dir]
  
  # remove overlapping points
  points = unique(points)
  
  # print output
  cat(nrow(points),'points remaining\n')
  #print_points(points)
}

# print final result
print_points(points)

# get OCR recognition
ocr_points(points)

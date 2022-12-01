get_advent = function(day, year, raw = FALSE, trim = TRUE, split1 = '\n', split2 = ',', as.numeric = TRUE) {
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
# Day 13: Mine Cart Madness -----------------------------------------------
#

# print track function
print_track = function(track, carts = F) {
  for(y in seq_len(length(track))) {
    for(x in seq_len(length(track[[y]]))) {
      if(!isFALSE(carts) && !('crashed' %in% colnames(carts)) && sum(carts$x == x & carts$y == y) > 0)
        cat(sort(carts$dir[carts$x == x & carts$y == y], d=T)[1])
      else if(!isFALSE(carts) && ('crashed' %in% colnames(carts)) && sum(carts$x == x & carts$y == y & carts$crashed == FALSE) > 0)
        cat(sort(carts$dir[carts$x == x & carts$y == y & carts$crashed == FALSE], d=T)[1])
      else
        cat(track[[y]][x])
    }
    cat('\n')
  }
}

# single tick for task 13A
tick_a = function(map, carts) {
  
  # sort the carts into the order they will move this tick
  carts = carts[order(carts$y, carts$x),]
  
  # did we collide yet?
  collided = FALSE
  
  # move each cart, 1 tick
  for(n in seq_len(nrow(carts))) {
    
    # get cart from df
    cart = carts[n,]
    
    # move cart
    if(cart$dir == '<') cart$x = cart$x - 1
    if(cart$dir == '>') cart$x = cart$x + 1
    if(cart$dir == '^') cart$y = cart$y - 1
    if(cart$dir == 'v') cart$y = cart$y + 1
    
    # determine next direction
    road = map[[cart$y]][cart$x]
    all_dirs = c('^', '>', 'v', '<')
    # possible roads: -|+/\
    # - = don't change direction
    # | = don't change direction
    # + = turn based on turncount, update turncount
    if(road == '+') {
      if(cart$turncount == 0) cart$dir = all_dirs[(which(cart$dir == all_dirs)+2)%%4+1]
      if(cart$turncount == 2) cart$dir = all_dirs[(which(cart$dir == all_dirs))%%4+1]
      cart$turncount = (cart$turncount+1)%%3
    }
    
    # / = turn based on previous direction
    if(road == '/') {
      new_dirs = c('>', '^', '<', 'v')
      cart$dir = new_dirs[which(cart$dir == all_dirs)]
    }
    
    # \ = turn based on previous direction
    if(road == '\\') {
      new_dirs = c('<', 'v', '>', '^')
      cart$dir = new_dirs[which(cart$dir == all_dirs)]
    }
    
    # check for collision
    if(sum(carts$x == cart$x & carts$y == cart$y) > 0) {
      cat("boom!!!!!!\n")
      cat('X:', cart$x, ' Y:', cart$y, ' answer:', cart$x-1,',',cart$y-1, sep='', end='\n')
      cart$dir = 'X'
      collided = TRUE
    }
    
    # store updated cart
    carts[n,] = cart
    
    # break on collision
    if(collided) break
    
  }
  
  # print
  #print_track(map, carts)
  #carts
  
  # return updated carts
  return(list(carts=carts, collided=collided))
  
}

# single tick for task 13B
tick_b = function(map, carts) {
  
  # sort the carts into the order they will move this tick
  carts = carts[order(carts$y, carts$x),]
  
  # move each cart, 1 tick
  for(n in seq_len(nrow(carts))) {
    
    # get cart from df
    cart = carts[n,]
    
    # skip cart if it has crashed
    if(cart$crashed) next
    
    # move cart
    if(cart$dir == '<') cart$x = cart$x - 1
    if(cart$dir == '>') cart$x = cart$x + 1
    if(cart$dir == '^') cart$y = cart$y - 1
    if(cart$dir == 'v') cart$y = cart$y + 1
    
    # determine next direction
    road = map[[cart$y]][cart$x]
    all_dirs = c('^', '>', 'v', '<')
    # possible roads: -|+/\
    # - = don't change direction
    # | = don't change direction
    # + = turn based on turncount, update turncount
    if(road == '+') {
      if(cart$turncount == 0) cart$dir = all_dirs[(which(cart$dir == all_dirs)+2)%%4+1]
      if(cart$turncount == 2) cart$dir = all_dirs[(which(cart$dir == all_dirs))%%4+1]
      cart$turncount = (cart$turncount+1)%%3
    }
    
    # / = turn based on previous direction
    if(road == '/') {
      new_dirs = c('>', '^', '<', 'v')
      cart$dir = new_dirs[which(cart$dir == all_dirs)]
    }
    
    # \ = turn based on previous direction
    if(road == '\\') {
      new_dirs = c('<', 'v', '>', '^')
      cart$dir = new_dirs[which(cart$dir == all_dirs)]
    }
    
    # store updated cart
    carts[n,] = cart
    
    # check for collisions with this cart
    if(sum(carts$x == cart$x & carts$y == cart$y & carts$crashed == FALSE) > 1) {
      cat('crash at',cart$x, cart$y,'\n')
      carts$crashed[carts$x == cart$x & carts$y == cart$y] = TRUE
    }
  }
  
  # how many cars haven't crashed?
  uncrashed = sum(!carts$crashed)
  
  # print
  #print_track(map, carts)
  #carts
  
  # return updated carts
  return(list(carts=carts, uncrashed=uncrashed))
  
}

# load map and carts from input
load_map_and_carts = function(task) {
  
  # load map from task
  map = str_split(task, '\n')[[1]] # split at \n
  map = head(map, -1)                   # remove empty last line
  map = str_split(map, '')
  
  # load carts and remove them from map
  carts_hor = c('<','>'); carts_ver = c('^','v'); carts_all = c(carts_hor, carts_ver)
  carts_x = carts_y = carts_dir = c()
  
  for(y in seq_len(length(map))) {
    for(x in seq_len(length(map[[y]]))) {
      if(map[[y]][x] %in% carts_all) {
        carts_x = c(carts_x, x)
        carts_y = c(carts_y, y)
        carts_dir = c(carts_dir, map[[y]][x])
        if(map[[y]][x] %in% carts_hor) map[[y]][x] = '-' else map[[y]][x] = '|'
      }
    }
  }
  
  carts = data.frame(x = carts_x, y = carts_y, dir = carts_dir, turncount = 0)
  
  # print loaded map and carts
  print_track(map, carts)
  print(carts)
  
  return(list(map=map, carts=carts))
  
}

#
# task A
#

# example task
task2018_13a ="/->-\\        
|   |  /----\\
| /-+--+-\\  |
| | |  | v  |
\\-+-/  \\-+--/
 \\------/   
"

# real task
task2018_13a = get_advent(13, 2018, raw=T)

# load map, carts
x = load_map_and_carts(task2018_13a)
map = x$map; carts = x$carts; rm(x)

# run tick_a until collision
collided = FALSE
while(!collided) {
  result = tick_a(map, carts)
  carts = result$carts
  collided = result$collided 
}; rm(result)
print_track(map, carts)

#
# task B
#

# example task
# task2018_13b = "/>-<\\  
# |   |  
# | /<+-\\
# | | | v
# \\>+</ |
#   |   ^
#   \\<->/
# "

# real task
task2018_13b = get_advent(13, 2018, raw=T)

# load map, carts
x = load_map_and_carts(task2018_13b)
map = x$map; carts = x$carts; rm(x)

# add crashed status to cars
carts$crashed = FALSE

tick = 0
# run a tick
while(T) {
  tick = tick+ 1
  if(tick%%1000 == 0) cat('tick',tick,'\n')
  result = tick_b(map, carts)
  carts = result$carts
  if(result$uncrashed < 2) break
}; rm(result)

print_track(map, carts)
carts
cat('answer: ',subset(carts,crashed==FALSE)$x-1,',',subset(carts,crashed==FALSE)$y-1, sep='', end='\n')

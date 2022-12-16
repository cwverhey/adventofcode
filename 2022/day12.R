setwd(dirname(rstudioapi::getSourceEditorContext()$path))
source('functions.R')


# part 1 ------------------------------------------------------------------

year = 2022
day = 12
part = 1

task(year, day, part)

src <- input(year, day)

map <- strsplit(src, '', T) |> stringi::stri_list2matrix() |> t()

  rows <- nrow(map)
  cols <- ncol(map)

  start  <- c( (which(map=='S')-1)%%rows + 1, (which(map=='S')-1)%/%rows + 1 )
  map[start[1], start[2]] <- 'a'

  target <- c( (which(map=='E')-1)%%rows + 1, (which(map=='E')-1)%/%rows + 1 )
  map[target[1], target[2]] <- 'z'

  map <- mapply(\(x) which(letters == x), map) |> matrix(nrow = rows)

getValidNeighbors <- function(row, col) {

  neighbors <- list(c(row-1, col),
                    c(row+1, col),
                    c(row, col-1),
                    c(row, col+1))

  valid <- sapply(neighbors, \(point) {
    point[1] >= 1 && point[1] <= rows &&
      point[2] >= 1 && point[2] <= cols &&
      map[ point[1], point[2] ] - map[ row, col ] <= 1
  })

  return( neighbors[valid] )

}

distance_map <- map
  distance_map[] <- NA

todo <- list(start)
distance <- -1
target_reached <- FALSE

while(length(todo) && !target_reached) {

  distance <- distance + 1

  newtodo <- list()

  for(point in todo) if( is.na( distance_map[point[1],point[2]] ) ) {
    distance_map[point[1],point[2]] <- distance
    if( identical(point, target) ) target_reached <- TRUE
    newtodo <- append(newtodo, getValidNeighbors(point[1],point[2]))
  }
  todo <- newtodo

}

answer <- distance

submit(answer, year, day, part)


# part 2 ------------------------------------------------------------------

part = 2

task(year, day, part)

start_options <- which(map == 1) |> lapply(\(x) c( (x-1)%%rows + 1, (x-1)%/%rows + 1 ))

best_distance <- Inf

for(start in start_options) {

  distance_map <- map
  distance_map[] <- NA

  todo <- list(start)
  distance <- -1
  target_reached <- FALSE

  while(length(todo) && !target_reached && distance < best_distance) {

    distance <- distance + 1

    newtodo <- list()

    for(point in todo) if( is.na( distance_map[point[1],point[2]] ) ) {
      distance_map[point[1],point[2]] <- distance
      if( identical(point, target) ) target_reached <- TRUE
      newtodo <- append(newtodo, getValidNeighbors(point[1],point[2]))
    }
    todo <- newtodo

  }

  cat(start, distance, target_reached, '\n')
  if(target_reached) {
    print('yay')
    best_distance <- distance
  }

}

answer <- best_distance

submit(answer, year, day, part)


# git push ----------------------------------------------------------------

git_push()

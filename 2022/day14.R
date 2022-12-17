setwd(dirname(rstudioapi::getSourceEditorContext()$path))
source('functions.R')


# part 1 ------------------------------------------------------------------

year = 2022
day = 14
part = 1

task(year, day, part)

src <- input(year, day)

addRocks <- function() {
  for(path in rockPaths) for(i in seq_along(path[-1])) {
    start <- strsplit(path[i], ',')[[1]] |> as.numeric()
    end <- strsplit(path[i+1], ',')[[1]] |> as.numeric()
    for(col in start[1]:end[1]) for(row in start[2]:end[2]) {
      map[row, col] <<- '#'
    }
  }
}

printMap <- function() {
  for(row in ylims[1]:ylims[2]) {
    for(col in xlims[1]:xlims[2]) {
      val <- map[row,col]
      cat(ifelse(is.na(val), '·', val))
    }
    cat('\n')
  }
}

addSand <- function(row, col) {

  if( is.na(map[row+1, col]) ) return(addSand(row+1, col))
  if( is.na(map[row+1, col-1]) ) return(addSand(row+1, col-1))
  if( is.na(map[row+1, col+1]) ) return(addSand(row+1, col+1))
  map[row, col] <<- 'o'

}

rockPaths <- strsplit(src, ' -> ', fixed=T)
  xlims <- unlist(rockPaths) |> append("500,0") |> strsplit(',') |> sapply(\(coords) coords[1]) |> as.numeric() |> range()
  ylims <- unlist(rockPaths) |> append("500,0") |> strsplit(',') |> sapply(\(coords) coords[2]) |> as.numeric() |> range()

map <- matrix(nrow = ylims[2], ncol = xlims[2])
  addRocks()

printMap()

while(T) addSand(0, 500)

printMap()

answer <- which(map == "o") |> length()

submit(answer, year, day, part)


# part 2 ------------------------------------------------------------------

part = 2

task(year, day, part)

addSand <- function(row, col) {

  if( is.na(map[row+1, col]) ) return(addSand(row+1, col))
  if( is.na(map[row+1, col-1]) ) return(addSand(row+1, col-1))
  if( is.na(map[row+1, col+1]) ) return(addSand(row+1, col+1))
  if( ! is.na(map[row, col]) ) stop('error!')
  map[row, col] <<- 'o'

}

rockPaths <- strsplit(src, ' -> ', fixed=T)
  xlims <- unlist(rockPaths) |> append("500,0") |> strsplit(',') |> sapply(\(coords) coords[1]) |> as.numeric() |> range()
  ylims <- unlist(rockPaths) |> append("500,0") |> strsplit(',') |> sapply(\(coords) coords[2]) |> as.numeric() |> range()

floorPath <- c(sprintf("%s,%s", 500 - ylims[2] - 4, ylims[2]+2), sprintf("%s,%s", 500 + ylims[2] + 4, ylims[2]+2))
  rockPaths <- append(rockPaths, list(floorPath))
  xlims <- unlist(rockPaths) |> append("500,0") |> strsplit(',') |> sapply(\(coords) coords[1]) |> as.numeric() |> range()
  ylims <- unlist(rockPaths) |> append("500,0") |> strsplit(',') |> sapply(\(coords) coords[2]) |> as.numeric() |> range()

map <- matrix(nrow = ylims[2], ncol = xlims[2])
addRocks()

printMap()

while(T) addSand(0, 500)

printMap()

answer <- which(map == "o") |> length() + 1

submit(answer, year, day, part)


# git push ----------------------------------------------------------------

git_push()

setwd(dirname(rstudioapi::getSourceEditorContext()$path))
source('functions.R')

library('tibble')

# part 1 ------------------------------------------------------------------

year = 2022
day = 15
part = 1

task(year, day, part)

src <- input(year, day)

target_y <- 2000000

sensors <- stringr::str_match_all(src, "-?\\d+") |> lapply(as.vector) |> lapply(as.numeric)

# get range of impossible x positions per sensor
x_ranges <- list()
for(sensor in sensors) {

  distance <- abs(sensor[1]-sensor[3]) + abs(sensor[2]-sensor[4])
  distance_y <- abs(sensor[2]-target_y)
  distance_x <- distance - distance_y

  if(distance_x < 1) next

  xmin <- sensor[1] - distance_x
  xmax <- sensor[1] + distance_x

  if(sensor[4] == target_y) {
    if(sensor[3] == xmin) xmin <- xmin+1
    if(sensor[3] == xmax) xmax <- xmax-1
  }

  cat(xmin, xmax, '\n')
  x_ranges <- append(x_ranges, list(c(xmin, xmax)))

}

# merge impossible ranges
merge_ranges <- function(ranges) {
  new_ranges <- list()
  for(range in ranges) {
    success <- F
    for(i in seq_along(new_ranges)) {
      #cat(range, new_ranges[[i]], '\n')
      if((new_ranges[[i]][1] <= range[1] && range[1] <= new_ranges[[i]][2] + 1)
         ||
         (new_ranges[[i]][1] <= range[2] + 1 && range[2] <= new_ranges[[i]][2] + 1)
         ||
         (range[1] <= new_ranges[[i]][1] && new_ranges[[i]][2] <= range[2])) {
        new_ranges[[i]] <- c(min(range[1], new_ranges[[i]][1]), max(range[2], new_ranges[[i]][2]))
        success <- T
      }
    }
    if(!success) new_ranges <- append(new_ranges, list(range))
  }
  if(length(new_ranges) < length(ranges)) new_ranges <- merge_ranges(new_ranges)

  return(new_ranges)
}

x_range <- merge_ranges(x_ranges)

answer <- sapply(x_range, \(x) x[2]-x[1]+1) |> sum()

submit(answer, year, day, part)

# part 2 ------------------------------------------------------------------

part = 2

task(year, day, part)

# not in detected area
# 0 ≤ x ≤ 4000000
# 0 ≤ y ≤ 4000000
# tuning freq = x × 4000000 + y

find_impossible_x <- function(target_y) {

  x_ranges <- list()
  for(sensor in sensors) {

    distance <- abs(sensor[1]-sensor[3]) + abs(sensor[2]-sensor[4])
    distance_y <- abs(sensor[2]-target_y)
    distance_x <- distance - distance_y

    if(distance_x < 1) next

    xmin <- sensor[1] - distance_x
    xmax <- sensor[1] + distance_x

    x_ranges <- append(x_ranges, list(c(xmin, xmax)))

  }

  x_ranges <- merge_ranges(x_ranges)

  return(x_ranges)
}

for(y in 4000000:0) {
  if(y %% 10000 == 0) cat(y, '\n')
  find_impossible_x(y)
}

answer <- (x[[1]][2]+1) * 4000000 + y
submit(answer, year, day, part)



# part 2 - version 2 ------------------------------------------------------

sensors <- stringr::str_match_all(src, "-?\\d+") |> do.call(rbind, args = _) |> as.integer()
sensors <- data.frame(matrix(sensors, ncol=4, byrow=TRUE))
colnames(sensors) <- c('Sx','Sy','Bx','By')
sensors$dist <- abs(sensors$Sx-sensors$Bx) + abs(sensors$Sy-sensors$By)

find_impossible_x <- function(target_y) {

  dist_x <- sensors$dist - abs(sensors$Sy-target_y)

  Sx <- sensors$Sx[dist_x > 0]
  dist_x <- dist_x[dist_x > 0]

  range_starts <- Sx - dist_x
  range_ends <- Sx + dist_x

  ord <- order(range_starts)
  range_starts <- range_starts[ord]
  range_ends <- range_ends[ord]

  end <- range_ends[1]
  for(i in seq_along(range_starts)) {
    if(range_starts[i] > end + 1) {
      return(end+1)
    } else {
      end <- max(end, range_ends[i])
    }
  }

  return(FALSE)

}

for(y in 3000000:4000000) {
  if(y %% 10000 == 0) cat(y, '\n')
  x <- find_impossible_x(y)
  if(!isFALSE(x)) { stop('done; x=', x, ' y=',y) }
}

answer <- x * 4000000 + y


# git push ----------------------------------------------------------------

git_push()

setwd(dirname(rstudioapi::getSourceEditorContext()$path))
source('functions.R')


# part 1 ------------------------------------------------------------------

year = 2022
day = 2
part = 1

task(year, day, part)

src <- input(year, day, splitlines = T)

games <- stringr::str_replace_all(src, c('A'='r', 'B'='p', 'C'='s', 'X'='r', 'Y'='p', 'Z'='s'))

scoring_shape <- c('r' = 1, 'p' = 2, 's' = 3)
scoring_outcome <- c('r r' = 3, 'r p' = 6, 'r s' = 0,
                     'p r' = 0, 'p p' = 3, 'p s' = 6,
                     's r' = 6, 's p' = 0, 's s' = 3)

points_shapes <- scoring_shape[ vapply(games, \(x) substr(x, 3, 3), '') ]
points_outcomes <- scoring_outcome[ games ]

answer <- sum(points_shapes) + sum(points_outcomes)

submit(answer, year, day, part)

# part 2 ------------------------------------------------------------------

part = 2

task(year, day, part)

src <- input(year, day, splitlines = T)

games <- stringr::str_replace_all(src, c('A'='r', 'B'='p', 'C'='s'))

shapes <- c('r', 'p', 's')
objectives <- c('X' = -1, 'Y' = 0, 'Z' = +1)
get_response_shape <- function(line) {
  shape <- which(shapes == substr(line, 1, 1))
  objective <- objectives[ substr(line, 3, 3) ]
  req <- shape + objective
  if(req == 0) req <- 3
  if(req == 4) req <- 1
  return( paste0(substr(line, 1, 2), shapes[req]) )
}

games <- vapply(games, get_response_shape, '')

points_shapes <- scoring_shape[ vapply(games, \(x) substr(x, 3, 3), '') ]
points_outcomes <- scoring_outcome[ games ]

answer <- sum(points_shapes) + sum(points_outcomes)

submit(answer, year, day, part)

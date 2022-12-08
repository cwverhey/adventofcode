setwd(dirname(rstudioapi::getSourceEditorContext()$path))
source('functions.R')


# part 1 ------------------------------------------------------------------

year = 2022
day = 8
part = 1

task(year, day, part)

src <- input(year, day, splitlines = T)

# create matrix from src
cols <- nchar(src[1])
rows <- length(src)
map <- matrix( strsplit(paste(src, collapse = ''), '')[[1]] |> as.numeric(), nrow = rows, ncol = cols, byrow = T)
visible <- matrix( rep(FALSE, cols*rows), nrow = rows, ncol = cols, byrow = T)

# raytracing function
ray <- function(row_start, row_end, row_dir, col_start, col_end, col_dir) {

  peak <- -1
  for(row in seq(row_start, row_end, row_dir))
    for(col in seq(col_start, col_end, col_dir))
      if(map[row,col] > peak) {
        visible[row,col] <<- TRUE
        peak <- map[row,col]
        }
}

# raytracing
for(row in seq_len(rows)) ray(row, row, 0, 1, cols, +1)  # left to right
for(row in seq_len(rows)) ray(row, row, 0, cols, 1, -1)  # right to left
for(col in seq_len(cols)) ray(1, rows, +1, col, col, 0)  # top to bottom
for(col in seq_len(cols)) ray(rows, 1, -1, col, col, 0)  # bottom to top

answer <- sum(visible)

submit(answer, year, day, part)


# part 2 ------------------------------------------------------------------

part = 2

task(year, day, part)

count_viewable <- function(trees) {

  height <- trees[1]
  view <- trees[-1]

  for(i in seq_along(view)) if(view[i] >= height) break
  return( ifelse(is.null(i), 0, i) )

}

scenic <- function(row, col) {

  height <- map[row, col]

  up    <- map[row:1,    col]
  down  <- map[row:rows, col]

  left  <- map[row, col:1]
  right <- map[row, col:cols]

  counts <- sapply( list(up, down, left, right), count_viewable)
  score  <- prod(counts)

  return(score)

}

scenic_scores <- matrix( rep(numeric(0), cols*rows), nrow = rows, ncol = cols, byrow = T)
for(row in seq_len(rows))
  for(col in seq_len(cols))
    scenic_scores[row, col] <- scenic(row, col)

answer <- max(scenic_scores)

submit(answer, year, day, part)


# git push ----------------------------------------------------------------

system(sprintf('git add "%s"', basename(rstudioapi::getSourceEditorContext()$path)))
system(sprintf('git commit -m "%s"', basename(rstudioapi::getSourceEditorContext()$path)))
system('git push')

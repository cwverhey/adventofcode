setwd(dirname(rstudioapi::getSourceEditorContext()$path))
source('functions.R')


# part 1 ------------------------------------------------------------------

year = 2022
day = 20
part = 1

task(year, day, part)

src <- input(year, day) |> as.numeric()

ord <- seq_along(src)

for(i in seq_along(src)) {
  pos <- which(ord == i)  # current position
  mov <- (pos + src[i]) %% (length(src)-1)  # where to move
  ord <- append(ord[-pos], ord[pos], after=mov-1)
}

values <- src[ord]

answer <- c(1000, 2000, 3000) |>
  sapply(\(x) values[x + which(values == 0)]) |>
  sum()

submit(answer, year, day, part)  # 10707


# part 2 ------------------------------------------------------------------

part = 2

task(year, day, part)

key <- 811589153
data <- src * key

ord <- seq_along(data)

for(x in 1:10) for(i in seq_along(data)) {
  pos <- which(ord == i)  # current position
  mov <- (pos + data[i]) %% (length(data)-1)  # where to move
  if(mov < 2) mov <- mov + length(data) - 1
  ord <- append(ord[-pos], ord[pos], after=mov-1)
}

values <- data[ord]

answer <- c(1000, 2000, 3000) |>
  sapply(\(x) values[x + which(values == 0)]) |>
  sum()

submit(answer, year, day, part)


# git push ----------------------------------------------------------------

git_push()

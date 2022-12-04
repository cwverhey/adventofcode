setwd(dirname(rstudioapi::getSourceEditorContext()$path))
source('functions.R')


# part 1 ------------------------------------------------------------------

year = 2022
day = 4
part = 1

task(year, day, part)

src <- input(year, day, splitlines = T)

overlap <- sapply(src, \(x) {
  x <- strsplit(x, ',', fixed=T)[[1]]
  x <- strsplit(x, '-', fixed=T)
  x <- lapply(x, as.numeric)
  return(
    (x[[1]][1] <= x[[2]][1] && x[[1]][2] >= x[[2]][2]) ||
    (x[[1]][1] >= x[[2]][1] && x[[1]][2] <= x[[2]][2])
  )
})

answer <- sum(overlap)

submit(answer, year, day, part)


# part 2 ------------------------------------------------------------------

part = 2

task(year, day, part)

overlap <- sapply(src, \(x) {
  x <- strsplit(x, ',', fixed=T)[[1]]
  x <- strsplit(x, '-', fixed=T)
  x <- lapply(x, as.numeric)
  x <- x[ sapply(x, \(y) y[1]) |> order() ]
  return(x[[1]][2] >= x[[2]][1])
})

answer <- sum(overlap)

submit(answer, year, day, part)


# git push ----------------------------------------------------------------

system(sprintf('git add "%s"', basename(rstudioapi::getSourceEditorContext()$path)))
system(sprintf('git commit -m "%s"', basename(rstudioapi::getSourceEditorContext()$path)))
system('git push')

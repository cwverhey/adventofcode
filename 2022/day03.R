setwd(dirname(rstudioapi::getSourceEditorContext()$path))
source('functions.R')


# part 1 ------------------------------------------------------------------

year = 2022
day = 3
part = 1

task(year, day, part)

src <- input(year, day, splitlines = T)

letterValues <- 1:52
names(letterValues) <- c(letters[1:26],LETTERS[1:26])

overlapValues <- sapply(src, \(x) {
  x <- strsplit(x, '', T)[[1]]
  x <- split(x, rep(c(1, 2), each = length(x) / 2))
  overlap <- intersect(x[[1]], x[[2]])
  return(letterValues[overlap])
})

answer <- sum(overlapValues)

submit(answer, year, day, part)


# part 2 ------------------------------------------------------------------

part = 2

task(year, day, part)

elfGroups <- split(src, rep(seq(length(src)/3), each = 3))

overlapValues <- sapply(elfGroups, \(x) {
  x <- strsplit(x, '')
  overlap <- intersect(intersect(x[[1]], x[[2]]), x[[3]])
  return(letterValues[overlap])
})

answer <- sum(overlapValues)

submit(answer, year, day, part)


# git push ----------------------------------------------------------------

system(sprintf('git add "%s"', basename(rstudioapi::getSourceEditorContext()$path)))
system(sprintf('git commit -m "%s"', basename(rstudioapi::getSourceEditorContext()$path)))
system('git push')

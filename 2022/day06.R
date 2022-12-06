setwd(dirname(rstudioapi::getSourceEditorContext()$path))
source('functions.R')


# part 1 ------------------------------------------------------------------

year = 2022
day = 6
part = 1

task(year, day, part)

src <- input(year, day, splitlines = T)

line <- strsplit(src, '')[[1]]
for(i in 4:length(line)) {
  x <- line[(i-3):i] |> unique(x) |> length()
  if(x == 4) break
}

answer <- i

submit(answer, year, day, part)


# part 2 ------------------------------------------------------------------

part = 2

task(year, day, part)

for(i in 14:length(line)) {
  x <- line[(i-13):i] |> unique(x) |> length()
  if(x == 14) break
}

answer <- i

submit(answer, year, day, part)


# git push ----------------------------------------------------------------

system(sprintf('git add "%s"', basename(rstudioapi::getSourceEditorContext()$path)))
system(sprintf('git commit -m "%s"', basename(rstudioapi::getSourceEditorContext()$path)))
system('git push')

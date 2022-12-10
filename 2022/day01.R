setwd(dirname(rstudioapi::getSourceEditorContext()$path))
source('functions.R')


# part 1 ------------------------------------------------------------------

year = 2022
day = 1
part = 1

task(year, day, part)

src <- input(year, day, raw = T)

calories <- strsplit(src, '\n\n')[[1]]
calories <- vapply(calories,
                   \(x) {
                     sum(as.numeric(strsplit(x, '\n')[[1]]))
                   },
                   0)
answer <- max(calories)

submit(answer, year, day, part)

# part 2 ------------------------------------------------------------------

part = 2

task(year, day, part)

answer <- calories |> sort() |> tail(n=3) |> sum()

submit(answer, year, day, part)


# git push ----------------------------------------------------------------

git_push()

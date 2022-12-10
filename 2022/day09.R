setwd(dirname(rstudioapi::getSourceEditorContext()$path))
source('functions.R')


# part 1 ------------------------------------------------------------------

year = 2022
day = 9
part = 1

task(year, day, part)

src <- input(year, day, splitlines = T)

Hpos <- c(x = 0, y = 0)
Tpos <- c(x = 0, y = 0)
Tposlog <- list(Tpos)

constrain <- function(x, minx, maxx) sapply(x, \(y) max(minx, min(y, maxx)))

movement <- list('U' = c(0, 1), 'D' = c(0, -1), 'L' = c(-1, 0), 'R' = c(1, 0))

for(moves in src) {

  parts <- strsplit(moves, ' ', fixed = T)[[1]]
  direction <- parts[1]
  times <- parts[2] |> as.numeric()

  for(. in seq_len(times)) {
    Hpos <- Hpos + movement[[direction]]

    if( max(abs(Hpos-Tpos)) > 1 ) {
      Tpos <- Tpos + constrain( Hpos - Tpos, -1, 1)
      Tposlog <- append(Tposlog, list(Tpos))
    }

    # cat(moves, '➡️ H', Hpos, '/ T', Tpos, '\n')
  }

}

answer <- length(unique(Tposlog))

submit(answer, year, day, part)


# part 2 ------------------------------------------------------------------

part = 2

task(year, day, part)

ropePos <- lapply(1:10, \(x) c(x=0, y=0))
Tposlog <- list(ropePos[[10]])

for(moves in src) {

  parts <- strsplit(moves, ' ', fixed = T)[[1]]
  direction <- parts[1]
  times <- parts[2] |> as.numeric()

  for(. in seq_len(times)) {

    ropePos[[1]] <- ropePos[[1]] + movement[[direction]]

    for(i in 2:10) if( max(abs(ropePos[[i-1]]-ropePos[[i]])) > 1 ) {
      ropePos[[i]] <- ropePos[[i]] + constrain( ropePos[[i-1]] - ropePos[[i]], -1, 1)
      if(i == 10) Tposlog <- append(Tposlog, list(ropePos[[10]]))
    }

  }

}

answer <- length(unique(Tposlog))

submit(answer, year, day, part)


# git push ----------------------------------------------------------------

system(sprintf('git add "%s"', basename(rstudioapi::getSourceEditorContext()$path)))
system(sprintf('git commit -m "%s"', basename(rstudioapi::getSourceEditorContext()$path)))
system('git push')

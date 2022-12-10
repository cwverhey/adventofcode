setwd(dirname(rstudioapi::getSourceEditorContext()$path))
source('functions.R')


# part 1 ------------------------------------------------------------------

year = 2022
day = 10
part = 1

task(year, day, part)

src <- input(year, day)

cycle <- 1
X <- 1
Xlog <- data.frame(cycle = cycle, X = X)

for(command in src) {

  if(command == "noop") {
    cycle <- cycle + 1
    next
  }

  if(startsWith(command, "addx ")) {
    cycle <- cycle + 2
    X <- X + strsplit(command, ' ', fixed=T)[[1]][2] |> as.numeric()
    Xlog[nrow(Xlog) + 1,] = list(cycle, X)
  }
}

signal_strengths <- sapply(seq(20, 220, 40),
                           \(x) {
                             x * Xlog$X[Xlog$cycle <= x] |> tail(n = 1)
                           })

answer <- sum(signal_strengths)

submit(answer, year, day, part)


# part 2 ------------------------------------------------------------------

part = 2

task(year, day, part)

X <- 1
Xlog <- c(X)

for(cmd in src) {
  Xlog <- c(Xlog, X)
  if(cmd != "noop") {
    X <- X + (strsplit(cmd, ' ', fixed=T)[[1]][2] |> as.numeric())
    Xlog <- c(Xlog, X)
  }
}

for(cycle in 1:240) {

  crt_position <- (cycle -1) %% 40

  cat(
    ifelse( abs(crt_position - Xlog[cycle]) <= 1,
          '⬛️',
          '⬜️')
  )

  if(cycle%%40 == 0) cat('\n')
}

answer <- "ZUPRFECL"

submit(answer, year, day, part)


# git push ----------------------------------------------------------------

git_push()

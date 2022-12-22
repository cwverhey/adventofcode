setwd(dirname(rstudioapi::getSourceEditorContext()$path))
source('functions.R')


# part 1 ------------------------------------------------------------------

year = 2022
day = 21
part = 1

task(year, day, part)

src <- input(year, day, url = 'https://adventofcode.com/2022/day/21/input')

monkeys <- strsplit(src, ': ', T) |>
  unlist() |>
  matrix(ncol = 2, byrow = T) |>
  as_tibble()
colnames(monkeys) <- c('name', 'cmd')
monkeys$value <- as.numeric(monkeys$cmd)

monkeys$deps <- monkeys$cmd |>
    strsplit(' ', T) |>
    lapply(\(row) {
      sapply(row, \(d) which(monkeys$name == d) ) |>
        unlist() |> unname()
      })

monkeys$op <- monkeys$cmd |> stringr::str_match('[+-/*]') |> as.vector()

while(T) {
  change <- F

  for(row in which(is.na(monkeys$value))) {
    deps.na <- sapply(monkeys$deps[[row]], \(x) is.na(monkeys$value[[x]]))
    if(!any(deps.na)) {

      change <- T

      deps <- sapply(monkeys$deps[[row]], \(x) monkeys$value[[x]])
      if(monkeys$op[[row]] == '+') {
        monkeys$value[[row]] <- deps[1] + deps[2]
      } else if(monkeys$op[[row]] == '-') {
        monkeys$value[[row]] <- deps[1] - deps[2]
      } else if(monkeys$op[[row]] == '*') {
        monkeys$value[[row]] <- deps[1] * deps[2]
      } else if(monkeys$op[[row]] == '/') {
        monkeys$value[[row]] <- deps[1] / deps[2]
      }

      print(row)
    }
  }

  if(!change) break
}

answer <- monkeys$value[monkeys$name=="root"]

submit(answer, year, day, part)


# part 2 ------------------------------------------------------------------

library('Ryacas')

part = 2

task(year, day, part)

src <- input(year, day, url = 'https://adventofcode.com/2022/day/21/input')

# load input to tibble
monkeys <- strsplit(src, ': ', T) |>
  unlist() |>
  matrix(ncol = 2, byrow = T) |>
  as_tibble()
colnames(monkeys) <- c('name', 'cmd')
monkeys$value <- as.numeric(monkeys$cmd)

monkeys$op <- monkeys$cmd |> stringr::str_match('[+-/*]') |> as.vector()

# remove human and root
rootcmd <- monkeys$cmd[monkeys$name == "root"] |> strsplit(' ', T)
monkeys <- monkeys[! monkeys$name %in% c('humn','root'),]

# get dependencies as indices
monkeys$deps <- monkeys$cmd |>
  strsplit(' ', T) |>
  lapply(\(row) {
    sapply(row, \(d) which(monkeys$name == d) ) |>
      unlist() |> unname()
  })

# fill values where possible
while(T) {
  change <- F

  for(row in which(is.na(monkeys$value))) {
    deps.na <- sapply(monkeys$deps[[row]], \(x) is.na(monkeys$value[[x]]))
    if(!any(deps.na) && length(deps.na) == 2) {

      change <- T

      deps <- sapply(monkeys$deps[[row]], \(x) monkeys$value[[x]])
      if(monkeys$op[[row]] == '+') {
        monkeys$value[[row]] <- deps[1] + deps[2]
      } else if(monkeys$op[[row]] == '-') {
        monkeys$value[[row]] <- deps[1] - deps[2]
      } else if(monkeys$op[[row]] == '*') {
        monkeys$value[[row]] <- deps[1] * deps[2]
      } else if(monkeys$op[[row]] == '/') {
        monkeys$value[[row]] <- deps[1] / deps[2]
      }

      print(row)
    }
  }

  if(!change) break
}

# write out comparison
getMonkey <- function(name) {
  id <- which(monkeys$name == name)
  if(length(id) != 1) return(name)

  val <- monkeys$value[[id]]
  if(!is.na(val)) return(val)

  parts <- strsplit(monkeys$cmd[[id]], ' ', T)[[1]]
  return(sprintf('(%s %s %s)', getMonkey(parts[1]), parts[2], getMonkey(parts[3])))
}

eq <- paste(getMonkey(rootcmd[[1]][1]), '==', getMonkey(rootcmd[[1]][3]))
solution <- solve(ysym(eq), "humn")
answer <- solution |> stringr::str_extract('\\d+') |> as.numeric()

submit(answer, year, day, part)


# git push ----------------------------------------------------------------

git_push()

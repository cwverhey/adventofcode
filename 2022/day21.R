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

# (optional) fill values where possible
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


# part 2 - without external solving library -------------------------------

part = 2

task(year, day, part)

src <- input(year, day, url = 'https://adventofcode.com/2022/day/21/input')

# load input to tibble
data <- strsplit(src, ': ', T) |>
  unlist() |>
  matrix(ncol = 2, byrow = T)

monkeys <- data.frame(cmd = data[,2], val = as.numeric(data[,2]))
rownames(monkeys) <- data[,1]

# recursively lookup the value to a monkey's name; return list of [value|name] + operation + [value|name] if numerical value isn't available
getMonkey <- function(name) {
  if(name == "humn") return(name)

  val <- monkeys[name, 'val']
  if(!is.na(val)) return(val)

  parts <- strsplit(monkeys[name, 'cmd'], ' ', T)[[1]]
  part_vals <- list(getMonkey(parts[1]), getMonkey(parts[3]))
  if( part_vals |> sapply(is.numeric) |> all() ) return(switch(parts[2],
                                                               "+" = part_vals[[1]] + part_vals[[2]],
                                                               "-" = part_vals[[1]] - part_vals[[2]],
                                                               "*" = part_vals[[1]] * part_vals[[2]],
                                                               "/" = part_vals[[1]] / part_vals[[2]]))

  return(list(part_vals[[1]], parts[2], part_vals[[2]]))
}

# recursively strip a tree of operations level by level, while performing the inverse of the same operation on a number
simplify <- function(listtree, number) {

  # are we there yet?
  if(length(listtree) == 1) {
    cat(sprintf('%s == %s\n', listtree, number))
    return(number)
  }

  # split this level of the tree into: * [num]eric part, * rest of [tree], * [order] they're in, * [op]eration
  if(is.numeric(listtree[[1]])) {
    tree <- listtree[[3]]
    num <- listtree[[1]]
    order <- 'NOT'
  } else if(is.numeric(listtree[[3]])) {
    tree <- listtree[[1]]
    num <- listtree[[3]]
    order <- 'TON'
  }
  op <- listtree[[2]]

  # simplify this level depending on op and order
  if(op == '+') {
    return(simplify(tree, number - num))

  } else if(op == '-') {
    if(order == 'TON') {
      return(simplify(tree, num + number))
    } else {
      return(simplify(tree, num - number))
    }

  } else if(op == '*') {
    return(simplify(tree, number / num))

  } else if(op == '/') {
    if(order == 'TON') {
      return(simplify(tree, num * number))
    } else {
      return(simplify(tree, num / number))
    }

  }

}

# get equation for root
rootparts <- monkeys['root','cmd'] |> strsplit(' ', T) |> unlist()
cat('task:', rootparts[1], '==', rootparts[3])

# get values for each half of the equation
sides <- list(getMonkey(rootparts[1]), getMonkey(rootparts[3]))

# simplify
if(is.numeric(sides[[2]])) {
  answer <- simplify(sides[[1]], sides[[2]])
} else {
  answer <- simplify(sides[[2]], sides[[1]])
}

submit(answer, year, day, part)


# part 2 - minimal code ---------------------------------------------------

library('Ryacas')

part = 2

task(year, day, part)

src <- input(year, day, url = 'https://adventofcode.com/2022/day/21/input')

# load input to tibble
data <- strsplit(src, ': ', T) |> unlist() |> matrix(ncol = 2, byrow = T)
monkeys <- data.frame(cmd = data[,2])
rownames(monkeys) <- data[,1]

# recursively get value for a monkey by name
getMonkey <- function(name) {
  if(name == "humn") return("humn")

  val <- strsplit(monkeys[[name, 'cmd']], ' ', T)[[1]]
  if(length(val) == 1) return(val)

  return(sprintf('(%s %s %s)', getMonkey(val[1]), val[2], getMonkey(val[3])))
}

eq <- paste(getMonkey(rootcmd[[1]][1]), '==', getMonkey(rootcmd[[1]][3]))
answer <- solve(ysym(eq), "humn") |> stringr::str_extract('\\d+') |> as.numeric()

submit(answer, year, day, part)


# git push ----------------------------------------------------------------

git_push()

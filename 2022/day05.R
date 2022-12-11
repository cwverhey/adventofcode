setwd(dirname(rstudioapi::getSourceEditorContext()$path))
source('functions.R')


# part 1 ------------------------------------------------------------------

year = 2022
day = 5
part = 1

task(year, day, part)

src <- input(year, day, raw = T)

print_stacks <- function() for(stack in seq_along(stacks)) cat(stack, paste(stacks[[stack]], collapse=''), '\n')

x <- strsplit(src, '\n\n')[[1]]  # split initial stack from moves
x <- strsplit(x, '\n')  # split lines

# read initial stack
y <- rev(x[[1]])
stack_positions <- gregexpr('\\d+', y[1])[[1]] |> as.numeric()

stacks <- vector(mode="list", length=length(stack_positions))
for(row in 2:length(y)) for(col in seq_along(stack_positions)) {
  char <- substr(y[row], stack_positions[col], stack_positions[col])
  if(char != " ") stacks[[col]] <- c(stacks[[col]], char)
}

# read moves
moves <- stringr::str_match_all(x[[2]], '\\d+')
moves <- lapply(moves, \(x) as.numeric(x[,1]))

# process moves
for(move in moves) {
  print(move)
  # move move[1] elements from stacks[[ move[2] ]], to stacks[[ move[3] ]]
  stacks[[ move[3] ]] <- c( stacks[[ move[3] ]], tail(stacks[[ move[2] ]], n = move[1]) |> rev() )
  stacks[[ move[2] ]] <- head( stacks[[ move[2] ]], n = - move[1] )
  print_stacks()
  #readline("press enter")
}

# compile answer
answer <- sapply(stacks, \(x) tail(x, n=1)) |> paste(collapse = '')

submit(answer, year, day, part)


# part 2 ------------------------------------------------------------------

part = 2

task(year, day, part)

x <- strsplit(src, '\n\n')[[1]]  # split initial stack from moves
x <- strsplit(x, '\n')  # split lines

# read initial stack
y <- rev(x[[1]])
stack_positions <- gregexpr('\\d+', y[1])[[1]] |> as.numeric()

stacks <- vector(mode="list", length=length(stack_positions))
for(row in 2:length(y)) for(col in seq_along(stack_positions)) {
  char <- substr(y[row], stack_positions[col], stack_positions[col])
  if(char != " ") stacks[[col]] <- c(stacks[[col]], char)
}

# read moves
moves <- stringr::str_match_all(x[[2]], '\\d+')
moves <- lapply(moves, \(x) as.numeric(x[,1]))

# process moves
for(move in moves) {
  print(move)
  # move move[1] elements from stacks[[ move[2] ]], to stacks[[ move[3] ]]
  stacks[[ move[3] ]] <- c( stacks[[ move[3] ]], tail(stacks[[ move[2] ]], n = move[1]) )
  stacks[[ move[2] ]] <- head( stacks[[ move[2] ]], n = - move[1] )
  print_stacks()
  #readline("press enter")
}

# compile answer
answer <- sapply(stacks, \(x) tail(x, n=1)) |> paste(collapse = '')

submit(answer, year, day, part)


# git push ----------------------------------------------------------------

git_push()

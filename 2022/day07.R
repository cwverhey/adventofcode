setwd(dirname(rstudioapi::getSourceEditorContext()$path))
source('functions.R')


# part 1 ------------------------------------------------------------------

year = 2022
day = 7
part = 1

task(year, day, part)

src <- input(year, day)

# create data.frame with all files/dirs
files <- data.frame(path = character(0), size = numeric(0))
dirs <- data.frame(path = "//", size = NA)
cwd <- c()

for(cmd in src) {

  # commands
  if(startsWith(cmd, "$")) {

    if(cmd == "$ ls") {
      next

    } else if(startsWith(cmd, "$ cd ")) {
      dir <- substr(cmd, 6, nchar(cmd))
      if(dir == '..') {
        cwd <- head(cwd, n=-1)
      } else {
        cwd <- c(cwd, dir)
      }

    } else {
      stop('unknown command: ', cmd)
    }

  # file/dir listing
  } else {

    cmd <- strsplit(cmd, ' ', fixed=T)[[1]]
    path <- paste(c(cwd, cmd[2]), collapse='/')

    if(cmd[1] == "dir") {
      dirs[nrow(dirs) + 1,] <- list(path = path, size = NA)
    } else {
      files[nrow(files) + 1,] <- list(path = path, size = as.numeric(cmd[1]))
    }

  }
}

# summate sizes for dirs
for(dir in dirs$path) {
  dir_files <- files[startsWith(files$path, dir), ] |> distinct()  # get all unique files in dir
  size <- sum(dir_files$size)
  dirs$size[dirs$path == dir] <- size
}

# get answer
smol_dirs <- dirs[dirs$size <= 100000,] |> distinct()  # get all unique small dirs
answer <- sum(smol_dirs$size)

submit(answer, year, day, part)


# part 2 ------------------------------------------------------------------

part = 2

task(year, day, part)

# calculate required extra space
goal <- 30000000 - (70000000 - dirs$size[dirs$path == '//'])

# find smallest dir of at least size `goal`
answer <- dirs$size[dirs$size >= goal] |> min()

submit(answer, year, day, part)


# git push ----------------------------------------------------------------

git_push()

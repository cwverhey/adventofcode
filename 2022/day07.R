setwd(dirname(rstudioapi::getSourceEditorContext()$path))
source('functions.R')


# part 1 ------------------------------------------------------------------

year = 2022
day = 7
part = 1

task(year, day, part)

src <- input(year, day, splitlines = T)

library("dplyr")

# create data.frame with all files/dirs
fs <- data.frame(type = "dir", path = "//", size = NA)
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

    type <- ifelse(cmd[1] == "dir", "dir", "file")
    path <- paste(c(cwd, cmd[2]), collapse='/')
    size <- ifelse(cmd[1] == "dir", NA, as.numeric(cmd[1]))

    fs[nrow(fs) + 1,] <- list(type = type, path = path, size = size)

  }
}

# summate sizes for dirs
dirs <- fs$path[fs$type=="dir"]  # get all dirs
for(dir in dirs) {
  files <- fs[startsWith(fs$path, dir), ] |> distinct() # get all unique files
  size <- sum(files$size, na.rm = T)
  fs$size[fs$path == dir] <- size
}

# get answer
answer <- fs$size[fs$type == 'dir' & fs$size <= 100000] |> sum()

submit(answer, year, day, part)


# part 2 ------------------------------------------------------------------

part = 2

task(year, day, part)

# calculate required extra space
goal <- 30000000 - (70000000 - fs$size[fs$path == '//'])

# find smallest dir of at least size `goal`
dirs <- fs[fs$type == 'dir' & fs$size >= goal, ]
answer <- min(dirs$size)

submit(answer, year, day, part)


# git push ----------------------------------------------------------------

system(sprintf('git add "%s"', basename(rstudioapi::getSourceEditorContext()$path)))
system(sprintf('git commit -m "%s"', basename(rstudioapi::getSourceEditorContext()$path)))
system('git push')

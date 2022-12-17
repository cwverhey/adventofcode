setwd(dirname(rstudioapi::getSourceEditorContext()$path))
source('functions.R')


# part 1 ------------------------------------------------------------------

year = 2022
day = 13
part = 1

task(year, day, part)

src <- input(year, day, raw = T)

data <- strsplit(src, '\n\n', fixed = T)[[1]] |> strsplit('\n', fixed = T)

cmpLists <- function(list1, list2) {

  cat( '\t', jsonlite::toJSON(list1), 'vs', jsonlite::toJSON(list2), '\n' )

  if(typeof(list1) != "list") list1 <- list(list1) # single int to list
  if(typeof(list2) != "list") list2 <- list(list2) # single int to list

  for(i in seq_along(list1)) {

    if(length(list2) < i) return(-1) # list2 ran out: wrong order

    if(typeof(list1[[i]]) == "list" || typeof(list2[[i]]) == "list")
      cmp <- cmpLists(list1[[i]], list2[[i]])
    else
      cmp <- cmpInts(list1[[i]], list2[[i]])

    if(cmp != 0) return(cmp)

  }

  if(length(list2) > length(list1)) return(1) # list 1 ran out first: right order

  return(0) # no decisions; continue checking

}

cmpInts <- function(int1, int2) {
  cat('\t', int1, 'vs', int2, '\n')
  if(int1 < int2) return(1) # right order
  if(int2 < int1) return(-1) # wrong order
  return(0) # continue checking
}

correct_indices <- c()

for(i in seq_along(data)) {
  dat1 <- jsonlite::fromJSON(data[[i]][1], simplifyVector = F)
  dat2 <- jsonlite::fromJSON(data[[i]][2], simplifyVector = F)
  cat( jsonlite::toJSON(dat1), 'vs', jsonlite::toJSON(dat2), '\n' )

  cmp <- cmpLists(dat1, dat2)
  cat('result: ', cmp, '\n\n')
  if(cmp == 1) correct_indices <- c(correct_indices, i)
}

answer <- sum(correct_indices)

submit(answer, year, day, part)


# part 2 ------------------------------------------------------------------

part = 2

task(year, day, part)

data <- gsub('\n\n','\n', src, fixed = T) |> strsplit('\n', fixed = T)
data <- c(data[[1]], '[[2]]', '[[6]]')

# presort
data <- data[ gsub('\\[|\\]', '', data) |> gsub('10', 'X', x = _) |> order() |> rev() ]

# insertion sort
sorted <- c()

for(i in seq_along(data)) {
  for(position in seq_along(sorted)) if( cmpLists(jsonlite::fromJSON(data[i], simplifyVector = F), jsonlite::fromJSON(sorted[position], simplifyVector = F)) == 1 ) {
    position <- position - 1
    break
  }

  if(is.null(position)) position <- 0

  cat('insert', data[i], 'after position', position, '\n')

  sorted <- append(sorted, data[i], after = position)
}

answer <- which(sorted == "[[2]]") * which(sorted == "[[6]]")

submit(answer, year, day, part)


# git push ----------------------------------------------------------------

git_push()

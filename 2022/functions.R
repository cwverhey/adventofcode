# Sys.setenv(AOC_COOKIE = 'foobarbazaa25d42de5b45e5ea75d5068ae3aa572be6b1a79f6bcd6a3e1a78056cfd9')

Sys.setenv(AOC_COOKIE = strsplit(readLines('~/.config/adventofcode-cookie.txt'), '=')[[1]][2])

library('httr')
library('xml2')
library('rvest')


# task --------------------------------------------------------------------

task <- function(year = format(Sys.time(), "%Y"), day = as.numeric(format(Sys.time(), "%d")), part = 1) {

  cachefile <- sprintf('cache/task_%s_%s_%s.txt', year, day, part)
  if(file.exists(cachefile)) {
    html <- paste(readLines(cachefile), collapse='\n')
  } else {
    html <- GET(sprintf('https://adventofcode.com/%s/day/%s', year, day), set_cookies(session = Sys.getenv("AOC_COOKIE")))
    cat(as.character(content(html, encoding = 'UTF-8')), file=cachefile)
  }

  html <- read_html(html)
  parts <- html |> html_elements('article')
  str <- parts[part]

  cat(html_text2(str))

}


# input -------------------------------------------------------------------

input <- function(year = format(Sys.time(), "%Y"), day = as.numeric(format(Sys.time(), "%d")), url = NULL, raw = FALSE) {

  if(is.null(url)) {

    # fetch task
    task_cachefile1 <- sprintf('cache/task_%s_%s_%s.txt', year, day, 1)
    task_cachefile2 <- sprintf('cache/task_%s_%s_%s.txt', year, day, 2)
    if(file.exists(task_cachefile2)) {
      html <- paste(readLines(task_cachefile2), collapse='\n')
    } else if(file.exists(task_cachefile1)) {
      html <- paste(readLines(task_cachefile1), collapse='\n')
    } else {
      html <- GET(sprintf('https://adventofcode.com/%s/day/%s', year, day), set_cookies(session = Sys.getenv("AOC_COOKIE")))
    }

    html <- read_html(html)
    urls <- html |> html_element('main') |> html_elements('a') |> html_attr('href')
    urls <- urls[grep('^\\d', urls)]
    urls <- sprintf('https://adventofcode.com/%s/day/%s', year, urls)

    if(length(urls) != 1) stop(length(urls),' urls found\n', paste(urls, collapse = '\n'))
    url <- urls[1]
  }

  # fetch URL
  cachefile <- sprintf('cache/input_%s_.txt', fs::path_sanitize(url, replacement = '_'))
  if(file.exists(cachefile)) {

    txt <- cachefile |> readLines() |> paste(collapse = '\n')

  } else {

    txt <- GET(url, set_cookies(session = Sys.getenv("AOC_COOKIE")))
    txt <- content(txt, encoding = 'UTF-8')
    cat(txt, file = cachefile)

  }

  if(!raw) {
    txt <- trimws(txt)
    txt <- strsplit(txt, '\n', fixed=T)[[1]]
  }

  return(txt)

}


# submit ------------------------------------------------------------------

submit <- function(answer, year = format(Sys.time(), "%Y"), day = as.numeric(format(Sys.time(), "%d")), part = 1) {

  cat(sprintf("Submitting '%s' for part %s\n\n", answer, part))

  html <- POST(sprintf('https://adventofcode.com/%s/day/%s/answer', year, day),
               body = list(level = part, answer = answer),
               encode = "form",
               set_cookies(session = Sys.getenv("AOC_COOKIE")))
  html <- read_html(html)

  html |> html_element('article') |> html_text2() |> cat()

}


# git_push ----------------------------------------------------------------

git_push <- function(msg = NULL) {

  if(is.null(msg)) msg <- basename(rstudioapi::getSourceEditorContext()$path)

  system(sprintf('git add "%s"', basename(rstudioapi::getSourceEditorContext()$path)))
  system(sprintf('git commit -m "%s"', msg))
  system('git push')

}

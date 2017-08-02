echo off
set spider=%1
set file=%2
del %file%
scrapy crawl %spider% -o %file%
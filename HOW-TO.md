# Installation

## Required packages

You need to install as a minimum the following packages:

```
pkgs <- c(
   "janitor",
   "knitr",
   "kableExtra",
   "openintro",
   "patchwork",
   "tidyverse",
   "scales",
   "skimr",
   "ggpubr",
   "bookdown",
   "tinytex",
   "ragg",
   NULL
)
install.packages(pkgs)
```

## (La)TeX and Co.

You should have (La)Tex installed.
The [`{tinytex}`](https://yihui.org/tinytex/), https://yihui.org/tinytex/, can help with
setting things up.


## Pandoc

If you use RStudio IDE, `pandoc` comes pre-installed, otherwise you should have
it available in your `PATH`.

## Graphical device

We have set `ragg_png` as the graphical device. This uses the
[`{ragg}`](https://ragg.r-lib.org), https://ragg.r-lib.org, package and should
provide better graphical output.


# Generation of web and PDF book

## Web book

In order to generate the whole book in the first format as defined in `_output.yml`
just open `index.Rmd` in RStudio and press the `Knit` button.
This is equivalent to run

```
bookdown::render_book(input = 'index.Rmd', output_format = 'bookdown::bs4_book')
```

which you can run from a terminal as

```
$ Rscript -e "bookdown::render_book(input = 'index.Rmd', output_format = 'bookdown::pdf_book')"
```

see also the `_build.sh` script.


For a chapter file, just open it and press `Knit` to compile and preview it.

## PDF book

In the RStudio console pane execute the following:

```
bookdown::render_book(input = 'index.Rmd', output_format = 'bookdown::pdf_book')
```


# Introduction R Markdown / bookdown

* [R Markdown: The Definitive Guide](https://bookdown.org/yihui/rmarkdown/)
* [R Markdown Cookbook](https://bookdown.org/yihui/rmarkdown-cookbook/)
* [bookdown](https://bookdown.org/yihui/bookdown/)

A short hands-on guide: https://ewfrees.github.io/StyleGuideLDA/S-SampleSection.html


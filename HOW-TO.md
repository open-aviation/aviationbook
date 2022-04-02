# Installation

The book is now rendered using [quarto](https://quarto.org/).

The book uses some R to generate a the acronym table in the appendix, so you
need R and a few packages installed as explained below.

For PDF rendering you need to install TinyTeX:

```
quarto tools install tinytex
```

## Required packages

You need to install as a minimum the following packages:

```
pkgs <- c(
   "bookdown",
   "tinytex",
   "here",
   "gt",
   NULL
)
install.packages(pkgs)
```

Installing R with conda, I had to install the following Ubuntu dependencies + two packages pre-compiled:

```
sudo apt install libharfbuzz-dev libfribidi-dev libfreetype6-dev libpng-dev libtiff5-dev libjpeg-dev
mamba install fontfonfig r-systemfonts r-ragg r-here r-gt pandoc-citep
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

Run `quarto preview` to have a local preview from your browser.

## PDF book

TBD

# Bibliography

We have a group Zotero: https://www.zotero.org/groups/4370174/aviation-book

The best way to edit the entries is via the Zotero app and automatically export
to the book's `bibliography.bib` file.
Otherwise via the web interface.


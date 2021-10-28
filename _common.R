# _common.R based on IMS: https://github.com/OpenIntroStat/ims/blob/master/_common.R
set.seed(7691)
options(digits = 3)

# packages ---------------------------------------------------------------------

suppressMessages(library(tidyverse))
suppressMessages(library(here))
suppressMessages(library(gt))
suppressMessages(library(jsonlite))

suppressMessages(library(janitor))
suppressMessages(library(knitr))
suppressMessages(library(kableExtra))
suppressMessages(library(openintro))
suppressMessages(library(patchwork))
suppressMessages(library(scales))
suppressMessages(library(skimr))
suppressMessages(library(ggpubr))

# knitr chunk options ----------------------------------------------------------

knitr::opts_chunk$set(
   #eval     = FALSE,
   comment   = "#>",
   collapse  = TRUE,
   message   = FALSE,
   warning   = FALSE,
   cache     = FALSE, # only use TRUE for quick testing!
   echo      = FALSE, # hide code unless otherwise noted in chunk options
   fig.align = "center",
   fig.width = 6,
   fig.asp   = 0.618,  # 1 / phi
   fig.show  = "hold",
   dpi       = 300,
   fig.pos   = "h",
   fig.width = "80%"
)

if (knitr::is_html_output()) {
   knitr::opts_chunk$set(out.width = "90%")
} else if (knitr::is_latex_output()) {
   knitr::opts_chunk$set(out.width = "80%")
}

# knit options -----------------------------------------------------------------

options(knitr.kable.NA = "")

# kableExtra options -----------------------------------------------------------

options(kableExtra.html.bsTable = TRUE)

# dplyr options ----------------------------------------------------------------

options(dplyr.print_min = 6, dplyr.print_max = 6)

# ggplot2 theme and colors -----------------------------------------------------

if (knitr::is_html_output()) {
   ggplot2::theme_set(ggplot2::theme_minimal(base_size = 13))
} else if (knitr::is_latex_output()) {
   ggplot2::theme_set(ggplot2::theme_minimal(base_size = 11))
}

ggplot2::update_geom_defaults("point", list(color = openintro::IMSCOL["blue","full"],
                                            fill = openintro::IMSCOL["blue","full"]))
ggplot2::update_geom_defaults("bar", list(fill = openintro::IMSCOL["blue","full"],
                                          color = "#FFFFFF"))
ggplot2::update_geom_defaults("col", list(fill = openintro::IMSCOL["blue","full"],
                                          color = "#FFFFFF"))
ggplot2::update_geom_defaults("boxplot", list(color = openintro::IMSCOL["blue","full"]))
ggplot2::update_geom_defaults("density", list(color = openintro::IMSCOL["blue","full"]))
ggplot2::update_geom_defaults("line", list(color = openintro::IMSCOL["gray", "full"]))
ggplot2::update_geom_defaults("smooth", list(color = openintro::IMSCOL["gray", "full"]))
ggplot2::update_geom_defaults("dotplot", list(color = openintro::IMSCOL["blue","full"],
                                              fill = openintro::IMSCOL["blue","full"]))

# function: caption helper -----------------------------------------------------

caption_helper <- function(txt) {
   if (knitr::is_latex_output())
      stringr::str_replace_all(txt, "([^`]*)`(.*?)`", "\\1\\\\texttt{\\2}") %>%
      stringr::str_replace_all("_", "\\\\_")
   else
      txt
}

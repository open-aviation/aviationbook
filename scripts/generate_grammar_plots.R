#!/usr/bin/env Rscript
# Generate committed static ggplot2 plots for the grammar-of-graphics chapter.
#
# Run with the rig-managed R (see HOW-TO.md for the one-time setup):
#
#   Rscript scripts/generate_grammar_plots_ggplot2.R
#
# If `Rscript` on the PATH resolves to an old R, invoke the new one directly:
#
#   /Library/Frameworks/R.framework/Versions/4.6/Resources/bin/Rscript \
#     scripts/generate_grammar_plots_ggplot2.R

library(ggplot2)
library(dplyr)
library(tidyr)
library(scales)
library(svglite)
library(patchwork)
library(readr)

root <- normalizePath(file.path(getwd(), ".."), winslash = "/")
if (!file.exists(file.path(root, "data", "gapminder.csv"))) {
  root <- getwd()
}
data_path <- file.path(root, "data", "gapminder.csv")
out_dir <- file.path(root, "media", "plots", "grammar", "ggplot2")
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)

gap <- read_csv(data_path, show_col_types = FALSE)
g2007 <- gap |> filter(year == 2007)
france <- gap |> filter(country == "France")

font_regular <- file.path(root, "media", "fonts", "IBMPlexSans-Regular.ttf")
font_semibold <- file.path(root, "media", "fonts", "IBMPlexSans-SemiBold.ttf")
systemfonts::register_font(
  "IBM Plex Sans",
  plain = font_regular,
  bold = font_semibold
)

continents <- sort(unique(g2007$continent))
palette <- setNames(
  scales::hue_pal()(length(continents)), continents
)

# SI-style formatting (60400000 -> 60M), like d3's ~s.
si_format <- function() scales::label_number(scale_cut = scales::cut_short_scale())
theme_page <- function() {
  theme_minimal(base_size = 11) +
    theme(
      plot.title = element_text(hjust = 0, face = "bold"),
      panel.grid.minor = element_blank()
    )
}

save_plot <- function(
  plot, name, width = 6.4, height = 4.2, apply_page_theme = TRUE
) {
  if (apply_page_theme) plot <- plot + theme_page()
  path <- file.path(out_dir, paste0(name, ".svg"))
  ggsave(
    path, plot, device = svglite::svglite,
    width = width, height = height, units = "in"
  )
  cat(relpath(path), "\n", sep = "")
}

save_plot_png <- function(plot, name, width = 6.0, height = 3.6) {
  path <- file.path(out_dir, paste0(name, ".png"))
  ggsave(
    path, plot, device = ragg::agg_png,
    width = width, height = height, units = "in", dpi = 192,
    background = "white"
  )
  cat(relpath(path), "\n", sep = "")
}

relpath <- function(path) {
  gsub("^./", "", path)
}

# 1. Rosling scatter, 2007 -----------------------------------------------
p_scatter <- ggplot(g2007, aes(
  x = gdp_per_capita, y = life_expectancy,
  colour = continent, size = population
)) +
  geom_point(alpha = 0.85) +
  scale_x_log10(labels = si_format()) +
  scale_size_continuous(range = c(1.5, 14), guide = "none") +
  labs(x = "GDP per capita", y = "life expectancy", colour = "continent")
save_plot(p_scatter, "scatter-2007")

# 2. Nominal continent squares ------------------------------------------
p_squares <- ggplot(g2007 |> mutate(x = 0), aes(x, continent, colour = continent)) +
  geom_point(shape = 15, size = 6) +
  scale_colour_manual(values = palette, guide = "none") +
  scale_x_continuous(breaks = NULL) +
  labs(x = NULL, y = NULL)
save_plot(p_squares, "continent-squares", width = 5.4, height = 2.8)

# 4. France population line ---------------------------------------------
p_france <- ggplot(france, aes(year, population)) +
  geom_line() +
  scale_y_continuous(labels = si_format()) +
  labs(x = "year", y = "population")
save_plot(p_france, "france-population", width = 6.2, height = 3.6)

# 5. Median GDP per continent -------------------------------------------
p_median <- ggplot(g2007, aes(
  gdp_per_capita,
  reorder(continent, gdp_per_capita, FUN = median),
  fill = continent
)) +
  stat_summary(fun = median, geom = "bar", orientation = "y") +
  scale_fill_manual(values = palette, guide = "none") +
  scale_x_continuous(labels = si_format()) +
  labs(x = "median GDP per capita", y = NULL)
save_plot(p_median, "median-gdp-continent", width = 6.2, height = 3.8)

# 6. Distinct country count per continent -------------------------------
country_count <- gap |>
  group_by(continent) |>
  summarise(countries = n_distinct(country), .groups = "drop") |>
  mutate(continent = reorder(continent, countries))
p_count <- ggplot(country_count, aes(countries, continent, fill = continent)) +
  geom_col() +
  scale_fill_manual(values = palette, guide = "none") +
  labs(x = "number of countries", y = NULL)
save_plot(p_count, "country-count-continent", width = 6.2, height = 3.8)

# 7. Mean GDP coloured by standard deviation ----------------------------
dispersion <- g2007 |>
  group_by(continent) |>
  summarise(mean = mean(gdp_per_capita), stdev = sd(gdp_per_capita), .groups = "drop") |>
  mutate(continent = reorder(continent, mean))
p_disp <- ggplot(dispersion, aes(mean, continent, fill = stdev)) +
  geom_col() +
  scale_fill_distiller(palette = "Blues", direction = 1, limits = c(0, 20000)) +
  scale_x_continuous(labels = si_format()) +
  labs(x = "mean GDP per capita", y = NULL, fill = "standard deviation") +
  theme(legend.position = "right")
save_plot(p_disp, "gdp-dispersion-continent", width = 6.8, height = 4.0)

# 8. GDP per capita box plots -------------------------------------------
p_box <- ggplot(g2007, aes(gdp_per_capita, continent)) +
  geom_boxplot() +
  scale_x_continuous(labels = si_format()) +
  labs(x = "GDP per capita", y = NULL)
save_plot(p_box, "gdp-boxplot", width = 6.4, height = 4.0)

# 9. Histograms: plain and stacked by continent -------------------------
p_hist1 <- ggplot(g2007, aes(gdp_per_capita)) +
  geom_histogram(bins = 30, fill = "grey50") +
  labs(x = "GDP per capita", y = "number of countries")
p_hist2 <- ggplot(g2007, aes(gdp_per_capita, fill = continent)) +
  geom_histogram(bins = 30, position = "stack") +
  scale_fill_manual(values = palette) +
  labs(x = "GDP per capita", y = "number of countries")
save_plot(p_hist1 | p_hist2, "gdp-histograms", width = 10.5, height = 3.8)

# 10. Population composition (totals, points, stacked total) ------------
totals <- g2007 |>
  group_by(continent) |>
  summarise(population = sum(population), .groups = "drop") |>
  mutate(continent = reorder(continent, population))
p_totals <- ggplot(totals, aes(population, continent, fill = continent)) +
  geom_col() +
  scale_fill_manual(values = palette, guide = "none") +
  scale_x_continuous(labels = si_format()) +
  labs(x = "population", y = NULL)
p_points <- ggplot(g2007, aes(population, continent, colour = continent)) +
  geom_point(alpha = 0.6) +
  scale_colour_manual(values = palette, guide = "none") +
  scale_x_continuous(labels = si_format()) +
  labs(x = "population", y = NULL)
stack_frame <- totals |>
  mutate(category = "total") |>
  select(category, continent, population)
p_stack <- ggplot(stack_frame, aes(population, category, fill = continent)) +
  geom_col() +
  scale_fill_manual(values = palette) +
  scale_x_continuous(labels = si_format()) +
  labs(x = "population", y = NULL)
composition <- (p_totals | p_points) / p_stack + plot_layout(heights = c(1, 1))
save_plot(composition, "population-layout", width = 11.0, height = 6.0)

# 11. Stacked area, large European countries ----------------------------
mean_pop <- gap |>
  group_by(country) |>
  summarise(mean_pop = mean(population), .groups = "drop")
large_europe <- gap |>
  filter(continent == "Europe") |>
  inner_join(mean_pop, by = "country") |>
  filter(mean_pop > 5e7) |>
  mutate(country = reorder(country, -mean_pop))
p_area <- ggplot(large_europe, aes(year, population, fill = country)) +
  geom_area() +
  scale_fill_manual(values = scales::hue_pal()(n_distinct(large_europe$country))) +
  scale_y_continuous(labels = si_format()) +
  labs(x = "year", y = "population", fill = "country") +
  theme(legend.position = "right")
save_plot(p_area, "large-europe-population", width = 7.6, height = 4.2)

# 12. Top 10 by population and by GDP per capita ------------------------
top_pop <- g2007 |>
  slice_max(population, n = 10) |>
  mutate(country = reorder(country, population))
top_gdp <- g2007 |>
  slice_max(gdp_per_capita, n = 10) |>
  mutate(country = reorder(country, gdp_per_capita))
p_top_pop <- ggplot(top_pop, aes(population, country, fill = continent)) +
  geom_col() +
  scale_fill_manual(values = palette, guide = "none") +
  scale_x_continuous(labels = si_format()) +
  labs(x = "population", y = NULL)
p_top_gdp <- ggplot(top_gdp, aes(gdp_per_capita, country, fill = continent)) +
  geom_col() +
  scale_fill_manual(values = palette, guide = "none") +
  scale_x_continuous(labels = si_format()) +
  labs(x = "GDP per capita", y = NULL)
save_plot(p_top_pop | p_top_gdp, "top10-population-gdp", width = 11.0, height = 4.8)

# 13. Static Rosling bubble chart, initial 2007 state -------------------
p_bubble <- ggplot(g2007, aes(
  gdp_per_capita, life_expectancy,
  colour = continent, size = population
)) +
  geom_point(alpha = 0.85) +
  scale_x_log10(limits = c(300, 1e5), labels = si_format()) +
  scale_y_continuous(limits = c(20, 90)) +
  scale_size_continuous(
    range = c(1.5, 18), breaks = c(1e6, 1e7, 1e8, 1e9), guide = "none"
  ) +
  labs(x = "GDP per capita", y = "life expectancy", colour = "continent")
save_plot(p_bubble, "rosling-bubbles-2007", width = 6.4, height = 4.8)

# 14. Styled France population line -------------------------------------
p_styled <- ggplot(france, aes(year, population)) +
  geom_line(colour = "#008f6b", linewidth = 1) +
  scale_x_continuous(
    breaks = seq(1950, 2010, by = 5),
    limits = c(1949, 2011),
    expand = expansion(mult = 0)
  ) +
  scale_y_continuous(
    breaks = c(45e6, 50e6, 55e6, 60e6),
    limits = c(41e6, 62e6),
    labels = si_format(),
    expand = expansion(mult = 0)
  ) +
  labs(title = "Population of France", x = NULL, y = NULL) +
  theme_minimal(base_family = "IBM Plex Sans", base_size = 11) +
  theme(
    plot.title = element_text(
      family = "IBM Plex Sans", face = "bold", size = 13.2,
      hjust = 0, margin = margin(b = 6)
    ),
    axis.text = element_text(
      family = "IBM Plex Sans", colour = "#4D4D4D", size = 8.8
    ),
    axis.ticks = element_blank(),
    panel.grid.major = element_line(colour = "#EBEBEB", linewidth = 0.5),
    panel.grid.minor = element_blank(),
    plot.margin = margin(t = 5.29, r = 12.02, b = 4.03, l = 6.64)
  )
save_plot_png(p_styled, "france-population-styled")

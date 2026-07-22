# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "altair==5.5.0",
#   "pandas>=2.2,<3",
#   "vl-convert-python>=1.7,<2",
#   "seaborn>=0.13,<1",
#   "matplotlib>=3.9,<4",
# ]
# ///
"""Generate committed static plots for the grammar-of-graphics chapter.

Run from any directory with:

    uv run scripts/generate_grammar_plots.py

The Quarto book displays these SVG files directly. Its Python examples are
therefore visible without starting Jupyter during a normal book build.
"""

from base64 import b64encode
from pathlib import Path
import re

import altair as alt
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib import font_manager
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from matplotlib.ticker import EngFormatter

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "gapminder.csv"
ALTAIR_DIR = ROOT / "media" / "plots" / "grammar" / "altair"
SEABORN_DIR = ROOT / "media" / "plots" / "grammar" / "seaborn"
FONT_REGULAR = ROOT / "media" / "fonts" / "IBMPlexSans-Regular.ttf"
FONT_SEMIBOLD = ROOT / "media" / "fonts" / "IBMPlexSans-SemiBold.ttf"
FONT_WEB = ROOT / "media" / "fonts" / "IBMPlexSans-Latin.woff2"

for font_path in (FONT_REGULAR, FONT_SEMIBOLD):
    font_manager.fontManager.addfont(font_path)

STYLE_FONT = "IBM Plex Sans"
STYLE_GREEN = "#008f6b"
STYLE_GRID = "#EBEBEB"
STYLE_TEXT = "#4D4D4D"
STYLE_X_DOMAIN = (1949, 2011)
STYLE_X_TICKS = list(range(1950, 2011, 5))
STYLE_Y_DOMAIN = (41_000_000, 62_000_000)
STYLE_Y_TICKS = [45_000_000, 50_000_000, 55_000_000, 60_000_000]


def embed_webfont(path: Path) -> None:
    """Embed IBM Plex Sans in an SVG that will be loaded through an img tag."""
    font_data = b64encode(FONT_WEB.read_bytes()).decode("ascii")
    font_face = (
        "<defs><style>"
        "@font-face{font-family:'IBM Plex Sans';font-style:normal;"
        "font-weight:100 700;src:url(data:font/woff2;base64,"
        f"{font_data}) format('woff2');}}"
        "</style></defs>"
    )
    svg = path.read_text(encoding="utf-8")
    svg = re.sub(r"(<svg\b[^>]*>)", rf"\1{font_face}", svg, count=1)
    path.write_text(svg, encoding="utf-8")


def save(
    chart: alt.TopLevelMixin, name: str, *, embed_font: bool = False
) -> None:
    """Save an Altair/Vega-Lite chart as a self-contained SVG."""
    path = ALTAIR_DIR / f"{name}.svg"
    path.parent.mkdir(parents=True, exist_ok=True)
    chart.save(path)
    if embed_font:
        embed_webfont(path)
    print(path.relative_to(ROOT))


def altair_plots(gap: pd.DataFrame) -> None:
    g2007 = gap.query("year == 2007")
    france = gap.query('country == "France"')

    scatter = (
        alt.Chart(g2007)
        .encode(
            x=alt.X("gdp_per_capita:Q", scale=alt.Scale(type="log")),
            y="life_expectancy:Q",
            color="continent:N",
            size=alt.Size("population:Q", legend=None),
            tooltip=["country:N", "population:Q"],
        )
        .mark_circle()
        .properties(width=500, height=300)
    )
    save(scatter, "scatter-2007")

    continents = (
        alt.Chart(g2007)
        .encode(
            y=alt.Y("continent:N", title=None),
            color=alt.Color("continent:N", legend=None),
        )
        .mark_square(size=100)
    )
    save(continents, "continent-squares")

    france_line = (
        alt.Chart(france)
        .encode(
            x=alt.X("year:Q", title="year", axis=alt.Axis(format="d")),
            y=alt.Y(
                "population:Q",
                scale=alt.Scale(zero=False),
                axis=alt.Axis(format="~s"),
            ),
        )
        .mark_line()
        .properties(width=500)
    )
    save(france_line, "france-population")

    median_gdp = (
        alt.Chart(g2007)
        .encode(
            x=alt.X(
                "median(gdp_per_capita):Q",
                title="median GDP per capita",
                axis=alt.Axis(format="~s"),
            ),
            y=alt.Y("continent:N", sort="-x"),
            color="continent:N",
        )
        .mark_bar()
        .properties(width=500)
    )
    save(median_gdp, "median-gdp-continent")

    country_count = (
        alt.Chart(gap)
        .encode(
            x=alt.X("distinct(country):Q", title="number of countries"),
            y=alt.Y("continent:N", sort="-x"),
            color=alt.Color("continent:N", legend=None),
        )
        .mark_bar()
    )
    save(country_count, "country-count-continent")

    dispersion = (
        alt.Chart(g2007)
        .encode(
            x=alt.X(
                "mean(gdp_per_capita):Q",
                axis=alt.Axis(format="~s"),
                title="mean GDP per capita",
            ),
            y=alt.Y("continent:N", sort="-x"),
            color=alt.Color(
                "stdev(gdp_per_capita):Q",
                title="standard deviation",
                scale=alt.Scale(domain=(0, 20_000), scheme="blues"),
            ),
        )
        .mark_bar()
    )
    save(dispersion, "gdp-dispersion-continent")

    boxplot = (
        alt.Chart(g2007)
        .encode(
            x=alt.X(
                "gdp_per_capita:Q",
                axis=alt.Axis(format="~s"),
                title="GDP per capita",
            ),
            y="continent:N",
            tooltip="country:N",
        )
        .mark_boxplot()
    )
    save(boxplot, "gdp-boxplot")

    histogram_base = (
        alt.Chart(g2007)
        .encode(
            x=alt.X(
                "gdp_per_capita:Q",
                bin=alt.Bin(maxbins=30),
                title="GDP per capita",
            ),
            y=alt.Y("count():Q", title="number of countries"),
        )
        .mark_bar()
        .properties(width=300, height=200)
    )
    save(histogram_base | histogram_base.encode(color="continent:N"), "gdp-histograms")

    population_base = (
        alt.Chart(g2007)
        .encode(
            x=alt.X(
                "sum(population):Q",
                title="total population in 2007",
                axis=alt.Axis(format="~s"),
            ),
            color=alt.Color("continent:N", legend=None),
        )
        .mark_bar(size=10)
        .properties(width=280)
    )
    population_layout = (
        population_base.encode(y=alt.Y("continent:N", title=None))
        | population_base.encode(
            x=alt.X("population:Q", axis=alt.Axis(format="~s")),
            y=alt.Y("continent:N", title=None),
        ).mark_point()
    ) & population_base.properties(width=680)
    save(population_layout, "population-layout")

    large_europe = (
        alt.Chart(gap)
        .encode(
            x=alt.X("year:T", title="year"),
            y=alt.Y("population:Q", axis=alt.Axis(format="~s")),
            color=alt.Color("country:N", title="country"),
            order=alt.Order("mean_pop:Q", sort="descending"),
        )
        .mark_area()
        .transform_joinaggregate(mean_pop="mean(population)", groupby=["country"])
        .transform_filter("datum.continent == 'Europe' && datum.mean_pop > 50000000")
        .properties(width=480, height=240)
    )
    save(large_europe, "large-europe-population")

    ranking_base = (
        alt.Chart(g2007)
        .mark_bar(size=10)
        .encode(
            y=alt.Y("country:N", sort="-x", title="country"),
            color=alt.Color("continent:N", legend=None),
        )
        .transform_window(
            rank_pop="rank(population)",
            sort=[alt.SortField("population", order="descending")],
        )
        .transform_window(
            rank_gdp="rank(gdp_per_capita)",
            sort=[alt.SortField("gdp_per_capita", order="descending")],
        )
        .properties(width=300, height=220)
    )
    ranking = ranking_base.encode(
        x=alt.X("population:Q", axis=alt.Axis(format="~s"))
    ).transform_filter("datum.rank_pop <= 10") | ranking_base.encode(
        x=alt.X(
            "gdp_per_capita:Q",
            axis=alt.Axis(format="~s"),
            title="GDP per capita",
        )
    ).transform_filter("datum.rank_gdp <= 10")
    save(ranking, "top10-population-gdp")

    year_slider = alt.binding_range(min=1952, max=2007, step=5, name="year:")
    year_selector = alt.selection_point(
        name="year_selection",
        fields=["year"],
        bind=year_slider,
        value=[{"year": 2007}],
    )
    bubble = (
        alt.Chart(gap)
        .encode(
            x=alt.X(
                "gdp_per_capita:Q",
                scale=alt.Scale(type="log", domain=(300, 1e5)),
                title="GDP per capita",
            ),
            y=alt.Y(
                "life_expectancy:Q",
                scale=alt.Scale(domain=(20, 90)),
                title="life expectancy",
            ),
            color="continent:N",
            size=alt.Size(
                "population:Q",
                scale=alt.Scale(domain=(2e5, 1.4e9), type="log"),
                legend=None,
            ),
            tooltip="country:N",
        )
        .transform_filter(year_selector)
        .properties(width=420, height=320)
        .mark_circle()
        .add_params(year_selector)
    )
    save(bubble, "rosling-bubbles-2007")

    styled = (
        alt.Chart(france)
        .encode(
            x=alt.X(
                "year:Q",
                scale=alt.Scale(domain=STYLE_X_DOMAIN, nice=False),
                axis=alt.Axis(
                    title=None,
                    values=STYLE_X_TICKS,
                    format="d",
                    grid=True,
                    gridColor=STYLE_GRID,
                    gridWidth=1.43,
                    domain=False,
                    ticks=False,
                    labelColor=STYLE_TEXT,
                    labelFont=STYLE_FONT,
                    labelFontSize=12,
                    labelFlush=True,
                    labelOverlap=False,
                    labelPadding=7,
                ),
            ),
            y=alt.Y(
                "population:Q",
                scale=alt.Scale(domain=STYLE_Y_DOMAIN, nice=False),
                axis=alt.Axis(
                    title=None,
                    values=STYLE_Y_TICKS,
                    format="~s",
                    grid=True,
                    gridColor=STYLE_GRID,
                    gridWidth=1.43,
                    domain=False,
                    ticks=False,
                    labelColor=STYLE_TEXT,
                    labelFont=STYLE_FONT,
                    labelFontSize=12,
                    labelPadding=0,
                ),
            ),
        )
        .mark_line(color=STYLE_GREEN, strokeWidth=2.84)
        .properties(
            title="Population of France",
            width=576,
            height=346,
            autosize=alt.AutoSizeParams(type="fit", contains="padding"),
        )
        .configure_title(
            anchor="start",
            color="#000000",
            font=STYLE_FONT,
            fontSize=18,
            fontWeight=600,
            dx=33.4,
            offset=8,
        )
        .configure_view(stroke=None)
    )
    save(styled, "france-population-styled", embed_font=True)


def save_mpl(fig: plt.Figure, name: str, *, tight: bool = True) -> None:
    """Save a matplotlib/seaborn figure as SVG and release its resources."""
    path = SEABORN_DIR / f"{name}.svg"
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, format="svg", bbox_inches="tight" if tight else None)
    plt.close(fig)
    print(path.relative_to(ROOT))


def save_mpl_png(fig: plt.Figure, name: str) -> None:
    """Save a browser-portable, double-density matplotlib PNG."""
    path = SEABORN_DIR / f"{name}.png"
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, format="png", dpi=192, facecolor="white")
    plt.close(fig)
    print(path.relative_to(ROOT))


def seaborn_plots(gap: pd.DataFrame) -> None:
    sns.set_theme(style="whitegrid")
    g2007 = gap.query("year == 2007")
    france = gap.query('country == "France"')
    continents = sorted(g2007["continent"].unique())
    palette = dict(zip(continents, sns.color_palette("tab10", len(continents))))
    formatter = EngFormatter(sep="")

    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    sns.scatterplot(
        data=g2007,
        x="gdp_per_capita",
        y="life_expectancy",
        hue="continent",
        size="population",
        sizes=(20, 500),
        palette=palette,
        ax=ax,
    )
    ax.set(xscale="log", xlabel="GDP per capita", ylabel="life expectancy")
    sns.move_legend(ax, "center left", bbox_to_anchor=(1, 0.5), frameon=False)
    save_mpl(fig, "scatter-2007")

    fig, ax = plt.subplots(figsize=(5.4, 2.8))
    sns.scatterplot(
        data=g2007.assign(x=0),
        x="x",
        y="continent",
        hue="continent",
        marker="s",
        s=110,
        palette=palette,
        legend=False,
        ax=ax,
    )
    ax.set(xlabel=None, ylabel=None, xticks=[])
    sns.despine(ax=ax, bottom=True)
    save_mpl(fig, "continent-squares")

    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    sns.lineplot(data=france, x="year", y="population", ax=ax)
    ax.yaxis.set_major_formatter(formatter)
    ax.set(xlabel="year", ylabel="population")
    save_mpl(fig, "france-population")

    median_order = (
        g2007.groupby("continent")["gdp_per_capita"]
        .median()
        .sort_values()
        .index
    )
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    sns.barplot(
        data=g2007,
        x="gdp_per_capita",
        y="continent",
        hue="continent",
        estimator="median",
        errorbar=None,
        order=median_order,
        palette=palette,
        legend=False,
        ax=ax,
    )
    ax.xaxis.set_major_formatter(formatter)
    ax.set(xlabel="median GDP per capita", ylabel=None)
    save_mpl(fig, "median-gdp-continent")

    country_count = (
        gap.groupby("continent", as_index=False)
        .agg(countries=("country", "nunique"))
        .sort_values("countries")
    )
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    sns.barplot(
        data=country_count,
        x="countries",
        y="continent",
        hue="continent",
        palette=palette,
        legend=False,
        ax=ax,
    )
    ax.set(xlabel="number of countries", ylabel=None)
    save_mpl(fig, "country-count-continent")

    dispersion = (
        g2007.groupby("continent", as_index=False)["gdp_per_capita"]
        .agg(mean="mean", stdev="std")
        .sort_values("mean")
    )
    norm = Normalize(0, 20_000)
    cmap = plt.get_cmap("Blues")
    dispersion_palette = {
        row.continent: cmap(norm(row.stdev)) for row in dispersion.itertuples()
    }
    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    sns.barplot(
        data=dispersion,
        x="mean",
        y="continent",
        hue="continent",
        palette=dispersion_palette,
        legend=False,
        ax=ax,
    )
    fig.colorbar(
        ScalarMappable(norm=norm, cmap=cmap),
        ax=ax,
        label="standard deviation",
    )
    ax.xaxis.set_major_formatter(formatter)
    ax.set(xlabel="mean GDP per capita", ylabel=None)
    save_mpl(fig, "gdp-dispersion-continent")

    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    sns.boxplot(data=g2007, x="gdp_per_capita", y="continent", ax=ax)
    ax.xaxis.set_major_formatter(formatter)
    ax.set(xlabel="GDP per capita", ylabel=None)
    save_mpl(fig, "gdp-boxplot")

    fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.8), sharey=True)
    sns.histplot(data=g2007, x="gdp_per_capita", bins=30, ax=axes[0])
    sns.histplot(
        data=g2007,
        x="gdp_per_capita",
        hue="continent",
        palette=palette,
        multiple="stack",
        bins=30,
        ax=axes[1],
    )
    for ax in axes:
        ax.set(xlabel="GDP per capita", ylabel="number of countries")
    save_mpl(fig, "gdp-histograms")

    totals = (
        g2007.groupby("continent", as_index=False)["population"]
        .sum()
        .sort_values("population")
    )
    fig = plt.figure(figsize=(11.0, 6.0), layout="constrained")
    grid = fig.add_gridspec(2, 2)
    ax_total = fig.add_subplot(grid[0, 0])
    ax_points = fig.add_subplot(grid[0, 1])
    ax_stack = fig.add_subplot(grid[1, :])
    sns.barplot(
        data=totals,
        x="population",
        y="continent",
        hue="continent",
        palette=palette,
        legend=False,
        ax=ax_total,
    )
    sns.scatterplot(
        data=g2007,
        x="population",
        y="continent",
        hue="continent",
        palette=palette,
        legend=False,
        ax=ax_points,
    )
    left = 0
    for row in totals.itertuples():
        ax_stack.barh(
            ["total"],
            row.population,
            left=left,
            color=palette[row.continent],
            label=row.continent,
        )
        left += row.population
    ax_stack.legend(ncol=3, frameon=False)
    for ax in (ax_total, ax_points, ax_stack):
        ax.xaxis.set_major_formatter(formatter)
        ax.set_xlabel("population")
    save_mpl(fig, "population-layout")

    mean_population = gap.groupby("country")["population"].transform("mean")
    large_europe = gap[(gap["continent"] == "Europe") & (mean_population > 50e6)]
    wide = large_europe.pivot(index="year", columns="country", values="population")
    fig, ax = plt.subplots(figsize=(7.6, 4.2))
    colours = sns.color_palette("tab10", wide.shape[1])
    ax.stackplot(
        wide.index,
        *[wide[column] for column in wide.columns],
        labels=wide.columns,
        colors=colours,
    )
    ax.yaxis.set_major_formatter(formatter)
    ax.set(xlabel="year", ylabel="population")
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.5), frameon=False)
    save_mpl(fig, "large-europe-population")

    top_population = g2007.nlargest(10, "population").sort_values("population")
    top_gdp = g2007.nlargest(10, "gdp_per_capita").sort_values("gdp_per_capita")
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.8))
    sns.barplot(
        data=top_population,
        x="population",
        y="country",
        hue="continent",
        palette=palette,
        legend=False,
        ax=axes[0],
    )
    sns.barplot(
        data=top_gdp,
        x="gdp_per_capita",
        y="country",
        hue="continent",
        palette=palette,
        legend=False,
        ax=axes[1],
    )
    axes[0].set(xlabel="population", ylabel=None)
    axes[1].set(xlabel="GDP per capita", ylabel=None)
    for ax in axes:
        ax.xaxis.set_major_formatter(formatter)
    save_mpl(fig, "top10-population-gdp")

    with plt.rc_context({
        "font.family": STYLE_FONT,
        "font.size": 8.8,
        "axes.titlesize": 13.2,
        "axes.titleweight": 600,
        "axes.titlecolor": "#000000",
        "xtick.color": STYLE_TEXT,
        "ytick.color": STYLE_TEXT,
        "svg.fonttype": "none",
    }):
        fig, ax = plt.subplots(figsize=(6.0, 3.6))
        fig.subplots_adjust(
            left=29.25 / 432,
            right=420 / 432,
            bottom=(259.2 - 242.25) / 259.2,
            top=(259.2 - 23.25) / 259.2,
        )
        sns.lineplot(
            data=france,
            x="year",
            y="population",
            color=STYLE_GREEN,
            linewidth=2.13,
            solid_capstyle="butt",
            ax=ax,
        )
        ax.set_title("Population of France", loc="left", pad=8.5)
        ax.set(
            xlabel=None,
            ylabel=None,
            xlim=STYLE_X_DOMAIN,
            ylim=STYLE_Y_DOMAIN,
            xticks=STYLE_X_TICKS,
            yticks=STYLE_Y_TICKS,
        )
        ax.yaxis.set_major_formatter(formatter)
        ax.grid(True, which="major", color=STYLE_GRID, linewidth=1.07)
        for gridline in (*ax.get_xgridlines(), *ax.get_ygridlines()):
            gridline.set_solid_capstyle("butt")
        ax.tick_params(axis="both", length=0, labelsize=8.8, pad=5)
        sns.despine(ax=ax, left=True, bottom=True)
        save_mpl_png(fig, "france-population-styled")


def main() -> None:
    gap = pd.read_csv(DATA)
    altair_plots(gap)
    seaborn_plots(gap)


if __name__ == "__main__":
    main()

See [How-TO](HOW-TO.md) for setup and usage.

# Aviation book

## Titles (suggestions)

- The rough guide to aviation data
- Flying around aviation data
- Exploring aviation through (open) data
- The Flying Bytes
- Flying Colours
- Opening Aviation
- Data Science for Aviation

## Subtitles:

- Access, process, visualise and share aviation data
- A comprehensive handbook for aviation data

Xavier, Junzi, Enrico, Rainer (David?)

## Synopsis

About a century after the invention of powered flight, aviation has
slowly become a vital element of everyday life. While pioneers and
flying aces build the collective imaginary around the early days of
aviation, technical advances around surveillance systems, the use of
radar in civil aviation in the 1950s, the generalisation of GPS for
civil applications in the 1980s and the ADS-B mandate emerging in the
2000s make the use of data in aviation an interesting field of research
for many disciplines. In particular, such effort has been justified by
the historic growth of traffic from the early 2000s, and new challenges
such as world-wide crises, pandemics or new unmanned technologies.

Aviation and air transportation are data-rich environments. At the very
start of each aircraft, it comes with its own design information and
performance data. During flight operations, it can collect several
gigabytes of raw data per flight including trajectory data and sensor
information. Beyond the aircraft itself, information regarding
procedures, flight tables, surveillance states, and weather reports are
also constantly being generated and aggregated.

Traditionally, open data has not been a well adopted concept in the
aviation industry. The availability and sharing of data on a global
scale and with a varied community of researchers and practitioners is
limited. Such a lack of transparency hampers the industry as a whole,
limiting its efficiency and sustainability.

In recent years, the open data philosophy is gaining ground within the
aviation research community, primarily thanks to the wide adoption of
Automatic Dependent Surveillance--Broadcast (ADS-B) technology. Data
sharing within the aviation industry has also been identified as an
enabler for a more rational use of resources. With lower cost of storage
devices and more convenient internet access, large open data has become
one of the strong foundations for researchers, and a gold mine of
information for the passionate.

In such a Eureka moment in open aviation science, four aviation
enthusiasts with different backgrounds come together and present this
open book. This book presents the ecosystem of common data formats used
in aviation. It takes the readers onto a data journey, with a strong
focus on open access. With a little bit of programming knowledge and
aviation background, this book also presents insights of data mining and
visualisation techniques that convey a colorful story of aviation.

## Who is this book for?

This book was written for graduate students, academics, scientists and
analysts addressing data based aviation research. This includes
questions related to aviation data science, aircraft performance,
environment impact, economic analysis, and more. A basic set of skills
in one programming language commonly used in data science is required:
in its current form, the book covers Javascript, Python and R. The book
will give the reader a comprehensive overview on common aviation data
formats, data sources, and a decent command in the language of her
choice to address data parsing, data analysis and data visualisation
techniques.

## Who is this book not for?

Do not expect to find in this book a crash course in Python, R or
Javascript. If you are passionate about aviation, some chapters may be
of interest, but you should get proficient in basic programming to enjoy
the full content.

## How to get a copy of this book?

The book is designed as an online book, edited with TU Delft OPEN
Publishing, and is made available online
(https://smart_and_catchy.url) all along the writing process. Stable
outstanding versions will be tagged, marked with a DOI and made **freely
and openly** available as web versions, printable PDF and ebook
documents.

The content of this book is licensed as Creative Commons CC-BY-NC-ND.
This license lets you download the book and share it with others as long
as you credit the authors. You are not allowed to change the content in
any way or to use the text for commercial purposes.

## How is this book organised?

*Part 1. Introduction to aviation*

This part brings in the minimal background necessary to comprehend the
aviation world, including vocabulary and historical aspects which led to
the current situation.

*Part 2. The ecosystem of aviation data*

This part goes through all the most commonly used data formats in the
aviation and ATM data analysis community.

*Part 3. Access and Explore Data*

This part presents popular frameworks of data analytics and digs into
the insides of aviation commonly used data formats, accessible data
sources (open or not), together with basic programming literacy for
exploring such datasets.

*Part 4. Process Data*

This part introduces more advanced mathematical and programming skills.
The tidy paradigm to manipulate data frames is introduced. Challenges
associated with geometrical shapes, geographical coordinates,
trajectories, projections are presented, before introducing common AI
tools for information extraction, prediction and optimisation.

*Part 5. Visualise Data*

This part turns to the data visualisation aspects. It explains how to
choose the most appropriate tool to convey a message with particular
focus on geographical information.

*Part 6. Share Data *

The most overlooked aspect of data analysis probably turns around data
sharing. Data curation is often a very time consuming process and
enriching data by labelling specific tags or merging several sources of
information brings additional value to a dataset. This part deals with
the data sharing and publication process. (paper reproducibility?)

## Table of contents

1.  **Prologue**
    > *Introduction example with some short basic storytelling*

### Part 1. Introduction to aviation

1.  **Aviation 101 by Rainer**
    > not sure this is an own part, but it might be good to have a
    > small section speaking about aviation vs air transport, airspace
    > vs controlled/ATC, airport airside (landside or why we skip this),
    > active/secondary surveillance, \.... This might be the place to
    > also speak about trajectory \~ flight and other basics.

2.  **Historical aspects**
    > (radar, routes, vors, ils, flight plans, etc)

### Part 2. The ecosystem of aviation data

1.  **Trajectories**
    -   Trajectories: radar tracks, ADS-B
    -   Flight plans
    -   DDR formats: exp2 m1 m3 ALL FT+

2.  **Structure**
    -   Airspaces & / or aeronautical information in general (e.g.
        airport information \[ARP, runway thresholds, parking
        positions\] / AIRAC

3.  **Environment**
    -   METAR
    -   SIGMET
    -   Weather, atmosphere
    -   noise

4.  **Performance**
    -   BADA
    -   OpenAP
    -   ECAC

### Part 3. Access and explore data

1.  **The ecosystem of analytics tools**
    > (R, Python, Javascript/Observable, more?)

2.  **Common data sources**
    > \#include
    > [[https://atmdata.github.io/]{.underline}](https://atmdata.github.io/)\
    > Promote flight table project (RQ)

3.  **An overview of open datasets for aviation**

4.  **Exploring a dataset**
    > (scrape,) parse, open, visualise

### Part 4. Process data

1.  **The tidy paradigm**
    > Examples in R, Javascript, Python

2.  **Processing geometric and geographical data**

3.  **Processing aircraft trajectories**

4.  **Information extraction**

5.  **Optimisation in data analytics**
    > *Include prediction, or make it a different chapter\...*

6.  **Handling uncertainty**

### Part 5. Visualise data

1.  **The art of storytelling**

2.  **Grammar of graphics**

3.  **Produce meaningful maps**

### Part 6. Share data

*Introduction about reproducible research. This would also include
sharing the code beyond the dataset cleaning to producing related
summaries, tables/graphics, etc.*

1.  **Good practices for producing a clean dataset**
    > \#include and use some of the datasets in 'traffic' / Zenodo /
    > ... these could be used in the examples in the book (and it would
    > be great to explain how to arrive to a clean dataset)

2.  **Issues around dataset sharing**
    > open data, licensing, etc.?

### Appendix

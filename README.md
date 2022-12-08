
![logo](pyTREVL_logo.png)

### What is pyTREVL?

At Trendence, we are using [Cube.js](https://cube.dev/) to serve some of our data. We want to visualize
the resulting data with the manifold power of [Highcharts](https://www.highcharts.com/) in our apps,
but also within Jupyter notebook environments.

To achieve this, we have written an API connecting both parts. Our API can read a Trendence-specific DSL
for visualizations that we call TREVL ("Trendence Visualization Language") where we can reference data cubes
and define visualization options.

**pyTREVL** is a Python package that makes generating Highcharts viz from cube data easy and helps
our Data Scientists with the generation of TREVL code, enabling them to experiment
with our data served by Cube in a Jupyter notebook environment.

### Why are you sharing pyTREVL?

We are strong believers in the power of Open Source Software. TREVL itself works currently only with a proprietary API that
we are not entirely ready to share at this stage, but pyTREVL also offers the opportunity to plug in any Cube connection and we believe
other people may are also interested in combination of Cube.js and Highcharts within Jupyter notebooks environments.

So our goal is to provide a little foundational step here. And because we are excited about it, you are maybe, too 🤓 If you are interested,
feel free to play around with pyTREVL. In case of questions or Feedback, open a GitHub Issue or reach out to us via [pytrevl@trendence.com](mailto:pytrevl@trendence.com)


### How do I plug in my own Cube endpoint?

You just have to set some ENV variables. Details coming Soon 🤗 🚧

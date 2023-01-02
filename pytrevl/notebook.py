"""Display a single Highcharts chart in an IFrame."""
import html
import json

# Default template for the IFrame source
_default_template = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link href="https://www.highcharts.com/highslide/highslide.css" rel="stylesheet" />
    <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
    <script type="text/javascript" src="https://code.highcharts.com/6/highcharts.js"></script>
    <script type="text/javascript" src="https://code.highcharts.com/6/highcharts-more.js"></script>
    <script type="text/javascript" src="https://code.highcharts.com/6/modules/heatmap.js"></script>
    <script type="text/javascript" src="https://code.highcharts.com/6/modules/exporting.js"></script>
  </head>
  <body style="margin:0;padding:0">
    <div id="container" style="">Loading....</div>
    <script>
      $(function(){{
        console.log('AA');
        Highcharts.setOptions({{ "global": {{}}, "lang": {{}}, }});
        var options = {options};
        var chart = new Highcharts.Chart('container', options);

      }});
    </script>
  </body>
</html>
"""

def chart_iframe(chart_options, width=800, height=400, template=None):
    """Build IFrame from Highcharts chart options."""
    if template is None:
        template = _default_template

    page_src = template.format(options=json.dumps(chart_options))
    # We need to HTML-escape the source document
    src_doc = html.escape(page_src).replace('\n', ' ')
    return f"""<iframe width={width} height={height} srcdoc="{src_doc}"></iframe>"""

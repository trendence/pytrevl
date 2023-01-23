"""Display a single Highcharts chart in an IFrame."""
import html
import json

def render_component(comp, *args, **kwargs):
    if comp['type'] == 'chart':
        return render_chart(comp, *args, **kwargs)
    if comp['type'] == 'score':
        return render_score(comp, *args, **kwargs)
    raise ValueError(f"Unknown component type {comp['type']!r}")

# Default template for the IFrame source
_highcharts_template = """
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

_score_template = """
<div>
  <p>{value} {unit} (rounded to {digits})</p>
  <p>{text}</p>
</div>"""

def render_chart(chart_options, width=800, height=400, template=None):
    """Build IFrame from Highcharts chart options."""
    if template is None:
        template = _highcharts_template

    page_src = template.format(options=json.dumps(chart_options))
    # We need to HTML-escape the source document
    src_doc = html.escape(page_src).replace('\n', ' ')
    return f"""<iframe width={width} height={height} srcdoc="{src_doc}"></iframe>"""

def render_score(comp):
    defaults = {
        'unit': 'no-unit',
        'digits': 'no-digits',
        'text': 'no-text',
    }
    return _score_template.format(**{**defaults, **comp})

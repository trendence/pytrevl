import html
import json

class IpythonHC:
    # template for the IFrame
    iframe_template = """
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
    console.log('A');
      $(function(){{
        console.log('AA');
        Highcharts.setOptions({{ "global": {{}}, "lang": {{}}, }});
        var options = {options};
        var chart = new Highcharts.Chart('container', options);
        console.log('B'); 
      }});
    console.log('BB');
    </script>
  </body>
</html>
    """
    def __init__(self, options):
        self.options = options
        
    @property
    def iframe(self):
        return self.iframe_template.format(options=json.dumps(self.options))
        
    def _repr_html_(self):
        src_doc = html.escape(self.iframe).replace('\n', ' ')
        return ''.join((
            "<p><p>",
            f"""<iframe width=800 height=400 srcdoc="{src_doc}"></iframe>""",
            "<p><p>",
        ))
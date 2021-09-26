<%@ page import="langpop.Site" %>
<!DOCTYPE html>
<html>
  <head>
    <g:javascript src="Chart.bundle.min.js" />
    <canvas id="myChart"></canvas>
    <script>
    var xmlhttp = new XMLHttpRequest();
    var url = "ajaxGetTopLangs";

    xmlhttp.onreadystatechange = function() {
      if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
        var chartData = JSON.parse(xmlhttp.responseText);
        displayChart(chartData);
      }
    };
    xmlhttp.open("GET", url, true);
    xmlhttp.send();

    function displayChart(chartData) {
      var ctx = document.getElementById("myChart");
      var myChart = new Chart(ctx, {
        type: 'line',
        data: chartData
      });
    }
    </script>
  </head>
  <body>
  </body>
</html>

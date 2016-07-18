<%@ page import="langpop.Site" %>
<!DOCTYPE html>
<html>
  <head>
    <g:javascript src="Chart.bundle.min.js" />
    <canvas id="myChart"></canvas>
    <script>
    var ctx = document.getElementById("myChart");
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [${raw(dataLabels)}],
            datasets: [
                {
                    label: "${dataSetLabels[0]}",
                    fill: false,
                    lineTension: 0.1,
                    backgroundColor: "rgba(63,81,181,0.4)",
                    borderColor: "rgba(63,81,181,1)",
                    data: ${data1},
                },
                {
                    label: "${dataSetLabels[1]}",
                    fill: false,
                    lineTension: 0.1,
                    backgroundColor: "rgba(3,169,244,0.4)",
                    borderColor: "rgba(3,169,244,1)",
                    data: ${data2},
                },
                {
                    label: "${dataSetLabels[2]}",
                    fill: false,
                    lineTension: 0.1,
                    backgroundColor: "rgba(0,150,136,0.4)",
                    borderColor: "rgba(0,150,136,1)",
                    data: ${data3},
                },
                {
                    label: "${dataSetLabels[3]}",
                    fill: false,
                    lineTension: 0.1,
                    backgroundColor: "rgba(139,195,74,0.4)",
                    borderColor: "rgba(139,195,74,1)",
                    data: ${data4},
                },
                {
                    label: "${dataSetLabels[4]}",
                    fill: false,
                    lineTension: 0.1,
                    backgroundColor: "rgba(255,235,59,0.4)",
                    borderColor: "rgba(255,235,59,1)",
                    data: ${data5},
                }
            ]
        }
    });
    </script>
  </head>
  <body>
  </body>
</html>

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
            labels: ["January", "February", "March", "April", "May", "June", "July"],
            datasets: [
                {
                    label: "One",
                    fill: false,
                    lineTension: 0.1,
                    backgroundColor: "rgba(63,81,181,0.4)",
                    borderColor: "rgba(63,81,181,1)",
                    data: [40, 55, 56, 59, 65, 80, 81],
                },
                {
                    label: "Two",
                    fill: false,
                    lineTension: 0.1,
                    backgroundColor: "rgba(3,169,244,0.4)",
                    borderColor: "rgba(3,169,244,1)",
                    data: [41, 49, 57, 70, 72, 79, 79],
                },
                {
                    label: "Three",
                    fill: false,
                    lineTension: 0.1,
                    backgroundColor: "rgba(0,150,136,0.4)",
                    borderColor: "rgba(0,150,136,1)",
                    data: [36, 45, 50, 71, 88, 93, 97],
                },
                {
                    label: "Four",
                    fill: false,
                    lineTension: 0.1,
                    backgroundColor: "rgba(139,195,74,0.4)",
                    borderColor: "rgba(139,195,74,1)",
                    data: [35, 51, 71, 72, 80, 96, 99],
                },
                {
                    label: "Five",
                    fill: false,
                    lineTension: 0.1,
                    backgroundColor: "rgba(255,235,59,0.4)",
                    borderColor: "rgba(255,235,59,1)",
                    data: [25, 35, 41, 47, 51, 54, 60],
                }
            ]
        }
    });
    </script>
  </head>
  <body>
  </body>
</html>

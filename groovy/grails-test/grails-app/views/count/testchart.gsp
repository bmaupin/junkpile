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
        data: {"labels":["2016-07-18","2016-04-19","2016-01-20","2015-10-22","2015-07-24"],"datasets":[{"label":"JavaScript","fill":false,"lineTension":0.1,"backgroundColor":"rgba(63,81,181,0.4)","borderColor":"rgba(63,81,181,1)","data":[3589073,3256912,2906467,2634192,0]},{"label":"Java","fill":false,"lineTension":0.1,"backgroundColor":"rgba(3,169,244,0.4)","borderColor":"rgba(3,169,244,1)","data":[3237993,2946852,2618301,2361223,0]},{"label":"PHP","fill":false,"lineTension":0.1,"backgroundColor":"rgba(0,150,136,0.4)","borderColor":"rgba(0,150,136,1)","data":[1872815,1756334,1626937,1519412,0]},{"label":"Python","fill":false,"lineTension":0.1,"backgroundColor":"rgba(139,195,74,0.4)","borderColor":"rgba(139,195,74,1)","data":[1762429,1605598,1435770,1300540,0]},{"label":"HTML","fill":false,"lineTension":0.1,"backgroundColor":"rgba(255,235,59,0.4)","borderColor":"rgba(255,235,59,1)","data":[1516848,1304396,1075359,900316,0]},{"label":"C#","fill":false,"lineTension":0.1,"backgroundColor":"rgba(255,152,0,0.4)","borderColor":"rgba(255,152,0,1)","data":[1515712,1414741,1308666,1219386,0]},{"label":"Ruby","fill":false,"lineTension":0.1,"backgroundColor":"rgba(233,30,99,0.4)","borderColor":"rgba(233,30,99,1)","data":[1220492,1159923,1093882,1034747,0]},{"label":"CSS","fill":false,"lineTension":0.1,"backgroundColor":"rgba(103,58,183,0.4)","borderColor":"rgba(103,58,183,1)","data":[1162009,1058272,953716,871665,0]},{"label":"C++","fill":false,"lineTension":0.1,"backgroundColor":"rgba(33,150,243,0.4)","borderColor":"rgba(33,150,243,1)","data":[1073916,1002739,914258,841575,0]},{"label":"C","fill":false,"lineTension":0.1,"backgroundColor":"rgba(0,188,212,0.4)","borderColor":"rgba(0,188,212,1)","data":[742269,697173,634470,582639,0]}]}
    });
    </script>
  </head>
  <body>
  </body>
</html>

//function modify(new_legend){
//
//var legend_keys=[];
//var series_array = [];
//for (var k in new_legend) {
//  var series_item = new Array();
//  legend_keys.push(k)
//  var series_item = {'name': k, 'type': 'line', 'data': new_legend[k]};
//
//  console.log(series_item);
//  series_array.push(series_item);
//}
//return series_array
//}

//绘制统计图
jQuery(document).ready(function() {
var x_axis = $("#x_axis").html();

var x_test = $("#x_ax").html();
var x_test_item = eval('(' + x_test + ')')



new_xaxis = x_axis.replace('/u/g','').replace('[','').replace(']', '').split(',')
var legend = $("#legend").html();

var new_legend = eval('(' + legend + ')');

var legend_keys=[];
var series_array = [];
for (var k in new_legend) {
  var series_item = new Array();
  legend_keys.push(k)
  var series_item = {'name': k, 'type': 'line', 'data': new_legend[k]};

  console.log(series_item);
  series_array.push(series_item);
}
//var series_array = modify(new_legend);

var arima = $("#arima").html();
var new_arima = eval('(' + arima + ')');

var legend_keys2=[];
var series_array2 = [];
for (var k in new_arima) {
  var series_item2 = new Array();
  legend_keys2.push(k)
  var series_item2 = {'name': k, 'type': 'line', 'data': new_arima[k]};

  console.log(series_item2);
  series_array2.push(series_item2);
}


//var series_array2 = modify(new_arima);

var lstm = $("#lstm").html();
var new_lstm = eval('(' + lstm + ')');
var legend_keys3=[];
var series_array3 = [];
for (var k in new_lstm) {
  var series_item3 = new Array();
  legend_keys3.push(k)
  var series_item3 = {'name': k, 'type': 'line', 'data': new_lstm[k]};

  console.log(series_item3);
  series_array3.push(series_item3);
}
//var series_array3 = modify(new_lstm);



var myCharts1 = echarts.init(document.getElementById('container'));
var myCharts2 = echarts.init(document.getElementById('container2'));
var myCharts3 = echarts.init(document.getElementById('container3'));
var  option= {
    title: {
        text: ''  //'Step Line'
    },
    tooltip: {
        trigger: 'axis'
    },
    legend: {
        data: legend_keys // ['Step Start', 'Step Middle', 'Step End']
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    toolbox: {
        feature: {
            saveAsImage: {}
        }
    },
    xAxis: {
        type: 'category',
        data: x_test_item['x']  //['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    },
    yAxis: {
        type: 'value'
    },
    dataZoom:
    {type: 'inside',
        start: 0,
        end: 10},
    series: series_array
//    [
//        {
//            name:'Step Start',
//            type:'line',
//            step: 'start',
//            data:[120, 132, 101, 134, 90, 230, 210]
//        },
//        {
//            name:'Step Middle',
//            type:'line',
//            step: 'middle',
//            data:[220, 282, 201, 234, 290, 430, 410]
//        },
//        {
//            name:'Step End',
//            type:'line',
//            step: 'end',
//            data:[450, 432, 401, 454, 590, 530, 510]
//        }
//    ]
};


//

var  option2= {
    title: {
        text: ''
    },
    tooltip: {
        trigger: 'axis'
    },
    legend: {
        data: legend_keys2
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    toolbox: {
        feature: {
            saveAsImage: {}
        }
    },
    xAxis: {
        type: 'category',
        data: x_test_item['x']
    },
    yAxis: {
        type: 'value'
    },
    series: series_array2

};


var  option3= {
    title: {
        text: ''
    },
    tooltip: {
        trigger: 'axis'
    },
    legend: {
        data: legend_keys3
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    toolbox: {
        feature: {
            saveAsImage: {}
        }
    },
    xAxis: {
        type: 'category',
        data: x_test_item['x']
    },
    yAxis: {
        type: 'value'
    },
    series: series_array3

};
myCharts1.setOption(option);
myCharts2.setOption(option2);
myCharts3.setOption(option3);

 });

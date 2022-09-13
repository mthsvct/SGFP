window.onload = function colcocaCor(){
    
    let todas = document.getElementsByClassName('opcao')
    let i, cor;
    let tam = todas.length;
    let botaoCor;

    for(i=0; i<tam; i++){
        cor = todas[i].getElementsByClassName('corzinha')[0].textContent;
        botaoCor = todas[i].getElementsByClassName('botaoCor')[0]
        botaoCor.style.backgroundColor = cor;
    }
}

google.charts.load('current', {packages: ['corechart']});
google.charts.setOnLoadCallback(drawBasic);

function drawBasic() {

    var data = google.visualization.arrayToDataTable([
        ['mes','valor'],
        ['Jan',100],
        ['Fev',400],
        ['Mar',250],
        ['abr',500]
    ]);

    var options = {
        title: 'Gastos por mês',
        titleTextStyle: {
            fontSize: 16,
        
          },
          width: 600,
          height: 400,
        colors : ['#4BB9AF'],
        legend: 'none'
    };

    var chart = new google.visualization.LineChart(document.getElementById('gr1'));

    chart.draw(data, options);

    var data2 = google.visualization.arrayToDataTable([
        ['Status', 'qnt'],
        ['Disponivel', 100],
        ['Usado',400]
      ]);
  
      var options2 = {
        title: 'Limite dos cartões',
        width: 600,
        height: 400,
        colors: ['#AEEEE0','#4BB9AF'],
       
      };
  
      var chart2 = new google.visualization.PieChart(document.getElementById('gr2'));
  
      chart2.draw(data2, options2);

      var data3 = google.visualization.arrayToDataTable([
        ["Element", "Density" ],
        ["1", 8.94],
        ["2", 10.49],
        ["3", 19.30],
        ["4", 21.45]
      ]);

      var options3 = {
        title: "Gastos por categoria",
        width: 600,
        height: 400,
        bar: {groupWidth: "95%"},
        legend: { position: "none" },
        colors: ['#AEEEE0']
      };
      var chart3 = new google.visualization.ColumnChart(document.getElementById("gr3"));
      chart3.draw(data3, options3);
}
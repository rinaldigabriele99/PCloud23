//$(document).ready(function() {
//  document.addEventListener('DOMContentLoaded', function() {
//    //setTimeout(function() {}, 1000);
//    functionData();
//    functionMostraNascondi();
//  });
//});


document.addEventListener('DOMContentLoaded', function() {
  $("#div2").removeClass("hidden");
  functionMostraNascondi();
  functionData();
});


function functionMostraNascondi(){
  $("#showDiv1").click(function(){
    $("#div1").removeClass("hidden");
    $("#div2").addClass("hidden");
    $("#div3").addClass("hidden");
    $("#div4").addClass("hidden");
  });

  // Mostra/nascondi Div 2
  $("#showDiv2").click(function(){
    $("#div1").addClass("hidden");
    $("#div2").removeClass("hidden");
    $("#div3").addClass("hidden");
    $("#div4").addClass("hidden");
  });

  // Mostra/nascondi Div 3
  $("#showDiv3").click(function(){
    $("#div3").removeClass("hidden");
    $("#div2").addClass("hidden");
    $("#div1").addClass("hidden");
    $("#div4").addClass("hidden");
  });

  $("#showDiv4").click(function(){
    $("#div4").removeClass("hidden");
    $("#div2").addClass("hidden");
    $("#div3").addClass("hidden");
    $("#div1").addClass("hidden");
  });
}

function functionData(){
  datiJson = $.ajax({
    url: '/sensors/all',
    type: 'GET',
    dataType: 'json',
    success: function(data) {
      popolaTabella()
      valoriMinMaxMean()
      functionGraph01()
      functionGraph02()
      functionGraph03()
      functionGraph04()
      functionGraph05()
    },
    error: function(error) {
      console.error('Error fetching JSON:', error);
    }
  })
}


function popolaTabella(){
    console.log(datiJson.responseJSON)
    $('#dataTable').DataTable({
      data: datiJson.responseJSON,
      columns: [
          { title: 'Sensor', data: 'Sensors' },
          { title: 'Date', data: 'date' },
          { title: '%IronFeed', data: '%IronFeed' },
          { title: '%SilicaFeed', data: '%SilicaFeed' },
          { title: 'StarchFlow', data: 'StarchFlow' },
          { title: 'AminaFlow', data: 'AminaFlow'},
          { title: 'Flow', data: 'OrePulpFlow'},
          { title: 'PH', data: 'OrePulppH' },
          { title: 'Density', data: 'OrePulpDensity' },
          { title: '1AirFlow', data: 'FlotationColumn01AirFlow' },
          { title: '2AirFlow', data: 'FlotationColumn02AirFlow', name: 'FlotationColumn02AirFlow'},
          { title: '3AirFlow', data: 'FlotationColumn03AirFlow' },
          { title: '4AirFlow', data: 'FlotationColumn04AirFlow' },
          { title: '5AirFlow', data: 'FlotationColumn05AirFlow' },
          { title: '6AirFlow', data: 'FlotationColumn06AirFlow' },
          { title: '7AirFlow', data: 'FlotationColumn07AirFlow' },
          { title: '1Level', data: 'FlotationColumn01Level' },
          { title: '2Level', data: 'FlotationColumn02Level' },
          { title: '3Level', data: 'FlotationColumn03Level' },
          { title: '4Level', data: 'FlotationColumn04Level' },
          { title: '5Level', data: 'FlotationColumn05Level' },
          { title: '6Level', data: 'FlotationColumn06Level' },
          { title: '7Level', data: 'FlotationColumn07Level' },
          { title: '%Iron', data: '%IronConcentrate' },
          { title: '%Silica', data: '%SilicaConcentrate' }
      ],
      columnDefs: [
        // nascondiamo alcune colonne perchè sono troppe e nella pagina vengono visualizzate male
        { targets: [10,11,12,13,14,15,17,18,19,20,21,22], visible: false}
      ],
      lengthMenu: [ 5,10,15,20 ], 
      pageLength: 5
    });  
  }
  
function  functionDataGraph01(){
  data = datiJson.responseJSON
  listaDatiGraph = [['Sensors', 'StarchFlow']]
  rigaGraph = []
  for (var i = 0; i < data.length; i++) {
    var oggettoJson = data[i];
    rigaGraph = []
    rigaGraph.push(oggettoJson.Sensors)
    rigaGraph.push(parseFloat(oggettoJson.StarchFlow.replace(',', '.')))
    listaDatiGraph.push(rigaGraph)
  }
  console.log(listaDatiGraph)
  return listaDatiGraph
}

function  functionDataGraph02(){
  data = datiJson.responseJSON
  listaDatiGraph = [['Sensors', 'AminaFlow']]
  rigaGraph = []
  for (var i = 0; i < data.length; i++) {
    var oggettoJson = data[i];
    rigaGraph = []
    rigaGraph.push(oggettoJson.Sensors)
    rigaGraph.push(parseFloat(oggettoJson.AminaFlow.replace(',', '.')))
    listaDatiGraph.push(rigaGraph)
  }
  console.log(listaDatiGraph)
  return listaDatiGraph
}

function  functionDataGraph03(){
  data = datiJson.responseJSON
  listaDatiGraph = [['Sensors', 'Ore Pulp Flow']]
  rigaGraph = []
  for (var i = 0; i < data.length; i++) {
    var oggettoJson = data[i];
    rigaGraph = []
    rigaGraph.push(oggettoJson.Sensors)
    rigaGraph.push(parseFloat(oggettoJson.OrePulpFlow.replace(',', '.')))
    listaDatiGraph.push(rigaGraph)
  }
  console.log(listaDatiGraph)
  return listaDatiGraph
}

function functionDataGraph04(){
  data = datiJson.responseJSON
  listaDatiGraph = [['Sensors', '% Silica Concentrate']]
  rigaGraph = []
  for (var i = 0; i < data.length; i++) {
    var oggettoJson = data[i];
    rigaGraph = []
    rigaGraph.push(oggettoJson.Sensors)
    rigaGraph.push(parseFloat(oggettoJson['%SilicaConcentrate'].replace(',', '.')))
    listaDatiGraph.push(rigaGraph)
  }
  console.log(listaDatiGraph)
  return listaDatiGraph
}

function functionDataGraph05(){
  data = datiJson.responseJSON
  listaDatiGraph = [['% Silica Concentrate', 'Count']]
  listaSilica = []
  rigaGraph = []
  //faccio questo for per creare la lista contenete i valori silica una sola volta!
  for (var i = 0; i < data.length; i++) {
    var oggettoJson = data[i];
    if (!listaSilica.includes(parseFloat(oggettoJson['%SilicaConcentrate'].replace(',', '.')))){
      listaSilica.push(parseFloat(oggettoJson['%SilicaConcentrate'].replace(',', '.')))
    }
  }
  //scorro la lista di silica per determinare quante volte è presente quel valore
  for (var i = 0; i < listaSilica.length; i++) {
    rigaGraph = []
    conta = 0
    for (var j = 0; j < data.length; j++) {
      var oggettoJson = data[j];
      if (listaSilica[i] == parseFloat(oggettoJson['%SilicaConcentrate'].replace(',', '.')))
        conta ++
    }
    rigaGraph.push(listaSilica[i])
    rigaGraph.push(conta)
    listaDatiGraph.push(rigaGraph)
  }
  console.log(listaDatiGraph)
  return listaDatiGraph
}

function valoriMinMaxMean(){
  data = datiJson.responseJSON
  console.log('data:', data)
  lista = []
  media = 0
  for (var i = 0; i < data.length; i++) {
    lista.push(parseFloat(data[i]['%SilicaConcentrate'].replace(',', '.')))
  }
  console.log('lista:', lista)
  var somma = 0;
  for (var i = 0; i < lista.length; i++) {
    somma += lista[i]
  }
  media = somma/lista.length
  min = Math.min(...lista)
  max = Math.max(...lista)

  var mediaSilica = document.getElementById("media");
  mediaSilica.textContent = media
  var minSilica = document.getElementById("min");
  minSilica.textContent = min
  var maxSilica = document.getElementById("max");
  maxSilica.textContent = max
}

function functionGraph01(){
  google.charts.load('current', {'packages':['bar']});
  google.charts.setOnLoadCallback(drawChart);

  function drawChart() {
    var data = google.visualization.arrayToDataTable(functionDataGraph01());
    setTimeout(function() {
              var options = {
              chart: {title: 'Sensors - StarchFlow'},
              hAxis: {title: 'Sensors',  titleTextStyle: {color: '#333'}},
              vAxis: {minValue: 0},
              bars: 'vertical',
              width: 1200,
              height: 400
        }; 
        var chart = new google.charts.Bar(document.getElementById('columnchart_material01'));
        chart.draw(data, google.charts.Bar.convertOptions(options));
    }, 1500);

  }
}

function functionGraph02(){
  google.charts.load('current', {'packages':['bar']});
  google.charts.setOnLoadCallback(drawChart);

  function drawChart() {
    var data = google.visualization.arrayToDataTable(functionDataGraph02());
    setTimeout(function() {
      var options = {
      chart: {title: 'Sensors - AminaFlow'},
      hAxis: {title: 'Sensors',  titleTextStyle: {color: '#333'}},
      vAxis: {minValue: 500},
      bars: 'vertical',
      width: 1200,
      height: 400
    }; 
    var chart = new google.charts.Bar(document.getElementById('columnchart_material02'));
    chart.draw(data, google.charts.Bar.convertOptions(options));
    }, 1500);
  }
}

function functionGraph03(){
  google.charts.load('current', {'packages':['bar']});
  google.charts.setOnLoadCallback(drawChart);

  function drawChart() {
    var data = google.visualization.arrayToDataTable(functionDataGraph03());
    setTimeout(function() {
      var options = {
      chart: {title: 'Sensors - Ore Pulp Density'},
      hAxis: {title: 'Sensors',  titleTextStyle: {color: '#333'}},
      vAxis: {minValue: 350, maxValue: 450},
      bars: 'vertical',
      width: 1200,
      height: 400
    }; 
    var chart = new google.charts.Bar(document.getElementById('columnchart_material03'));
    chart.draw(data, google.charts.Bar.convertOptions(options));
    }, 1500);

  }
}

function functionGraph04(){
  google.charts.load('current', {'packages':['bar']});
  google.charts.setOnLoadCallback(drawChart);

  function drawChart() {
    var data = google.visualization.arrayToDataTable(functionDataGraph04());
    setTimeout(function() {
      var options = {
      chart: {title: 'Sensors - % Silica Concentrate'},
      hAxis: {title: 'Sensors',  titleTextStyle: {color: '#333'}},
      vAxis: {minValue: 0},
      bars: 'vertical',
      width: 1200,
      height: 400
    }; 
    var chart = new google.charts.Bar(document.getElementById('columnchart_material04'));
    chart.draw(data, google.charts.Bar.convertOptions(options));
    }, 1500);
  }
}

function functionGraph05(){
  google.charts.load('current', {'packages':['bar']});
  google.charts.setOnLoadCallback(drawChart);

  function drawChart() {
    var data = google.visualization.arrayToDataTable(functionDataGraph05());
    setTimeout(function() {
      var options = {
      chart: {title: '% Silica Concentrate - Count'},
      hAxis: {title: '% Silica Concentrate',  titleTextStyle: {color: '#333'}},
      vAxis: {minValue: 0},
      bars: 'vertical',
      width: 1200,
      height: 400
    }; 
    var chart = new google.charts.Bar(document.getElementById('columnchart_material05'));
    chart.draw(data, google.charts.Bar.convertOptions(options));
    }, 1500);
  }
}

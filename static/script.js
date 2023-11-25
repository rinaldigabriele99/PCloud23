$(document).ready(function() {

  functionTable();
  functionGraph();
  functionML();

});

function functionTable(){
  datiJson = $.ajax({
    url: '/sensors/all',
    type: 'GET',
    dataType: 'json',
    success: function(data) {
      popolaTabella()
      functionGraph01()
      functionGraph02()
      functionGraph03()
      functionGraph04()
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
        // Example: Hide the second column
        { targets: [10,11,12,13,14,15,17,18,19,20,21,22], visible: false}
        //,{ targets: [1], width: '300px'}
      ],
      lengthMenu: [ 5,10,15,20 ], // Display only the option for 10 rows per page
      pageLength: 5
    });  
  }
  


function functionGraph01(){
  google.charts.load('current', {'packages':['bar']});
  google.charts.setOnLoadCallback(drawChart);

  function drawChart() {
    var data = google.visualization.arrayToDataTable([
          ['Year', 'Sales', 'Expenses', 'Profit'],
          ['2014', 1000, 400, 200],
          ['2015', 1170, 460, 250],
          ['2016', 660, 1120, 300],
          ['2017', 1030, 540, 350]
    ]);

    var options = {
          chart: {
            title: 'Company Performance',
            subtitle: 'Sales, Expenses, and Profit: 2014-2017',
            width: 500, // Larghezza iniziale del grafico
            height: 300 // Altezza iniziale del grafico
          }
    };

    var chart = new google.charts.Bar(document.getElementById('columnchart_material01'));

        chart.draw(data, google.charts.Bar.convertOptions(options));
  }
}

function functionGraph02(){
  google.charts.load('current', {'packages':['bar']});
  google.charts.setOnLoadCallback(drawChart);

  function drawChart() {
    var data = google.visualization.arrayToDataTable([
          ['Year', 'Sales', 'Expenses', 'Profit'],
          ['2014', 1000, 400, 200],
          ['2015', 1170, 460, 250],
          ['2016', 660, 1120, 300],
          ['2017', 1030, 540, 350]
    ]);

    var options = {
          chart: {
            title: 'Company Performance',
            subtitle: 'Sales, Expenses, and Profit: 2014-2017',
            width: 500, // Larghezza iniziale del grafico
            height: 300 // Altezza iniziale del grafico
          }
    };

    var chart = new google.charts.Bar(document.getElementById('columnchart_material02'));

        chart.draw(data, google.charts.Bar.convertOptions(options));
  }
}

function functionGraph03(){
  google.charts.load('current', {'packages':['bar']});
  google.charts.setOnLoadCallback(drawChart);

  function drawChart() {
    var data = google.visualization.arrayToDataTable([
          ['Year', 'Sales', 'Expenses', 'Profit'],
          ['2014', 1000, 400, 200],
          ['2015', 1170, 460, 250],
          ['2016', 660, 1120, 300],
          ['2017', 1030, 540, 350]
    ]);

    var options = {
          chart: {
            title: 'Company Performance',
            subtitle: 'Sales, Expenses, and Profit: 2014-2017',
            width: 500, // Larghezza iniziale del grafico
            height: 300 // Altezza iniziale del grafico
          }
    };

    var chart = new google.charts.Bar(document.getElementById('columnchart_material03'));

        chart.draw(data, google.charts.Bar.convertOptions(options));
  }
}

function functionGraph04(){
  google.charts.load('current', {'packages':['bar']});
  google.charts.setOnLoadCallback(drawChart);

  function drawChart() {
    var data = google.visualization.arrayToDataTable([
          ['Year', 'Sales', 'Expenses', 'Profit'],
          ['2014', 1000, 400, 200],
          ['2015', 1170, 460, 250],
          ['2016', 660, 1120, 300],
          ['2017', 1030, 540, 350]
    ]);

    var options = {
          chart: {
            title: 'Company Performance',
            subtitle: 'Sales, Expenses, and Profit: 2014-2017',
            width: 500, // Larghezza iniziale del grafico
            height: 300 // Altezza iniziale del grafico
          }
    };

    var chart = new google.charts.Bar(document.getElementById('columnchart_material04'));

        chart.draw(data, google.charts.Bar.convertOptions(options));
  }
}

function functionML(){
  
}
 
/*
  console.log('pippo')
    // Use jQuery AJAX to fetch JSON data from the server
    $.ajax({
      url: '/sensors/all',
      type: 'GET',
      dataType: 'json',
      success: function(data) {
        // Process the JSON data
        console.log('1',data);
  
        // Display the data on the page (modify this part based on your needs)
        //$('#result').text(JSON.stringify(data, null, 2));
      },
      error: function(error) {
        console.error('Error fetching JSON:', error);
      }
    });
    //console.log('2', json)

    //converti il json_data in una lista di json
    //passi il la lista di json alla datatable

    //converti il json_data in una lista di dati per fare i grafici
*/
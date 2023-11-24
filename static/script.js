$(document).ready(function() {
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
    
});
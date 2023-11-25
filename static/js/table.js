
d3.json("/api/table/requests/active").then(data => {

    // extract keys from json
    let keys = new Set();
    for (let key in data[0]) {
        keys.add(key)
    };

    // use keys to create html header information
    let headerHTML = "";
    let columns = [...keys];
    columns.forEach(i => {headerHTML = headerHTML + `<th>${i}</th>`} );

    // create table 
    let table_loc = d3.select('#request-table');
    let table = table_loc.append('table');
    table.attr('class','styled-table');
    
    // add header row
    let table_head = table.append('thead').append('tr')
        
    table_head.html(headerHTML);

    // add table body and rows for each json object
    let rows = table.append('tbody')
        .selectAll('tr')
        .data(data)
        .enter()
        .append('tr');
   
    // add data to each row from json objects
    let cells = rows.selectAll('td')
        .data((d) => Object.entries(d))
        .enter()
        .append('td')
        // .text(d => d[1]);

    cells.filter(d => d[0] == "Request ID")
    	.append("a")
        .attr("href", function(d) {
            return "https://www.google.com/search?q=" + d[1];
        })
        .html(function(d) {
            return (d[1]);
        });

    cells.filter(d => d[0] != "Request ID")
        .html(function(d) {
            return (d[1]);
        });


    table_head.append('td').text('')
    table_head.append('td').text('')

    rows.append('td').append('button').attr('class','btn btn-secondary').text('Report Lost')
    rows.append('td').append('button').attr('class','btn btn-secondary').text('Return')

});
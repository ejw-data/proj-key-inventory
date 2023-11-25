
d3.json("/api/table/requests/active").then(data => {

    // extract keys from json
    let keys = new Set();
    for (let key in data[0]) {
        keys.add(key)
    };

    // use keys to create html header information
    let headerHTML = "";
    let header_keywords = [...keys];
    header_keywords.forEach(i => {headerHTML = headerHTML + `<th>${i}</th>`} );

    // create table 
    let table_loc = d3.select('#request-table');
    let table = table_loc.append('table');
    table.attr('class','styled-table');
    
    // add header row
    let table_head = table.append('thead').append('tr')
        
    table_head.html(headerHTML);

    // add table body and rows for each json object
    let row = table.append('tbody')
        .selectAll('tr')
        .data(data)
        .enter()
        .append('tr');
   
    // add data to each row from json objects
    row.selectAll('td')
        .data((d,i) => Object.values(d))
        .enter()
        .append('td')
        .text(d=> d);

    table_head.append('td').text('')
    table_head.append('td').text('')

    row.append('td').append('button').attr('class','btn btn-secondary').text('Report Lost')
    row.append('td').append('button').attr('class','btn btn-secondary').text('Return')

});
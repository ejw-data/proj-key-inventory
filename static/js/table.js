let data_url = "/api/table/requests/active";
// let hyperlink_columns = {
//     'columns_name': ['Request ID'],
//     'column_url': ['/api/request/details/']
// };

let hyperlinks = [
    {'column_name':'Request ID',
     'column_url': '/api/request/details/'}
];

let buttons = [
    {'name': 'Report Lost',
     'url': '/api/request/lost/',
     'column': 'Request ID' 
    },
    {'name': 'Return',
     'url': '/api/request/return/',
     'column': 'Request ID' 
    }
];


function createTable(data, buttons){
    d3.json(data).then(data => {

        // extract keys from json
        let keys = new Set();
        for (let key in data[0]) {
            keys.add(key)
        };

        console.log(buttons)

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
    
        // create the cells
        let cells = rows.selectAll('td')
            .data((d) => Object.entries(d))
            .enter()
            .append('td')
 

        // add data to each row from json objects
        cells.filter(d => d[0] == "Request ID")
            .append("a")
            .attr("href", function(d) {
                return "/api/request/details/" + d[1];
            })
            .html(function(d) {
                return (d[1]);
            });

        cells.filter(d => d[0] != "Request ID")
            .html(function(d) {
                return (d[1]);
            });


        // add empty header columns and buttons
        buttons.forEach( button => {
            table_head.append('td').text('');
            rows.append('td')
                .append('a')
                .attr("href", function(d){return button.url + d[button.column]})
                .append('button')
                .attr('class','btn btn-secondary')
                .text(button.name)
        });

    });
}

createTable(data_url, buttons)
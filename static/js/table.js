function createTable(data, id, buttons=[], hyperlinks=[], nullmessage="No results found."){
    d3.json(data).then(data => {

        let include_buttons = true
        // console.log(data)
        // check to see if no data exists
        if (data.length === 0){
            data = [{"Status": nullmessage}]
            include_buttons = false;
        }

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
        let table_loc = d3.select(id);
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


        // add data to cells and hyperlinks as specificied
        let hyper_columns = hyperlinks.map(i => i.column_name);
        
        columns.forEach(column =>{
            
            if (hyper_columns.includes(column)){
                // get column url
                let loop_url = hyperlinks.filter(i => i.column_name == column)[0].column_url;

                cells.filter(d => d[0] == column)
                    .append("a")
                    .attr("href", function(d) {
                        return loop_url + d[1];
                    })
                    .html(function(d) {
                        return (d[1]);
                    });
            }
            else if (!hyper_columns.includes(column)) {
                cells.filter(d => d[0] == column)
                .html(function(d) {
                    return (d[1]);
                });
            }
            else {
                cells.html(function(d) {
                    return (d[1]);
                });
            }
        });

        if (include_buttons){
            // add empty header columns and buttons
            buttons.forEach( button => {
                table_head.append('td').text('');
                rows.append('td')
                    // .append('a')
                    // .attr("href", function(d){return button.url + d[button.column]})
                    .append('button')
                    .attr('class','btn btn-secondary')
                    .attr('data-bs-toggle', 'modal')
                    .attr('data-bs-target', '#tableButtonModal')
                    .attr('data-bs-dismiss', 'modal')
                    .text(button.name)
                    .on('click', d => tableModalHTML(button.url, d[button.column], button.message, button.options))
                    
            })
        }

    });
}

function refreshPage() {
    setTimeout(function(){window.parent.location = window.parent.location.href;}, 10);
}

// This function supplies the appropriate information to the modal
function tableModalHTML(url, id, message, options=None){
    
    if (options == 'dropdown'){

        d3.select("#order-status-form-id").attr('action', url + id)    
    }
    else {
        d3.select("#button-link").attr('href', url + id)    
        d3.select("#button-message").text(message)
    }
    //     d3.select("#button-message").text(message)
    //     d3.select("#button-link").attr('href', url + id)
    // }
    // else if (options == "drop-down"){
    //     d3.select("#button-message").text(message)
    //     d3.select("#button-link").attr('href', url + id + "/" +)
    // }
    // else {
    //     d3.select("#button-message").text(message)
    //     d3.select("#button-link").attr('href', url + id)
    // }
}

let table_id = '#request-table';
let data_url = "/api/table/requests/active";
createTable(data_url, table_id)

let hyperlinks = [
    {'column_name':'Request ID',
     'column_url': '/api/request/details/'},
    //  {'column_name':'Room Code',
    //   'column_url': '/api/room/details/'}
];
let buttons = [
    {'name': 'Report Lost',
     'url': '/api/key/lost/',
     'column': 'Request ID',
     'message':"Please Confirm the key is lost."
    },
    {'name': 'Return',
     'url': '/api/key/return/',
     'column': 'Request ID',
     'message':"Please confirm that you are returning the key."
    }
];
data_url = "/api/table/requests/inactive";
table_id = '#keys-table';
createTable(data_url, table_id, buttons, hyperlinks, nullmessage="Records indicate no outstanding keys.")


data_url = 'api/table/rooms/';
table_id = '#room-table';
createTable(data_url, table_id)

data_url = '/api/table/users/';
table_id = '#user-table';
createTable(data_url, table_id)

data_url = '/api/table/matrix/';
table_id = '#access-matrix';
createTable(data_url, table_id)

data_url = '/api/table/approver';
table_id = '#approver-table';
createTable(data_url, table_id)

data_url = '/api/table/zones';
table_id = '#zones-table';
createTable(data_url, table_id)

data_url = '/api/table/users/group';
table_id = '#user-group-table';
createTable(data_url, table_id)


data_url = '/api/table/buildings/group';
table_id = '#building-access';
createTable(data_url, table_id)

data_url = '/api/table/inventory'
table_id = '#key-inventory'
createTable(data_url, table_id)

// for tables, a custom modal could be made to meet the needs by adding a key called 'modal'
buttons = [
    {'name': 'Update Status',
     'url': '/api/orders/status/',
     'column': 'Request #',
     'options': 'dropdown',
     'message':"Please Confirm that you want to submit."
    }
];
data_url = '/api/table/orders'
table_id = '#orders'
createTable(data_url, table_id, buttons)

data_url = '/api/table/keyshop'
table_id = '#key-shop'
createTable(data_url, table_id)

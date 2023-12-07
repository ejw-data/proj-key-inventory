console.log("Orders script is running!")


function showForm(){
    let keyForm = d3.select("#key-request-form");
    keyForm.classed("d-none", !keyForm.classed("d-none"))

    if (addKeyButton.text() == 'Hide Key Form'){
        addKeyButton.text('Create Key Order Basket')
    } else {
        addKeyButton.text('Hide Key Form')
    }
}

let addKeyButton = d3.select('#add-key');
addKeyButton.on('click', i => showForm());

let submitKey = d3.select('#basket_submit')
submitKey.on('click', i => updateTable())

function updateTable() {
    setTimeout(function (){
        d3.text("/order-content").then(html => {
        let basketDiv = d3.select('#basket-section');
        console.log("updateTableRan", html)
        basketDiv.html(html);
        });
    }, 1000);
}

updateTable()

//     d3.select('#basket-table').select('tbody').append('tr').append('td').text("No entries yet.")

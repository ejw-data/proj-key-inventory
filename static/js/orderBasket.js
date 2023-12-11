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

let submitKey = d3.select('#add-key-submit')
submitKey.on('click', i => updateTable())
submitKey.on('click', i => addMsg())

function updateTable() {
    setTimeout(function (){
        d3.text("/order-content").then(html => {
            let basketDiv = d3.select('#basket-section');
            basketDiv.html(html);
        });
    }, 1000);
}

function addMsg(){
    setTimeout(function (){
        d3.text("/post/basket/add").then(html =>{
            let outcomeDiv = d3.select('#basket-section');
            outcomeDiv.html(html);
        });
    }, 1000);
}

updateTable()


// let submitOrder('click', i => )
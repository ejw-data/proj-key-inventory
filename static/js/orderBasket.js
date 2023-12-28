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

// change button after submit
function changeButton(){
    // hide/reveal submit button
    let basketSubmitButton = d3.select("#order-submit");
    basketSubmitButton.classed("d-none", !basketSubmitButton.classed("d-none"))
    // hide/reveal clear button
    let basketClearButton = d3.select("#order-clear");
    basketClearButton.classed("d-none", !basketClearButton.classed("d-none"))
    // hide/reveal close button
    let basketCloseButton = d3.select("#order-close");
    basketCloseButton.classed("d-none", !basketCloseButton.classed("d-none"))
}

// update order table
function updateTable() {
    setTimeout(function (){
        console.log('Table Update Running')
        d3.text("/order-content").then(html => {
            let basketDiv = d3.select('#basket-section');
            basketDiv.html(html);
        });
    }, 1000);
}

// add message below order table
function addMsg(){
    setTimeout(function (){
        d3.text("/post/basket/msg").then(html =>{
            let outcomeDiv = d3.select('#msg-section');
            outcomeDiv.html(html);
        });
    }, 1000);
}

function clearTable(){
    d3.text('/post/basket/clear').then(html => {
        let basketDiv = d3.select('#basket-section');
        basketDiv.html(html);
    })
}

// event runs when Request Key button is clicked
// popup occurs through data actions
let addKeyButton = d3.select('#add-key');
addKeyButton.on('click', i => {
    showForm();
});

// event runs when form is submitted  
// form data sent to route which adds data to session variable
// add-key-submit only adds keys to local browser session variables
let submitKey = d3.select('#add-key-submit')
submitKey.on('click', i => {
    updateTable();
    activateSubmit();
})

// event runs when basket is submitted
let submitBasket = d3.select('#order-submit')
submitBasket.on('click', i => {
    addMsg();
    changeButton();
    updateTable();
})

// event runs when basket clear button is clicked
let clearBasket = d3.select('#order-clear')
clearBasket.on('click', i => {
    clearTable();
    activateSubmit();
})

// event runs when bottom of form modal close button is pressed
let basketCloseButton = d3.select("#order-close");
basketCloseButton.on('click', i => {
    clearTable();
    changeButton();
    addMsg();
    showForm();
    location.reload(true);
});


function activateSubmit(){
     setTimeout(function (){
        console.log('on-change')
        let dataRow = d3.select('#key-table');
        let submitBasket = d3.select('#order-submit')
        if (dataRow.classed('empty')){
            submitBasket.classed("disabled", true)
        }
        else {
            submitBasket.classed("disabled", false)}
    }, 2000)
}

updateTable();
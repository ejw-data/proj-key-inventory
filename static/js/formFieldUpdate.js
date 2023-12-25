d3.select('#wing').attr("disabled", "true");
d3.select('#floor').attr("disabled", "true");
d3.select('#room').attr("disabled", "true");
// d3.select('#approver_id').attr("disabled", "true");


// function updateDropDown(building_id, trigger_id, restricted_id, data_category){
//     let input_field = d3.select(trigger_id)
//     input_field.on('change', (i) => {
    
//     let building_number = d3.select(building_id).node().value;
//     console.log(building_number)

//     // capture building number from dropdown
//     url = `/api/building/info/${building_number}`

//     d3.json(url).then(data => {

//         console.log(data)
//          // in the future the data will be from an api that receives building_number as an input
//         // building_record = data.filter(i => i.building == building_number);

//         // select the floor form selector and its options and remove
//         //  replaces '#room_type > option' - below is more readable
//         let blocked_field = d3.select(restricted_id);// enable dropdown
//         blocked_field.attr('disabled', null);
//         blocked_field.selectAll('option').remove();

//         blocked_field.append('option')
//             .text('Make Selection')
//             .property('value', 0)
//         // adds options from data

//         blocked_field.data(data[data_category])
//             .append('option')
//             .text(d =>  d)
//             .property('value', d => d );

//         })
//     })
// };


// updateDropDown('#building_number','#building_number', '#wing', 'wings')



















// used in admin.html in the Room Add form
let building_field = d3.select('#building_number')
building_field.on('change', (i) => {


    // capture building number from dropdown
    building_number = building_field.node().value;
    url = `/api/building/info/${building_number}`

    d3.json(url).then(data => {

        console.log(data)
         // in the future the data will be from an api that receives building_number as an input
        // building_record = data.filter(i => i.building == building_number);

        // select the floor form selector and its options and remove
        //  replaces '#room_type > option' - below is more readable
        let wing_field = d3.select('#wing');// enable dropdown
        wing_field.attr('disabled', null);
        wing_field.selectAll('option').remove();

        wing_field.append('option')
            .text('Select Wing')
            .property('value', 0);
        // adds options from data
        option_wing = wing_field.selectAll('option')
            .exit()
            .data(data['wings'])
            .enter()
            .append('option');
        
        option_wing.text(d =>  d)
            .property('value', d => d );

        wing_field.on('change', (i) => {
            let wing_value = d3.select('#wing').node().value;
            let floor_field = d3.select('#floor');// enable dropdown
            floor_field.attr('disabled', null);
            floor_field.selectAll('option').remove();

            floor_field.append('option')
                .text('Select Floor')
                .property('value', 0);
            // adds options from data
            let option_floor = floor_field.selectAll('option')
                .exit()
                .data(data['wing'][wing_value]['floors'])
                .enter()
                .append('option');

            option_floor.text(d =>  d)
                .property('value', d => d );

            floor_field.on('change', (i) => {
                let room_field = d3.select('#room');// enable dropdown
                let wing_value = d3.select('#wing').node().value;
                let floor_value = d3.select('#floor').node().value;
                room_field.attr('disabled', null);
                room_field.selectAll('option').remove();

                room_field.append('option')
                    .text('Select Room')
                    .property('value', 0);
                // adds options from data
                let option_room = room_field.selectAll('option')
                    .exit()
                    .data(data['wing'][wing_value]['floor'][floor_value])
                    .enter()
                    .append('option')

                option_room.text(d =>  d)
                    .property('value', d => d );


            })

        })
        

    })
});
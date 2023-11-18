
building_field = d3.select('#room_building_number')
building_field.on('change', (i) => {


    data = [
        {'building': 24, 
        'wings':[1],
        'wing': {1:{'floor': {
                                    1:[1],
                                    2:[1,2]
                                },
                    'floors':[1,2]
                    },

            }
        },
        {'building': 44,
        'wings':[1,2],
        'wing': { 1:{'floor': {
                                    1: [1,2,3],
                                },
                     'floors':[1]
                        },
                  2:{'floor': {
                                    1: [1,2]
                                },
                     'floors':[1]
                        }

                }
        }
                    
    ];
    

    // capture building number from dropdown
    building_number = building_field.node().value;

    // in the future the data will be from an api that receives building_number as an input
    building_record = data.filter(i => i.building == building_number);

    // select the floor form selector and its options and remove
    //  replaces '#room_type > option' - below is more readable
    floor_field = d3.select('#room_type');
    floor_field.selectAll('option').remove();

    // adds options from data
    floor_field.selectAll('option')
        .data(building_record[0]['wings'])
        .enter()
        .append('option')
        .text(d =>  d);

    // disable dropdown
    floor_field.attr("disabled", "true");
});
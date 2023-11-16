
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
                    
    ]
        
    console.log(data)

    console.log(building_field.node().value)

    //  replaces '#room_type > option' - below is more readable
    floor_field = d3.select('#room_type')
    floor_inputs = floor_field.selectAll('option')
    floor_inputs.remove()

    floor_field.selectAll('option')
        .data(data[1]['wings'])
        .enter()
        .append('option')
        .text(d =>  d)
    
});
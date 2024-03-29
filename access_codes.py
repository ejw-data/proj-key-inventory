from query import get_access_code
import numpy as np


def asc_length(e):
    return len(e["value"])


def reduce_results(matrix: list, requested: list) -> list:
    """
    removes items from list that has more entries than requested entries
    and removes items from list that don't include requested entries
    """

    # remove entries that have too many options
    filter1 = filter(lambda x: len(x["value"]) <= len(requested), matrix)

    def remove_extra_options(list_item, required: list) -> bool:
        """
        checks list item for entries not in the required list
        """
        # print("inputcheck", type(list_item), list_item, required)
        if isinstance(list_item, str):
            val = True if list_item in required else False
            print("topIF", val)
        else:
            val = all([True if n in required else False for n in list_item])
            # print("Bottom Else", val, [True if n in required else False for n in list_item])
        return val

    # remove entries that include unnecessary entries
    filter2 = filter(lambda x: remove_extra_options(x["value"], requested), filter1)
    result = list(filter2)

    # convert filter object into list
    # result = list(filter2)
    print("results", result)
    return result


# fake get_access_code
# def get_access_code(lookup):
#     room_access_codes = [
#         {"id": 1, "value": ("r1",), "count": 1},
#         {"id": 2, "value": ("r2",), "count": 1},
#         {"id": 3, "value": ("r3",), "count": 1},
#         {"id": 4, "value": ("r4",), "count": 1},
#         {"id": 5, "value": ("r5",), "count": 1},
#         {"id": 6, "value": ("r6",), "count": 1},
#         {"id": 7, "value": ("r1", "r2"), "count": 2},
#         {"id": 8, "value": ("r3", "r5"), "count": 2},
#         {"id": 9, "value": ("r3", "r4", "r5"), "count": 3},
#         {"id": 10, "value": ("r1", "r2", "r3"), "count": 3},
#         {"id": 11, "value": ("r5", "r6"), "count": 2},
#         {"id": 12, "value": ("r1", "r2", "r3", "r5", "r6"), "count": 5},
#         {"id": 13, "value": ("r1", "r2", "r3", "r5", "r6", "r7"), "count": 6},
#     ]

#     result = [i["id"] for i in room_access_codes if i["value"] == tuple(lookup)]

#     if len(result) == 0:
#         result = 0
#     else:
#         result = result[0]

#     return result


# Assume the list above of options is already filtered by building and by list containing any options in lst
# next filter out lists that are larger than the lst list
# next filter any lists that have any elements not contained in lst


# maybe add message to dictionary
def flatten_list(data):
    flat_list = []
    if data is None:
        pass
    else:
        for tuple_or_number in data:
            if isinstance(tuple_or_number, tuple):
                for item in tuple_or_number:
                    flat_list.append(item)
            else:
                flat_list.append(tuple_or_number)
    return flat_list


def flatten_dict(data):
    flat_list = set()
    if data is None:
        pass
    else:
        for obj in data:
            for i in obj["value"]:
                flat_list.add(i)
    return list(flat_list)


def find_codes(requested_rooms, room_access_codes):
    best_fit = tuple()
    stored_codes = tuple()
    missing_room_removed_at_start = []
    loop_limit = 5
    # missing_codes = requested_rooms  # probably not needeed
    no_break = True
    # outer_for_break = False
    while (loop_limit > 0) and no_break:
        # allow outer for loop break to execute
        outer_for_break = False
        # print("\n", "Loop number: ", loop_limit, "\n")

        # need to fix so if filtered_codes is only one record; j loop does not run

        # process to follow if there is only one room being requested
        # this could be the final code being searched or an initial search
        # with only one key

        print("section a, check if one code exists", requested_rooms)

        resultant_codes = get_access_code(requested_rooms)

        print(
            "Zero indicates multiple codes needed and/or code needs created: ",
            resultant_codes,
        )

        # single access code found for all requested rooms
        if resultant_codes != 0:
            stored_codes = stored_codes + tuple([resultant_codes])
            # best fit:  codes found, rooms not found, number of rooms not found, dict of code/rooms found
            best_fit = (stored_codes, (), 0, [{stored_codes[0]: list(requested_rooms)}])
            no_break = False
            break
        # single room requested and no codes found
        # request for key code to be created
        elif (len(requested_rooms) == 1) and (resultant_codes == 0):
            # no exact matches found
            print("Code not found - ")
            # request key and notify person
            stored_codes = stored_codes + tuple([resultant_codes])

            if best_fit:
                current_status = best_fit[3] + [
                    {"Request in Progress": requested_rooms[0]}
                ]
            else:
                current_status = [{"Request in Progress": requested_rooms[0]}]

            # best fit:  codes found, rooms not found, number of rooms not found, dict of code/rooms found
            best_fit = (stored_codes, requested_rooms, 1, current_status)
            no_break = False
            break

        print(
            "Multiple rooms requested and no single match - need to check code combinations for matches."
        )
        # code may be a combination of codes, go to section b
        # process to follow if there is multiple access codes available
        print("section b, check if multiple access codes available")
        # print(room_access_codes)
        filtered_codes = reduce_results(room_access_codes, requested_rooms)

        # ####################################################################################################
        # if any of the rooms do not exist in filtered codes then remove them from the search
        # so it wont cause problems and add them to the missing rooms.
        # then seach for room combinations

        missing_room_removed_at_start = []
        temp = []
        flattened_filtered_codes = flatten_dict(filtered_codes)
        for i, room in enumerate(requested_rooms):
            if room not in flattened_filtered_codes:
                missing_room_removed_at_start.append(room)
                print("issue: ", i, room)
            else:
                temp.append(room)
        requested_rooms = tuple(temp)
        # make sure missing_rooms does not needed added back later to record their status
        print("missing_room_removed: ", missing_room_removed_at_start)
        print("modified requested_rooms: ", requested_rooms)
        # for loop code combos
        filtered_codes.sort(reverse=True, key=asc_length)
        print("special sorting test: ", filtered_codes)
        # print("filtered codes: ", np.ravel([i["value"] for i in filtered_codes]))

        ######################################################################################################
        # after rooms removed, do a single room check..
        if len(requested_rooms) != 0:
            resultant_codes = get_access_code(requested_rooms)
        else:
            resultant_codes = 0

        print(
            "Zero indicates multiple codes needed and/or code needs created: ",
            resultant_codes,
        )

        # single access code found for all requested rooms
        if resultant_codes != 0:
            stored_codes = stored_codes + tuple([resultant_codes])
            # best fit:  codes found, rooms not found, number of rooms not found, dict of code/rooms found
            best_fit = (stored_codes, (), 0, [{stored_codes[0]: list(requested_rooms)}])
            no_break = False
            break
        # single room requested and no codes found
        # request for key code to be created
        elif (len(requested_rooms) == 1) and (resultant_codes == 0):
            # no exact matches found
            print("Code not found - ")
            # request key and notify person
            stored_codes = stored_codes + tuple([resultant_codes])

            if best_fit:
                current_status = best_fit[3] + [
                    {"Request in Progress": requested_rooms[0]}
                ]
            else:
                current_status = [{"Request in Progress": requested_rooms[0]}]

            # best fit:  codes found, rooms not found, number of rooms not found, dict of code/rooms found
            best_fit = (stored_codes, requested_rooms, 1, current_status)
            no_break = False
            break

        # might not be needed if I fix rejected request unit test
        elif (len(requested_rooms) == 0) and (resultant_codes == 0):
            best_fit = (
                stored_codes,
                missing_room_removed_at_start,
                len(missing_room_removed_at_start),
                (),
            )
            no_break = False
            break

        # best fit:  codes found, rooms not found, number of rooms not found, dict of code/rooms found
        # best fit needs dictionary of rooms per access code
        # Change:  first element was None instead of filtered_codes
        # best_fit is just used to initialize - the values from this section are typically overwritten
        missing_codes = missing_room_removed_at_start
        difference = len(missing_room_removed_at_start)

        if len(requested_rooms) > 0:
            request_status = requested_rooms[0]
        else:
            request_status = 0

        best_fit = (
            (0,),
            tuple(missing_codes),
            difference,
            [{"Request in Progress": request_status}],
        )
        print("test222 ", best_fit)

        # if filtered_codes length is 1 then assign as key and request access code for other rooms
        if len(filtered_codes) == 1:
            missing_rooms = list(requested_rooms).copy()
            # print("missing rooms", missing_rooms)
            # print(filtered_codes[0]["value"][0])
            for only_found_rooms in filtered_codes[0]["value"]:
                missing_rooms.remove(only_found_rooms)
            difference = len(missing_rooms)
            resultant_codes = filtered_codes[0]["id"]
            # best fit:  codes found, rooms not found, number of rooms not found, dict of code/rooms found

            best_fit = (
                tuple([filtered_codes[0]["id"]]),
                tuple(missing_rooms),
                difference,
                [{resultant_codes: list(filtered_codes[0]["value"])}],
            )
            print("only one code: ", best_fit)
            # request access code to be created

            no_break = False
            break

        # otherwise search through list
        for i, filtered_code in enumerate(filtered_codes):
            if outer_for_break:
                break
            for j in range(i):
                # print(
                #     "for loop check: ", filtered_codes[i]["id"], filtered_codes[j]["id"]
                # )
                room_combination = (
                    filtered_codes[i]["value"] + filtered_codes[j]["value"]
                )

                print(
                    "section b, multiple access codes, combination",
                    room_combination,
                )
                # check if pair is matched
                if sorted(room_combination) == sorted(requested_rooms):
                    print("section b, multiple access codes, exact match found")
                    # print(
                    #     "lists match",
                    #     filtered_codes[i]["id"],
                    #     filtered_codes[j]["id"],
                    # )
                    resultant_codes = (
                        filtered_codes[i]["id"],
                        filtered_codes[j]["id"],
                    )
                    new_dict = []
                    for code in resultant_codes:
                        code_dict = list(
                            filter(lambda x: x["id"] == code, room_access_codes)
                        )
                        new_dict.append({code: code_dict[0]["value"]})
                    missing_rooms = tuple()
                    difference = 0
                    # best fit:  codes found, rooms not found, number of rooms not found, dict of code/rooms found
                    best_fit = (
                        resultant_codes,
                        missing_rooms,
                        difference,
                        new_dict,
                    )
                    stored_codes = stored_codes + resultant_codes
                    no_break = False
                    outer_for_break = True
                    break
                # check that there are no duplicates in the combined access codes
                elif len(set(room_combination)) != len(room_combination):
                    print(
                        "section b, multiple access code, duplicates in access code combo: ",
                        room_combination,
                    )
                    difference = len(requested_rooms)
                    # go to next loop
                    continue
                # check to see if some rooms are not found in the search
                # calculate the number of missing codes
                elif len(room_combination) < len(requested_rooms):
                    requested_rooms_lst = list(requested_rooms)
                    print(
                        "section b, multiple access code, incomplete match",
                        room_combination,
                    )

                    # identify missing codes
                    for access_code in room_combination:
                        requested_rooms_lst.remove(access_code)

                    missing_codes = tuple(requested_rooms_lst)
                    print("Missing codes: ", missing_codes)

                    difference = len(missing_codes)

                    if difference <= best_fit[2]:
                        # print("Updated room requests: ", requested_rooms_lst)
                        # print("Updated missing codes: ", missing_codes)
                        # print(
                        #     "Updated id combo",
                        #     filtered_codes[i]["id"],
                        #     filtered_codes[j]["id"],
                        #     difference,
                        # )
                        resultant_codes = (
                            filtered_codes[i]["id"],
                            filtered_codes[j]["id"],
                        )
                        new_dict = []
                        for code in resultant_codes:
                            code_dict = list(
                                filter(lambda x: x["id"] == code, room_access_codes)
                            )
                            new_dict.append({code: code_dict[0]["value"]})
                        # best fit:  codes found, rooms not found, number of rooms not found, dict of code/rooms found
                        best_fit = (
                            resultant_codes,
                            missing_rooms,
                            difference,
                            new_dict,
                        )
                        # stored_codes = stored_codes + resultant_codes
                        print("Best fit for partial: ", best_fit)

                    # need to go to top of forloop to complete loop for exact matches
                    # on subsequent loops, it needs to replace the value if difference is smaller

        if difference == 0:
            # miscellaneous test - show what code goes with which room

            print("Needed Keys Calculated")
            print(f"The access codes need are: {stored_codes}")
            print(f"The missing codes are:  {missing_codes}")
            print("Best Fit: ", best_fit)

            no_break = False

            # request access code creation for missing codes

        else:
            # need to go to top of script outside for loop
            requested_rooms = list(best_fit[1])
            print(
                "section c, start next while loop with requested rooms",
                requested_rooms,
            )
            # print("Stored codes: ", stored_codes)
            # print("Resultant codes: ", resultant_codes)

            stored_codes = stored_codes + tuple([resultant_codes])
            outer_for_break = True
        loop_limit -= 1

    print("Out of while loop")

    if best_fit[2] == 0:
        requested_spaces = list(best_fit[3])
        access_codes = list(best_fit[0])
        # add message

    elif best_fit[0] is None:
        print("No codes found")
        pass
    else:
        print("last check: ", best_fit)
        requested_spaces = list(best_fit[3])
        access_codes = list(best_fit[0])
        # query each code in the list to get the building number, space_owner, space_id, and access_code -
        # change it so the access_code_id is listed and and space_number_id becomes
        # part of a space_numbe_id list.
        # instead of query, extract first couple letters from room-request

    results = {
        "requested_spaces": list(best_fit[3]),
        "access_codes": flatten_list(best_fit[0]),
        "missing": list(best_fit[1]) + missing_room_removed_at_start,
    }
    return results


# new_matrix = reduce_results(room_access_codes, tuple(["r1"]))
# len(new_matrix)
# print("Last best fit: ", best_fit)
# print("Final results: ", stored_codes)

# requested_rooms = ("r1", "r3", "r4")
# requested_rooms = ("r5", "r3", "r6", "r2")
# requested_rooms = ("r1", "r2", "r3", "r5", "r6")
# requested_rooms = ("r1", "r2", "r3", "r5", "r4")
# requested_rooms = ("r1",)
# requested_rooms = ("r1", "r2")
# requested_rooms = ("r1", "r4")
# requested_rooms = ("r1", "r4", "r7")
# requested_rooms = ("r1", "r4", "r3", "r5", "r6")
# requested_rooms = ("r1", "r2", "r3", "r4", "r5", "r6")
# requested_rooms = ("r22",)


# room_access_codes = [
#     {"id": 1, "value": ("r1",), "count": 1},
#     {"id": 2, "value": ("r2",), "count": 1},
#     {"id": 3, "value": ("r3",), "count": 1},
#     {"id": 4, "value": ("r4",), "count": 1},
#     {"id": 5, "value": ("r5",), "count": 1},
#     {"id": 6, "value": ("r6",), "count": 1},
#     {"id": 7, "value": ("r1", "r2"), "count": 2},
#     {"id": 8, "value": ("r3", "r5"), "count": 2},
#     {"id": 9, "value": ("r3", "r4", "r5"), "count": 3},
#     {"id": 10, "value": ("r1", "r2", "r3"), "count": 3},
#     {"id": 11, "value": ("r5", "r6"), "count": 2},
#     {"id": 12, "value": ("r1", "r2", "r3", "r5", "r6"), "count": 5},
#     {"id": 13, "value": ("r1", "r2", "r3", "r5", "r6", "r7"), "count": 6},
# ]

# find_codes(requested_rooms, room_access_codes)


# string_item = 'R10200122'
# string_item[0:3]

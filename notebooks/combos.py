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
    # print('results', result)
    return result


requested_rooms = ("r1", "r3", "r4")
requested_rooms = ("r1", "r2")

room_access_codes = [
    {"id": 1, "value": ("r1",), "count": 1},
    {"id": 2, "value": ("r2",), "count": 1},
    {"id": 3, "value": ("r3",), "count": 1},
    {"id": 4, "value": ("r4",), "count": 1},
    {"id": 5, "value": ("r5",), "count": 1},
    {"id": 6, "value": ("r6",), "count": 1},
    {"id": 7, "value": ("r1", "r2"), "count": 2},
    {"id": 8, "value": ("r3", "r5"), "count": 2},
    {"id": 9, "value": ("r3", "r4", "r5"), "count": 3},
    {"id": 10, "value": ("r1", "r2", "r3"), "count": 3},
    {"id": 11, "value": ("r5", "r6"), "count": 2},
    {"id": 12, "value": ("r1", "r2", "r3", "r5", "r6"), "count": 5},
    {"id": 13, "value": ("r1", "r2", "r3", "r5", "r6", "r7"), "count": 6},
]


# fake get_access_code
def get_access_code(lookup):
    room_access_codes = [
        {"id": 1, "value": ("r1",), "count": 1},
        {"id": 2, "value": ("r2",), "count": 1},
        {"id": 3, "value": ("r3",), "count": 1},
        {"id": 4, "value": ("r4",), "count": 1},
        {"id": 5, "value": ("r5",), "count": 1},
        {"id": 6, "value": ("r6",), "count": 1},
        {"id": 7, "value": ("r1", "r2"), "count": 2},
        {"id": 8, "value": ("r3", "r5"), "count": 2},
        {"id": 9, "value": ("r3", "r4", "r5"), "count": 3},
        {"id": 10, "value": ("r1", "r2", "r3"), "count": 3},
        {"id": 11, "value": ("r5", "r6"), "count": 2},
        {"id": 12, "value": ("r1", "r2", "r3", "r5", "r6"), "count": 5},
        {"id": 13, "value": ("r1", "r2", "r3", "r5", "r6", "r7"), "count": 6},
    ]

    result = [i["id"] for i in room_access_codes if i["value"] == tuple(lookup)]

    if result[0] == "":
        result = ["empty"]
    return result[0]


# Assume the list above of options is already filtered by building and by list containing any options in lst
# next filter out lists that are larger than the lst list
# next filter any lists that have any elements not contained in lst


# pylint: disable=no-member
best_fit = tuple()
stored_codes = tuple()
loop_limit = 5
missing_codes = requested_rooms  # probably not needeed
no_break = True
outer_for_break = False
while (loop_limit > 0) and (no_break == True):
    print(loop_limit)
    # need to fix so if filtered_codes is only one record; j loop does not run

    # process to follow if there is only one room being requested
    # this could be the final code being searched or an initial search
    # with only one key
    if len(requested_rooms) == 1:
        print("section a, one room requested", requested_rooms)
        resultant_codes = get_access_code(requested_rooms)
        # code not found
        print(resultant_codes)
        if resultant_codes == 0:
            print("Code not found - ")
            # request key and notify person
            # or maybe have
            stored_codes = stored_codes + tuple([resultant_codes])
            best_fit = (stored_codes, requested_rooms, 1)
        # code found
        else:
            stored_codes = stored_codes + tuple([resultant_codes])
            # best fit has tuple of codes, missing codes, and total missing codes
            best_fit = (stored_codes, (), 0)
        no_break = False
        break
        # if the stored searches has a zero then a key creation request is needed
    else:
        print("section b")
        # check for exact match given multiple entries

        #
        filtered_codes = reduce_results(room_access_codes, requested_rooms)
        # process to follow if there is only one access code available
        if len(filtered_codes) == 1:
            print("section b, only one access code found")
            default_needed_code = filtered_codes[0]["value"]
            stored_codes = stored_codes + default_needed_code
            remaining_codes_not_found = set(requested_rooms).difference(stored_codes)
            best_fit = (
                stored_codes,
                remaining_codes_not_found,
                len(remaining_codes_not_found),
            )

            # probably need to request a new key if number remaining codes is gr than 1

            # end loop
            no_break = False
            break

        # proess to follow if there is multiple access codes available
        else:
            print("section b, multiple access codes available")
            # for loop code combos
            filtered_codes.sort(reverse=True, key=asc_length)
            for i, filtered_code in enumerate(filtered_codes):
                if outer_for_break:
                    break
                for j in range(i):
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
                        print(
                            "lists match",
                            filtered_codes[i]["id"],
                            filtered_codes[j]["id"],
                        )
                        resultant_codes = (
                            filtered_codes[i]["id"],
                            filtered_codes[j]["id"],
                        )
                        missing_codes = tuple()
                        difference = 0
                        best_fit = (resultant_codes, missing_codes, difference)
                        stored_codes = stored_codes + resultant_codes
                        no_break = False
                        outer_for_break = True
                        break
                    # check that there are no duplicates in the combined access codes
                    elif len(set(room_combination)) != len(room_combination):
                        print(
                            "section b, multiple access code, duplicates in access code combo"
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
                            print("access code", access_code)
                            requested_rooms_lst.remove(access_code)
                        print("tuple_lst", requested_rooms_lst)
                        missing_codes = tuple(requested_rooms_lst)
                        print("missing_codes", missing_codes)
                        difference = len(missing_codes)
                        print(
                            "final elif",
                            filtered_codes[i]["id"],
                            filtered_codes[j]["id"],
                            difference,
                        )
                        resultant_codes = (
                            filtered_codes[i]["id"],
                            filtered_codes[j]["id"],
                        )
                        best_fit = (resultant_codes, missing_codes, difference)
                        stored_codes = stored_codes + resultant_codes
                        print(best_fit)

                    if difference == 0:
                        print("Needed Keys Calculated")
                        print(f"The access codes need are: {stored_codes}")
                        print(f"The missing codes are:  {missing_codes}")
                        no_break = False

                        # request access code creation for missing codes

                    else:
                        # need to go to top of script outside for loop
                        requested_rooms = list(missing_codes)
                        print(
                            "section c, start next while loop with requested rooms",
                            requested_rooms,
                        )
                        outer_for_break = True
            loop_limit -= 1


# pylint: enable=no-member
# new_matrix = reduce_results(room_access_codes, tuple(["r1"]))
# len(new_matrix)
print("Last best fit: ", best_fit)
print("Final results: ", stored_codes)


lst = ("r1", "r2", "r3", "r5", "r6")

lst = ("r1", "r3", "r4")

options = [
    ("r1",),
    ("r2",),
    ("r3",),
    ("r4",),
    ("r5",),
    ("r6",),
    ("r1", "r2"),
    ("r3", "r5"),
    ("r3", "r4", "r5"),
    ("r1", "r2", "r3"),
    ("r5", "r6"),
    ("r1", "r2", "r3", "r5", "r6"),
    ("r1", "r2", "r3", "r5", "r6", "r7"),
]

option2 = [
    {"id": 1, "value": ("r1",), "count": 1},
    {"id": 2, "value": ("r2",), "count": 1},
    {"id": 3, "value": ("r3",), "count": 1},
    {"id": 4, "value": ("r4",), "count": 1},
    {"id": 5, "value": ("r5",), "count": 1},
    {"id": 6, "value": ("r6",), "count": 1},
    {"id": 7, "value": ("r1", "r2"), "count": 2},
    {"id": 8, "value": ("r3", "r5"), "count": 2},
    {"id": 9, "value": ("r3", "r4", "r5"), "count": 3},
    {"id": 10, "value": ("r1", "r2", "r3"), "count": 3},
    {"id": 11, "value": ("r5", "r6"), "count": 2},
    {"id": 12, "value": ("r1", "r2", "r3", "r5", "r6"), "count": 5},
    {"id": 13, "value": ("r1", "r2", "r3", "r5", "r6", "r7"), "count": 6},
]
# Assume the list above of options is already filtered by building and by list containing any options in lst
# next filter out lists that are larger than the lst list
# next filter any lists that have any elements not contained in lst


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
    # print('results', result)
    return result


new_matrix = reduce_results(option2, lst)


def asc_length(e):
    return len(e["value"])


new_matrix.sort(reverse=True, key=asc_length)
print(new_matrix)

# pylint: disable=no-member
best_fit = tuple()
stored_searches = tuple()
loop_limit = 5
no_break = True
while (loop_limit > 0) and (no_break == True):
    for i in range(len(new_matrix)):
        for j in range(i):
            print("indexes", i, j)
            if no_break:
                if len(lst) == 1:
                    val = new_matrix[j]["value"]
                else:
                    val = new_matrix[i]["value"] + new_matrix[j]["value"]
                # check if pair is matched
                if sorted(val) == sorted(lst):
                    print("lists match", new_matrix[i]["id"], new_matrix[j]["id"])
                    resultant_codes = (new_matrix[i]["id"], new_matrix[j]["id"])
                    best_fit = (resultant_codes, (), 0)
                    no_break = False
                    break
                elif len(set(val)) != len(val):
                    print("lists have repeated values")
                    # go to next loop

                    continue
                elif len(val) < len(lst):
                    new_lst = list(lst)
                    for k in val:
                        new_lst.remove(k)
                    missing_codes = tuple(new_lst)
                    difference = len(missing_codes)
                    print(
                        "final elif",
                        new_matrix[i]["id"],
                        new_matrix[j]["id"],
                        difference,
                    )
                    resultant_codes = (new_matrix[i]["id"], new_matrix[j]["id"])
                    best_fit = (resultant_codes, missing_codes, difference)
                    print(best_fit)
        # set missing_codes to previous variable
        if difference == 0:
            no_break = False
        else:
            stored_searches = stored_searches + resultant_codes
            print("stored searches", stored_searches)
            lst = missing_codes
            new_matrix = reduce_results(option2, lst)
            if len(new_matrix) == 1:
                resultant_codes = get_access_code(new_matrix)
                if resultant_codes == 0:
                    print(f"Code not found for {lst}")
                    # request new code
                else:
                    stored_searches = stored_searches + resultant_codes
                    no_break = False

            loop_limit -= 1

# pylint: enable=no-member
new_matrix = reduce_results(option2, tuple(["r1"]))
len(new_matrix)
print(best_fit)
print(stored_searches)

for i in range(0):
    print(1)
# make it work for multiple entries or closest fit
lst = (1, 2, 3)
val = (1, 3)
new_lst = list(lst)
for i in val:
    new_lst.remove(i)
tuple(new_lst)

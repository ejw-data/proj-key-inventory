lst = ("r1", "r2", "r3", "r5", "r6")

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
    filter1 = filter(lambda x: len(x) <= len(requested), matrix)

    def remove_extra_options(list_item, required: list) -> bool:
        """
        checks list item for entries not in the required list
        """
        if isinstance(list_item, str):
            val = True if list_item in required else False
        else:
            # print("runs")
            val = all([True if n in required else False for n in list_item])
        # print(i, val, [True if n in lst else False for n in i])
        return val

    # remove entries that include unnecessary entries
    filter2 = filter(lambda x: remove_extra_options(x, requested), filter1)

    # convert filter object into list
    result = [i for i in filter2]

    return result


new_matrix = reduce_results(options, lst)


def asc_length(e):
    return len(e)


new_matrix.sort(reverse=True, key=asc_length)
print(new_matrix)

for i in range(len(new_matrix)):
    for j in range(i):
        if i != j:
            val = new_matrix[i] + new_matrix[j]
            if sorted(val) == sorted(lst):
                print(new_matrix[i], new_matrix[j])






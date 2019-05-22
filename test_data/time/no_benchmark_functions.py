N = 100000
seq_list = list(range(N))
seq_set = set(range(N))


def search_in_list(num_items=N):
    return num_items - 1 in seq_list


def search_in_set(num_items=N):
    return num_items - 1 in seq_set

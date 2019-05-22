from benchmarkit import benchmark


N = 1000000
seq_list = list(range(N))
seq_set = set(range(N))


@benchmark(num_iters=100, save_params=True)
def search_in_list(num_items=N):
    return num_items - 1 in seq_list


@benchmark(num_iters=100, save_params=True)
def search_in_set(num_items=N):
    return num_items - 1 in seq_set

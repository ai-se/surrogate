def generate_data(problem, number_of_points):
    dataset = []
    while len(dataset) < number_of_points:
        for run in range(number_of_points):
            dataset.append(problem.generateInput())

        import itertools
        dataset.sort()
        dataset = list(dataset for dataset,_ in itertools.groupby(dataset))

    from random import shuffle
    shuffle(dataset)
    return dataset[:number_of_points]


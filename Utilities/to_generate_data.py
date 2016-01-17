def generate_data(problem, number_of_points):
    dataset = []
    for run in range(number_of_points):
        dataset.append(problem.generateInput())
    return dataset


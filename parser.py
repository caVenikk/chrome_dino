def get_scores_from_file(filename):
    with open(filename, 'r') as file:
        d = [line.split() for line in file.readlines()]
        return sorted([{'name': r[0], 'score': int(r[1]), 'date': r[2], 'time': r[3]} for r in d], key=lambda item: item['score'], reverse=True)
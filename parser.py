import datetime


def save_score(name, gameState):
    now = datetime.datetime.now()
    f = open('score.txt', 'r')
    lines = f.readlines()
    lines.append(
        f'{name} {gameState.count} {"0" if len(str(now.day)) == 1 else ""}{now.day}.' +
        f'{"0" if len(str(now.month)) == 1 else ""}{now.month}.{now.year} ' +
        f'{"0" if len(str(now.hour)) == 1 else ""}{now.hour}:{"0" if len(str(now.minute)) == 1 else ""}{now.minute}\n')
    f.close()
    f = open('score.txt', 'w')
    f.writelines(lines)
    f.close()


def get_scores_from_file(filename):
    with open(filename, 'r') as file:
        d = [line.split() for line in file.readlines()]
        return sorted([{'name': r[0], 'score': int(r[1]), 'date': r[2], 'time': r[3]} for r in d],
                      key=lambda item: item['score'], reverse=True)

import csv

STATUSES_FILE = '/data/statuses.csv'
BOARDS_FILE = '/data/boards.csv'
CARDS_FILE = '/data/cards.csv'

_cache = {}  # We store cached data in this dict to avoid multiple file readings


def _read_csv(file_name):
    """
    Reads content of a .csv file
    :param file_name: relative path to data file
    :return: OrderedDict
    """
    with open(file_name) as boards:
        rows = csv.DictReader(boards, delimiter=',', quotechar='"')
        formatted_data = []
        for row in rows:
            formatted_data.append(dict(row))
        return formatted_data


def _get_data(data_type, file, force):
    """
    Reads defined type of data from file or cache
    :param data_type: key where the data is stored in cache
    :param file: relative path to data file
    :param force: if set to True, cache will be ignored
    :return: OrderedDict
    """
    if force or data_type not in _cache:
        _cache[data_type] = _read_csv(file)
    return _cache[data_type]


def clear_cache():
    for k in list(_cache.keys()):
        _cache.pop(k)


def get_statuses(force=False):
    return _get_data('statuses', STATUSES_FILE, force)


def get_boards(force=False):
    return _get_data('boards', BOARDS_FILE, force)


def get_board(board_id):
    boards = get_boards()
    print(boards)

    for board in boards:
        if board['id'] == str(board_id):
            this_board = board
            return this_board


def get_cards(force=False):
    return _get_data('cards', CARDS_FILE, force)


def save_board(board_name):
    boards = get_boards()
    id_board = len(boards) + 1
    board = [board_name, id_board]

    save_item(BOARDS_FILE, board)


def save_status(column_name):
    statuses = get_statuses()

    for status in statuses:
        if status['title'] == column_name:
            new_status_id = status['id']
        else:
            new_status_id = len(statuses) + 1

    new_status = [column_name, new_status_id]
    save_item(STATUSES_FILE, new_status)
    return new_status


def get_cards_with_numbers():
    cards = _read_csv(CARDS_FILE)
    return cards


def save_item(file, item):
    with open(file, 'a', newline='') as f:
        f.write(f'{item[1]}, {item[0]}')
        f.write('\n')


def save_data(list_items, mode, file):
    keys = list_items[0].keys()
    with open(file, mode, newline='') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(list_items)


def write_new_board_name(old_name, new_name):
    boards = get_boards()
    print(boards)
    for board in boards:
        if board['title'] == old_name:
            board['title'] = new_name

    save_data(boards, 'w', BOARDS_FILE)


def write_new_card_name(card_id, new_name):
    cards = _read_csv(CARDS_FILE)
    print(cards)
    for card in cards:
        if card['id'] == card_id:
            card['title'] = new_name

    save_data(cards, 'w', CARDS_FILE)


def write_new_card(board_id, card_name):
    clear_cache()
    cards = get_cards(False)
    new_order = [int(y['order']) for y in cards if int(y['board_id']) == int(board_id) and y['status_id'] == '0']
    new_id = [int(y['id']) for y in cards]
    new_card = {'id': max(new_id) + 1 if len(new_id) != 0 else 1, 'board_id': board_id, 'title': card_name,
                'status_id': 0,
                'order': max(new_order) + 1 if len(new_order) != 0 else 0}
    cards.append(new_card)
    save_data(cards, 'w', CARDS_FILE)


def save_new_order(cards_id):
    clear_cache()
    cards = get_cards(False)
    for key in cards_id:
        for i in range(0, len(cards_id[key])):
            for card in cards:
                if card['id'] == cards_id[key][i]:
                    card['order'] = str(i)
                    card['status_id'] = key
    cards = sorted(cards, key=lambda k: k['order'])
    save_data(cards, 'w', CARDS_FILE)


def delete_card_id(card_id):
    clear_cache()
    cards = get_cards(False)
    for i in range(len(cards)):
        if cards[i]['id'] == card_id:
            cards.pop(i)
            break
    save_data(cards, 'w', CARDS_FILE)


def save_new_cards_statuses(cards):
    save_data(cards, 'w', CARDS_FILE)

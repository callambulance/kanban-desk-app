from flask import Flask, render_template, url_for, request, session
from util import json_response
import re

import data_handler

app = Flask(__name__)
app.secret_key = "hello"

SESSION_USERNAME = 'username'
SESSION_ID = 'id'
registrationMode = "registration"
loginMode = "login"
privateType = "private"


@app.route("/")
def index():
    """
    This is a one-pager which shows all the boards and cards
    """
    if SESSION_USERNAME in session:
        session.pop(SESSION_USERNAME, None)
    if SESSION_ID in session:
        session.pop(SESSION_ID, None)
    return render_template('index.html')


@app.route("/get-boards")
@json_response
def get_boards():
    """
    All the boards
    """
    boards = data_handler.get_boards()
    if SESSION_USERNAME in session:
        private_boards = data_handler.get_private_boards(session[SESSION_ID])
        for board in private_boards:
            board['id'] = str(board['id']) + '-p'
        return boards, private_boards

    return boards


@app.route("/get-statuses/<board_id>")
@json_response
def get_statuses(board_id):
    if board_id.endswith('-p'):
        table = 'private_boards'
        board_id = int(board_id.split("-")[0])
        statuses = data_handler.get_statuses_by_board(board_id, True, table)
    else:
        table = 'boards'
        statuses = data_handler.get_statuses_by_board(board_id, False, table)

    return statuses


@app.route("/get-board/<board_id>")
@json_response
def get_board(board_id):
    if board_id.endswith('-p'):
        board_id = int(board_id.split("-")[0])
        print(board_id)
        board = data_handler.get_board_sql(board_id, "private_boards")
        board['id'] = str(board['id']) + '-p'
    else:
        board = data_handler.get_board_sql(board_id, "boards")

    return board


@app.route("/get-cards/<board_id>")
@json_response
def get_cards_for_board(board_id):
    """
    All cards that belongs to a board
    :param board_id: id of the parent board
    """
    if type(board_id) == str and board_id.endswith('-p'):
        table = 'private_boards'
        cards = 'private_cards'
        board_id = int(board_id.split("-")[0])
        cards = data_handler.get_cards_sql(board_id, cards, table)
    else:
        table = 'boards'
        cards = 'cards'
        cards = data_handler.get_cards_sql(board_id, cards, table)
    return cards


@app.route("/save-board/<board_name>/<board_type>")
@json_response
def save_new_board(board_name: str, board_type: str):
    print(board_type, board_name)
    if board_type == privateType:
        user_id = data_handler.get_user_id(session[SESSION_USERNAME])['id']
        board_id = data_handler.save_new_private_board(board_name, user_id)
        data_handler.create_default_statuses(board_id['id'], True)
        print("columns")

    else:
        board_id = data_handler.save_new_board_sql(board_name)
        data_handler.create_default_statuses(board_id['id'], False)
    """
    All cards that belongs to a board
    :param board_id: id of the parent board
    """

@app.route("/change-title/<board_id>/<new_name>")
@json_response
def save_new_board_name(board_id: int, new_name: str):
    data_handler.save_new_board_name_sql(board_id, new_name)


@app.route("/change-card-title/<card_id>/<new_name>")
@json_response
def save_new_card_name(card_id: int, new_name: str):

    data_handler.save_new_card_name_sql(card_id, new_name)


@app.route("/change-column-title/<column_name>/<column_id>/<board_id>/")
@json_response
def save_new_column_name(column_name: str, column_id: int, board_id):
    status_is_new = True
    private_board = False
    write_status_to_board = True
    cards = "cards"
    boards = "boards"
    statuses = data_handler.get_statuses_sql()

    # check if board is private
    if type(board_id) == str and board_id.endswith('-p'):
        board_id = int(board_id.split("-")[0])
        private_board = True
        cards = "private_cards"
        boards = "private_boards"

    #   check if this status is already exist in statuses table
    for s in statuses:
        if s['title'] == column_name:
            status_is_new = False
            # if yes, get it's id
            status_id = s['id']
            status = data_handler.get_status(status_id, boards, board_id)
            print(status)
            # check if this status is already exist on the same board
            if status is not None:
                write_status_to_board = False

    # delete status that is renamed
    data_handler.delete_status_from_board(board_id, column_id, private_board)
    print(f"{board_id}, {column_id}, {private_board} ....")

    # if status is brand new
    if status_is_new:
        # writing status to the status table
        new_status = data_handler.save_new_column_name_sql(column_name, column_id, board_id)
        status_id = new_status['id']

    # if status don't already exist on the same board, write it
    if write_status_to_board:
        data_handler.write_status_to_board(board_id, status_id, private_board)

    # changing cards statuses for the new
    data_handler.change_cards_statuses(status_id, column_id, board_id, cards)


@app.route("/save-card/<board_id>/<card_name>")
@json_response
def save_new_card(board_id, card_name: str):
    if type(board_id) == str and board_id.endswith('-p'):
        max_order = data_handler.get_max_order('private_cards', board_id.replace('-p', ''), 0)
        if len(max_order) == 0:
            max_order = 0
        else:
            max_order = max_order[0]['card_order'] + 1
        new_card_value = {'board_id': int(board_id.replace('-p', '')), 'card_title': card_name, 'status_id': 0,
                          'card_order': max_order, 'archived': 0}
        table_name = 'private_cards'
    else:
        max_order = data_handler.get_max_order('cards', board_id, 0)
        if len(max_order) == 0:
            max_order = 0
        else:
            max_order = max_order[0]['card_order'] + 1
        new_card_value = {'board_id': board_id, 'card_title': card_name, 'status_id': 0, 'card_order': max_order,
                          'archived': 0}
        table_name = 'cards'

    data_handler.save_new_card(table_name, new_card_value)


@app.route("/change-card-order/<board_id>/<cards_id>")
@json_response
def change_card_order(board_id, cards_id: list):
    new_cards_order = data_handler.change_card_order(cards_id)
    if type(board_id) == str and board_id.endswith('-p'):
        table_name = 'private_cards'
    else:
        table_name = 'cards'
    for keys in new_cards_order:
        for i in range(len(new_cards_order[keys])):
            data_handler.save_new_card_order_sql(table_name, new_cards_order[keys][i], keys, i)


@app.route("/delete-card/<board_id>/<card_id>")
@json_response
def delete_card(board_id, card_id: str):
    if type(board_id) == str and board_id.endswith('-p'):
        table_name = 'private_cards'
    else:
        table_name = 'cards'
    card_id = int(card_id.replace("delete-card", ""))

    data_handler.delete_card(table_name, card_id)


@app.route("/delete-board/<board_id>")
@json_response
def delete_board(board_id: str):
    board_id = board_id.replace("delete-board", "")
    if type(board_id) == str and board_id.endswith('-p'):
        board_id = int(board_id.split("-")[0])
        table_board_name = 'private_boards'
        table_cards_name = 'private_cards'
    else:
        board_id = int(board_id)
        table_board_name = 'boards'
        table_cards_name = 'cards'


    data_handler.delete_cards(table_cards_name, board_id)
    data_handler.delete_board(table_board_name, board_id)

@app.route("/delete-status/<board_id>/<status_id>")
@json_response
def delete_status(board_id, status_id):
    if type(board_id) == str and board_id.endswith('-p'):
        private_board = True
        board_id = int(board_id.split("-")[0])
    else:
        private_board = False

    print(board_id, status_id, private_board)
    data_handler.delete_status_from_board(board_id, status_id, private_board)


@app.route('/account', methods=['POST'])
@json_response
def check_user_data():
    data = request.get_json()
    user = data[0]
    current_mode = data[1]
    if current_mode == registrationMode:
        username_taken = data_handler.check_if_username_taken(user['username'])
        if username_taken:
            return False
        else:
            data_handler.register_new_user(user)
            return True
    elif current_mode == loginMode:
        if data_handler.validate_login_data(user):
            session[SESSION_USERNAME] = user['username']
            session[SESSION_ID] = data_handler.get_user_id(session[SESSION_USERNAME])['id']
            return True
        else:
            return False


@app.route('/logout')
@json_response
def logout():
    session.pop(SESSION_USERNAME, None)
    session.pop(SESSION_ID, None)


@app.route('/archive-card/<card_id>/<board_id>/<archive>')
@json_response
def archive_card(card_id, board_id, archive):
    card_id = card_id.replace('archive-card', '').replace('un', '')
    if type(board_id) == str and board_id.endswith('-p'):
        data_handler.archive_cards_sql(card_id, "private_cards", archive)
    else:
        data_handler.archive_cards_sql(card_id, "cards", archive)


def main():
    app.run(debug=True)

    # Serving the favicon
    with app.app_context():
        app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='favicon/favicon.ico'))


if __name__ == '__main__':
    main()




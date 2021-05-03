import persistence
import database_common
from psycopg2 import sql
from psycopg2.extras import RealDictCursor


@database_common.connection_handler
def get_boards_sql(cursor: RealDictCursor) -> list:
    query = f"""
        SELECT id, title
        FROM boards
        ORDER BY boards.id asc"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_cards_sql(cursor: RealDictCursor, board_id, table_name, boards) -> list:
    query = f"""
        SELECT {table_name}.id, board_id, card_title, card_order, archived, b.title, s.status_title, s.id as status_id
        FROM {table_name}
        JOIN {boards} b on b.id = {table_name}.board_id
        JOIN statuses s on s.id = {table_name}.status_id
        WHERE board_id = {board_id}
        ORDER BY card_order asc"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_board_sql(cursor: RealDictCursor, board_id, table) -> list:
    query = f"""
        SELECT id, title
        FROM {table}
        WHERE id = {board_id}"""
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def get_statuses_sql(cursor: RealDictCursor) -> list:
    query = f"""
        SELECT id, status_title as title
        FROM statuses"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_statuses_by_board(cursor: RealDictCursor, board_id, private_board, table) -> list:
    query = f"""
        SELECT board_number as board_id, private_board, status_number as id, s.status_title as title
        FROM status_boards
        INNER JOIN statuses s on status_boards.status_number = s.id
        INNER JOIN {table} b on status_boards.board_number = b.id
        WHERE board_number = {board_id} AND private_board = {private_board}
 """
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def write_status_to_board(cursor: RealDictCursor, board_id, status_id, private_board) -> list:
    query = f"""
            INSERT INTO status_boards(board_number, private_board, status_number)
            VALUES ({board_id}, {private_board}, {status_id})
            """
    cursor.execute(query)

@database_common.connection_handler
def delete_status_from_board(cursor: RealDictCursor, board_id, status_id, private_board) -> list:
    query = f"""
            DELETE FROM status_boards
            WHERE board_number = {board_id} AND private_board = {private_board} AND status_number = {status_id}
            """
    cursor.execute(query)

@database_common.connection_handler
def save_new_board_sql(cursor: RealDictCursor, board_name) -> list:
    query = f"""
        INSERT INTO boards(title)
        VALUES ('{board_name}')
        RETURNING id
        """
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def create_default_statuses(cursor: RealDictCursor, board_id, private_board) -> list:
    query = f"""
            INSERT INTO status_boards(board_number, status_number, private_board)
            VALUES ('{board_id}', 0, {private_board} ),
                   ('{board_id}', 1, {private_board} ),
                   ('{board_id}', 2, {private_board} ),
                   ('{board_id}', 3, {private_board} )
"""
    cursor.execute(query)


@database_common.connection_handler
def save_new_board_name_sql(cursor: RealDictCursor, board_id: int, board_name: str) -> list:
    query = f"""
        UPDATE boards
        SET title = '{board_name}'
        WHERE boards.id = '{board_id}'"""
    cursor.execute(query)


@database_common.connection_handler
def save_new_card_name_sql(cursor: RealDictCursor, card_id: int, new_name: str) -> list:
    query = f"""
        UPDATE cards
        SET card_title = '{new_name}'
        WHERE cards.id = '{card_id}'"""
    cursor.execute(query)


@database_common.connection_handler
def save_new_column_name_sql(cursor: RealDictCursor, column_name: str, column_id: int, board_id: int) -> list:
    query_1 = f"""
         INSERT INTO statuses(status_title)
         VALUES ('{column_name}')"""
    cursor.execute(query_1)

    query_2 = f"""
                SELECT id, status_title
                FROM statuses
                WHERE status_title = '{column_name}'"""
    cursor.execute(query_2)
    return cursor.fetchone()



@database_common.connection_handler
def change_cards_statuses(cursor: RealDictCursor, new_status: int, old_status: int, board_id: int, table: str) -> list:
    query = f"""
           UPDATE {table}
           SET status_id = '{new_status}'
           WHERE status_id = '{old_status}' AND board_id = '{board_id}'"""
    cursor.execute(query)


@database_common.connection_handler
def get_status(cursor: RealDictCursor, status_id: int, boards, board_id) -> list:
    query = f"""
        SELECT board_number as board_id, private_board, status_number as id, s.status_title as title
        FROM status_boards
        INNER JOIN statuses s on status_boards.status_number = s.id
        INNER JOIN {boards} b on status_boards.board_number = b.id
        WHERE s.id = {status_id} and b.id = {board_id}
"""
    cursor.execute(query)
    return cursor.fetchone()

@database_common.connection_handler
def save_new_card(cursor: RealDictCursor, table_name, new_card):
    query = f"""
            INSERT INTO {table_name} (board_id, card_title, status_id, card_order, archived)
            VALUES (%(board_id)s, %(card_title)s, %(status_id)s, %(card_order)s, %(archived)s)
            """
    cursor.execute(query, new_card)


def change_card_order(cards_id):
    cards_id = cards_id.split(",")
    cards_id_dict = {}
    for i in range(len(cards_id)):
        cards_id[i] = cards_id[i].split("card")
    for i in range(len(cards_id)):
        if int(cards_id[i][0]) in cards_id_dict.keys():
            cards_id_dict[int(cards_id[i][0])].append(int(cards_id[i][1]))
        else:
            cards_id_dict[int(cards_id[i][0])] = [int(cards_id[i][1])]
    return cards_id_dict


@database_common.connection_handler
def delete_card(cursor: RealDictCursor, table_name, card_id: int):
    query = f"""
            DELETE FROM {table_name}
            WHERE {table_name}.id = '{card_id}'
            """
    cursor.execute(query)


@database_common.connection_handler
def delete_board(cursor: RealDictCursor, table_name, board_id: int):
    query = f"""
            DELETE FROM {table_name}
            WHERE {table_name}.id = '{board_id}'
            """
    cursor.execute(query)


@database_common.connection_handler
def delete_cards(cursor: RealDictCursor, table_name, board_id: int):
    query = f"""
            DELETE FROM {table_name}
            WHERE {table_name}.board_id = '{board_id}'
            """
    cursor.execute(query)


@database_common.connection_handler
def check_if_username_taken(cursor: RealDictCursor, username: str) -> bool:
    query = f"""
            SELECT *
            FROM users
            WHERE username = '{username}'
            """
    cursor.execute(query)
    return cursor.rowcount > 0


@database_common.connection_handler
def register_new_user(cursor: RealDictCursor, user: dict):
    query = """
            INSERT INTO users (username, hash_pass)
            VALUES (%(username)s, crypt(%(password)s, gen_salt('bf',8)))
            """
    cursor.execute(query, user)


@database_common.connection_handler
def validate_login_data(cursor: RealDictCursor, user):
    query = """
            SELECT *
            FROM users
            WHERE username=%(username)s AND hash_pass=crypt(%(password)s, hash_pass)
            """
    cursor.execute(query, user)
    return cursor.rowcount > 0


@database_common.connection_handler
def get_user_id(cursor: RealDictCursor, username: str):
    query = f"""
            SELECT id
            FROM users
            WHERE username='{username}'
            """
    cursor.execute(query)
    return cursor.fetchone()


@database_common.connection_handler
def save_new_private_board(cursor: RealDictCursor, board_name: str, user_id: int):
    query = f"""
            INSERT INTO private_boards (title, forum_user_id)
            VALUES ('{board_name}', {user_id})
            RETURNING id
            """
    cursor.execute(query, board_name)
    return cursor.fetchone()


@database_common.connection_handler
def get_private_boards(cursor: RealDictCursor, user_id: int):
    query = f"""
            SELECT id, title
            FROM private_boards
            WHERE forum_user_id='{user_id}'
            """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_boards(cursor: RealDictCursor):
    query = f"""
            SELECT id, title
            FROM boards
            ORDER BY boards.id asc
            """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_max_order(cursor: RealDictCursor, table_name, board_id, status_id):
    query = f"""
            SELECT card_order
            FROM {table_name}
            WHERE {table_name}.board_id = {board_id} and {table_name}.status_id = {status_id}
            ORDER BY card_order DESC
            LIMIT 1
            """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def save_new_card_order_sql(cursor: RealDictCursor, table_name, card_id: int, status_id: int, new_order: int) -> list:
    query = f"""
        UPDATE {table_name}
        SET card_order = '{new_order}',
            status_id = '{status_id}'
        WHERE {table_name}.id = '{card_id}'"""
    cursor.execute(query)


@database_common.connection_handler
def archive_cards_sql(cursor: RealDictCursor, card_id, table_name, archive_status) -> list:
    query = f"""
        UPDATE {table_name}
        SET archived = {archive_status}
        WHERE {table_name}.id = {card_id}"""
    cursor.execute(query)

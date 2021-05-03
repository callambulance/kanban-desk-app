--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.6
-- Dumped by pg_dump version 9.5.6
-- CREATE EXTENSION pgcrypto;

ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS pk_user_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.boards DROP CONSTRAINT IF EXISTS pk_board_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.private_boards DROP CONSTRAINT IF EXISTS pk_private_board_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.private_boards DROP CONSTRAINT IF EXISTS fk_user_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.statuses DROP CONSTRAINT IF EXISTS pk_status_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.cards DROP CONSTRAINT IF EXISTS pk_card_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.cards DROP CONSTRAINT IF EXISTS fk_board_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.cards DROP CONSTRAINT IF EXISTS fk_status_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.private_cards DROP CONSTRAINT IF EXISTS pk_private_cards_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.private_cards DROP CONSTRAINT IF EXISTS fk_private_board_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.private_cards DROP CONSTRAINT IF EXISTS fk_status_id CASCADE;



DROP TABLE IF EXISTS public.boards;
CREATE TABLE boards (
    id serial NOT NULL,
    title text
);

DROP TABLE IF EXISTS public.statuses;
CREATE TABLE statuses (
    id serial NOT NULL,
    status_title text
);

DROP TABLE IF EXISTS public.cards;
CREATE TABLE cards (
    id serial NOT NULL,
    board_id integer,
    card_title text,
    status_id integer,
    card_order integer,
    archived integer
);


DROP TABLE IF EXISTS public.users;
CREATE TABLE users (
    id serial NOT NULL,
    username text,
    hash_pass text
);


DROP TABLE IF EXISTS public.private_boards;
CREATE TABLE private_boards (
    id serial NOT NULL,
    title text,
    forum_user_id integer
);


DROP TABLE IF EXISTS public.private_cards;
CREATE TABLE private_cards (
    id serial NOT NULL,
    board_id integer,
    card_title text,
    status_id integer,
    card_order integer,
    archived integer
);


DROP TABLE IF EXISTS public.status_boards;
CREATE TABLE status_boards (
    id serial NOT NULL,
    board_number integer NOT NULL,
    private_board bool NOT NULL default FALSE,
    status_number integer NOT NULL
);



ALTER TABLE ONLY boards
    ADD CONSTRAINT pk_board PRIMARY KEY (id);

ALTER TABLE ONLY users
    ADD CONSTRAINT pk_user_id PRIMARY KEY (id);

ALTER TABLE ONLY private_boards
    ADD CONSTRAINT pk_private_board_id PRIMARY KEY (id);


ALTER TABLE ONLY statuses
    ADD CONSTRAINT pk_status_id PRIMARY KEY (id);

ALTER TABLE ONLY cards
    ADD CONSTRAINT pk_card_id PRIMARY KEY (id);

ALTER TABLE ONLY private_cards
    ADD CONSTRAINT pk_private_cards_id  PRIMARY KEY (id);

ALTER TABLE ONLY status_boards
    ADD CONSTRAINT pk_status_board_id  PRIMARY KEY (id);

ALTER TABLE ONLY private_boards
    ADD CONSTRAINT fk_user_id FOREIGN KEY (forum_user_id) REFERENCES users(id);

ALTER TABLE ONLY cards
    ADD CONSTRAINT fk_board_id FOREIGN KEY (board_id) REFERENCES boards(id);

ALTER TABLE ONLY cards
    ADD CONSTRAINT fk_status_id FOREIGN KEY (status_id) REFERENCES statuses(id);

ALTER TABLE ONLY private_cards
    ADD CONSTRAINT fk_private_board_id FOREIGN KEY (board_id) REFERENCES private_boards(id);

ALTER TABLE ONLY private_cards
    ADD CONSTRAINT fk_status_id FOREIGN KEY (status_id) REFERENCES statuses(id);


INSERT INTO boards VALUES (1, 'Board 1!!!');
INSERT INTO boards VALUES (2, 'This is a board 2');
INSERT INTO boards VALUES (3, 'Board 3');
INSERT INTO boards VALUES (4, 'Hello');
INSERT INTO boards VALUES (5, 'This is a board');
INSERT INTO boards VALUES (6, 'another board');

SELECT pg_catalog.setval('boards_id_seq', 6, true);


INSERT INTO statuses VALUES (0, 'new');
INSERT INTO statuses VALUES (1, 'in progress');
INSERT INTO statuses VALUES (2, 'testing');
INSERT INTO statuses VALUES (3, 'done');

SELECT pg_catalog.setval('statuses_id_seq', 3, true);


INSERT INTO cards VALUES (1, 1, 'new card 1!!', 0, 0, 0);
INSERT INTO cards VALUES (2, 1, 'new card 2', 0, 0, 0);
INSERT INTO cards VALUES (3, 1, 'in progress card', 1, 0, 0);
INSERT INTO cards VALUES (4, 1, 'planning', 2, 0, 0);
INSERT INTO cards VALUES (5, 1, 'done card 1', 3, 0, 0);
INSERT INTO cards VALUES (6, 1, 'done card 1', 3, 1, 0);
INSERT INTO cards VALUES (7, 2, 'new card 1-2', 0, 0, 0);
INSERT INTO cards VALUES (8, 2, 'new card 2-2', 0, 1, 0);
INSERT INTO cards VALUES (9, 2, 'in progress card-2', 1, 0, 0);
INSERT INTO cards VALUES (10, 2, 'planning-2', 2, 0, 0);
INSERT INTO cards VALUES (11, 2, 'done card 1-2', 3, 0, 0);
INSERT INTO cards VALUES (12, 2, 'done card 1-2', 3, 1, 0);
INSERT INTO cards VALUES (13, 3, 'in progress card-2', 1, 0, 0);
INSERT INTO cards VALUES (14, 3, 'planning-2', 2, 0, 0);
INSERT INTO cards VALUES (15, 3, 'done card 1-3', 3, 0, 0);
INSERT INTO cards VALUES (16, 3, 'done card 1-3', 3, 1, 0);

SELECT pg_catalog.setval('cards_id_seq', 16, true);

INSERT INTO  status_boards VALUES (0, 1, false, 0);
INSERT INTO  status_boards VALUES (1, 1, false, 1);
INSERT INTO  status_boards VALUES (2, 1, false, 2);
INSERT INTO  status_boards VALUES (3, 1, false, 3);
INSERT INTO  status_boards VALUES (4, 2, false, 0);
INSERT INTO  status_boards VALUES (5, 2, false, 1);
INSERT INTO  status_boards VALUES (6, 2, false, 2);
INSERT INTO  status_boards VALUES (7, 2, false, 3);
INSERT INTO  status_boards VALUES (8, 3, false, 0);
INSERT INTO  status_boards VALUES (9, 3, false, 1);
INSERT INTO  status_boards VALUES (10, 3, false, 2);
INSERT INTO  status_boards VALUES (11, 3, false, 3);
INSERT INTO  status_boards VALUES (12, 4, false, 0);
INSERT INTO  status_boards VALUES (13, 4, false, 1);
INSERT INTO  status_boards VALUES (14, 4, false, 2);
INSERT INTO  status_boards VALUES (15, 4, false, 3);
INSERT INTO  status_boards VALUES (16, 5, false, 0);
INSERT INTO  status_boards VALUES (17, 5, false, 1);
INSERT INTO  status_boards VALUES (18, 5, false, 2);
INSERT INTO  status_boards VALUES (19, 5, false, 3);
INSERT INTO  status_boards VALUES (20, 6, false, 0);
INSERT INTO  status_boards VALUES (21, 6, false, 1);
INSERT INTO  status_boards VALUES (22, 6, false, 2);
INSERT INTO  status_boards VALUES (23, 6, false, 3);

SELECT pg_catalog.setval('status_boards_id_seq', 24, true);
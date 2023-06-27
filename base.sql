CREATE TABLE public.users
(
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    password character varying(50),
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS public.users
    OWNER to postgres;



INSERT INTO users (id, username, password)
VALUES (1, 'teste', '123')

INSERT INTO users (id, username, password)
VALUES (2, 'dsadadsda', 'dsada2131')

INSERT INTO users (id, username, password)
VALUES (3, 'odah', '123das')



CREATE TABLE public.games
(
    team character,
    points integer
);

ALTER TABLE IF EXISTS public.games
    OWNER to postgres;
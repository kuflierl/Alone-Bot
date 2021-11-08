--
-- PostgreSQL database dump
--

-- Dumped from database version 11.5
-- Dumped by pg_dump version 11.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: afk; Type: TABLE; Schema: public; Owner: hadock
--

CREATE TABLE public.afk (
    user_id bigint NOT NULL,
    reason text,
    "time" bigint
);


ALTER TABLE public.afk OWNER TO hadock;

--
-- Name: blacklist; Type: TABLE; Schema: public; Owner: hadock
--

CREATE TABLE public.blacklist (
    user_id bigint NOT NULL,
    reason text,
    "time" bigint
);


ALTER TABLE public.blacklist OWNER TO hadock;

--
-- Name: guilds; Type: TABLE; Schema: public; Owner: hadock
--

CREATE TABLE public.guilds (
    guild_id bigint NOT NULL,
    prefix text
);


ALTER TABLE public.guilds OWNER TO hadock;

--
-- Name: minecord; Type: TABLE; Schema: public; Owner: hadock
--

CREATE TABLE public.minecord (
    user_id bigint NOT NULL,
    wood bigint,
    stone bigint,
    obsidian bigint,
    coal bigint,
    iron bigint,
    gold bigint,
    redstone bigint,
    lapis bigint,
    diamond bigint,
    emerald bigint,
    quartz bigint,
    coins bigint,
    pickaxe bigint NOT NULL,
    axe bigint NOT NULL,
    pet bigint
);


ALTER TABLE public.minecord OWNER TO hadock;

--
-- Name: tags; Type: TABLE; Schema: public; Owner: hadock
--

CREATE TABLE public.tags (
    owner_id bigint NOT NULL,
    created_at bigint,
    name text,
    content text
);


ALTER TABLE public.tags OWNER TO hadock;

--
-- Name: todo; Type: TABLE; Schema: public; Owner: hadock
--

CREATE TABLE public.todo (
    user_id bigint NOT NULL,
    number bigint NOT NULL,
    action text NOT NULL
);


ALTER TABLE public.todo OWNER TO hadock;

--
-- Name: users; Type: TABLE; Schema: public; Owner: hadock
--

CREATE TABLE public.users (
    user_id bigint NOT NULL,
    prefix text
);


ALTER TABLE public.users OWNER TO hadock;

--
-- Data for Name: afk; Type: TABLE DATA; Schema: public; Owner: hadock
--

COPY public.afk (user_id, reason, "time") FROM stdin;
\.


--
-- Data for Name: blacklist; Type: TABLE DATA; Schema: public; Owner: hadock
--

COPY public.blacklist (user_id, reason, "time") FROM stdin;
\.


--
-- Data for Name: guilds; Type: TABLE DATA; Schema: public; Owner: hadock
--

COPY public.guilds (guild_id, prefix) FROM stdin;
\.


--
-- Data for Name: tags; Type: TABLE DATA; Schema: public; Owner: hadock
--

COPY public.tags (owner_id, created_at, name, content) FROM stdin;
\.


--
-- Data for Name: todo; Type: TABLE DATA; Schema: public; Owner: hadock
--

COPY public.todo (user_id, number, action) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: hadock
--

COPY public.users (user_id, prefix) FROM stdin;
\.


--
-- Name: afk afk_pkey; Type: CONSTRAINT; Schema: public; Owner: hadock
--

ALTER TABLE ONLY public.afk
    ADD CONSTRAINT afk_pkey PRIMARY KEY (user_id);


--
-- Name: blacklist blacklist_pkey; Type: CONSTRAINT; Schema: public; Owner: hadock
--

ALTER TABLE ONLY public.blacklist
    ADD CONSTRAINT blacklist_pkey PRIMARY KEY (user_id);


--
-- Name: guilds guilds_pkey; Type: CONSTRAINT; Schema: public; Owner: hadock
--

ALTER TABLE ONLY public.guilds
    ADD CONSTRAINT guilds_pkey PRIMARY KEY (guild_id);


--
-- Name: minecord minecord_pkey; Type: CONSTRAINT; Schema: public; Owner: hadock
--

ALTER TABLE ONLY public.minecord
    ADD CONSTRAINT minecord_pkey PRIMARY KEY (user_id);


--
-- Name: tags tags_pkey; Type: CONSTRAINT; Schema: public; Owner: hadock
--

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_pkey PRIMARY KEY (owner_id);


--
-- Name: todo todo_pkey; Type: CONSTRAINT; Schema: public; Owner: hadock
--

ALTER TABLE ONLY public.todo
    ADD CONSTRAINT todo_pkey PRIMARY KEY (user_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: hadock
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- PostgreSQL database dump complete
--


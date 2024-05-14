--
-- PostgreSQL database dump
--

-- Dumped from database version 11.10
-- Dumped by pg_dump version 11.11

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

CREATE SCHEMA dbschema;
create user :dbuser password :'dbpasswd' ;
grant create on database :database to :dbuser ;
grant connect on database :database to :dbuser ;
grant all privileges on schema dbschema to :dbuser ;
ALTER SCHEMA dbschema OWNER TO :dbuser ;

--
-- Name: add_user(text, text, text, text); Type: PROCEDURE; Schema: dbschema; Owner: :dbuser 
--

CREATE PROCEDURE dbschema.add_user(fname text, lname text, email text, password text)
    LANGUAGE plpgsql
    AS $$
begin
    insert into Users(fname, lname, email, password)
    values(fname, lname, email, password);
    commit;
end;$$;


ALTER PROCEDURE dbschema.add_user(fname text, lname text, email text, password text) OWNER TO :dbuser ;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: apparels; Type: TABLE; Schema: dbschema; Owner: :dbuser
--

CREATE TABLE dbschema.apparels (
    id integer NOT NULL,
    name text,
    description text,
    img_url text,
    category text,
    inventory integer,
    price double precision
);


ALTER TABLE dbschema.apparels OWNER TO :dbuser;

--
-- Name: bicycles; Type: TABLE; Schema: dbschema; Owner: :dbuser
--

CREATE TABLE dbschema.bicycles (
    id integer NOT NULL,
    name text,
    description text,
    img_url text,
    category text,
    inventory integer,
    price double precision
);


ALTER TABLE dbschema.bicycles OWNER TO :dbuser;

--
-- Name: fashion; Type: TABLE; Schema: dbschema; Owner: :dbuser
--

CREATE TABLE dbschema.fashion (
    id integer NOT NULL,
    name text,
    description text,
    img_url text,
    category text,
    inventory integer,
    price double precision
);


ALTER TABLE dbschema.fashion OWNER TO :dbuser;

--
-- Name: jewelry; Type: TABLE; Schema: dbschema; Owner: :dbuser
--

CREATE TABLE dbschema.jewelry (
    id integer NOT NULL,
    name text,
    description text,
    img_url text,
    category text,
    inventory integer,
    price double precision
);


ALTER TABLE dbschema.jewelry OWNER TO :dbuser;

--
-- Name: kart; Type: TABLE; Schema: dbschema; Owner: :dbuser
--

CREATE TABLE dbschema.kart (
    userid integer NOT NULL,
    productid integer NOT NULL,
    qty integer
);


ALTER TABLE dbschema.kart OWNER TO :dbuser;

--
-- Name: order_details; Type: TABLE; Schema: dbschema; Owner: :dbuser
--

CREATE TABLE dbschema.order_details (
    order_id integer NOT NULL,
    item_id integer NOT NULL,
    qty integer,
    total numeric,
    unit_price numeric
);


ALTER TABLE dbschema.order_details OWNER TO :dbuser;

--
-- Name: orders; Type: TABLE; Schema: dbschema; Owner: :dbuser
--

CREATE TABLE dbschema.orders (
    order_id integer NOT NULL,
    customer_id integer,
    order_date date,
    order_total numeric,
    email text
);


ALTER TABLE dbschema.orders OWNER TO :dbuser;

--
-- Name: reviews; Type: TABLE; Schema: dbschema; Owner: :dbuser
--

CREATE TABLE dbschema.reviews (
    item_id integer NOT NULL,
    category text NOT NULL,
    username text NOT NULL,
    review text,
    rating integer
);


ALTER TABLE dbschema.reviews OWNER TO :dbuser;

--
-- Name: users; Type: TABLE; Schema: dbschema; Owner: :dbuser
--

CREATE TABLE dbschema.users (
    id integer NOT NULL,
    fname text,
    lname text,
    email text,
    password text
);


ALTER TABLE dbschema.users OWNER TO :dbuser;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: dbschema; Owner: :dbuser
--

CREATE SEQUENCE dbschema.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE SEQUENCE dbschema.order_seq
    AS integer
    START WITH 4
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE dbschema.order_seq OWNER TO :dbuser;
ALTER SEQUENCE dbschema.users_id_seq OWNER TO :dbuser;
ALTER SEQUENCE dbschema.order_seq OWNER TO :dbuser;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: dbschema; Owner: :dbuser
--

ALTER SEQUENCE dbschema.users_id_seq OWNED BY dbschema.users.id;
ALTER SEQUENCE dbschema.order_seq OWNED BY dbschema.orders.order_id;


--
-- Name: users id; Type: DEFAULT; Schema: dbschema; Owner: :dbuser
--

ALTER TABLE ONLY dbschema.users ALTER COLUMN id SET DEFAULT nextval('dbschema.users_id_seq'::regclass);


--
-- Data for Name: apparels; Type: TABLE DATA; Schema: dbschema; Owner: :dbuser
--

COPY dbschema.apparels (id, name, description, img_url, category, inventory, price) FROM stdin;
5000010	DB Specialist SA Cap	<p>Database Specialist SA Cap</p>	/static/images/products/hat.jpeg	Caps	0	42.9500000000000028
5000000	Kurtha (Indian Attire)	<p>Kurtha (Indian Attire) Red Color</p>	/static/images/products/kurtha.jpeg		0	13.9499999999999993
\.


--
-- Data for Name: bicycles; Type: TABLE DATA; Schema: dbschema; Owner: :dbuser
--

COPY dbschema.bicycles (id, name, description, img_url, category, inventory, price) FROM stdin;
7000081	Bicycle White	<p>Bicycle White Color</p>	/static/images/products/bicyle_white.jpeg	Bicycles	7	162.949999999999989
7000183	Bicycle Red	<p>Bicycle Red Color</p>	/static/images/products/bicycle_red.jpg	Bicycle, Bicycles, Bike, Blue, Fixed Gear, Fixie, Pure Fix Cycles, White, WTB	32	199.949999999999989
\.


--
-- Data for Name: fashion; Type: TABLE DATA; Schema: dbschema; Owner: :dbuser
--

COPY dbschema.fashion (id, name, description, img_url, category, inventory, price) FROM stdin;
2	Bracelet Silver	<p><meta charset=utf-8>\n<p><span>A Demo bracelet. 100% Sterling Silver. Made in U.S.A. </span></p></p>	/static/images/products/silver_bracelet.jpeg	1-100, Accessories, arrivals, AW15, Bracelets, gift guide, jewelry, Man, mothermoon, signature, silver, spring2, visible, Woman	74	42.9500000000000028
3	Bracelet Gold	<p><meta charset=utf-8>\n<p><span>A Demo Bracelet. 14k Gold. Made in U.S.A. </span></p></p>	/static/images/products/gold_bracelet.jpeg	1-100, Accessories, Bracelets, cooloff, gift guide, jewelry, last, Man, S14, silver, visible, Woman	99	90.9500000000000028
\.


--
-- Data for Name: jewelry; Type: TABLE DATA; Schema: dbschema; Owner: :dbuser
--

COPY dbschema.jewelry (id, name, description, img_url, category, inventory, price) FROM stdin;
9000000	22k Gold Necklace	<p>22k Carret Gold Necklace</p>	/static/images/products/jewelry1.jpeg	Yellow Gold	0	9507.949999999999989
9000001	Perl Necklace	<p>Perl Necklace</p>	/static/images/products/jewelry2.jpeg	Perls	38	197.949999999999989
\.


--
-- Data for Name: kart; Type: TABLE DATA; Schema: dbschema; Owner: :dbuser
--

COPY dbschema.kart (userid, productid, qty) FROM stdin;
4	3	\N
4	2	\N
\.


--
-- Data for Name: order_details; Type: TABLE DATA; Schema: dbschema; Owner: :dbuser
--

COPY dbschema.order_details (order_id, item_id, qty, total) FROM stdin;
1	2	1	67.95
1	3	1	38.95
\.


--
-- Data for Name: orders; Type: TABLE DATA; Schema: dbschema; Owner: :dbuser
--

COPY dbschema.orders (order_id, customer_id, order_date, order_total) FROM stdin;
1	4	2021-06-08	200
2	4	2021-06-08	300
3	4	2021-06-08	200
\.


--
-- Data for Name: reviews; Type: TABLE DATA; Schema: dbschema; Owner: :dbuser
--

COPY dbschema.reviews (item_id, category, username, review, rating) FROM stdin;
2	fashion	test1	awesome product 1	4
2	fashion	test2	awesome product 2	3
2	fashion	test3	awesome product 3	4
2	fashion	test4	awesome product 4	3
2	fashion	test5	awesome product 5	4
2	fashion	test6	awesome product 6	3
2	fashion	test7	awesome product 7	4
2	fashion	test8	awesome product 8	3
2	fashion	test9	awesome product 9	4
2	fashion	test10	awesome product 10	4
2	fashion	test11	awesome product 11	4
2	fashion	test12	awesome product 12	3
2	fashion	test13	awesome product 13	5
2	fashion	test14	awesome product 14	5
2	fashion	test15	awesome product 15	5
2	fashion	test16	awesome product 16	4
2	fashion	test17	awesome product 17	5
2	fashion	test18	awesome product 18	3
2	fashion	test19	awesome product 19	5
2	fashion	test20	awesome product 20	4
2	fashion	test21	awesome product 21	3
3	fashion	test6	awesome product 6	5
3	fashion	test7	awesome product 7	3
3	fashion	test8	awesome product 8	2
3	fashion	test9	awesome product 9	5
3	fashion	test10	awesome product 10	3
3	fashion	test11	awesome product 11	4
3	fashion	test12	awesome product 12	2
3	fashion	test13	awesome product 13	5
3	fashion	test14	awesome product 14	5
3	fashion	test15	awesome product 15	4
3	fashion	test16	awesome product 16	2
3	fashion	test17	awesome product 17	3
3	fashion	test18	awesome product 18	4
3	fashion	test19	awesome product 19	4
3	fashion	test20	awesome product 20	5
3	fashion	test21	awesome product 21	2
3	fashion	test22	awesome product 22	5
3	fashion	test23	awesome product 23	5
3	fashion	test24	awesome product 24	5
3	fashion	test25	awesome product 25	4
3	fashion	test26	awesome product 26	3
3	fashion	test27	awesome product 27	4
3	fashion	test28	awesome product 28	5
3	fashion	test29	awesome product 29	2
3	fashion	test30	awesome product 30	5
3	fashion	test31	awesome product 31	2
3	fashion	test32	awesome product 32	5
3	fashion	test33	awesome product 33	2
3	fashion	test34	awesome product 34	4
3	fashion	test35	awesome product 35	5
3	fashion	test36	awesome product 36	3
3	fashion	test37	awesome product 37	3
3	fashion	test38	awesome product 38	2
3	fashion	test39	awesome product 39	3
3	fashion	test1	awesome product 1	2
3	fashion	test2	awesome product 2	3
3	fashion	test3	awesome product 3	2
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: dbschema; Owner: :dbuser
--

COPY dbschema.users (id, fname, lname, email, password) FROM stdin;
1	krishna	sarabu	ksarabu@yahoo.com	welcome
\.


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: dbschema; Owner: :dbuser
--

SELECT pg_catalog.setval('dbschema.users_id_seq', 6, true);


--
-- Name: apparels apparels_pkey; Type: CONSTRAINT; Schema: dbschema; Owner: :dbuser
--

ALTER TABLE ONLY dbschema.apparels
    ADD CONSTRAINT apparels_pkey PRIMARY KEY (id);


--
-- Name: bicycles bicycles_pkey; Type: CONSTRAINT; Schema: dbschema; Owner: :dbuser
--

ALTER TABLE ONLY dbschema.bicycles
    ADD CONSTRAINT bicycles_pkey PRIMARY KEY (id);


--
-- Name: fashion fashion_pkey; Type: CONSTRAINT; Schema: dbschema; Owner: :dbuser
--

ALTER TABLE ONLY dbschema.fashion
    ADD CONSTRAINT fashion_pkey PRIMARY KEY (id);


--
-- Name: jewelry jewelry_pkey; Type: CONSTRAINT; Schema: dbschema; Owner: :dbuser
--

ALTER TABLE ONLY dbschema.jewelry
    ADD CONSTRAINT jewelry_pkey PRIMARY KEY (id);


--
-- Name: kart kart_pk; Type: CONSTRAINT; Schema: dbschema; Owner: :dbuser
--

ALTER TABLE ONLY dbschema.kart
    ADD CONSTRAINT kart_pk PRIMARY KEY (userid, productid);


--
-- Name: order_details order_details_pk; Type: CONSTRAINT; Schema: dbschema; Owner: :dbuser
--

ALTER TABLE ONLY dbschema.order_details
    ADD CONSTRAINT order_details_pk PRIMARY KEY (order_id, item_id);


--
-- Name: orders orders_pk; Type: CONSTRAINT; Schema: dbschema; Owner: :dbuser
--

ALTER TABLE ONLY dbschema.orders
    ADD CONSTRAINT orders_pk PRIMARY KEY (order_id);


--
-- Name: reviews reviews_pk; Type: CONSTRAINT; Schema: dbschema; Owner: :dbuser
--

ALTER TABLE ONLY dbschema.reviews
    ADD CONSTRAINT reviews_pk PRIMARY KEY (item_id, category, username);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: dbschema; Owner: :dbuser
--

ALTER TABLE ONLY dbschema.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


alter user :dbuser set search_path="dbschema", "public";
--
-- PostgreSQL database dump complete
--


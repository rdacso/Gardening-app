--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.4
-- Dumped by pg_dump version 9.5.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'LATIN1';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: alerts; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE alerts (
    alert_id integer NOT NULL,
    user_plant_id integer,
    date timestamp without time zone,
    completion boolean,
    alert_type_id integer
);


ALTER TABLE alerts OWNER TO vagrant;

--
-- Name: alerts_alert_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE alerts_alert_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE alerts_alert_id_seq OWNER TO vagrant;

--
-- Name: alerts_alert_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE alerts_alert_id_seq OWNED BY alerts.alert_id;


--
-- Name: alerttype; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE alerttype (
    alert_type_id integer NOT NULL,
    alert_type character varying
);


ALTER TABLE alerttype OWNER TO vagrant;

--
-- Name: alerttype_alert_type_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE alerttype_alert_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE alerttype_alert_type_id_seq OWNER TO vagrant;

--
-- Name: alerttype_alert_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE alerttype_alert_type_id_seq OWNED BY alerttype.alert_type_id;


--
-- Name: plants; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE plants (
    plant_id integer NOT NULL,
    common_name character varying,
    duration character varying,
    active_growth_period character varying,
    flower_color character varying,
    flower_conspicuous character varying,
    foliage_color character varying,
    height double precision,
    adapted_to_coarse_textured_soil character varying,
    adapted_to_medium_textured_soil character varying,
    adapted_to_fine_textured_soil character varying,
    drought_tolerance character varying,
    fertility_requirement character varying,
    soil_ph_min double precision,
    soil_ph_max double precision,
    shade_tolerance character varying,
    temperature_min integer,
    plant_image bytea
);


ALTER TABLE plants OWNER TO vagrant;

--
-- Name: plants_plant_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE plants_plant_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE plants_plant_id_seq OWNER TO vagrant;

--
-- Name: plants_plant_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE plants_plant_id_seq OWNED BY plants.plant_id;


--
-- Name: userplants; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE userplants (
    up_id integer NOT NULL,
    plant_id integer,
    user_id integer,
    qty integer
);


ALTER TABLE userplants OWNER TO vagrant;

--
-- Name: userplants_up_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE userplants_up_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE userplants_up_id_seq OWNER TO vagrant;

--
-- Name: userplants_up_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE userplants_up_id_seq OWNED BY userplants.up_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE users (
    user_id integer NOT NULL,
    email character varying(64),
    password character varying(64),
    first_name character varying(65),
    last_name character varying(65),
    phone_number character varying,
    city character varying(25),
    state character varying(25),
    zip_code character varying(15),
    tmz timestamp without time zone,
    alerts boolean
);


ALTER TABLE users OWNER TO vagrant;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE users_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE users_user_id_seq OWNER TO vagrant;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE users_user_id_seq OWNED BY users.user_id;


--
-- Name: alert_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY alerts ALTER COLUMN alert_id SET DEFAULT nextval('alerts_alert_id_seq'::regclass);


--
-- Name: alert_type_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY alerttype ALTER COLUMN alert_type_id SET DEFAULT nextval('alerttype_alert_type_id_seq'::regclass);


--
-- Name: plant_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY plants ALTER COLUMN plant_id SET DEFAULT nextval('plants_plant_id_seq'::regclass);


--
-- Name: up_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY userplants ALTER COLUMN up_id SET DEFAULT nextval('userplants_up_id_seq'::regclass);


--
-- Name: user_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY users ALTER COLUMN user_id SET DEFAULT nextval('users_user_id_seq'::regclass);


--
-- Data for Name: alerts; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY alerts (alert_id, user_plant_id, date, completion, alert_type_id) FROM stdin;
1	1	2016-11-30 00:00:00	t	1
\.


--
-- Name: alerts_alert_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('alerts_alert_id_seq', 1, true);


--
-- Data for Name: alerttype; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY alerttype (alert_type_id, alert_type) FROM stdin;
1	Watering
2	Fertilizing
3	Trimming
\.


--
-- Name: alerttype_alert_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('alerttype_alert_type_id_seq', 3, true);


--
-- Data for Name: plants; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY plants (plant_id, common_name, duration, active_growth_period, flower_color, flower_conspicuous, foliage_color, height, adapted_to_coarse_textured_soil, adapted_to_medium_textured_soil, adapted_to_fine_textured_soil, drought_tolerance, fertility_requirement, soil_ph_min, soil_ph_max, shade_tolerance, temperature_min, plant_image) FROM stdin;
1	Common yarrow	perennial	spring	white	yes	green	3	no	yes	no	medium	medium	6	8	intermediate	-38	\\x68747470733a2f2f666c69632e6b722f702f6578686d6d6322
2	Indian ricegrass	perennial	spring, summer, fall	yellow	no	green	2	yes	yes	no	high	low	6.59999999999999964	8.59999999999999964	intolerant	-43	\\x687474703a2f2f6c372e616c616d792e636f6d2f7a6f6f6d732f61383632623134363762353634396438393534353835643765653861396564642f612d6669656c642d66756c6c2d6f662d696e6469616e2d7269636567726173732d6163686e6174686572756d2d68796d656e6f696465732d73686f77732d6f66662d6435326472342e6a706722
3	Rosemary	perennial	spring and summer	blue	yes	dark green	5	yes	yes	no	high	low	5	7.5	intolerant	-3	\\x68747470733a2f2f7374617469632e706578656c732e636f6d2f70686f746f732f3133353136382f706578656c732d70686f746f2d3133353136382e6a70656722
4	Scarlet indian paintbrush	annual	spring and summer	red	yes	green	1.60000000000000009	no	yes	no	low	low	4.90000000000000036	6.79999999999999982	tolerant	-28	\\x687474703a2f2f63382e616c616d792e636f6d2f636f6d702f61706b7072722f736361726c65742d7061696e7462727573682d696e6469616e2d7061696e7462727573682d67726561742d7265642d7061696e7462727573682d63617374696c6c656a612d61706b7072722e6a706722
5	White poplar	perennial	spring and summer	yellow	no	green	100	yes	yes	yes	medium	medium	4.90000000000000036	7	intolerant	-38	\\x687474703a2f2f75732e31323372662e636f6d2f343530776d2f6a616e6865746d616e2f6a616e6865746d616e313530362f6a616e6865746d616e3135303630303031372f34313037343932392d69766965642d77686974652d706f706c61722d7472756e6b2d616e642d6272616e636865732d696e2d7468652d666f726573742e6a70673f7665723d3622
6	Narrowleaf cottonwood	perennial	summer	white	yes	green	60	yes	yes	no	low	low	6	7.5	intolerant	-28	\\x687474703a2f2f6c372e616c616d792e636f6d2f7a6f6f6d732f64363064303836333436653534643634623832633838656632316437623165612f6e6172726f776c6561662d636f74746f6e776f6f642d747265652d77696c6c6f772d66616d696c792d67726f77696e672d616c6f6e672d7468652d62616e6b732d6f662d6274633033372e6a706722
7	Balsam poplar	perennial	spring and summer	yellow	no	yellow-green	80	yes	yes	yes	low	medium	4.5	7	intolerant	-79	\\x687474703a2f2f73312e747265652d74696d652e63612f74742f696d616765732f706f706c61725f62616c73616d5f3031345f30315f3630302e6a706722
8	Varileaf cinquefoil	perennial	spring and summer	yellow	yes	green	3	yes	yes	yes	low	low	7	8	intermediate	-33	\\x687474703a2f2f736e6f77626972647069782e636f6d2f696d616765732f6d742f706c616e74732f6a6f7267656e73656e2f706f74656e74696c6c615f64697665727369666f6c696130312e6a706722
9	Slender cinquefoil	perennial	spring and summer	yellow	yes	gray-green	2.39999999999999991	yes	yes	no	medium	low	4	7.5	intolerant	-43	\\x687474703a2f2f6c372e616c616d792e636f6d2f7a6f6f6d732f31346534383439313065613234633932613630666330363938366333656334382f736d616c6c2d79656c6c6f772d666c6f7765722d6f662d67616c616e67616c2d65726563742d63696e717565666f696c2d6765786e33642e6a706722
10	Common selfheal	perennial	spring and summer	purple	yes	gray-green	1.5	yes	yes	yes	medium	medium	5.40000000000000036	8	intermediate	-38	\\x2f7374617469632f636f6d6d6f6e2d73656c666865616c2e6a706722
11	American plum	perennial	spring and summer	white	yes	green	24	yes	yes	no	none	medium	5	7	intolerant	-38	\\x2f7374617469632f706c756d2d747265652d6d2d782e6a706722
12	Bluebunch wheatgrass	perennial	spring, summer, fall	yellow	no	gray-green	3	yes	yes	yes	high	low	6.59999999999999964	8.40000000000000036	intolerant	-38	\\x2f7374617469632f626c756562756e63682d776865617467726173732e6a706722
13	Greater creeping spearwort	perennial	summer	yellow	yes	green	1.5	no	yes	yes	low	medium	6	7.5	tolerant	-33	\\x2f7374617469632f677265617465722d6372656570696e672d7370656172776f72742e6a70656722
14	Scarlet firethorn	perennial	spring and summer	white	yes	green	8	no	yes	yes	low	high	5.79999999999999982	8	intolerant	12	\\x2f7374617469632f736361726c65742d6669726574686f726e2e6a706722
15	Lombardy poplar	perennial	spring and summer	white	no	green	190	yes	yes	no	low	medium	5	8.5	intolerant	-28	\\x2f7374617469632f6c6f6d62617264792d706f706c61722e6a70656722
16	Austrian pine	perennial	spring	yellow	no	green	120	no	yes	no	medium	medium	5.5	7.5	intolerant	-38	\\x2f7374617469632f617573747269616e2d70696e652e6a70656722
17	Stalkless yellowcress	annual	spring, summer, fall	yellow	yes	green	1.5	yes	yes	yes	none	medium	5.5	7.5	intermediate	52	\\x2f7374617469632f7374616c6b6c6573732d79656c6c6f7763726573732e6a706722
18	Brazilian peppertree	perennial	year round	white	yes	dark green	30	yes	yes	yes	low	low	6.5	7.5	intolerant	28	\\x2f7374617469632f6272617a696c69616e2d706570706572747265652e6a706722
19	Old-man-in-the-spring	annual, biennial	spring and summer	yellow	no	green	1.5	yes	yes	yes	medium	medium	5	8.5	intolerant	47	\\x2f7374617469632f6f6c642d6d616e2d696e2d7468652d737072696e672e6a706722
20	Maryland senna	perennial	spring and summer	yellow	yes	green	6.59999999999999964	yes	yes	no	medium	low	4	7	intermediate	-18	\\x2f7374617469632f6d6172796c616e6473656e6e612e6a706722
21	Idaho blue-eyed grass	perennial	spring and summer	blue	yes	yellow-green	1.69999999999999996	yes	yes	yes	low	medium	6.40000000000000036	8.19999999999999929	tolerant	-38	\\x2f7374617469632f696461686f2d626c75652d657965642d67726173732e6a706722
22	Wreath goldenrod	perennial	spring and summer	yellow	yes	dark green	3	no	yes	yes	low	low	5.5	7	intermediate	-28	\\x2f7374617469632f777265617468676f6c64656e726f642e6a706722
\.


--
-- Name: plants_plant_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('plants_plant_id_seq', 22, true);


--
-- Data for Name: userplants; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY userplants (up_id, plant_id, user_id, qty) FROM stdin;
1	11	1	\N
\.


--
-- Name: userplants_up_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('userplants_up_id_seq', 1, true);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY users (user_id, email, password, first_name, last_name, phone_number, city, state, zip_code, tmz, alerts) FROM stdin;
1	al@test.com	admin123	Al	Beback	8327947918	\N	\N	\N	2016-11-23 01:42:42.154358	t
\.


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('users_user_id_seq', 1, true);


--
-- Name: alerts_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY alerts
    ADD CONSTRAINT alerts_pkey PRIMARY KEY (alert_id);


--
-- Name: alerttype_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY alerttype
    ADD CONSTRAINT alerttype_pkey PRIMARY KEY (alert_type_id);


--
-- Name: plants_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY plants
    ADD CONSTRAINT plants_pkey PRIMARY KEY (plant_id);


--
-- Name: userplants_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY userplants
    ADD CONSTRAINT userplants_pkey PRIMARY KEY (up_id);


--
-- Name: users_email_key; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: alerts_alert_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY alerts
    ADD CONSTRAINT alerts_alert_type_id_fkey FOREIGN KEY (alert_type_id) REFERENCES alerttype(alert_type_id);


--
-- Name: alerts_user_plant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY alerts
    ADD CONSTRAINT alerts_user_plant_id_fkey FOREIGN KEY (user_plant_id) REFERENCES userplants(up_id);


--
-- Name: userplants_plant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY userplants
    ADD CONSTRAINT userplants_plant_id_fkey FOREIGN KEY (plant_id) REFERENCES plants(plant_id);


--
-- Name: userplants_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY userplants
    ADD CONSTRAINT userplants_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--


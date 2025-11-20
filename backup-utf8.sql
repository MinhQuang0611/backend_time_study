--
-- PostgreSQL database dump
--

\restrict eoTGlatzIu14JXhCvvEcF68eaM14PAdD9PQG0zSb29pr5CtGPjYgzwk8kh6Kp6y

-- Dumped from database version 16.11 (Debian 16.11-1.pgdg13+1)
-- Dumped by pg_dump version 16.11 (Debian 16.11-1.pgdg13+1)

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

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: default_settings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.default_settings (
    default_setting_id integer NOT NULL,
    setting_key character varying NOT NULL,
    default_value character varying,
    data_type character varying,
    category character varying,
    description character varying,
    is_configurable integer
);


ALTER TABLE public.default_settings OWNER TO postgres;

--
-- Name: default_settings_default_setting_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.default_settings_default_setting_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.default_settings_default_setting_id_seq OWNER TO postgres;

--
-- Name: default_settings_default_setting_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.default_settings_default_setting_id_seq OWNED BY public.default_settings.default_setting_id;


--
-- Name: goals; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.goals (
    goal_id integer NOT NULL,
    user_id integer NOT NULL,
    goal_date double precision,
    target_sessions integer,
    completed_sessions integer,
    completion_percentage integer,
    is_achieved integer,
    achieved_at double precision,
    created_at double precision,
    updated_at double precision
);


ALTER TABLE public.goals OWNER TO postgres;

--
-- Name: goals_goal_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.goals_goal_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.goals_goal_id_seq OWNER TO postgres;

--
-- Name: goals_goal_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.goals_goal_id_seq OWNED BY public.goals.goal_id;


--
-- Name: session_pauses; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.session_pauses (
    pause_id integer NOT NULL,
    session_id integer NOT NULL,
    pause_start double precision,
    pause_end double precision,
    pause_duration integer
);


ALTER TABLE public.session_pauses OWNER TO postgres;

--
-- Name: session_pauses_pause_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.session_pauses_pause_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.session_pauses_pause_id_seq OWNER TO postgres;

--
-- Name: session_pauses_pause_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.session_pauses_pause_id_seq OWNED BY public.session_pauses.pause_id;


--
-- Name: sessions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sessions (
    session_id integer NOT NULL,
    user_id integer NOT NULL,
    session_date double precision,
    start_time double precision,
    end_time double precision,
    duration_minutes integer,
    actual_duration_minutes integer,
    session_type character varying,
    status character varying,
    focus_session_count integer,
    is_completed integer,
    pause_count integer,
    total_pause_duration integer,
    created_at double precision,
    updated_at double precision
);


ALTER TABLE public.sessions OWNER TO postgres;

--
-- Name: sessions_session_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sessions_session_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sessions_session_id_seq OWNER TO postgres;

--
-- Name: sessions_session_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sessions_session_id_seq OWNED BY public.sessions.session_id;


--
-- Name: statistics_cache; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.statistics_cache (
    cache_id integer NOT NULL,
    user_id integer NOT NULL,
    cache_date double precision,
    cache_type character varying NOT NULL,
    total_sessions integer,
    total_focus_time integer,
    total_break_time integer,
    completed_tasks integer,
    goal_achieved integer,
    current_streak integer,
    best_streak integer,
    cached_at double precision
);


ALTER TABLE public.statistics_cache OWNER TO postgres;

--
-- Name: statistics_cache_cache_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.statistics_cache_cache_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.statistics_cache_cache_id_seq OWNER TO postgres;

--
-- Name: statistics_cache_cache_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.statistics_cache_cache_id_seq OWNED BY public.statistics_cache.cache_id;


--
-- Name: streak_records; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.streak_records (
    streak_id integer NOT NULL,
    user_id integer NOT NULL,
    streak_date double precision,
    has_activity integer,
    session_count integer,
    focus_time integer
);


ALTER TABLE public.streak_records OWNER TO postgres;

--
-- Name: streak_records_streak_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.streak_records_streak_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.streak_records_streak_id_seq OWNER TO postgres;

--
-- Name: streak_records_streak_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.streak_records_streak_id_seq OWNED BY public.streak_records.streak_id;


--
-- Name: task_sessions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.task_sessions (
    task_session_id integer NOT NULL,
    task_id integer NOT NULL,
    session_id integer NOT NULL,
    time_spent integer,
    notes character varying,
    created_at double precision
);


ALTER TABLE public.task_sessions OWNER TO postgres;

--
-- Name: task_sessions_task_session_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.task_sessions_task_session_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.task_sessions_task_session_id_seq OWNER TO postgres;

--
-- Name: task_sessions_task_session_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.task_sessions_task_session_id_seq OWNED BY public.task_sessions.task_session_id;


--
-- Name: tasks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tasks (
    task_id integer NOT NULL,
    user_id integer NOT NULL,
    title character varying,
    description character varying,
    priority character varying,
    task_date double precision,
    is_completed integer,
    completed_at double precision,
    total_time_spent integer,
    estimated_sessions integer,
    actual_sessions integer,
    order_index integer,
    created_at double precision,
    updated_at double precision
);


ALTER TABLE public.tasks OWNER TO postgres;

--
-- Name: tasks_task_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tasks_task_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tasks_task_id_seq OWNER TO postgres;

--
-- Name: tasks_task_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tasks_task_id_seq OWNED BY public.tasks.task_id;


--
-- Name: user_settings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_settings (
    setting_id integer NOT NULL,
    user_id integer NOT NULL,
    setting_key character varying NOT NULL,
    setting_value character varying,
    data_type character varying,
    created_at double precision,
    updated_at double precision
);


ALTER TABLE public.user_settings OWNER TO postgres;

--
-- Name: user_settings_setting_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_settings_setting_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_settings_setting_id_seq OWNER TO postgres;

--
-- Name: user_settings_setting_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_settings_setting_id_seq OWNED BY public.user_settings.setting_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    email character varying,
    display_name character varying,
    profile_picture_url character varying,
    created_at double precision,
    last_login double precision,
    is_anonymous integer
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_base; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users_base (
    sso_sub character varying,
    username character varying,
    email character varying,
    dob double precision,
    gender character varying,
    first_name character varying,
    last_name character varying,
    full_name character varying,
    phone character varying,
    address character varying,
    identity_card character varying,
    identity_card_date double precision,
    identity_card_place character varying,
    is_active boolean,
    last_login double precision,
    hashed_password character varying(255),
    roles character varying[],
    id integer NOT NULL,
    created_at double precision,
    updated_at double precision
);


ALTER TABLE public.users_base OWNER TO postgres;

--
-- Name: users_base_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_base_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_base_id_seq OWNER TO postgres;

--
-- Name: users_base_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_base_id_seq OWNED BY public.users_base.id;


--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_user_id_seq OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: default_settings default_setting_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.default_settings ALTER COLUMN default_setting_id SET DEFAULT nextval('public.default_settings_default_setting_id_seq'::regclass);


--
-- Name: goals goal_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.goals ALTER COLUMN goal_id SET DEFAULT nextval('public.goals_goal_id_seq'::regclass);


--
-- Name: session_pauses pause_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.session_pauses ALTER COLUMN pause_id SET DEFAULT nextval('public.session_pauses_pause_id_seq'::regclass);


--
-- Name: sessions session_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sessions ALTER COLUMN session_id SET DEFAULT nextval('public.sessions_session_id_seq'::regclass);


--
-- Name: statistics_cache cache_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.statistics_cache ALTER COLUMN cache_id SET DEFAULT nextval('public.statistics_cache_cache_id_seq'::regclass);


--
-- Name: streak_records streak_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.streak_records ALTER COLUMN streak_id SET DEFAULT nextval('public.streak_records_streak_id_seq'::regclass);


--
-- Name: task_sessions task_session_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_sessions ALTER COLUMN task_session_id SET DEFAULT nextval('public.task_sessions_task_session_id_seq'::regclass);


--
-- Name: tasks task_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks ALTER COLUMN task_id SET DEFAULT nextval('public.tasks_task_id_seq'::regclass);


--
-- Name: user_settings setting_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_settings ALTER COLUMN setting_id SET DEFAULT nextval('public.user_settings_setting_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Name: users_base id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_base ALTER COLUMN id SET DEFAULT nextval('public.users_base_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
initial
\.


--
-- Data for Name: default_settings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.default_settings (default_setting_id, setting_key, default_value, data_type, category, description, is_configurable) FROM stdin;
\.


--
-- Data for Name: goals; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.goals (goal_id, user_id, goal_date, target_sessions, completed_sessions, completion_percentage, is_achieved, achieved_at, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: session_pauses; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.session_pauses (pause_id, session_id, pause_start, pause_end, pause_duration) FROM stdin;
\.


--
-- Data for Name: sessions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sessions (session_id, user_id, session_date, start_time, end_time, duration_minutes, actual_duration_minutes, session_type, status, focus_session_count, is_completed, pause_count, total_pause_duration, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: statistics_cache; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.statistics_cache (cache_id, user_id, cache_date, cache_type, total_sessions, total_focus_time, total_break_time, completed_tasks, goal_achieved, current_streak, best_streak, cached_at) FROM stdin;
\.


--
-- Data for Name: streak_records; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.streak_records (streak_id, user_id, streak_date, has_activity, session_count, focus_time) FROM stdin;
\.


--
-- Data for Name: task_sessions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.task_sessions (task_session_id, task_id, session_id, time_spent, notes, created_at) FROM stdin;
\.


--
-- Data for Name: tasks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tasks (task_id, user_id, title, description, priority, task_date, is_completed, completed_at, total_time_spent, estimated_sessions, actual_sessions, order_index, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: user_settings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_settings (setting_id, user_id, setting_key, setting_value, data_type, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (user_id, email, display_name, profile_picture_url, created_at, last_login, is_anonymous) FROM stdin;
\.


--
-- Data for Name: users_base; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users_base (sso_sub, username, email, dob, gender, first_name, last_name, full_name, phone, address, identity_card, identity_card_date, identity_card_place, is_active, last_login, hashed_password, roles, id, created_at, updated_at) FROM stdin;
\.


--
-- Name: default_settings_default_setting_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.default_settings_default_setting_id_seq', 1, false);


--
-- Name: goals_goal_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.goals_goal_id_seq', 1, false);


--
-- Name: session_pauses_pause_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.session_pauses_pause_id_seq', 1, false);


--
-- Name: sessions_session_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sessions_session_id_seq', 1, false);


--
-- Name: statistics_cache_cache_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.statistics_cache_cache_id_seq', 1, false);


--
-- Name: streak_records_streak_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.streak_records_streak_id_seq', 1, false);


--
-- Name: task_sessions_task_session_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.task_sessions_task_session_id_seq', 1, false);


--
-- Name: tasks_task_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tasks_task_id_seq', 1, false);


--
-- Name: user_settings_setting_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_settings_setting_id_seq', 1, false);


--
-- Name: users_base_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_base_id_seq', 1, false);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_user_id_seq', 1, false);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: default_settings default_settings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.default_settings
    ADD CONSTRAINT default_settings_pkey PRIMARY KEY (default_setting_id);


--
-- Name: default_settings default_settings_setting_key_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.default_settings
    ADD CONSTRAINT default_settings_setting_key_key UNIQUE (setting_key);


--
-- Name: goals goals_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.goals
    ADD CONSTRAINT goals_pkey PRIMARY KEY (goal_id);


--
-- Name: session_pauses session_pauses_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.session_pauses
    ADD CONSTRAINT session_pauses_pkey PRIMARY KEY (pause_id);


--
-- Name: sessions sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_pkey PRIMARY KEY (session_id);


--
-- Name: statistics_cache statistics_cache_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.statistics_cache
    ADD CONSTRAINT statistics_cache_pkey PRIMARY KEY (cache_id);


--
-- Name: streak_records streak_records_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.streak_records
    ADD CONSTRAINT streak_records_pkey PRIMARY KEY (streak_id);


--
-- Name: task_sessions task_sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_sessions
    ADD CONSTRAINT task_sessions_pkey PRIMARY KEY (task_session_id);


--
-- Name: tasks tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (task_id);


--
-- Name: goals uq_goals_user_date; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.goals
    ADD CONSTRAINT uq_goals_user_date UNIQUE (user_id, goal_date);


--
-- Name: statistics_cache uq_statistics_cache_user_date_type; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.statistics_cache
    ADD CONSTRAINT uq_statistics_cache_user_date_type UNIQUE (user_id, cache_date, cache_type);


--
-- Name: user_settings uq_user_settings_user_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_settings
    ADD CONSTRAINT uq_user_settings_user_key UNIQUE (user_id, setting_key);


--
-- Name: user_settings user_settings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_settings
    ADD CONSTRAINT user_settings_pkey PRIMARY KEY (setting_id);


--
-- Name: users_base users_base_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users_base
    ADD CONSTRAINT users_base_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: idx_default_settings_category; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_default_settings_category ON public.default_settings USING btree (category);


--
-- Name: idx_goals_goal_date; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_goals_goal_date ON public.goals USING btree (goal_date);


--
-- Name: idx_goals_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_goals_user_id ON public.goals USING btree (user_id);


--
-- Name: idx_sessions_session_date; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_sessions_session_date ON public.sessions USING btree (session_date);


--
-- Name: idx_sessions_session_type; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_sessions_session_type ON public.sessions USING btree (session_type);


--
-- Name: idx_sessions_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_sessions_status ON public.sessions USING btree (status);


--
-- Name: idx_sessions_user_date; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_sessions_user_date ON public.sessions USING btree (user_id, session_date);


--
-- Name: idx_sessions_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_sessions_user_id ON public.sessions USING btree (user_id);


--
-- Name: idx_tasks_is_completed; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_tasks_is_completed ON public.tasks USING btree (is_completed);


--
-- Name: idx_tasks_priority; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_tasks_priority ON public.tasks USING btree (priority);


--
-- Name: idx_tasks_task_date; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_tasks_task_date ON public.tasks USING btree (task_date);


--
-- Name: idx_tasks_user_date; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_tasks_user_date ON public.tasks USING btree (user_id, task_date);


--
-- Name: idx_tasks_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_tasks_user_id ON public.tasks USING btree (user_id);


--
-- Name: idx_users_created_at; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_users_created_at ON public.users USING btree (created_at);


--
-- Name: idx_users_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_users_email ON public.users USING btree (email);


--
-- Name: ix_default_settings_category; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_default_settings_category ON public.default_settings USING btree (category);


--
-- Name: ix_sessions_session_type; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_sessions_session_type ON public.sessions USING btree (session_type);


--
-- Name: ix_users_base_address; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_base_address ON public.users_base USING btree (address);


--
-- Name: ix_users_base_dob; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_base_dob ON public.users_base USING btree (dob);


--
-- Name: ix_users_base_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_users_base_email ON public.users_base USING btree (email);


--
-- Name: ix_users_base_first_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_base_first_name ON public.users_base USING btree (first_name);


--
-- Name: ix_users_base_full_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_base_full_name ON public.users_base USING btree (full_name);


--
-- Name: ix_users_base_gender; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_base_gender ON public.users_base USING btree (gender);


--
-- Name: ix_users_base_identity_card; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_base_identity_card ON public.users_base USING btree (identity_card);


--
-- Name: ix_users_base_identity_card_date; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_base_identity_card_date ON public.users_base USING btree (identity_card_date);


--
-- Name: ix_users_base_identity_card_place; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_base_identity_card_place ON public.users_base USING btree (identity_card_place);


--
-- Name: ix_users_base_last_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_base_last_name ON public.users_base USING btree (last_name);


--
-- Name: ix_users_base_phone; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_base_phone ON public.users_base USING btree (phone);


--
-- Name: ix_users_base_sso_sub; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_users_base_sso_sub ON public.users_base USING btree (sso_sub);


--
-- Name: ix_users_base_username; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_users_base_username ON public.users_base USING btree (username);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: goals goals_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.goals
    ADD CONSTRAINT goals_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: session_pauses session_pauses_session_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.session_pauses
    ADD CONSTRAINT session_pauses_session_id_fkey FOREIGN KEY (session_id) REFERENCES public.sessions(session_id) ON DELETE CASCADE;


--
-- Name: sessions sessions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: statistics_cache statistics_cache_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.statistics_cache
    ADD CONSTRAINT statistics_cache_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: streak_records streak_records_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.streak_records
    ADD CONSTRAINT streak_records_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: task_sessions task_sessions_session_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_sessions
    ADD CONSTRAINT task_sessions_session_id_fkey FOREIGN KEY (session_id) REFERENCES public.sessions(session_id) ON DELETE CASCADE;


--
-- Name: task_sessions task_sessions_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_sessions
    ADD CONSTRAINT task_sessions_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.tasks(task_id) ON DELETE CASCADE;


--
-- Name: tasks tasks_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: user_settings user_settings_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_settings
    ADD CONSTRAINT user_settings_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict eoTGlatzIu14JXhCvvEcF68eaM14PAdD9PQG0zSb29pr5CtGPjYgzwk8kh6Kp6y


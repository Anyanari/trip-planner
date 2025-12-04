-- Схема БД
-- Trip Planner Database Schema
-- Автор: Эрфурт Анна

-- ============================================
-- 1. СОЗДАНИЕ ТАБЛИЦ (если их нет)
-- ============================================

BEGIN;


CREATE TABLE IF NOT EXISTS public.expense_shares
(
    id serial NOT NULL,
    expense_id integer NOT NULL,
    user_id integer NOT NULL,
    share numeric(3, 2) NOT NULL,
    CONSTRAINT expense_shares_pkey PRIMARY KEY (id),
    CONSTRAINT expense_shares_expense_id_user_id_key UNIQUE (expense_id, user_id)
);

CREATE TABLE IF NOT EXISTS public.expenses
(
    id serial NOT NULL,
    trip_id integer NOT NULL,
    title character varying(255) COLLATE pg_catalog."default" NOT NULL,
    amount numeric(10, 2) NOT NULL,
    currency character varying(3) COLLATE pg_catalog."default" DEFAULT 'RUB'::character varying,
    paid_by integer NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT expenses_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.places
(
    id serial NOT NULL,
    name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    lat numeric(10, 8) NOT NULL,
    lng numeric(11, 8) NOT NULL,
    osm_id character varying(255) COLLATE pg_catalog."default",
    address text COLLATE pg_catalog."default",
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT places_pkey PRIMARY KEY (id),
    CONSTRAINT places_osm_id_key UNIQUE (osm_id)
);

CREATE TABLE IF NOT EXISTS public.routes
(
    id serial NOT NULL,
    trip_id integer NOT NULL,
    place_id integer NOT NULL,
    day_number integer NOT NULL,
    order_in_day integer NOT NULL,
    planned_time time without time zone,
    estimated_cost numeric(10, 2),
    notes text COLLATE pg_catalog."default",
    added_by integer,
    added_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT routes_pkey PRIMARY KEY (id),
    CONSTRAINT routes_trip_id_day_number_order_in_day_key UNIQUE (trip_id, day_number, order_in_day),
    CONSTRAINT routes_trip_id_place_id_key UNIQUE (trip_id, place_id)
);

CREATE TABLE IF NOT EXISTS public.suggestions
(
    id serial NOT NULL,
    trip_id integer NOT NULL,
    place_id integer NOT NULL,
    suggested_by integer NOT NULL,
    suggested_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    status character varying(20) COLLATE pg_catalog."default" DEFAULT 'voting'::character varying,
    votes_for integer DEFAULT 0,
    votes_against integer DEFAULT 0,
    CONSTRAINT suggestions_pkey PRIMARY KEY (id),
    CONSTRAINT suggestions_trip_id_place_id_key UNIQUE (trip_id, place_id)
);

CREATE TABLE IF NOT EXISTS public.trip_members
(
    id serial NOT NULL,
    trip_id integer NOT NULL,
    user_id integer NOT NULL,
    joined_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    role character varying(20) COLLATE pg_catalog."default" DEFAULT 'member'::character varying,
    CONSTRAINT trip_members_pkey PRIMARY KEY (id),
    CONSTRAINT trip_members_trip_id_user_id_key UNIQUE (trip_id, user_id)
);

CREATE TABLE IF NOT EXISTS public.trips
(
    id serial NOT NULL,
    title character varying(200) COLLATE pg_catalog."default" NOT NULL,
    description text COLLATE pg_catalog."default",
    start_date date NOT NULL,
    end_date date NOT NULL,
    admin integer,
    created_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    is_active boolean DEFAULT true,
    CONSTRAINT trips_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.users
(
    id serial NOT NULL,
    email character varying(255) COLLATE pg_catalog."default" NOT NULL,
    username character varying(100) COLLATE pg_catalog."default" NOT NULL,
    created_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT users_pkey PRIMARY KEY (id),
    CONSTRAINT users_email_key UNIQUE (email),
    CONSTRAINT users_username_key UNIQUE (username)
);

CREATE TABLE IF NOT EXISTS public.votes
(
    id serial NOT NULL,
    suggestion_id integer NOT NULL,
    user_id integer NOT NULL,
    vote boolean NOT NULL,
    voted_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT votes_pkey PRIMARY KEY (id),
    CONSTRAINT votes_suggestion_id_user_id_key UNIQUE (suggestion_id, user_id)
);

ALTER TABLE IF EXISTS public.expense_shares
    ADD CONSTRAINT expense_shares_expense_id_fkey FOREIGN KEY (expense_id)
    REFERENCES public.expenses (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS public.expense_shares
    ADD CONSTRAINT expense_shares_user_id_fkey FOREIGN KEY (user_id)
    REFERENCES public.users (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS public.expenses
    ADD CONSTRAINT expenses_paid_by_fkey FOREIGN KEY (paid_by)
    REFERENCES public.users (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS public.expenses
    ADD CONSTRAINT expenses_trip_id_fkey FOREIGN KEY (trip_id)
    REFERENCES public.trips (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS public.routes
    ADD CONSTRAINT routes_added_by_fkey FOREIGN KEY (added_by)
    REFERENCES public.users (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.routes
    ADD CONSTRAINT routes_place_id_fkey FOREIGN KEY (place_id)
    REFERENCES public.places (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS public.routes
    ADD CONSTRAINT routes_trip_id_fkey FOREIGN KEY (trip_id)
    REFERENCES public.trips (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS public.suggestions
    ADD CONSTRAINT suggestions_place_id_fkey FOREIGN KEY (place_id)
    REFERENCES public.places (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS public.suggestions
    ADD CONSTRAINT suggestions_suggested_by_fkey FOREIGN KEY (suggested_by)
    REFERENCES public.users (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS public.suggestions
    ADD CONSTRAINT suggestions_trip_id_fkey FOREIGN KEY (trip_id)
    REFERENCES public.trips (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS public.trip_members
    ADD CONSTRAINT trip_members_trip_id_fkey FOREIGN KEY (trip_id)
    REFERENCES public.trips (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS public.trip_members
    ADD CONSTRAINT trip_members_user_id_fkey FOREIGN KEY (user_id)
    REFERENCES public.users (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS public.trips
    ADD CONSTRAINT trips_admin_fkey FOREIGN KEY (admin)
    REFERENCES public.users (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.votes
    ADD CONSTRAINT votes_suggestion_id_fkey FOREIGN KEY (suggestion_id)
    REFERENCES public.suggestions (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;


ALTER TABLE IF EXISTS public.votes
    ADD CONSTRAINT votes_user_id_fkey FOREIGN KEY (user_id)
    REFERENCES public.users (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE;

END;

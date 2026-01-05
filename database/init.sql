-- Схема БД
-- Trip Planner Database Schema

-- ============================================
-- 1. СОЗДАНИЕ ТАБЛИЦ
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


-- ============================================
-- 2. ТРИГГЕРЫ
-- ============================================

CREATE OR REPLACE FUNCTION public.check_expense_shares_sum()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF
AS $BODY$
DECLARE
    total_shares DECIMAL;
BEGIN
    SELECT SUM(share) INTO total_shares
    FROM expense_shares
    WHERE expense_id = NEW.expense_id;
    
    IF total_shares != 1.00 THEN
        RAISE EXCEPTION 'Sum of all shares must equal 1.0, current sum: %', total_shares;
    END IF;
    
    RETURN NULL;
END;
$BODY$;

ALTER FUNCTION public.check_expense_shares_sum()
    OWNER TO postgres;

CREATE CONSTRAINT TRIGGER check_expense_shares_sum_trigger
    AFTER INSERT OR UPDATE
    ON public.expense_shares
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW
    EXECUTE FUNCTION public.check_expense_shares_sum();

CREATE OR REPLACE FUNCTION public.check_place_accepted()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF
AS $BODY$
DECLARE
    suggestion_status VARCHAR(20);
BEGIN
    SELECT status INTO suggestion_status
    FROM suggestions
    WHERE trip_id = NEW.trip_id AND place_id = NEW.place_id;
    
    IF suggestion_status != 'accepted' THEN
        RAISE EXCEPTION 'Place must be accepted in suggestions before adding to route';
    END IF;
    
    RETURN NEW;
END;
$BODY$;

ALTER FUNCTION public.check_place_accepted()
    OWNER TO postgres;

CREATE OR REPLACE TRIGGER check_place_accepted_trigger
    BEFORE INSERT
    ON public.routes
    FOR EACH ROW
    EXECUTE FUNCTION public.check_place_accepted();


CREATE OR REPLACE FUNCTION public.check_trip_dates()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF
AS $BODY$
BEGIN
    IF NEW.start_date > NEW.end_date THEN
        RAISE EXCEPTION 'Start date cannot be after end date';
    END IF;
    
    RETURN NEW;
END;
$BODY$;

ALTER FUNCTION public.check_trip_dates()
    OWNER TO postgres;

CREATE OR REPLACE TRIGGER check_trip_dates_trigger
    BEFORE INSERT OR UPDATE
    ON public.trips
    FOR EACH ROW
    EXECUTE FUNCTION public.check_trip_dates();

CREATE OR REPLACE FUNCTION public.update_vote_counters()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF
AS $BODY$
BEGIN
    IF TG_OP = 'INSERT' THEN
        IF NEW.vote = TRUE THEN
            UPDATE suggestions
            SET votes_for = votes_for + 1
            WHERE id = NEW.suggestion_id;
        ELSE
            UPDATE suggestions
            SET votes_against = votes_against + 1
            WHERE id = NEW.suggestion_id;
        END IF;
    ELSIF TG_OP = 'DELETE' THEN
        IF OLD.vote = TRUE THEN
            UPDATE suggestions
            SET votes_for = votes_for - 1
            WHERE id = OLD.suggestion_id;
        ELSE
            UPDATE suggestions
            SET votes_against = votes_against - 1
            WHERE id = OLD.suggestion_id;
        END IF;
    ELSIF TG_OP = 'UPDATE' THEN
        IF OLD.vote = TRUE THEN
            UPDATE suggestions
            SET votes_for = votes_for - 1
            WHERE id = OLD.suggestion_id;
        ELSE
            UPDATE suggestions
            SET votes_against = votes_against - 1
            WHERE id = OLD.suggestion_id;
        END IF;

        IF NEW.vote = TRUE THEN
            UPDATE suggestions
            SET votes_for = votes_for + 1
            WHERE id = NEW.suggestion_id;
        ELSE
            UPDATE suggestions
            SET votes_against = votes_against + 1
            WHERE id = NEW.suggestion_id;
        END IF;
    END IF;
    
    RETURN NULL;
END;
$BODY$;

ALTER FUNCTION public.update_vote_counters()
    OWNER TO postgres;


CREATE OR REPLACE TRIGGER update_vote_counters_trigger
    AFTER INSERT OR DELETE OR UPDATE
    ON public.votes
    FOR EACH ROW
    EXECUTE FUNCTION public.update_vote_counters();


CREATE OR REPLACE FUNCTION public.check_voter_is_member()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF
AS $BODY$
DECLARE
    is_member BOOLEAN;
BEGIN
    SELECT EXISTS(
        SELECT 1 FROM trip_members tm
        JOIN suggestions s ON tm.trip_id = s.trip_id
        WHERE s.id = NEW.suggestion_id
          AND tm.user_id = NEW.user_id
    ) INTO is_member;
    
    IF NOT is_member THEN
        RAISE EXCEPTION 'User % is not a member of this trip', NEW.user_id;
    END IF;
    
    RETURN NEW;
END;
$BODY$;

ALTER FUNCTION public.check_voter_is_member()
    OWNER TO postgres;

CREATE OR REPLACE TRIGGER check_voter_is_member_trigger
    BEFORE INSERT
    ON public.votes
    FOR EACH ROW
    EXECUTE FUNCTION public.check_voter_is_member();


-- ============================================
-- 3. ФУНКЦИИ
-- ============================================

CREATE OR REPLACE FUNCTION public.auto_close_votings(
	)
    RETURNS void
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
BEGIN
    UPDATE suggestions
    SET status = CASE
        WHEN votes_for > votes_against THEN 'accepted'
        ELSE 'rejected'
    END
    WHERE status = 'voting'
      AND suggested_at < CURRENT_TIMESTAMP - INTERVAL '7 days';
END;
$BODY$;

ALTER FUNCTION public.auto_close_votings()
    OWNER TO postgres;

CREATE OR REPLACE FUNCTION public.calculate_trip_balances(
	p_trip_id integer)
    RETURNS TABLE(debtor_id integer, debtor_name character varying, creditor_id integer, creditor_name character varying, amount numeric) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
BEGIN
    RETURN QUERY
    SELECT 
        es.user_id as debtor_id,
        du.username as debtor_name,
        e.paid_by as creditor_id,
        cu.username as creditor_name,
        SUM(e.amount * es.share) as amount
    FROM expenses e
    JOIN expense_shares es ON e.id = es.expense_id
    JOIN users du ON es.user_id = du.id
    JOIN users cu ON e.paid_by = cu.id
    WHERE e.trip_id = p_trip_id 
      AND es.user_id != e.paid_by
    GROUP BY es.user_id, du.username, e.paid_by, cu.username
    HAVING SUM(e.amount * es.share) > 0
    ORDER BY amount DESC;
END;
$BODY$;

ALTER FUNCTION public.calculate_trip_balances(integer)
    OWNER TO postgres;

CREATE OR REPLACE FUNCTION public.create_trip_with_admin(
	p_title character varying,
	p_description text,
	p_start_date date,
	p_end_date date,
	p_admin_id integer)
    RETURNS integer
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
DECLARE
    new_trip_id INT;
BEGIN
    -- ‘®§¤ Ґ¬ Ї®Ґ§¤Єг
    INSERT INTO trips (title, description, start_date, end_date, admin_id)
    VALUES (p_title, p_description, p_start_date, p_end_date, p_admin_id)
    RETURNING id INTO new_trip_id;
    
    -- „®Ў ў«пҐ¬ ®аЈ ­Ё§ в®а  Є Є гз бв­ЁЄ 
    INSERT INTO trip_members (trip_id, user_id, role)
    VALUES (new_trip_id, p_admin_id, 'admin');
    
    RETURN new_trip_id;
END;
$BODY$;

ALTER FUNCTION public.create_trip_with_admin(character varying, text, date, date, integer)
    OWNER TO postgres;

CREATE OR REPLACE FUNCTION public.get_or_create_place(
	p_name character varying,
	p_lat numeric,
	p_lng numeric,
	p_osm_id character varying,
	p_address text DEFAULT NULL::text)
    RETURNS integer
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
DECLARE
    place_id INT;
BEGIN
    SELECT id INTO place_id 
    FROM places 
    WHERE osm_id = p_osm_id;
   
    IF place_id IS NULL THEN
        INSERT INTO places (name, lat, lng, osm_id, address)
        VALUES (p_name, p_lat, p_lng, p_osm_id, p_address)
        RETURNING id INTO place_id;
    END IF;
    
    RETURN place_id;
END;
$BODY$;

ALTER FUNCTION public.get_or_create_place(character varying, numeric, numeric, character varying, text)
    OWNER TO postgres;

CREATE OR REPLACE FUNCTION public.vote_on_suggestion(
	p_suggestion_id integer,
	p_user_id integer,
	p_vote boolean)
    RETURNS boolean
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
AS $BODY$
BEGIN
    IF (SELECT status FROM suggestions WHERE id = p_suggestion_id) != 'voting' THEN
        RAISE EXCEPTION 'Voting is closed for this suggestion';
    END IF;
    
    INSERT INTO votes (suggestion_id, user_id, vote)
    VALUES (p_suggestion_id, p_user_id, p_vote)
    ON CONFLICT (suggestion_id, user_id) 
    DO UPDATE SET vote = p_vote, voted_time = CURRENT_TIMESTAMP;
    
    RETURN TRUE;
END;
$BODY$;

ALTER FUNCTION public.vote_on_suggestion(integer, integer, boolean)
    OWNER TO postgres;


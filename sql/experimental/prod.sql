PGDMP     /                     |            keys    13.2    13.2 �    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    51332    keys    DATABASE     h   CREATE DATABASE keys WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'English_United States.1252';
    DROP DATABASE keys;
                postgres    false                        3079    53145 	   tablefunc 	   EXTENSION     =   CREATE EXTENSION IF NOT EXISTS tablefunc WITH SCHEMA public;
    DROP EXTENSION tablefunc;
                   false            �           0    0    EXTENSION tablefunc    COMMENT     `   COMMENT ON EXTENSION tablefunc IS 'functions that manipulate whole tables, including crosstab';
                        false    2                       1255    53130    check_for_key()    FUNCTION     �  CREATE FUNCTION public.check_for_key() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
	record key_inventory%rowtype;
BEGIN  

SELECT * INTO record
	FROM key_inventory 
	WHERE (key_status_id = 2)   -- key_status = INVENTORY
	ORDER BY date_transferred ASC
	LIMIT 1;

IF EXISTS (
	SELECT
	FROM key_inventory 
	WHERE (key_status_id = 2)   -- key_status = INVENTORY
	ORDER BY date_transferred ASC
	LIMIT 1)
THEN
	-- update existing available key to be unavailable
	UPDATE key_inventory
	SET key_status_id = 7,    -- status = TRANSFERRED	
		date_transferred = NOW()
	WHERE request_id = record.request_id;
	
 	-- create new key record with reassigned key
 	INSERT INTO key_inventory (request_id, key_copy, access_code_id, key_status_id)
	VALUES (NEW.request_id, record.key_copy, record.access_code_id, 3);
	
	-- update key order status
	NEW.order_status_id := 3;  -- status = WAITING FOR DELIVERY
	
ELSE
	-- add key request to keyshop
	INSERT INTO keys_created (request_id, access_code_id)
	VALUES (NEW.request_id, NEW.access_code_id);

	-- update key_order status
	NEW.order_status_id := 2;  -- order_status = WAITING FOR FABRICATION
	
END IF;

-- insert record with parameters of NEW
RETURN NEW;

END;
$$;
 &   DROP FUNCTION public.check_for_key();
       public          postgres    false            �            1255    53125    insert_key_order()    FUNCTION     ?  CREATE FUNCTION public.insert_key_order() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
	IF (NEW.request_status_id <> OLD.request_status_id) AND (NEW.request_status_id = 2) THEN
		 INSERT INTO key_orders (request_id, access_code_id)
		 VALUES(OLD.request_id, OLD.access_code_id);
	END IF;

	RETURN NEW;
END;
$$;
 )   DROP FUNCTION public.insert_key_order();
       public          postgres    false            �            1255    53117    log_key_order()    FUNCTION     *  CREATE FUNCTION public.log_key_order() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
	IF (NEW.status_code <> OLD.status_code) AND (NEW.status_code = 2) THEN
		 INSERT INTO key_orders (request_id, access_code_id)
		 VALUES(OLD.request_id, OLD.access_code_id);
	END IF;

	RETURN NEW;
END;
$$;
 &   DROP FUNCTION public.log_key_order();
       public          postgres    false            �            1255    53144 h   pivotcode(character varying, character varying, character varying, character varying, character varying)    FUNCTION     j  CREATE FUNCTION public.pivotcode(tablename character varying, rowc character varying, colc character varying, cellc character varying, celldatatype character varying) RETURNS void
    LANGUAGE plpgsql
    AS $$
declare
    dynsql1 varchar;
    dynsql2 varchar;
    columnlist varchar;
begin
    -- 1. retrieve list of column names.
    dynsql1 = 'select string_agg(distinct '||colc||'||'' '||celldatatype||''','','' order by '||colc||'||'' '||celldatatype||''') from '||tablename||';';
    execute dynsql1 into columnlist;
    -- 2. set up the crosstab query
    dynsql2 = 'CREATE TEMPORARY TABLE temp_pivot AS select * from crosstab (''select '||rowc||','||colc||','||cellc||' from '||tablename||' group by 1,2 order by 1,2'',''select distinct '||colc||' from '||tablename||' order by 1'') as newtable ('||rowc||' varchar,'||columnlist||');';
    execute dynsql2;
end;
$$;
 �   DROP FUNCTION public.pivotcode(tablename character varying, rowc character varying, colc character varying, cellc character varying, celldatatype character varying);
       public          postgres    false            �            1255    53119    update_key_created()    FUNCTION     V  CREATE FUNCTION public.update_key_created() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
	IF (NEW.fabrication_status_id <> OLD.fabrication_status_id) AND (NEW.fabrication_status_id = 3)  THEN

		-- Insert new key record into key inventory
		 INSERT INTO key_inventory (request_id, access_code_id, key_copy, key_status_id)
		 VALUES(NEW.request_id, NEW.access_code_id, NEW.key_copy, 1);  -- key_status_id = ISSUED
	
		-- Updated key_order status  
		 UPDATE key_orders
		 SET order_status_id = 3  -- WAITING FOR DELIVERY
		 WHERE request_id = OLD.request_id;
	END IF;

	RETURN NEW;
END;
$$;
 +   DROP FUNCTION public.update_key_created();
       public          postgres    false            �            1255    53123    update_key_order()    FUNCTION     T  CREATE FUNCTION public.update_key_order() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
	IF (NEW.fabrication_status_id <> OLD.fabrication_status_id) AND (NEW.fabrication_status_id = 3)  THEN

		-- Insert new key record into key inventory
		 INSERT INTO key_inventory (request_id, access_code_id, key_copy, key_status_id)
		 VALUES(NEW.request_id, NEW.access_code_id, NEW.key_copy, 1);  -- key_status_id = ISSUED
	
		-- Updated key_order status  
		 UPDATE key_orders
		 SET order_status_id = 3  -- WAITING FOR DELIVERY
		 WHERE request_id = OLD.request_id;
	END IF;

	RETURN NEW;
END;
$$;
 )   DROP FUNCTION public.update_key_order();
       public          postgres    false            �            1255    53121    update_requests()    FUNCTION     	  CREATE FUNCTION public.update_requests() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
	IF NEW.order_status_id = 1 THEN   -- READY FOR PICKUP

		-- Updated request status  
		 UPDATE requests
		 SET  request_status_id = 5 -- KEY READY FOR PICKUP
		 WHERE request_id = OLD.request_id;
	END IF;

	IF NEW.order_status_id = 4 THEN   -- PICKUP COMPLETE

		-- Updated request status  
		 UPDATE requests
		 SET  request_status_id = 6 -- KEY ASSIGNED
		 WHERE request_id = OLD.request_id;
	END IF;

	RETURN NEW;
END;
$$;
 (   DROP FUNCTION public.update_requests();
       public          postgres    false            �            1259    52853 	   approvers    TABLE     �   CREATE TABLE public.approvers (
    approver_id integer NOT NULL,
    user_id integer,
    role_approved_by integer NOT NULL,
    date_approved timestamp without time zone DEFAULT now() NOT NULL,
    date_removed timestamp without time zone
);
    DROP TABLE public.approvers;
       public         heap    postgres    false            �            1259    52851 '   access_approvers_access_approver_id_seq    SEQUENCE     �   CREATE SEQUENCE public.access_approvers_access_approver_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 >   DROP SEQUENCE public.access_approvers_access_approver_id_seq;
       public          postgres    false    210            �           0    0 '   access_approvers_access_approver_id_seq    SEQUENCE OWNED BY     e   ALTER SEQUENCE public.access_approvers_access_approver_id_seq OWNED BY public.approvers.approver_id;
          public          postgres    false    209            �            1259    52953    access_codes    TABLE     �   CREATE TABLE public.access_codes (
    access_code_id integer NOT NULL,
    access_description character varying,
    created_by integer,
    authorized_by integer,
    created_on timestamp without time zone DEFAULT now() NOT NULL
);
     DROP TABLE public.access_codes;
       public         heap    postgres    false            �            1259    52951    access_codes_access_code_id_seq    SEQUENCE     �   CREATE SEQUENCE public.access_codes_access_code_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 6   DROP SEQUENCE public.access_codes_access_code_id_seq;
       public          postgres    false    218            �           0    0    access_codes_access_code_id_seq    SEQUENCE OWNED BY     c   ALTER SEQUENCE public.access_codes_access_code_id_seq OWNED BY public.access_codes.access_code_id;
          public          postgres    false    217            �            1259    53038    access_pairs    TABLE     z   CREATE TABLE public.access_pairs (
    access_code_id integer NOT NULL,
    space_number_id character varying NOT NULL
);
     DROP TABLE public.access_pairs;
       public         heap    postgres    false            �            1259    53181    approval_status    TABLE     w   CREATE TABLE public.approval_status (
    status_code integer NOT NULL,
    status_code_name character varying(128)
);
 #   DROP TABLE public.approval_status;
       public         heap    postgres    false            �            1259    52965    request_status    TABLE     �   CREATE TABLE public.request_status (
    request_status_id integer NOT NULL,
    request_status_name character varying NOT NULL
);
 "   DROP TABLE public.request_status;
       public         heap    postgres    false            �            1259    52963    approval_status_status_code_seq    SEQUENCE     �   CREATE SEQUENCE public.approval_status_status_code_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 6   DROP SEQUENCE public.approval_status_status_code_seq;
       public          postgres    false    220            �           0    0    approval_status_status_code_seq    SEQUENCE OWNED BY     h   ALTER SEQUENCE public.approval_status_status_code_seq OWNED BY public.request_status.request_status_id;
          public          postgres    false    219            �            1259    53179     approval_status_status_code_seq1    SEQUENCE     �   CREATE SEQUENCE public.approval_status_status_code_seq1
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 7   DROP SEQUENCE public.approval_status_status_code_seq1;
       public          postgres    false    238            �           0    0     approval_status_status_code_seq1    SEQUENCE OWNED BY     d   ALTER SEQUENCE public.approval_status_status_code_seq1 OWNED BY public.approval_status.status_code;
          public          postgres    false    237            �            1259    52868    authentication    TABLE     �   CREATE TABLE public.authentication (
    id integer NOT NULL,
    username character varying NOT NULL,
    password_hash character varying NOT NULL
);
 "   DROP TABLE public.authentication;
       public         heap    postgres    false            �            1259    52885 	   buildings    TABLE     �   CREATE TABLE public.buildings (
    building_number integer NOT NULL,
    building_name character varying NOT NULL,
    building_description character varying NOT NULL
);
    DROP TABLE public.buildings;
       public         heap    postgres    false            �            1259    53058    fabrication_status    TABLE     �   CREATE TABLE public.fabrication_status (
    fabrication_status_id integer NOT NULL,
    fabrication_status character varying NOT NULL
);
 &   DROP TABLE public.fabrication_status;
       public         heap    postgres    false            �            1259    53056 ,   fabrication_status_fabrication_status_id_seq    SEQUENCE     �   CREATE SEQUENCE public.fabrication_status_fabrication_status_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 C   DROP SEQUENCE public.fabrication_status_fabrication_status_id_seq;
       public          postgres    false    228            �           0    0 ,   fabrication_status_fabrication_status_id_seq    SEQUENCE OWNED BY     }   ALTER SEQUENCE public.fabrication_status_fabrication_status_id_seq OWNED BY public.fabrication_status.fabrication_status_id;
          public          postgres    false    227            �            1259    53098    key_inventory    TABLE       CREATE TABLE public.key_inventory (
    request_id integer NOT NULL,
    access_code_id integer,
    key_copy integer,
    key_status_id integer,
    date_transferred timestamp without time zone DEFAULT now() NOT NULL,
    date_returned timestamp without time zone
);
 !   DROP TABLE public.key_inventory;
       public         heap    postgres    false            �            1259    53018 
   key_orders    TABLE       CREATE TABLE public.key_orders (
    request_id integer NOT NULL,
    access_code_id integer,
    order_status_id integer,
    date_key_received date,
    date_key_handoff date,
    key_admin_user_id integer,
    key_pickup_user_id integer,
    hold_on_conditions boolean
);
    DROP TABLE public.key_orders;
       public         heap    postgres    false            �            1259    53087 
   key_status    TABLE     r   CREATE TABLE public.key_status (
    key_status_id integer NOT NULL,
    key_status character varying NOT NULL
);
    DROP TABLE public.key_status;
       public         heap    postgres    false            �            1259    53085    key_status_key_status_id_seq    SEQUENCE     �   CREATE SEQUENCE public.key_status_key_status_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 3   DROP SEQUENCE public.key_status_key_status_id_seq;
       public          postgres    false    231            �           0    0    key_status_key_status_id_seq    SEQUENCE OWNED BY     ]   ALTER SEQUENCE public.key_status_key_status_id_seq OWNED BY public.key_status.key_status_id;
          public          postgres    false    230            �            1259    53069    keys_created    TABLE     �   CREATE TABLE public.keys_created (
    request_id integer NOT NULL,
    access_code_id integer,
    key_copy integer,
    fabrication_status_id integer DEFAULT 1,
    key_maker_user_id integer,
    date_created date
);
     DROP TABLE public.keys_created;
       public         heap    postgres    false            �            1259    53007    order_status    TABLE     x   CREATE TABLE public.order_status (
    order_status_id integer NOT NULL,
    order_status character varying NOT NULL
);
     DROP TABLE public.order_status;
       public         heap    postgres    false            �            1259    53005     order_status_order_status_id_seq    SEQUENCE     �   CREATE SEQUENCE public.order_status_order_status_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 7   DROP SEQUENCE public.order_status_order_status_id_seq;
       public          postgres    false    224            �           0    0     order_status_order_status_id_seq    SEQUENCE OWNED BY     e   ALTER SEQUENCE public.order_status_order_status_id_seq OWNED BY public.order_status.order_status_id;
          public          postgres    false    223            �            1259    52978    requests    TABLE       CREATE TABLE public.requests (
    request_id integer NOT NULL,
    user_id integer,
    spaces_requested character varying,
    building_number integer,
    approver_id integer,
    access_code_id integer,
    request_status_id integer DEFAULT 1 NOT NULL,
    request_date timestamp without time zone DEFAULT now() NOT NULL,
    approved_date timestamp without time zone,
    approved boolean DEFAULT false,
    approval_comment character varying,
    rejection_comment character varying,
    space_owner_id integer
);
    DROP TABLE public.requests;
       public         heap    postgres    false            �            1259    52976    requests_request_id_seq    SEQUENCE     �   CREATE SEQUENCE public.requests_request_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.requests_request_id_seq;
       public          postgres    false    222            �           0    0    requests_request_id_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.requests_request_id_seq OWNED BY public.requests.request_id;
          public          postgres    false    221            �            1259    52817    roles    TABLE     f   CREATE TABLE public.roles (
    role_id integer NOT NULL,
    user_role character varying NOT NULL
);
    DROP TABLE public.roles;
       public         heap    postgres    false            �            1259    52815    roles_role_id_seq    SEQUENCE     �   CREATE SEQUENCE public.roles_role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.roles_role_id_seq;
       public          postgres    false    206            �           0    0    roles_role_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.roles_role_id_seq OWNED BY public.roles.role_id;
          public          postgres    false    205            �            1259    52938    room_amenities    TABLE     �   CREATE TABLE public.room_amenities (
    space_number_id character varying NOT NULL,
    room_projector boolean,
    room_seating integer
);
 "   DROP TABLE public.room_amenities;
       public         heap    postgres    false            �            1259    53223    room_assignment    TABLE     �   CREATE TABLE public.room_assignment (
    assignment_id integer NOT NULL,
    space_number_id character varying(128),
    user_id integer
);
 #   DROP TABLE public.room_assignment;
       public         heap    postgres    false            �            1259    53221    room_assignment_owner_id_seq    SEQUENCE     �   CREATE SEQUENCE public.room_assignment_owner_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 3   DROP SEQUENCE public.room_assignment_owner_id_seq;
       public          postgres    false    240            �           0    0    room_assignment_owner_id_seq    SEQUENCE OWNED BY     b   ALTER SEQUENCE public.room_assignment_owner_id_seq OWNED BY public.room_assignment.assignment_id;
          public          postgres    false    239            �            1259    52910    room_classification    TABLE     y   CREATE TABLE public.room_classification (
    room_type_id integer NOT NULL,
    room_type character varying NOT NULL
);
 '   DROP TABLE public.room_classification;
       public         heap    postgres    false            �            1259    52920    rooms    TABLE     �   CREATE TABLE public.rooms (
    space_number_id character varying NOT NULL,
    building_number integer,
    wing_number integer,
    floor_number integer,
    room_number integer,
    room_type_id integer
);
    DROP TABLE public.rooms;
       public         heap    postgres    false            �            1259    53140    temp_matrix    VIEW     �   CREATE VIEW public.temp_matrix AS
 SELECT (access_pairs.access_code_id)::text AS access_code_id,
    access_pairs.space_number_id,
    1 AS truth
   FROM public.access_pairs
  ORDER BY (access_pairs.access_code_id)::text, access_pairs.space_number_id;
    DROP VIEW public.temp_matrix;
       public          postgres    false    226    226            �            1259    52804    titles    TABLE     d   CREATE TABLE public.titles (
    title_id integer NOT NULL,
    title character varying NOT NULL
);
    DROP TABLE public.titles;
       public         heap    postgres    false            �            1259    52802    titles_title_id_seq    SEQUENCE     �   CREATE SEQUENCE public.titles_title_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.titles_title_id_seq;
       public          postgres    false    204            �           0    0    titles_title_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.titles_title_id_seq OWNED BY public.titles.title_id;
          public          postgres    false    203            �            1259    52830    users    TABLE     �   CREATE TABLE public.users (
    user_id integer NOT NULL,
    first_name character varying NOT NULL,
    last_name character varying NOT NULL,
    title_id integer,
    role_id integer,
    email character varying NOT NULL,
    sponsor_id integer
);
    DROP TABLE public.users;
       public         heap    postgres    false            �            1259    52828    users_user_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.users_user_id_seq;
       public          postgres    false    208            �           0    0    users_user_id_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;
          public          postgres    false    207            �            1259    52895    zones    TABLE     f   CREATE TABLE public.zones (
    building_number integer NOT NULL,
    approver_id integer NOT NULL
);
    DROP TABLE public.zones;
       public         heap    postgres    false            �           2604    52956    access_codes access_code_id    DEFAULT     �   ALTER TABLE ONLY public.access_codes ALTER COLUMN access_code_id SET DEFAULT nextval('public.access_codes_access_code_id_seq'::regclass);
 J   ALTER TABLE public.access_codes ALTER COLUMN access_code_id DROP DEFAULT;
       public          postgres    false    217    218    218            �           2604    53184    approval_status status_code    DEFAULT     �   ALTER TABLE ONLY public.approval_status ALTER COLUMN status_code SET DEFAULT nextval('public.approval_status_status_code_seq1'::regclass);
 J   ALTER TABLE public.approval_status ALTER COLUMN status_code DROP DEFAULT;
       public          postgres    false    237    238    238            �           2604    52856    approvers approver_id    DEFAULT     �   ALTER TABLE ONLY public.approvers ALTER COLUMN approver_id SET DEFAULT nextval('public.access_approvers_access_approver_id_seq'::regclass);
 D   ALTER TABLE public.approvers ALTER COLUMN approver_id DROP DEFAULT;
       public          postgres    false    209    210    210            �           2604    53061 (   fabrication_status fabrication_status_id    DEFAULT     �   ALTER TABLE ONLY public.fabrication_status ALTER COLUMN fabrication_status_id SET DEFAULT nextval('public.fabrication_status_fabrication_status_id_seq'::regclass);
 W   ALTER TABLE public.fabrication_status ALTER COLUMN fabrication_status_id DROP DEFAULT;
       public          postgres    false    228    227    228            �           2604    53090    key_status key_status_id    DEFAULT     �   ALTER TABLE ONLY public.key_status ALTER COLUMN key_status_id SET DEFAULT nextval('public.key_status_key_status_id_seq'::regclass);
 G   ALTER TABLE public.key_status ALTER COLUMN key_status_id DROP DEFAULT;
       public          postgres    false    230    231    231            �           2604    53010    order_status order_status_id    DEFAULT     �   ALTER TABLE ONLY public.order_status ALTER COLUMN order_status_id SET DEFAULT nextval('public.order_status_order_status_id_seq'::regclass);
 K   ALTER TABLE public.order_status ALTER COLUMN order_status_id DROP DEFAULT;
       public          postgres    false    223    224    224            �           2604    52968     request_status request_status_id    DEFAULT     �   ALTER TABLE ONLY public.request_status ALTER COLUMN request_status_id SET DEFAULT nextval('public.approval_status_status_code_seq'::regclass);
 O   ALTER TABLE public.request_status ALTER COLUMN request_status_id DROP DEFAULT;
       public          postgres    false    219    220    220            �           2604    52981    requests request_id    DEFAULT     z   ALTER TABLE ONLY public.requests ALTER COLUMN request_id SET DEFAULT nextval('public.requests_request_id_seq'::regclass);
 B   ALTER TABLE public.requests ALTER COLUMN request_id DROP DEFAULT;
       public          postgres    false    222    221    222            �           2604    52820    roles role_id    DEFAULT     n   ALTER TABLE ONLY public.roles ALTER COLUMN role_id SET DEFAULT nextval('public.roles_role_id_seq'::regclass);
 <   ALTER TABLE public.roles ALTER COLUMN role_id DROP DEFAULT;
       public          postgres    false    206    205    206            �           2604    53226    room_assignment assignment_id    DEFAULT     �   ALTER TABLE ONLY public.room_assignment ALTER COLUMN assignment_id SET DEFAULT nextval('public.room_assignment_owner_id_seq'::regclass);
 L   ALTER TABLE public.room_assignment ALTER COLUMN assignment_id DROP DEFAULT;
       public          postgres    false    239    240    240            �           2604    52807    titles title_id    DEFAULT     r   ALTER TABLE ONLY public.titles ALTER COLUMN title_id SET DEFAULT nextval('public.titles_title_id_seq'::regclass);
 >   ALTER TABLE public.titles ALTER COLUMN title_id DROP DEFAULT;
       public          postgres    false    203    204    204            �           2604    52833    users user_id    DEFAULT     n   ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);
 <   ALTER TABLE public.users ALTER COLUMN user_id DROP DEFAULT;
       public          postgres    false    208    207    208            �          0    52953    access_codes 
   TABLE DATA           q   COPY public.access_codes (access_code_id, access_description, created_by, authorized_by, created_on) FROM stdin;
    public          postgres    false    218   �       �          0    53038    access_pairs 
   TABLE DATA           G   COPY public.access_pairs (access_code_id, space_number_id) FROM stdin;
    public          postgres    false    226   ��       �          0    53181    approval_status 
   TABLE DATA           H   COPY public.approval_status (status_code, status_code_name) FROM stdin;
    public          postgres    false    238   ��       �          0    52853 	   approvers 
   TABLE DATA           h   COPY public.approvers (approver_id, user_id, role_approved_by, date_approved, date_removed) FROM stdin;
    public          postgres    false    210   ��       �          0    52868    authentication 
   TABLE DATA           E   COPY public.authentication (id, username, password_hash) FROM stdin;
    public          postgres    false    211   6�       �          0    52885 	   buildings 
   TABLE DATA           Y   COPY public.buildings (building_number, building_name, building_description) FROM stdin;
    public          postgres    false    212   �       �          0    53058    fabrication_status 
   TABLE DATA           W   COPY public.fabrication_status (fabrication_status_id, fabrication_status) FROM stdin;
    public          postgres    false    228   G�       �          0    53098    key_inventory 
   TABLE DATA           }   COPY public.key_inventory (request_id, access_code_id, key_copy, key_status_id, date_transferred, date_returned) FROM stdin;
    public          postgres    false    232   ��       �          0    53018 
   key_orders 
   TABLE DATA           �   COPY public.key_orders (request_id, access_code_id, order_status_id, date_key_received, date_key_handoff, key_admin_user_id, key_pickup_user_id, hold_on_conditions) FROM stdin;
    public          postgres    false    225   ��       �          0    53087 
   key_status 
   TABLE DATA           ?   COPY public.key_status (key_status_id, key_status) FROM stdin;
    public          postgres    false    231   ��       �          0    53069    keys_created 
   TABLE DATA           �   COPY public.keys_created (request_id, access_code_id, key_copy, fabrication_status_id, key_maker_user_id, date_created) FROM stdin;
    public          postgres    false    229   !�       �          0    53007    order_status 
   TABLE DATA           E   COPY public.order_status (order_status_id, order_status) FROM stdin;
    public          postgres    false    224   i�       �          0    52965    request_status 
   TABLE DATA           P   COPY public.request_status (request_status_id, request_status_name) FROM stdin;
    public          postgres    false    220   ��       �          0    52978    requests 
   TABLE DATA           �   COPY public.requests (request_id, user_id, spaces_requested, building_number, approver_id, access_code_id, request_status_id, request_date, approved_date, approved, approval_comment, rejection_comment, space_owner_id) FROM stdin;
    public          postgres    false    222   e�       �          0    52817    roles 
   TABLE DATA           3   COPY public.roles (role_id, user_role) FROM stdin;
    public          postgres    false    206   ��       �          0    52938    room_amenities 
   TABLE DATA           W   COPY public.room_amenities (space_number_id, room_projector, room_seating) FROM stdin;
    public          postgres    false    216   �       �          0    53223    room_assignment 
   TABLE DATA           R   COPY public.room_assignment (assignment_id, space_number_id, user_id) FROM stdin;
    public          postgres    false    240   P�       �          0    52910    room_classification 
   TABLE DATA           F   COPY public.room_classification (room_type_id, room_type) FROM stdin;
    public          postgres    false    214   ��       �          0    52920    rooms 
   TABLE DATA           w   COPY public.rooms (space_number_id, building_number, wing_number, floor_number, room_number, room_type_id) FROM stdin;
    public          postgres    false    215   ��       �          0    52804    titles 
   TABLE DATA           1   COPY public.titles (title_id, title) FROM stdin;
    public          postgres    false    204   9�       �          0    52830    users 
   TABLE DATA           e   COPY public.users (user_id, first_name, last_name, title_id, role_id, email, sponsor_id) FROM stdin;
    public          postgres    false    208   ��       �          0    52895    zones 
   TABLE DATA           =   COPY public.zones (building_number, approver_id) FROM stdin;
    public          postgres    false    213   U�       �           0    0 '   access_approvers_access_approver_id_seq    SEQUENCE SET     U   SELECT pg_catalog.setval('public.access_approvers_access_approver_id_seq', 2, true);
          public          postgres    false    209            �           0    0    access_codes_access_code_id_seq    SEQUENCE SET     M   SELECT pg_catalog.setval('public.access_codes_access_code_id_seq', 6, true);
          public          postgres    false    217            �           0    0    approval_status_status_code_seq    SEQUENCE SET     N   SELECT pg_catalog.setval('public.approval_status_status_code_seq', 1, false);
          public          postgres    false    219            �           0    0     approval_status_status_code_seq1    SEQUENCE SET     O   SELECT pg_catalog.setval('public.approval_status_status_code_seq1', 1, false);
          public          postgres    false    237            �           0    0 ,   fabrication_status_fabrication_status_id_seq    SEQUENCE SET     [   SELECT pg_catalog.setval('public.fabrication_status_fabrication_status_id_seq', 1, false);
          public          postgres    false    227            �           0    0    key_status_key_status_id_seq    SEQUENCE SET     K   SELECT pg_catalog.setval('public.key_status_key_status_id_seq', 1, false);
          public          postgres    false    230            �           0    0     order_status_order_status_id_seq    SEQUENCE SET     O   SELECT pg_catalog.setval('public.order_status_order_status_id_seq', 1, false);
          public          postgres    false    223            �           0    0    requests_request_id_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.requests_request_id_seq', 173, true);
          public          postgres    false    221            �           0    0    roles_role_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.roles_role_id_seq', 1, false);
          public          postgres    false    205            �           0    0    room_assignment_owner_id_seq    SEQUENCE SET     J   SELECT pg_catalog.setval('public.room_assignment_owner_id_seq', 5, true);
          public          postgres    false    239            �           0    0    titles_title_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.titles_title_id_seq', 1, false);
          public          postgres    false    203            �           0    0    users_user_id_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.users_user_id_seq', 1, false);
          public          postgres    false    207            �           2606    52862    approvers access_approvers_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.approvers
    ADD CONSTRAINT access_approvers_pkey PRIMARY KEY (approver_id);
 I   ALTER TABLE ONLY public.approvers DROP CONSTRAINT access_approvers_pkey;
       public            postgres    false    210            �           2606    52962    access_codes access_codes_pkey 
   CONSTRAINT     h   ALTER TABLE ONLY public.access_codes
    ADD CONSTRAINT access_codes_pkey PRIMARY KEY (access_code_id);
 H   ALTER TABLE ONLY public.access_codes DROP CONSTRAINT access_codes_pkey;
       public            postgres    false    218                       2606    53045    access_pairs access_pairs_pkey 
   CONSTRAINT     y   ALTER TABLE ONLY public.access_pairs
    ADD CONSTRAINT access_pairs_pkey PRIMARY KEY (access_code_id, space_number_id);
 H   ALTER TABLE ONLY public.access_pairs DROP CONSTRAINT access_pairs_pkey;
       public            postgres    false    226    226            �           2606    52973 #   request_status approval_status_pkey 
   CONSTRAINT     p   ALTER TABLE ONLY public.request_status
    ADD CONSTRAINT approval_status_pkey PRIMARY KEY (request_status_id);
 M   ALTER TABLE ONLY public.request_status DROP CONSTRAINT approval_status_pkey;
       public            postgres    false    220                       2606    53186 %   approval_status approval_status_pkey1 
   CONSTRAINT     l   ALTER TABLE ONLY public.approval_status
    ADD CONSTRAINT approval_status_pkey1 PRIMARY KEY (status_code);
 O   ALTER TABLE ONLY public.approval_status DROP CONSTRAINT approval_status_pkey1;
       public            postgres    false    238            �           2606    52975 3   request_status approval_status_status_code_name_key 
   CONSTRAINT     }   ALTER TABLE ONLY public.request_status
    ADD CONSTRAINT approval_status_status_code_name_key UNIQUE (request_status_name);
 ]   ALTER TABLE ONLY public.request_status DROP CONSTRAINT approval_status_status_code_name_key;
       public            postgres    false    220            �           2606    52899    zones approver_zones_pkey 
   CONSTRAINT     q   ALTER TABLE ONLY public.zones
    ADD CONSTRAINT approver_zones_pkey PRIMARY KEY (building_number, approver_id);
 C   ALTER TABLE ONLY public.zones DROP CONSTRAINT approver_zones_pkey;
       public            postgres    false    213    213            �           2606    52879 /   authentication authentication_password_hash_key 
   CONSTRAINT     s   ALTER TABLE ONLY public.authentication
    ADD CONSTRAINT authentication_password_hash_key UNIQUE (password_hash);
 Y   ALTER TABLE ONLY public.authentication DROP CONSTRAINT authentication_password_hash_key;
       public            postgres    false    211            �           2606    52875 "   authentication authentication_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.authentication
    ADD CONSTRAINT authentication_pkey PRIMARY KEY (id);
 L   ALTER TABLE ONLY public.authentication DROP CONSTRAINT authentication_pkey;
       public            postgres    false    211            �           2606    52877 *   authentication authentication_username_key 
   CONSTRAINT     i   ALTER TABLE ONLY public.authentication
    ADD CONSTRAINT authentication_username_key UNIQUE (username);
 T   ALTER TABLE ONLY public.authentication DROP CONSTRAINT authentication_username_key;
       public            postgres    false    211            �           2606    52894 %   buildings buildings_building_name_key 
   CONSTRAINT     i   ALTER TABLE ONLY public.buildings
    ADD CONSTRAINT buildings_building_name_key UNIQUE (building_name);
 O   ALTER TABLE ONLY public.buildings DROP CONSTRAINT buildings_building_name_key;
       public            postgres    false    212            �           2606    52892    buildings buildings_pkey 
   CONSTRAINT     c   ALTER TABLE ONLY public.buildings
    ADD CONSTRAINT buildings_pkey PRIMARY KEY (building_number);
 B   ALTER TABLE ONLY public.buildings DROP CONSTRAINT buildings_pkey;
       public            postgres    false    212                       2606    53068 <   fabrication_status fabrication_status_fabrication_status_key 
   CONSTRAINT     �   ALTER TABLE ONLY public.fabrication_status
    ADD CONSTRAINT fabrication_status_fabrication_status_key UNIQUE (fabrication_status);
 f   ALTER TABLE ONLY public.fabrication_status DROP CONSTRAINT fabrication_status_fabrication_status_key;
       public            postgres    false    228                       2606    53066 *   fabrication_status fabrication_status_pkey 
   CONSTRAINT     {   ALTER TABLE ONLY public.fabrication_status
    ADD CONSTRAINT fabrication_status_pkey PRIMARY KEY (fabrication_status_id);
 T   ALTER TABLE ONLY public.fabrication_status DROP CONSTRAINT fabrication_status_pkey;
       public            postgres    false    228                       2606    53105 7   key_inventory key_inventory_access_code_id_key_copy_key 
   CONSTRAINT     �   ALTER TABLE ONLY public.key_inventory
    ADD CONSTRAINT key_inventory_access_code_id_key_copy_key UNIQUE (access_code_id, key_copy);
 a   ALTER TABLE ONLY public.key_inventory DROP CONSTRAINT key_inventory_access_code_id_key_copy_key;
       public            postgres    false    232    232                       2606    53103     key_inventory key_inventory_pkey 
   CONSTRAINT     f   ALTER TABLE ONLY public.key_inventory
    ADD CONSTRAINT key_inventory_pkey PRIMARY KEY (request_id);
 J   ALTER TABLE ONLY public.key_inventory DROP CONSTRAINT key_inventory_pkey;
       public            postgres    false    232                       2606    53022    key_orders key_orders_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.key_orders
    ADD CONSTRAINT key_orders_pkey PRIMARY KEY (request_id);
 D   ALTER TABLE ONLY public.key_orders DROP CONSTRAINT key_orders_pkey;
       public            postgres    false    225                       2606    53097 $   key_status key_status_key_status_key 
   CONSTRAINT     e   ALTER TABLE ONLY public.key_status
    ADD CONSTRAINT key_status_key_status_key UNIQUE (key_status);
 N   ALTER TABLE ONLY public.key_status DROP CONSTRAINT key_status_key_status_key;
       public            postgres    false    231                       2606    53095    key_status key_status_pkey 
   CONSTRAINT     c   ALTER TABLE ONLY public.key_status
    ADD CONSTRAINT key_status_pkey PRIMARY KEY (key_status_id);
 D   ALTER TABLE ONLY public.key_status DROP CONSTRAINT key_status_pkey;
       public            postgres    false    231            
           2606    53074    keys_created keys_created_pkey 
   CONSTRAINT     d   ALTER TABLE ONLY public.keys_created
    ADD CONSTRAINT keys_created_pkey PRIMARY KEY (request_id);
 H   ALTER TABLE ONLY public.keys_created DROP CONSTRAINT keys_created_pkey;
       public            postgres    false    229            �           2606    53017 *   order_status order_status_order_status_key 
   CONSTRAINT     m   ALTER TABLE ONLY public.order_status
    ADD CONSTRAINT order_status_order_status_key UNIQUE (order_status);
 T   ALTER TABLE ONLY public.order_status DROP CONSTRAINT order_status_order_status_key;
       public            postgres    false    224                        2606    53015    order_status order_status_pkey 
   CONSTRAINT     i   ALTER TABLE ONLY public.order_status
    ADD CONSTRAINT order_status_pkey PRIMARY KEY (order_status_id);
 H   ALTER TABLE ONLY public.order_status DROP CONSTRAINT order_status_pkey;
       public            postgres    false    224            �           2606    52989    requests requests_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.requests
    ADD CONSTRAINT requests_pkey PRIMARY KEY (request_id);
 @   ALTER TABLE ONLY public.requests DROP CONSTRAINT requests_pkey;
       public            postgres    false    222            �           2606    52825    roles roles_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (role_id);
 :   ALTER TABLE ONLY public.roles DROP CONSTRAINT roles_pkey;
       public            postgres    false    206            �           2606    52827    roles roles_user_role_key 
   CONSTRAINT     Y   ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_user_role_key UNIQUE (user_role);
 C   ALTER TABLE ONLY public.roles DROP CONSTRAINT roles_user_role_key;
       public            postgres    false    206            �           2606    52945 "   room_amenities room_amenities_pkey 
   CONSTRAINT     m   ALTER TABLE ONLY public.room_amenities
    ADD CONSTRAINT room_amenities_pkey PRIMARY KEY (space_number_id);
 L   ALTER TABLE ONLY public.room_amenities DROP CONSTRAINT room_amenities_pkey;
       public            postgres    false    216                       2606    53228 $   room_assignment room_assignment_pkey 
   CONSTRAINT     m   ALTER TABLE ONLY public.room_assignment
    ADD CONSTRAINT room_assignment_pkey PRIMARY KEY (assignment_id);
 N   ALTER TABLE ONLY public.room_assignment DROP CONSTRAINT room_assignment_pkey;
       public            postgres    false    240            �           2606    52917 ,   room_classification room_classification_pkey 
   CONSTRAINT     t   ALTER TABLE ONLY public.room_classification
    ADD CONSTRAINT room_classification_pkey PRIMARY KEY (room_type_id);
 V   ALTER TABLE ONLY public.room_classification DROP CONSTRAINT room_classification_pkey;
       public            postgres    false    214            �           2606    52919 5   room_classification room_classification_room_type_key 
   CONSTRAINT     u   ALTER TABLE ONLY public.room_classification
    ADD CONSTRAINT room_classification_room_type_key UNIQUE (room_type);
 _   ALTER TABLE ONLY public.room_classification DROP CONSTRAINT room_classification_room_type_key;
       public            postgres    false    214            �           2606    52927    rooms rooms_pkey 
   CONSTRAINT     [   ALTER TABLE ONLY public.rooms
    ADD CONSTRAINT rooms_pkey PRIMARY KEY (space_number_id);
 :   ALTER TABLE ONLY public.rooms DROP CONSTRAINT rooms_pkey;
       public            postgres    false    215            �           2606    52812    titles titles_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.titles
    ADD CONSTRAINT titles_pkey PRIMARY KEY (title_id);
 <   ALTER TABLE ONLY public.titles DROP CONSTRAINT titles_pkey;
       public            postgres    false    204            �           2606    52814    titles titles_title_key 
   CONSTRAINT     S   ALTER TABLE ONLY public.titles
    ADD CONSTRAINT titles_title_key UNIQUE (title);
 A   ALTER TABLE ONLY public.titles DROP CONSTRAINT titles_title_key;
       public            postgres    false    204            �           2606    52840    users users_email_key 
   CONSTRAINT     Q   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);
 ?   ALTER TABLE ONLY public.users DROP CONSTRAINT users_email_key;
       public            postgres    false    208            �           2606    52838    users users_pkey 
   CONSTRAINT     S   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            postgres    false    208            .           2620    53131    key_orders check_key_status    TRIGGER     y   CREATE TRIGGER check_key_status BEFORE INSERT ON public.key_orders FOR EACH ROW EXECUTE FUNCTION public.check_for_key();
 4   DROP TRIGGER check_key_status ON public.key_orders;
       public          postgres    false    225    269            ,           2620    53127    requests create_key_order    TRIGGER     y   CREATE TRIGGER create_key_order AFTER UPDATE ON public.requests FOR EACH ROW EXECUTE FUNCTION public.insert_key_order();
 2   DROP TRIGGER create_key_order ON public.requests;
       public          postgres    false    252    222            /           2620    53128 $   keys_created update_key_order_status    TRIGGER     �   CREATE TRIGGER update_key_order_status AFTER UPDATE ON public.keys_created FOR EACH ROW EXECUTE FUNCTION public.update_key_order();
 =   DROP TRIGGER update_key_order_status ON public.keys_created;
       public          postgres    false    229    243            -           2620    53129     key_orders update_request_status    TRIGGER        CREATE TRIGGER update_request_status AFTER UPDATE ON public.key_orders FOR EACH ROW EXECUTE FUNCTION public.update_requests();
 9   DROP TRIGGER update_request_status ON public.key_orders;
       public          postgres    false    225    254                       2606    52863 +   approvers access_approvers_approver_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.approvers
    ADD CONSTRAINT access_approvers_approver_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);
 U   ALTER TABLE ONLY public.approvers DROP CONSTRAINT access_approvers_approver_id_fkey;
       public          postgres    false    208    210    3038            &           2606    53046 -   access_pairs access_pairs_access_code_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.access_pairs
    ADD CONSTRAINT access_pairs_access_code_id_fkey FOREIGN KEY (access_code_id) REFERENCES public.access_codes(access_code_id);
 W   ALTER TABLE ONLY public.access_pairs DROP CONSTRAINT access_pairs_access_code_id_fkey;
       public          postgres    false    218    3062    226            '           2606    53051 .   access_pairs access_pairs_space_number_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.access_pairs
    ADD CONSTRAINT access_pairs_space_number_id_fkey FOREIGN KEY (space_number_id) REFERENCES public.rooms(space_number_id);
 X   ALTER TABLE ONLY public.access_pairs DROP CONSTRAINT access_pairs_space_number_id_fkey;
       public          postgres    false    226    215    3058                       2606    52905 ,   zones approver_zones_access_approver_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.zones
    ADD CONSTRAINT approver_zones_access_approver_id_fkey FOREIGN KEY (approver_id) REFERENCES public.approvers(approver_id);
 V   ALTER TABLE ONLY public.zones DROP CONSTRAINT approver_zones_access_approver_id_fkey;
       public          postgres    false    213    3040    210                       2606    52900 )   zones approver_zones_building_number_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.zones
    ADD CONSTRAINT approver_zones_building_number_fkey FOREIGN KEY (building_number) REFERENCES public.buildings(building_number);
 S   ALTER TABLE ONLY public.zones DROP CONSTRAINT approver_zones_building_number_fkey;
       public          postgres    false    213    212    3050                       2606    52880 %   authentication authentication_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.authentication
    ADD CONSTRAINT authentication_id_fkey FOREIGN KEY (id) REFERENCES public.users(user_id);
 O   ALTER TABLE ONLY public.authentication DROP CONSTRAINT authentication_id_fkey;
       public          postgres    false    211    208    3038            +           2606    53111 .   key_inventory key_inventory_key_status_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.key_inventory
    ADD CONSTRAINT key_inventory_key_status_id_fkey FOREIGN KEY (key_status_id) REFERENCES public.key_status(key_status_id);
 X   ALTER TABLE ONLY public.key_inventory DROP CONSTRAINT key_inventory_key_status_id_fkey;
       public          postgres    false    231    3086    232            *           2606    53106 +   key_inventory key_inventory_request_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.key_inventory
    ADD CONSTRAINT key_inventory_request_id_fkey FOREIGN KEY (request_id) REFERENCES public.key_orders(request_id);
 U   ALTER TABLE ONLY public.key_inventory DROP CONSTRAINT key_inventory_request_id_fkey;
       public          postgres    false    225    3074    232            $           2606    53028 )   key_orders key_orders_access_code_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.key_orders
    ADD CONSTRAINT key_orders_access_code_id_fkey FOREIGN KEY (access_code_id) REFERENCES public.access_codes(access_code_id);
 S   ALTER TABLE ONLY public.key_orders DROP CONSTRAINT key_orders_access_code_id_fkey;
       public          postgres    false    218    3062    225            %           2606    53033 *   key_orders key_orders_order_status_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.key_orders
    ADD CONSTRAINT key_orders_order_status_id_fkey FOREIGN KEY (order_status_id) REFERENCES public.order_status(order_status_id);
 T   ALTER TABLE ONLY public.key_orders DROP CONSTRAINT key_orders_order_status_id_fkey;
       public          postgres    false    3072    225    224            #           2606    53023 %   key_orders key_orders_request_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.key_orders
    ADD CONSTRAINT key_orders_request_id_fkey FOREIGN KEY (request_id) REFERENCES public.requests(request_id);
 O   ALTER TABLE ONLY public.key_orders DROP CONSTRAINT key_orders_request_id_fkey;
       public          postgres    false    225    222    3068            (           2606    53075 -   keys_created keys_created_access_code_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.keys_created
    ADD CONSTRAINT keys_created_access_code_id_fkey FOREIGN KEY (access_code_id) REFERENCES public.access_codes(access_code_id);
 W   ALTER TABLE ONLY public.keys_created DROP CONSTRAINT keys_created_access_code_id_fkey;
       public          postgres    false    218    3062    229            )           2606    53080 4   keys_created keys_created_fabrication_status_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.keys_created
    ADD CONSTRAINT keys_created_fabrication_status_id_fkey FOREIGN KEY (fabrication_status_id) REFERENCES public.fabrication_status(fabrication_status_id);
 ^   ALTER TABLE ONLY public.keys_created DROP CONSTRAINT keys_created_fabrication_status_id_fkey;
       public          postgres    false    229    3080    228                        2606    52990 %   requests requests_access_code_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.requests
    ADD CONSTRAINT requests_access_code_id_fkey FOREIGN KEY (access_code_id) REFERENCES public.access_codes(access_code_id);
 O   ALTER TABLE ONLY public.requests DROP CONSTRAINT requests_access_code_id_fkey;
       public          postgres    false    3062    222    218            "           2606    53000 9   requests requests_building_number_access_approver_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.requests
    ADD CONSTRAINT requests_building_number_access_approver_id_fkey FOREIGN KEY (building_number, approver_id) REFERENCES public.zones(building_number, approver_id);
 c   ALTER TABLE ONLY public.requests DROP CONSTRAINT requests_building_number_access_approver_id_fkey;
       public          postgres    false    213    3052    222    213    222            !           2606    52995 "   requests requests_status_code_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.requests
    ADD CONSTRAINT requests_status_code_fkey FOREIGN KEY (request_status_id) REFERENCES public.request_status(request_status_id);
 L   ALTER TABLE ONLY public.requests DROP CONSTRAINT requests_status_code_fkey;
       public          postgres    false    222    3064    220                       2606    52946 2   room_amenities room_amenities_space_number_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.room_amenities
    ADD CONSTRAINT room_amenities_space_number_id_fkey FOREIGN KEY (space_number_id) REFERENCES public.rooms(space_number_id);
 \   ALTER TABLE ONLY public.room_amenities DROP CONSTRAINT room_amenities_space_number_id_fkey;
       public          postgres    false    216    215    3058                       2606    52928     rooms rooms_building_number_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.rooms
    ADD CONSTRAINT rooms_building_number_fkey FOREIGN KEY (building_number) REFERENCES public.buildings(building_number);
 J   ALTER TABLE ONLY public.rooms DROP CONSTRAINT rooms_building_number_fkey;
       public          postgres    false    215    3050    212                       2606    52933    rooms rooms_room_type_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.rooms
    ADD CONSTRAINT rooms_room_type_fkey FOREIGN KEY (room_type_id) REFERENCES public.room_classification(room_type_id);
 D   ALTER TABLE ONLY public.rooms DROP CONSTRAINT rooms_room_type_fkey;
       public          postgres    false    215    214    3054                       2606    52846    users users_role_id_fkey    FK CONSTRAINT     |   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(role_id);
 B   ALTER TABLE ONLY public.users DROP CONSTRAINT users_role_id_fkey;
       public          postgres    false    208    206    3032                       2606    52841    users users_title_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_title_id_fkey FOREIGN KEY (title_id) REFERENCES public.titles(title_id);
 C   ALTER TABLE ONLY public.users DROP CONSTRAINT users_title_id_fkey;
       public          postgres    false    204    208    3028            �   r   x�3�t�I,..����4B##c]CC]##C+c#+#C=3SKS.#N���Ҝ�J�����T�ļ���̒TB:�9݊��J ���r*	�0��:+3=/5%&���=... �z/o      �   '   x�3�t2210A.#0��m�e���I�1��=...       �      x������ � �      �   8   x�3�4�4�4202�54�52R04�26�22�33���0���2�4�4$�&F��� >�      �   �   x����N1 ��w\����7U
��xm�����_O������v������^��YX7%$Z�1Ο�vz�����|�>���&�b���� ��-���cf���D[�M�f���7{���l>������TG&� �J�
!�`PϽvb��4jɓ������c�ȩ���s���E9      �   5   x�32�t�H��,.)�D�\R�JrS�J�R�S��3��S�b���� 
�(      �   .   x�3���Suu�2�v�pu	�qu�2�t���q�c���� �x�      �      x������ � �      �      x������ � �      �   R   x���	�0 �s2E'�ޫM%T������s軿ؽS�	Xn����ѝO��Z�|�^q�ݴ��
�z��E�Lf�D� �!o      �   8   x�3�4�4�4B##c]CC]##. �9A�M��(��1~\1z\\\ �*      �   T   x�3�rut�Tp�R�t��2�w���s�9:y:;�x��q�ȸ��x��Er�p�t*�(8������r��qqq -��      �   �   x�]�;�@E�:^�W���a�@!$3��HY�/I"����M�x���k[�Ch�X�Y�{��B��t��=GE��0���-)�:6%�q�`V߻�:�]
/����S@�]fx&sڬ+�!�;@���=���hiX�9�0�      �   W   x�e̱�0C��n
 �}	'(�	�����n�<�����#S��HP�����ؐ���`4Y?�љ�����5K`净���'���      �   <   x�3�,J-,M-.I-�2�L,((�/2�9Sr3�2�K�K�L8�s*�K�b���� ���      �   (   x�s2210A�NS.' ��M�4��<�=... ڐk      �   0   x�3�t2210ANC.#0��3�2��<$�F\�P�X_� �'      �   I   x�320�,(�,K,IU�OK�LN�220�L��KK-J�KNU(����224�L�I,.���8�3�RS`zb���� ���      �   @   x�M��  Cѳc�8��ϡH0��J:�Hc4� �y�b�]�)>��(r�o$�b.�nf}|      �   {   x�e�KB1@�1��+0>���	
�$-5���{�c�'�w�i,^�xRH1Y,p���3 �c����S+���Ȩ��	X^���"=�ϫ����vO�MMG8�v���UCeಅ���x� ��,5A      �   �   x�]�;� �z8��)�� n ^�X����\�h�Ѽb^	�A�~mg���wܠ�%�B�� ���I�}J#�O��Ѣ���`�j��=
��g�ފ69{Ǵ�|+��{Us���n�Au      �      x�32�4����� mS     
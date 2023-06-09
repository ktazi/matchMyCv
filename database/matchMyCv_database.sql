PGDMP                           {           engineering_proj    15.2    15.2     %           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            &           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            '           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            (           1262    16396    engineering_proj    DATABASE     r   CREATE DATABASE engineering_proj WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'C';
     DROP DATABASE engineering_proj;
                postgres    false            �            1259    16398    announce    TABLE     �   CREATE TABLE public.announce (
    id_annonce integer NOT NULL,
    name_annonce text NOT NULL,
    pourc_ob integer NOT NULL,
    pourc_opt integer NOT NULL,
    pourc_pref integer NOT NULL,
    name_employer text DEFAULT ''::text
);
    DROP TABLE public.announce;
       public         heap    postgres    false            �            1259    16397    announce_id_annonce_seq    SEQUENCE     �   CREATE SEQUENCE public.announce_id_annonce_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.announce_id_annonce_seq;
       public          postgres    false    215            )           0    0    announce_id_annonce_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.announce_id_annonce_seq OWNED BY public.announce.id_annonce;
          public          postgres    false    214            �            1259    16416    cv    TABLE     �   CREATE TABLE public.cv (
    id_cv integer NOT NULL,
    parsed boolean DEFAULT false,
    cv_name text NOT NULL,
    id_annonce integer NOT NULL,
    score integer DEFAULT 0,
    score_suggere integer DEFAULT 0,
    is_note boolean DEFAULT false
);
    DROP TABLE public.cv;
       public         heap    postgres    false            �            1259    16415    cv_id_cv_seq    SEQUENCE     �   CREATE SEQUENCE public.cv_id_cv_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.cv_id_cv_seq;
       public          postgres    false    219            *           0    0    cv_id_cv_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.cv_id_cv_seq OWNED BY public.cv.id_cv;
          public          postgres    false    218            �            1259    16426    note    TABLE     �   CREATE TABLE public.note (
    id_cv integer NOT NULL,
    id_skill integer NOT NULL,
    id_annonce integer NOT NULL,
    checked boolean DEFAULT false NOT NULL
);
    DROP TABLE public.note;
       public         heap    postgres    false            �            1259    16407    skills    TABLE     �   CREATE TABLE public.skills (
    id_annonce integer NOT NULL,
    name_skill text NOT NULL,
    id_skill integer NOT NULL,
    type_opt boolean NOT NULL,
    type_ob boolean NOT NULL,
    type_pref boolean NOT NULL
);
    DROP TABLE public.skills;
       public         heap    postgres    false            �            1259    16406    skills_id_skill_seq    SEQUENCE     �   CREATE SEQUENCE public.skills_id_skill_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.skills_id_skill_seq;
       public          postgres    false    217            +           0    0    skills_id_skill_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.skills_id_skill_seq OWNED BY public.skills.id_skill;
          public          postgres    false    216            }           2604    16401    announce id_annonce    DEFAULT     z   ALTER TABLE ONLY public.announce ALTER COLUMN id_annonce SET DEFAULT nextval('public.announce_id_annonce_seq'::regclass);
 B   ALTER TABLE public.announce ALTER COLUMN id_annonce DROP DEFAULT;
       public          postgres    false    214    215    215            �           2604    16419    cv id_cv    DEFAULT     d   ALTER TABLE ONLY public.cv ALTER COLUMN id_cv SET DEFAULT nextval('public.cv_id_cv_seq'::regclass);
 7   ALTER TABLE public.cv ALTER COLUMN id_cv DROP DEFAULT;
       public          postgres    false    219    218    219                       2604    16410    skills id_skill    DEFAULT     r   ALTER TABLE ONLY public.skills ALTER COLUMN id_skill SET DEFAULT nextval('public.skills_id_skill_seq'::regclass);
 >   ALTER TABLE public.skills ALTER COLUMN id_skill DROP DEFAULT;
       public          postgres    false    217    216    217                      0    16398    announce 
   TABLE DATA           l   COPY public.announce (id_annonce, name_annonce, pourc_ob, pourc_opt, pourc_pref, name_employer) FROM stdin;
    public          postgres    false    215   ]       !          0    16416    cv 
   TABLE DATA           _   COPY public.cv (id_cv, parsed, cv_name, id_annonce, score, score_suggere, is_note) FROM stdin;
    public          postgres    false    219   z       "          0    16426    note 
   TABLE DATA           D   COPY public.note (id_cv, id_skill, id_annonce, checked) FROM stdin;
    public          postgres    false    220   �                 0    16407    skills 
   TABLE DATA           `   COPY public.skills (id_annonce, name_skill, id_skill, type_opt, type_ob, type_pref) FROM stdin;
    public          postgres    false    217   �       ,           0    0    announce_id_annonce_seq    SEQUENCE SET     F   SELECT pg_catalog.setval('public.announce_id_annonce_seq', 36, true);
          public          postgres    false    214            -           0    0    cv_id_cv_seq    SEQUENCE SET     <   SELECT pg_catalog.setval('public.cv_id_cv_seq', 370, true);
          public          postgres    false    218            .           0    0    skills_id_skill_seq    SEQUENCE SET     C   SELECT pg_catalog.setval('public.skills_id_skill_seq', 158, true);
          public          postgres    false    216            �           2606    16405    announce announce_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.announce
    ADD CONSTRAINT announce_pkey PRIMARY KEY (id_annonce);
 @   ALTER TABLE ONLY public.announce DROP CONSTRAINT announce_pkey;
       public            postgres    false    215            �           2606    16423 
   cv cv_pkey 
   CONSTRAINT     K   ALTER TABLE ONLY public.cv
    ADD CONSTRAINT cv_pkey PRIMARY KEY (id_cv);
 4   ALTER TABLE ONLY public.cv DROP CONSTRAINT cv_pkey;
       public            postgres    false    219            �           2606    16431    note note_pkey 
   CONSTRAINT     e   ALTER TABLE ONLY public.note
    ADD CONSTRAINT note_pkey PRIMARY KEY (id_cv, id_skill, id_annonce);
 8   ALTER TABLE ONLY public.note DROP CONSTRAINT note_pkey;
       public            postgres    false    220    220    220            �           2606    16414    skills skills_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.skills
    ADD CONSTRAINT skills_pkey PRIMARY KEY (id_skill);
 <   ALTER TABLE ONLY public.skills DROP CONSTRAINT skills_pkey;
       public            postgres    false    217                  x^����� � �      !      x^����� � �      "      x^����� � �            x^����� � �     
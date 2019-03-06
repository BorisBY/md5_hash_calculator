# md5_hash_calculator

Небольшой веб-сервис, позволяющий
посчитать MD5-хеш от файла, расположенного в сети Интернет.
Скачивание и расчет должны происходят в отдельном потоке.

Для работы данного проекта необходим установленный python3, 
БД Postgresql.
В Postgresql должна существовать роль "boston" с паролем "boston". 
Также в базе необходимо добавить таблицу maintables. 
Скрипт для добавления таблицы:

CREATE TABLE public.maintable
(
  id integer NOT NULL DEFAULT nextval('maintable_id_seq'::regclass),
  download character varying(100) NOT NULL,
  hash_sum character varying(100) NOT NULL,
  CONSTRAINT maintable_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.maintable
  OWNER TO boston;

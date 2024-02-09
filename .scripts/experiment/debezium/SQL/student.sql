SHOW wal_level;
--Requries restart
--ALTER SYSTEM SET wal_level = logical;

DROP table IF EXISTS public.student;

CREATE TABLE public.student (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	"name" varchar NOT NULL,
	updated timestamp NOT NULL,
	CONSTRAINT student_pk PRIMARY KEY (id)
);

alter table public.student replica identity full;

insert into public.student (name, updated) values ('Donald Trump', now());
insert into public.student (name, updated) values ('Song Li', now());

select id, name, updated from public.student;
drop table if exists public.simple_schema_table;

CREATE TABLE public.simple_schema_table (
	id int4 NOT NULL,
	data_entry varchar NULL,
	CONSTRAINT simple_schema_table_pk PRIMARY KEY (id)
);

-- upsert
-- for reference, keep the delete capability
create or replace procedure public.simple_schema_table_upsert(
	_id int,
	_data_entry varchar,
	_is_delete boolean default false
)
language plpgsql
as $$
begin
	IF _is_delete THEN
    	delete from public.simple_schema_table where id = _id;
	ELSE
	    insert into public.simple_schema_table values(_id, _data_entry) ON CONFLICT (id) 
		DO UPDATE SET data_entry = _data_entry;
	END IF;
end; $$;


-- delete
create or replace procedure public.simple_schema_table_delete(
	_id int
)
language plpgsql
as $$
begin
	delete from public.simple_schema_table where id = _id;
end; $$;

call public.simple_schema_table_upsert('1', 'Initial value');
call public.simple_schema_table_upsert('1', 'Initial value', 'true');
call public.simple_schema_table_delete('1');

select * from public.simple_schema_table;
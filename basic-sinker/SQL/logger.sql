DROP table IF EXISTS public.logger;

CREATE TABLE public.logger (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	message varchar NOT NULL,
	event_time timestamp NOT NULL,
	CONSTRAINT student_pk PRIMARY KEY (id)
);

create or replace procedure public.log_event(
	_message varchar
)
language plpgsql
SECURITY DEFINER
as $$
begin
	insert into public.logger(message, event_time) values(_message, now());
end; $$;

call public.log_event('Event no.1');
call public.log_event('Event no.2');

truncate table public.logger RESTART IDENTITY CASCADE;
select * from public.logger order by id desc;
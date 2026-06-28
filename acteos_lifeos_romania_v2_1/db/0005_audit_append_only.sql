-- 0005: enforce append-only audit events.
-- audit.events is the security/administrative audit ledger. Rows may be
-- inserted, but existing audit rows must not be updated or deleted.

create or replace function audit.prevent_audit_events_mutation()
returns trigger
language plpgsql
as $$
begin
    raise exception 'audit.events is append-only; attempted %% is not allowed', tg_op
        using errcode = 'check_violation';
end;
$$;

drop trigger if exists audit_events_append_only on audit.events;

create trigger audit_events_append_only
before update or delete on audit.events
for each row execute function audit.prevent_audit_events_mutation();

comment on trigger audit_events_append_only on audit.events is
    'Prevents UPDATE/DELETE on audit.events. Audit is append-only; corrections require a new audit row.';

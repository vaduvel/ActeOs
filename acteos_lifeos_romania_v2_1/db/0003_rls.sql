-- Reference RLS policies for Supabase. Adapt auth.uid() only if another issuer is used.
alter table app.profiles enable row level security;
alter table app.households enable row level security;
alter table app.household_members enable row level security;
alter table app.assets enable row level security;
alter table app.cases enable row level security;
alter table app.fact_values enable row level security;
alter table app.journeys enable row level security;
alter table app.journey_steps enable row level security;
alter table app.journey_requirements enable row level security;
alter table app.documents enable row level security;
alter table app.document_readiness_runs enable row level security;
alter table app.notification_preferences enable row level security;
alter table app.notifications enable row level security;
alter table app.feedback_reports enable row level security;

create policy profiles_self on app.profiles for all using (user_id = auth.uid()) with check (user_id = auth.uid());
create policy households_owner on app.households for all using (owner_user_id = auth.uid()) with check (owner_user_id = auth.uid());
create policy household_members_owner on app.household_members for all using (
 exists(select 1 from app.households h where h.id = household_id and h.owner_user_id = auth.uid() and h.deleted_at is null)
) with check (
 exists(select 1 from app.households h where h.id = household_id and h.owner_user_id = auth.uid() and h.deleted_at is null)
);
create policy assets_owner on app.assets for all using (owner_user_id = auth.uid()) with check (owner_user_id = auth.uid());
create policy cases_owner on app.cases for all using (user_id = auth.uid()) with check (user_id = auth.uid());
create policy facts_case_owner on app.fact_values for all using (
 exists(select 1 from app.cases c where c.id = case_id and c.user_id = auth.uid() and c.deleted_at is null)
) with check (
 exists(select 1 from app.cases c where c.id = case_id and c.user_id = auth.uid() and c.deleted_at is null)
);
create policy journeys_case_owner on app.journeys for select using (
 exists(select 1 from app.cases c where c.id = case_id and c.user_id = auth.uid() and c.deleted_at is null)
);
create policy steps_journey_owner on app.journey_steps for all using (
 exists(select 1 from app.journeys j join app.cases c on c.id=j.case_id where j.id=journey_id and c.user_id=auth.uid() and c.deleted_at is null)
) with check (
 exists(select 1 from app.journeys j join app.cases c on c.id=j.case_id where j.id=journey_id and c.user_id=auth.uid() and c.deleted_at is null)
);
create policy requirements_owner on app.journey_requirements for all using (
 exists(select 1 from app.journey_steps s join app.journeys j on j.id=s.journey_id join app.cases c on c.id=j.case_id where s.id=journey_step_id and c.user_id=auth.uid() and c.deleted_at is null)
) with check (
 exists(select 1 from app.journey_steps s join app.journeys j on j.id=s.journey_id join app.cases c on c.id=j.case_id where s.id=journey_step_id and c.user_id=auth.uid() and c.deleted_at is null)
);
create policy documents_owner on app.documents for all using (user_id = auth.uid()) with check (user_id = auth.uid());
create policy readiness_document_owner on app.document_readiness_runs for select using (
 exists(select 1 from app.documents d where d.id=document_id and d.user_id=auth.uid() and d.deleted_at is null)
);
create policy notification_prefs_owner on app.notification_preferences for all using (user_id=auth.uid()) with check (user_id=auth.uid());
create policy notifications_owner on app.notifications for select using (user_id=auth.uid());
create policy feedback_owner on app.feedback_reports for select using (user_id=auth.uid());

-- Content and audit schemas are not exposed directly to untrusted clients.
-- Service/API roles must enforce RBAC and separation of duties.

create table if not exists users (
  id uuid primary key default gen_random_uuid(),
  email text unique not null,
  name text not null,
  picture text,
  created_at timestamptz default now()
);

create table if not exists tasks (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  description text,
  status text not null default 'pending' check (status in ('pending', 'completed')),
  created_by uuid not null references users(id) on delete cascade,
  assigned_to uuid not null references users(id) on delete cascade,
  created_at timestamptz default now(),
  completed_at timestamptz
);
create index if not exists tasks_created_by_idx on tasks(created_by);
create index if not exists tasks_assigned_to_idx on tasks(assigned_to);

-- Only the Flask backend (service_role key) touches the data.
alter table users enable row level security;
alter table tasks enable row level security;

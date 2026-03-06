-- Supabase SQL script to create tables and indexes for clients and transactions
create table clients (
    id uuid primary key default gen_random_uuid(),

    client_name text not null,
    client_code text unique not null,

    created_at timestamptz default now(),
    updated_at timestamptz default now(),

    created_by text,
    updated_by text
);


create table transactions (
    transaction_uuid uuid primary key default gen_random_uuid(),

    client_id uuid not null references clients(id) on delete cascade,

    transaction_amount numeric(12,2) not null,

    created_at timestamptz default now(),
    updated_at timestamptz default now(),

    created_by text,
    updated_by text
);

-- Indexes for transactions table
create index idx_transactions_date 
on transactions(created_at);



create index idx_transactions_client 
on transactions(client_id);


create index idx_transactions_client_date
on transactions(client_id, created_at);
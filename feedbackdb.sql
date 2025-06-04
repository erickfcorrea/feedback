CREATE DATABASE feedbackdb;
create table feedback (
id serial primary key,
nome text not null,
mensagem text not null
)
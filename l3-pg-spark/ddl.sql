create schema stackoverflow_filtered;

create table stackoverflow_filtered."results" (
);


set search_path to stackoverflow_filtered;

-- Create a btree index on the reputation column within the results table.
CREATE UNIQUE INDEX reputation_idx ON results (reputation);
--CREATE INDEX reputation_idx ON results USING btree (display_name);


-- Create a hash index on the display_name column within the results table.
CREATE INDEX display_name_idx ON results USING hash (display_name);


-- From the results table, create a view with the column names display_name, city, questions_id 
-- where the accepted_answer_id is not null. Make sure this view goes into the right schema.
CREATE VIEW results_view AS
    SELECT display_name, city, questions_id
    FROM results
    WHERE accepted_answer_id is not null;


-- Create a materialized view similar to (6). They should have different names.
CREATE MATERIALIZED VIEW results_view_mat AS
    SELECT display_name, city, questions_id
    FROM results
    WHERE accepted_answer_id is not null;








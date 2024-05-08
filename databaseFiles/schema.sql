DROP TABLE IF EXISTS "public"."Resume" CASCADE;
DROP TABLE IF EXISTS "public"."Degree" CASCADE;
DROP TABLE IF EXISTS "public"."College" CASCADE;
DROP TABLE IF EXISTS "public"."Skills" CASCADE;
DROP TABLE IF EXISTS "public"."JobTitle" CASCADE;
DROP TABLE IF EXISTS "public"."Company" CASCADE;
DROP TABLE IF EXISTS "public"."Resume_College" CASCADE;
DROP TABLE IF EXISTS "public"."Resume_Skill" CASCADE;
DROP TABLE IF EXISTS "public"."Experience" CASCADE;



CREATE TABLE IF NOT EXISTS "Resume" (
  "resume_id" SERIAL PRIMARY KEY,
  "resume_text" TEXT
);

CREATE TABLE IF NOT EXISTS "Degree" (
  "degree_id" SERIAL PRIMARY KEY,
  "degree_name" TEXT
);

CREATE TABLE IF NOT EXISTS "College" (
  "college_id" SERIAL PRIMARY KEY,
  "college_name" TEXT
  -- "location" TEXT
);

CREATE TABLE IF NOT EXISTS "Skills" (
  "skill_id" SERIAL PRIMARY KEY,
  "skill_name" TEXT
);

CREATE TABLE IF NOT EXISTS "Resume_College" (
  "resume_id" INT,
  "college_id" INT,
  "degree_id" INT,
  PRIMARY KEY (resume_id, college_id, degree_id)
);

CREATE TABLE IF NOT EXISTS "Resume_Skill" (
  "resume_id" INT,
  "skill_id" INT,
  PRIMARY KEY (resume_id, skill_id)
);

CREATE TABLE IF NOT EXISTS "JobTitle" (
  "job_title_id" SERIAL PRIMARY KEY,
  "title_name" TEXT
);

CREATE TABLE IF NOT EXISTS "Company" (
  "company_id" SERIAL PRIMARY KEY,
  "company_name" TEXT
);

CREATE TABLE IF NOT EXISTS "Experience" (
  "experience_id" SERIAL PRIMARY KEY,
  "job_title_id" INT,
  "company_id" INT,
  "other" TEXT,
  "resume_id" INT
);

ALTER TABLE IF EXISTS "Resume_College" ADD FOREIGN KEY ("resume_id") REFERENCES "Resume" ("resume_id");

ALTER TABLE IF EXISTS "Resume_College" ADD FOREIGN KEY ("college_id") REFERENCES "College" ("college_id");

ALTER TABLE IF EXISTS "Resume_College" ADD FOREIGN KEY ("degree_id") REFERENCES "Degree" ("degree_id");

ALTER TABLE IF EXISTS "Resume_Skill" ADD FOREIGN KEY ("resume_id") REFERENCES "Resume" ("resume_id");

ALTER TABLE IF EXISTS "Resume_Skill" ADD FOREIGN KEY ("skill_id") REFERENCES "Skills" ("skill_id");

ALTER TABLE IF EXISTS "Experience" ADD FOREIGN KEY ("job_title_id") REFERENCES "JobTitle" ("job_title_id");

ALTER TABLE IF EXISTS "Experience" ADD FOREIGN KEY ("company_id") REFERENCES "Company" ("company_id");

ALTER TABLE IF EXISTS "Experience" ADD FOREIGN KEY ("resume_id") REFERENCES "Resume" ("resume_id");

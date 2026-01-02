
  create or replace   view TRUSTPILOT_REVIEWS.DEV.test_connection
  
  
  
  
  as (
    -- models/staging/test_connection.sql
SELECT * FROM TRUSTPILOT_REVIEWS.RAW.REVIEWS LIMIT 10
  );


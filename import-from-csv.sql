DROP TABLE properties;
CREATE TABLE properties(
  "assessor_id" INTEGER,
  "parcel_number" INTEGER,
  "parcel_number_building_id" TEXT,
  "building_year" YEAR,
  "building_type" TEXT,
  "finished_above_grade_sq_ft" INTEGER,
  "unfinished_above_grade_sq_ft" INTEGER,
  "finished_below_grade_sq_ft" INTEGER,
  "unfinished_below_grade_sqft" INTEGER,
  "car_storage_ft" INTEGER,
  "other_sq_ft" INTEGER,
  "outbuilding_sq_ft" INTEGER,
  "total_finished_sq_ft" INTEGER,
  "size_category" TEXT,
  "zone" TEXT,
  "address" TEXT,
  "lot_size" INTEGER,
  "neighborhood" TEXT,
  "rental_license" TEXT,
  "geometry" TEXT
);

.mode csv
.headers on
.import output/output.csv properties

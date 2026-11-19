ALTER TABLE inventory
ADD CONSTRAINT "foreign_key_inventory_food_code"
FOREIGN KEY (food_code)
REFERENCES food (food_code)
ON DELETE SET NULL
ON UPDATE CASCADE;

ALTER TABLE inventory
ADD CONSTRAINT "foreign_key_inventory_last_updated_by_code"
FOREIGN KEY (last_updated_by_code)
REFERENCES person (person_code)
ON DELETE SET NULL
ON UPDATE CASCADE;

ALTER TABLE inventory
ADD CONSTRAINT "foreign_key_inventory_last_recipe_code"
FOREIGN KEY (last_recipe_code)
REFERENCES recipe (recipe_code)
ON DELETE SET NULL
ON UPDATE CASCADE;

ALTER TABLE ingredient
ADD CONSTRAINT "foreign_key_ingredient_recipe_code"
FOREIGN KEY (recipe_code)
REFERENCES recipe (recipe_code)
ON DELETE SET NULL
ON UPDATE CASCADE;

ALTER TABLE ingredient
ADD CONSTRAINT "foreign_key_ingredient_food_code"
FOREIGN KEY (food_code)
REFERENCES food (food_code)
ON DELETE SET NULL
ON UPDATE CASCADE;
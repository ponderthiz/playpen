create table Food (
	food_code VARCHAR(20) not null,
	food_name VARCHAR(80) not null,
	category VARCHAR(80) not null,
	calorie_count INT,
	unit_price decimal(5,2)
	-- PRIMARY KEY (food_code) => saving
);

CREATE TABLE person (
person_code VARCHAR(20) NOT NULL,
first_name VARCHAR(80) NOT NULL,
last_name VARCHAR(80) NOT NULL,
birth_date DATE NULL,
age INT NULL
);

CREATE TABLE recipe (
recipe_code VARCHAR(20) NOT NULL,
recipe_name VARCHAR(80) NOT NULL,
total_time decimal(5,2) NULL,
serving_size VARCHAR(5) NULL,
link VARCHAR(150) NULL
);

CREATE TABLE ingredient (
ingredient_id INT NOT NULL,
recipe_code VARCHAR(20) NOT NULL,
food_code VARCHAR(20) NOT NULL,
unit_quantity VARCHAR(80) NOT NULL
);

CREATE TABLE inventory (
inventory_id INT NOT NULL,
food_code VARCHAR(20) NOT NULL,
food_quantity INT NOT NULL,
inventory_status VARCHAR(20) NOT NULL,
purchased_by VARCHAR(20) NULL,
purchased_date DATE NOT NULL,
expiration_date DATE NOT NULL,
last_updated_date DATE NOT NULL,
last_updated_by_code VARCHAR(20) NULL,
last_updated_reason VARCHAR(20) NULL,
last_recipe_code VARCHAR(20) NULL DEFAULT NULL
);



alter table food
add primary key (food_code);

alter table person
add primary key (person_code);

alter table ingredient 
add primary key (ingredient_id);

alter table inventory 
add primary key (inventory_id);

alter table recipe 
add primary key (recipe_code);

-- select
select * from food;
select * from inventory;

update inventory i set last_recipe_code = null where i.last_recipe_code = ''

insert into food(food_code, food_name, category, calorie_count, unit_price)
values( 'CARR', 'Carrot', 'Veggie', 25, .75)

-- like
select * from food where food_name like 's____'

-- inner joins
select i.inventory_status , f.food_name 
from inventory i 
join food f 
on i.food_code = f.food_code 
and i.inventory_status not in ('finished') and food_name like '%milk%'


-- ctes
with t1 as (
select r.recipe_name, sum( f.unit_price) as cost
from recipe r 
join ingredient i 
on r.recipe_code = i.recipe_code 
join food f 
on f.food_code = i.food_code 
group by r.recipe_name ),

T2 as (
select min(cost) as cheapest_recipe_cost
from t1
)

select * 
from t1 
join t2
on t1.cost = t2.cheapest_recipe_cost;




with t1 as (
select r.recipe_name, sum( f.unit_price) as cost
from recipe r 
join ingredient i 
on r.recipe_code = i.recipe_code 
join food f 
on f.food_code = i.food_code 
group by r.recipe_name ),

T2 as (
select avg(cost) as average_recipe_cost
from t1
)

select t1.recipe_name, t1.cost
from t1, t2
where cost > Average_Recipe_Cost

-- Formatting and Optimization
insert into person(person_code, first_name, last_name, birth_date, age)
values( 'DDULIK', 'Dahlia', 'Dulik', '1994-12-20', 28);


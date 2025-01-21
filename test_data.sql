USE bms_db;
-- Insert Sample Administrators
INSERT INTO Administrator (First_Name, Last_Name, Address, Mobile_Number, Email_Address, Password)
VALUES
('Alice', 'Smith', '123 Admin Street, Cityville', '12345678', 'alice.smith@example.com', 'AdminPass1'),
('Bob', 'Johnson', '456 Admin Avenue, Townsville', '87654321', 'bob.johnson@example.com', 'SecurePass2');

-- Insert Sample Attendees
INSERT INTO Attendee (First_Name, Last_Name, Address, Mobile_Number, Email_Address, Password, Attendee_Type, Affiliated_Organization)
VALUES
('Charlie', 'Brown', '789 Attendee Road, Village', '11223344', 'charlie.brown@example.com', 'StudentPass3', 'student', 'PolyU'),
('Diana', 'Prince', '321 Attendy Lane, Hamlet', '44332211', 'diana.prince@example.com', 'AlumniPass4', 'alumni', 'HKCC'),
('Ethan', 'Hunt', '654 Attendee Blvd, Metropolis', '55667788', 'ethan.hunt@example.com', 'GuestPass5', 'guest', 'Others'),
('Fiona', 'Gallagher', '987 Attendee Street, Urbantown', '66778899', 'fiona.gallagher@example.com', 'StaffPass6', 'staff', 'SPEED'),
('George', 'Martin', '159 Attendee Avenue, Cityopolis', '77889900', 'george.martin@example.com', 'GuestPass7', 'guest', 'PolyU');

-- Insert Sample Banquets
INSERT INTO New_banquet (Banquet_Name, Date, Time, Location, Available, Quota, Address, Contact_First_Name, Contact_Last_Name)
VALUES
('Gala Night 2023', '2023-12-15', '19:00:00', 'Grand Hall A', 'Y', 100, '123 Banquet Street, Cityville', 'Alice', 'Smith'),
('Annual Dinner', '2024-01-20', '18:30:00', 'Banquet Center', 'Y', 150, '456 Banquet Avenue, Townsville', 'Bob', 'Johnson'),
('Spring Fest', '2024-03-10', '17:00:00', 'Open Grounds', 'Y', 200, '789 Fest Road, Village', 'Charlie', 'Brown');

-- Insert Sample Meals for Gala Night 2023 (Assuming BIN = 1)
INSERT INTO Meal (Dish_Name, BIN, Type, Special_Cuisine, Price)
VALUES
('Grilled Salmon', 1, 'Main Course', 'Mediterranean', 25.50),
('Roasted Chicken', 1, 'Main Course', NULL, 20.00),
('Vegetable Stir Fry', 1, 'Vegetarian', 'Asian', 15.75),
('Beef Steak', 1, 'Main Course', 'American', 30.00);

-- Insert Sample Meals for Annual Dinner (Assuming BIN = 2)
INSERT INTO Meal (Dish_Name, BIN, Type, Special_Cuisine, Price)
VALUES
('Lobster Bisque', 2, 'Appetizer', 'French', 18.00),
('Caesar Salad', 2, 'Appetizer', NULL, 12.50),
('Pasta Primavera', 2, 'Main Course', 'Italian', 22.00),
('Duck Confit', 2, 'Main Course', 'French', 28.50);

-- Insert Sample Meals for Spring Fest (Assuming BIN = 3)
INSERT INTO Meal (Dish_Name, BIN, Type, Special_Cuisine, Price)
VALUES
('Falafel Wrap', 3, 'Vegetarian', 'Middle Eastern', 10.00),
('Chicken Tacos', 3, 'Main Course', 'Mexican', 15.00),
('Beef Burrito', 3, 'Main Course', 'Mexican', 16.50),
('Veggie Pizza', 3, 'Vegetarian', 'Italian', 14.00);

-- Insert Sample Registrations
INSERT INTO Registration (Attendee_ID, BIN, Seat_No, Time, Meal_Choice, Drink_Choice, Remarks)
VALUES
(1, 1, 1, '2023-12-15 10:00:00', 'Grilled Salmon', 'tea', 'Window seat preferred.'),
(2, 1, 2, '2023-12-15 10:05:00', 'Roasted Chicken', 'coffee', NULL),
(3, 2, 1, '2024-01-20 09:30:00', 'Lobster Bisque', 'lemon tea', 'Allergic to nuts.'),
(4, 3, 1, '2024-03-10 08:45:00', 'Falafel Wrap', 'coffee', NULL),
(5, 2, 2, '2024-01-20 09:35:00', 'Caesar Salad', 'tea', 'Vegan options needed.'),
(1, 3, 2, '2024-03-10 08:50:00', 'Chicken Tacos', 'lemon tea', NULL);

-- Verify Administrators
SELECT * FROM Administrator;

-- Verify Attendees
SELECT * FROM Attendee;

-- Verify Banquets
SELECT * FROM New_banquet;

-- Verify Meals
SELECT * FROM Meal;

-- Verify Registrations
SELECT * FROM Registration;
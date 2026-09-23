import sqlite3


# Connect to SQLite and create company.db if it does not already exist.
connection = sqlite3.connect("company.db")

# Create a cursor so that SQL statements can be executed.
cursor = connection.cursor()

# Create the department and employee tables.
cursor.execute("""
	CREATE TABLE IF NOT EXISTS department (
		id INTEGER PRIMARY KEY,
		name TEXT,
		location TEXT
	)
""")

cursor.execute("""
	CREATE TABLE IF NOT EXISTS employee (
		id INTEGER PRIMARY KEY,
		name TEXT,
		deptid INTEGER
	)
""")

# Remove old demo rows so every run keeps exactly five records in each table.
cursor.execute("DELETE FROM department")
cursor.execute("DELETE FROM employee")

# Insert five departments, including one department with no employees.
departments = [
	(1, "Finance", "Mumbai"),
	(2, "Human Resources", "Bengaluru"),
	(3, "Technology", "Hyderabad"),
	(4, "Marketing", "Delhi"),
	(5, "Operations", "Chennai"),
]
cursor.executemany(
	"INSERT INTO department (id, name, location) VALUES (?, ?, ?)",
	departments,
)

# Insert five employees. Employee 5 has no matching department.
employees = [
	(1, "Aarav Sharma", 1),
	(2, "Meera Patel", 2),
	(3, "Rohan Nair", 3),
	(4, "Ananya Iyer", 4),
	(5, "Vikram Singh", 99),
]
cursor.executemany(
	"INSERT INTO employee (id, name, deptid) VALUES (?, ?, ?)",
	employees,
)

# Save the table creation and inserted records.
connection.commit()

# Fetch and display all employee records.
cursor.execute("SELECT id, name, deptid FROM employee ORDER BY id")
employee_records = cursor.fetchall()

print("Employees:")
print("ID | Name          | DeptID")
print("---------------------------")
for employee in employee_records:
	print(f"{employee[0]}  | {employee[1]:13} | {employee[2]}")

# Fetch and display all department records.
cursor.execute("SELECT id, name, location FROM department ORDER BY id")
department_records = cursor.fetchall()

print("\nDepartments:")
print("ID | Name           | Location")
print("------------------------------")
for department in department_records:
	print(f"{department[0]}  | {department[1]:14} | {department[2]}")

# Find the names of employees who work in Human Resources.
cursor.execute("""
	SELECT employee.name
	FROM employee
	INNER JOIN department ON employee.deptid = department.id
	WHERE department.name = 'Human Resources'
""")
hr_employees = cursor.fetchall()

print("\nEmployees in Human Resources:")
for employee in hr_employees:
	print(employee[0])

# Close the cursor and database connection when the work is complete.
cursor.close()
connection.close()

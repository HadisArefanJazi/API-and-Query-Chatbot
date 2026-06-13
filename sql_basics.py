 
# ============================================================
# sql and sqlite beginner notes
# ============================================================

# sql stands for structured query language.
# sql is used to create, read, update, and delete data.

# sqlite is a lightweight database system.
# it stores the database in a local file such as school.db.

# python communicates with sqlite using the sqlite3 module.

import sqlite3


# ============================================================
# 1. connect to a database
# ============================================================

# connect to a database file.
# if the file does not exist, sqlite creates it.

conn = sqlite3.connect("school.db")

# create a cursor.
# the cursor sends sql commands to sqlite.

cursor = conn.cursor()


# ============================================================
# 2. create a table
# ============================================================

# create a students table.
# integer stores whole numbers.
# text stores words.
# real stores decimal numbers.
# primary key uniquely identifies each row.
# autoincrement automatically creates ids.

cursor.execute("""
create table if not exists students (
    id integer primary key autoincrement,
    name text,
    major text,
    grade real
)
""")


# ============================================================
# 3. insert one row
# ============================================================

# insert one student.
# ? placeholders safely receive values.

cursor.execute("""
insert into students (name, major, grade)
values (?, ?, ?)
""", ("Hari", "EE", 4.0))


# ============================================================
# 4. insert multiple rows
# ============================================================

# executemany inserts many rows.

students = [
    ("Zara", "CE", 3.8),
    ("Vani", "ME", 3.5),
    ("Mari", "ME", 2.8),
    ("Mohi", "CE", 1.9)
]

cursor.executemany("""
insert into students (name, major, grade)
values (?, ?, ?)
""", students)


# ============================================================
# 5. save changes
# ============================================================

# commit permanently saves changes.

conn.commit()


# ============================================================
# 6. select all rows
# ============================================================

# select reads data.
# * means all columns.

cursor.execute("""
select *
from students
""")

rows = cursor.fetchall()

print("\nall students")

for row in rows:
    print(row)


# ============================================================
# 7. select specific columns
# ============================================================

cursor.execute("""
select name, major
from students
""")

rows = cursor.fetchall()

print("\nname and major")

for name, major in rows:
    print(name, major)


# ============================================================
# 8. where
# ============================================================

# where filters rows.

cursor.execute("""
select *
from students
where major = ?
""", ("ME",))

rows = cursor.fetchall()

print("\nstudents in ME")

for row in rows:
    print(row)


# ============================================================
# 9. count
# ============================================================

# count(*) counts rows.

cursor.execute("""
select count(*)
from students
""")

total_students = cursor.fetchone()[0]

print("\nnumber of students")
print(total_students)


# ============================================================
# 10. avg
# ============================================================

# avg computes the average.

cursor.execute("""
select avg(grade)
from students
""")

average_grade = cursor.fetchone()[0]

print("\naverage grade")
print(average_grade)


# ============================================================
# 11. order by
# ============================================================

# desc sorts from highest to lowest.

cursor.execute("""
select name, grade
from students
order by grade desc
""")

rows = cursor.fetchall()

print("\nsorted by grade")

for row in rows:
    print(row)


# ============================================================
# 12. limit
# ============================================================

# limit restricts the number of rows returned.

cursor.execute("""
select name, grade
from students
order by grade desc
limit 1
""")

top_student = cursor.fetchone()

print("\ntop student")
print(top_student)


# ============================================================
# 13. update
# ============================================================

# update modifies existing rows.

cursor.execute("""
update students
set grade = ?
where name = ?
""", (3.2, "Mari"))

conn.commit()


# ============================================================
# 14. delete
# ============================================================

# delete removes rows.

cursor.execute("""
delete from students
where grade < ?
""", (2.0,))

conn.commit()


# ============================================================
# 15. group by
# ============================================================

# group by summarizes rows with the same value.

cursor.execute("""
select major, avg(grade)
from students
group by major
""")

rows = cursor.fetchall()

print("\naverage grade by major")

for row in rows:
    print(row)


# ============================================================
# 16. create second table
# ============================================================

# this table will be used for join examples.

cursor.execute("""
create table if not exists grades (
    id integer primary key autoincrement,
    student_id integer,
    course text,
    score real
)
""")


# ============================================================
# 17. insert grade data
# ============================================================

cursor.execute("delete from grades")

cursor.executemany("""
insert into grades (student_id, course, score)
values (?, ?, ?)
""", [
    (1, "sql", 95),
    (2, "python", 90),
    (3, "math", 88)
])

conn.commit()


# ============================================================
# 18. join
# ============================================================

# join combines data from two tables.

cursor.execute("""
select students.name,
       grades.course,
       grades.score
from students
join grades
on students.id = grades.student_id
""")

rows = cursor.fetchall()

print("\njoin example")

for row in rows:
    print(row)


# ============================================================
# 19. close database
# ============================================================

# always close the connection when finished.

conn.close()


# ============================================================
# summary
# ============================================================

# create table -> create a table
# insert into  -> add rows
# select       -> read data
# where        -> filter rows
# order by     -> sort rows
# limit        -> restrict rows
# count        -> count rows
# avg          -> compute average
# update       -> modify rows
# delete       -> remove rows
# group by     -> summarize rows
# join         -> combine tables
# commit       -> save changes
# close        -> close database
 

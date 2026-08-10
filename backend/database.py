import sqlite3
import hashlib


DATABASE = "smartintern.db"


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn


# =========================================================
# PASSWORD HASHING
# =========================================================

def hash_password(password):

    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# =========================================================
# CREATE TABLES
# =========================================================

def create_tables():

    conn = get_connection()

    cursor = conn.cursor()

    # -----------------------------------------------------
    # STUDENTS TABLE
    # -----------------------------------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        full_name TEXT,

        email TEXT UNIQUE,

        college TEXT,

        degree TEXT,

        skills TEXT

    )
    """)


    # -----------------------------------------------------
    # COMPANIES TABLE
    # -----------------------------------------------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS companies (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        company_name TEXT NOT NULL,

        email TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL,

        domain TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)


    conn.commit()

    conn.close()


# =========================================================
# INSERT / UPDATE STUDENT
# =========================================================

def insert_student(
    full_name,
    email,
    college,
    degree,
    skills
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO students
    (
        full_name,
        email,
        college,
        degree,
        skills
    )
    VALUES (?, ?, ?, ?, ?)

    ON CONFLICT(email)
    DO UPDATE SET

        full_name = excluded.full_name,

        college = excluded.college,

        degree = excluded.degree,

        skills = excluded.skills

    """, (
        full_name,
        email,
        college,
        degree,
        skills
    ))

    conn.commit()

    conn.close()


# =========================================================
# GET STUDENT BY EMAIL
# =========================================================

def get_student_by_email(email):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM students
        WHERE email = ?
        """,
        (email,)
    )

    student = cursor.fetchone()

    conn.close()

    return student


# =========================================================
# GET ALL STUDENTS
# =========================================================

def get_students():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students"
    )

    students = cursor.fetchall()

    conn.close()

    return students


# =========================================================
# COMPANY REGISTRATION
# =========================================================

def insert_company(
    company_name,
    email,
    password,
    domain
):

    conn = get_connection()

    cursor = conn.cursor()

    hashed_password = hash_password(password)

    cursor.execute("""
    INSERT INTO companies
    (
        company_name,
        email,
        password,
        domain
    )
    VALUES (?, ?, ?, ?)

    ON CONFLICT(email)
    DO UPDATE SET

        company_name = excluded.company_name,

        password = excluded.password,

        domain = excluded.domain

    """, (
        company_name,
        email,
        hashed_password,
        domain
    ))

    conn.commit()

    conn.close()


# =========================================================
# GET COMPANY BY EMAIL
# =========================================================

def get_company_by_email(email):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM companies
        WHERE email = ?
        """,
        (email,)
    )

    company = cursor.fetchone()

    conn.close()

    return company


# =========================================================
# VERIFY COMPANY LOGIN
# =========================================================

def verify_company_login(
    email,
    password
):

    company = get_company_by_email(email)

    if company is None:
        return None

    hashed_password = hash_password(password)

    if company["password"] == hashed_password:

        return company

    return None


# =========================================================
# GET ALL COMPANIES
# =========================================================

def get_companies():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, company_name, email, domain, created_at FROM companies"
    )

    companies = cursor.fetchall()

    conn.close()

    return companies
# =========================================================
# COMPANY TABLE
# =========================================================

def create_company_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS companies (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        company_name TEXT,

        email TEXT UNIQUE,

        password TEXT,

        location TEXT,

        domain TEXT

    )
    """)

    conn.commit()
    conn.close()


# =========================================================
# INSERT / UPDATE COMPANY
# =========================================================

def insert_company(
    company_name,
    email,
    password,
    location,
    domain
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO companies
    (
        company_name,
        email,
        password,
        location,
        domain
    )
    VALUES (?, ?, ?, ?, ?)

    ON CONFLICT(email)
    DO UPDATE SET

        company_name = excluded.company_name,
        password = excluded.password,
        location = excluded.location,
        domain = excluded.domain

    """, (
        company_name,
        email,
        password,
        location,
        domain
    ))

    conn.commit()
    conn.close()


# =========================================================
# GET COMPANY BY EMAIL
# =========================================================

def get_company_by_email(email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM companies
        WHERE email = ?
        """,
        (email,)
    )

    company = cursor.fetchone()

    conn.close()

    return company
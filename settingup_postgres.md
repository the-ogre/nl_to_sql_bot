# Setting Up PostgreSQL and Importing a Public Database

1. Install PostgreSQL
First, let's install PostgreSQL on your Linux system:

sudo apt update
sudo apt install postgresql postgresql-contrib

2. Verify the installation and check the version
sudo systemctl status postgresql
psql --version

3. Configure PostgreSQL access
By default, PostgreSQL uses "peer" authentication for local connections,
 meaning it uses your Linux username to authenticate.

- Switch to the postgres user
sudo -i -u postgres

- Access the PostgreSQL prompt
psql

- Create a new database user (replace 'youruser' with your username)
CREATE USER youruser WITH PASSWORD 'yourpassword';

- Grant privileges (optional, for full access)
ALTER USER youruser WITH SUPERUSER;

- Exit PostgreSQL prompt
\q

- Exit the postgres user session
exit

4. Create a database for the public dataset

sudo -i -u postgres
createdb publicdata
exit

5. Public dataset

mkdir dataset
cd dataset

sudo -u postgres psql -c "CREATE DATABASE chinook;"

sudo -u postgres psql -d chinook -f Chinook_PostgreSql.sql 
#while in the directory where the sql file is

6. Verify the import worked:

- Connect to the database
sudo -u postgres psql -d chinook

- List all tables
\dt

- Run a test query
SELECT * FROM "Artist" LIMIT 5;
\q

# About Chinook database

The Chinook database represents a digital music store, modeled after the iTunes database schema. It's a comprehensive sample database designed for learning and testing SQL queries across various database systems including PostgreSQL, MySQL, SQL Server, and SQLite.
Key Features

Contains 11 interconnected tables including artists, albums, tracks, invoices, and customers
Offers real-world data relationships perfect for demonstrating joins and complex queries
Includes international data with customer information spanning multiple countries
Models both business data (sales, invoices) and content data (music tracks, genres)
Small enough to be manageable (approximately 15,000 records) but complex enough to showcase advanced SQL techniques

This database is particularly valuable for visualizing relationships between musical entities, tracking sales patterns across regions, and analyzing customer purchasing behavior across different genres and artists.
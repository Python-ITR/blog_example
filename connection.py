import psycopg2 as pg


connection = pg.connect("user=postgres dbname=blog_example password=1234qwer host=localhost port=5555")

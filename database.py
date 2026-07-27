import mysql.connector

def connect_db():
    connection = mysql.connector.connect(
        host="nozomi.proxy.rlwy.net",
        port="13855",
        user="root",
        password="FnQGfEpxpFJiRbcsDCQmkxfxkOgUeYPH",
        database="railway"
    )
    

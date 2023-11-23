import sqlite3

#скачай программу sqlite через него открой файл catalog.db. Там с помощью команд
# INSERT INTO products (name, price, link) VALUES (?, ?, ?)', (name, price, link)
# DELETE FROM products WHERE name = '', (product_name,)
# SELECT * FROM products
# можно манипулировать базой данных
# однако вместо всей этой е""тни я сделал простую программу, которая дает интерфейс для взаимодействия с датабазами

#здесь выполняется функциия добавления товара на основе sql запроса

def add_product(conn, cursor, name, price, link):
    cursor.execute('INSERT INTO products (name, price, link) VALUES (?, ?, ?)', (name, price, link))
    conn.commit()
    print(f"товар добавлен")


    # здесь выполняется функциия удаления товара на основе sql запроса
def delete_product(conn, cursor, product_name):
    cursor.execute('DELETE FROM products WHERE name = ?', (product_name,))
    conn.commit()
    print("товар удален")



    # здесь выполняется функциия показ всех товаров на основе sql запроса
def display_products(cursor):
    products = cursor.execute('SELECT * FROM products').fetchall()
    print("Список товаров:")
    for product in products:
        print(product)



        #здесь простинькая программа интерфейса на python
def main():
    #коннект к датабазам
    conn = sqlite3.connect('catalog.db')
    cursor = conn.cursor()

    while True:
        print("\n1. новый товар")
        print("2. Удаление товара")
        print("3. список товаров")

        nomer = input("Выберите действие 1 2 3")

        if nomer == '1':
            name = input("название")
            price = float(input("цена"))
            link = input("ссылка")
            add_product(conn, cursor, name, price, link)
        elif nomer == '2':
            product_name = input("название товара для удаления ")
            delete_product(conn, cursor, product_name)
        elif nomer == '3':
            display_products(cursor)
        else:
            print("Некорректный ввод. Пожалуйста, выберите число от 1 до 3")

    conn.close()


main()
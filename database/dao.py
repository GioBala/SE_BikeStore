from database.DB_connect import DBConnect
from model.product import Product

class DAO:
    @staticmethod
    def get_date_range():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT order_date
                    FROM `order` 
                    ORDER BY order_date """
        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def get_categorie():
        conn = DBConnect.get_connection()
        cursor = conn.cursor()
        query = """ SELECT DISTINCT category_name FROM `category`"""
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row[0])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_prodotti(category_name):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT p.* FROM `product` p JOIN category ON p.category_id=category.id WHERE category.category_name=%s GROUP BY p.id"""
        cursor.execute(query, (category_name,))
        result = []
        for row in cursor:
            result.append(Product(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_nodi(y1,y2,category_name):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT product.id,COUNT(o.id) as c FROM `order` as o
JOIN order_item ON order_item.order_id=o.id 
JOIN product ON product.id=order_item.product_id 
JOIN category ON product.category_id=category.id
WHERE o.order_date BETWEEN %s AND %s AND category.category_name =%s
GROUP BY product.id"""
        cursor.execute(query, (y1,y2,category_name))
        result = []
        for row in cursor:
            #print(row)
            result.append((row["id"],row["c"]))

        cursor.close()
        conn.close()
        return result



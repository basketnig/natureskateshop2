import sqlite3


class Thing(object):
    def __init__(self, id, type, name, price, imgurl, color, size, availbility):
        self.id = id
        self.type = type
        self.name = name
        self.price = price
        self.imgurl = imgurl
        self.color = color
        self.size = size
        self.availbility = bool(availbility)

    def price_str(self):
        return "$%.2f" % self.price


    @classmethod
    def get_all(cls, max=30):
        cursor = db_connect()
        QUERY = """
                  SELECT id,
                         type,
                         name,
                         price,
                         imgurl,
                         color,
                         size,
                         availbility
                   FROM clothes
                   WHERE imgurl <> ''
                   LIMIT ?;
               """

        cursor.execute(QUERY, (max,))
        clothes_list = cursor.fetchall()
        clothes = [Thing(*row) for row in clothes_list]
        return clothes

    @classmethod
    def get_by_id(cls, id):
        cursor = db_connect()
        QUERY = """
                  SELECT id,
                         type,
                         name,
                         price,
                         imgurl,
                         color,
                         size,
                         availbility
                   FROM clothes
                   WHERE id = ?;
               """

        cursor.execute(QUERY, (id,))

        row = cursor.fetchone()

        if not row:
            return None

        thing = Thing(*row)

        return thing


class Cart():
    def __init__(self, thing_id, user_id, price):
        self.thing_id = thing_id
        self.user_id = user_id
        self.price = price

    @staticmethod
    def add_to_cart(item):
        conn = sqlite3.connect("templates/clothes.db")
        cursor = conn.cursor()
        QUERY = "INSERT INTO cart (thing_id, user_id, price) VALUES (?, ?, ?)"
        cursor.execute(QUERY, (item.thing_id, item.user_id, item.price))
        conn.commit()
        cursor.close()


def db_connect():
    conn = sqlite3.connect("templates/clothes.db")
    cursor = conn.cursor()
    return cursor


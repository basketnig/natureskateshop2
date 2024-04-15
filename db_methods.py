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


def db_connect():
    conn = sqlite3.connect("templates/clothes.db")
    cursor = conn.cursor()
    return cursor


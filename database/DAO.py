from database.DB_connect import DBConnect
from model.Arco import Arco

from model.Store import Store
from model.order import Order


class DAO():
    @staticmethod
    def getAllStores():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * from stores"

        cursor.execute(query)

        for row in cursor:
            results.append((row["store_id"],row["store_name"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(storeId):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select o.*
                from orders o , stores s 
                where s.store_id =o.store_id and s.store_id = %s"""

        cursor.execute(query,(storeId,))

        for row in cursor:
            results.append(Order(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(storeId,k, idMapS):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select tb1.order_id as ordine1, tb2.order_id as ordine2, (q1.quantita + q2.quantita)/DATEDIFF(tb2.order_date, tb1.order_date) as peso
from (select o.*
      from orders o, stores s
      where s.store_id = o.store_id and s.store_id = %s) as tb1,
     (select o.*
      from orders o, stores s
      where s.store_id = o.store_id and s.store_id = %s) as tb2,
     (select o.order_id, sum(oi.quantity) as quantita
      from orders o, order_items oi
      where o.order_id = oi.order_id
      group by o.order_id) as q1,
     (select o.order_id, sum(oi.quantity) as quantita
      from orders o, order_items oi
      where o.order_id = oi.order_id
      group by o.order_id) as q2
where DATEDIFF(tb2.order_date, tb1.order_date) <= %s
  and tb1.order_id != tb2.order_id
  and tb1.store_id = tb2.store_id
  and tb1.order_date < tb2.order_date
  and q1.order_id = tb1.order_id 
  and tb2.order_id = q2.order_id"""

        cursor.execute(query,(storeId,storeId,k))

        for row in cursor:
            results.append(Arco(idMapS[row["ordine1"]],idMapS[row["ordine2"]],row["peso"]))

        cursor.close()
        conn.close()
        return results
from database.DB_connect import DBConnect
from model.Arco import Arco
from model.Order import Order


class DAO():
    @staticmethod
    def getAllStores():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select DISTINCT s.*
                from stores s """

        cursor.execute(query)

        for row in cursor:
            results.append((row["store_id"],row["store_name"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(store_id):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct o.*
                from orders o 
                where o.store_id =%s """

        cursor.execute(query,(store_id,))

        for row in cursor:
            results.append(Order(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(store_id,k,idMap):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ select  distinct a1.order_id as ordine1, a2.order_id as ordine2 , (a1.n +a2.n )/DATEDIFF(a2.order_date ,a1.order_date ) as peso
                from (select  o.order_id , o.order_date , sum(oi.quantity) as n 
                from orders o, order_items oi  
                where o.store_id =%s
                and oi.order_id = o.order_id 
                group by o.order_id , o.order_date ) a1,
                (select  o.order_id , o.order_date ,sum(oi.quantity) as n 
                from orders o , order_items oi 
                where o.store_id =%s
                and oi.order_id =o.order_id 
                group by o.order_id , o.order_date  ) a2
                where a1.order_id < a2.order_id 
                and DATEDIFF(a2.order_date ,a1.order_date ) <=%s
                and a1.order_date < a2.order_date  """

        cursor.execute(query, (store_id,store_id,k))

        for row in cursor:
            results.append(Arco(idMap[row["ordine1"]],idMap[row["ordine2"]],row["peso"]))

        cursor.close()
        conn.close()
        return results

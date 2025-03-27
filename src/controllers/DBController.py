import mysql.connector
from models.Card import Card
from models.Offer import Offer

class DBController:

    mydb = mysql.connector.connect (
    host="localhost",
    user="usuario",
    password="usuario",
    database="APCS"
    )


    @staticmethod
    def insertCard(card:Card):
        mycursor = DBController.mydb.cursor()
        
        

        if(card.doble == False):
            
            sql = "INSERT INTO cards (title, mana_cost, type, pasive, stats, doble) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (card.title[0], card.mana_cost[0], card.type[0], card.pasive[0], card.stats[0], card.doble)
            mycursor.execute(sql, val)
            print(card.title[0]+" ha sido insertado con éxito")
        
        if(card.doble == True):
            sql = "INSERT INTO cards (title, mana_cost, type, pasive, stats, title_2, mana_cost_2, type_2, pasive_2, stats_2, doble) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (card.title[1], card.mana_cost[1], card.type[1], card.pasive[1], card.stats[1], card.title[2], card.mana_cost[2], card.type[2], card.pasive[2], card.stats[2], card.doble)
            mycursor.execute(sql, val)
            print(card.title[1]+" ha sido insertado con éxito")

        DBController.mydb.commit()


    @staticmethod
    def insertOffer(offer:Offer, idCard):
        mycursor = DBController.mydb.cursor()

        sql = "INSERT INTO offers (expansion, seller, quality, price, quantity, BCN) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (offer.expansion, offer.seller, offer.quality, offer.price, offer.quantity, offer.bcn)
    
        mycursor.execute(sql, val)
        offer_id = mycursor.lastrowid

    @staticmethod
    def insertImg(id:int, link:str):
        mycursor = DBController.mydb.cursor()
        
        sql = "UPDATE cards SET img = %s WHERE id = %s"

        val = (link, id)
        mycursor.execute(sql, val)
        DBController.mydb.commit()
        print(link+" ha sido insertado con éxito en la carta N:")
        print(id)


    @staticmethod
    def getCards():
        mycursor = DBController.mydb.cursor()
        
        sql = "SELECT id,title,title_2,doble  FROM cards"
        mycursor.execute(sql)

        results = mycursor.fetchall()

        return results
        #for row in results:
        #    print(row)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains  # Optional, depending on your needs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement  # To use WebElement in type hinting
from selenium.webdriver.common.by import By
from typing import List

from models.Card import Card
from controllers.DBController import DBController
import time
import os
import subprocess

class CardController:

    cardList:List[Card] = list()

    def getAllLinkCards(url:str):
        options = Options()
        options.headless = False  # Set to True for headless mode
        options.add_argument('--no-sandbox')  # Evita problemas con el sandboxing de Chrome
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)
        links:List[str] = []
        btn:WebElement
        driver.get(url)
        divCardList:List[WebElement] = driver.find_elements(By.CLASS_NAME, "card-grid-item-card")
        btnList:List[WebElement] = driver.find_elements(By.CSS_SELECTOR, "a.button-n")
        exitBool = False
        for i, bton in enumerate(btnList):
            if(i == 2):
                btn = bton

        while (exitBool == False):
        
            btnList:List[WebElement] = driver.find_elements(By.CSS_SELECTOR, "a.button-n")
            divCardList:List[WebElement] = driver.find_elements(By.CLASS_NAME, "card-grid-item-card")
            for k, bton in enumerate(btnList):
                if(k == 2):
                    btn = bton

            for j, divCard in enumerate(divCardList):
            
                print(divCard.get_attribute("href"))
                links.append(divCard.get_attribute("href"))
                
                

            if(driver.current_url == "https://scryfall.com/search?as=grid&order=name&page=470&q=%28game%3Apaper%29+legal%3Acommander&unique=cards"):
                    exitBool = True
                    break   

            try:
                driver.get(btn.get_attribute("href"))
                time.sleep(2)

            except:
                print("Last btn doesn't exist")

        return links   


    def writeDocument(path:str, listOf:List[str]):
        file = open(path, "w")
        for i, link in enumerate(listOf):
            file.write(link+'\n')
        
        file.close()

            
    def getCard(url:str, cardList:List[Card]):
        options = Options()
        options.headless = True  # Set to True for headless mode
        options.add_argument('--no-sandbox')  # Evita problemas con el sandboxing de Chrome

        
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(1)
        titleElementList:List[WebElement] = driver.find_elements(By.CLASS_NAME, "card-text-title")
        typeElementList:List[WebElement] = driver.find_elements(By.CLASS_NAME, "card-text-type-line")
        pasiveElementList:List[WebElement] = driver.find_elements(By.CLASS_NAME, "card-text-oracle")
        statsElementList:[WebElement] = driver.find_elements(By.CLASS_NAME, "card-text-stats")

        card:Card = Card()
        
        #If card have two faces
        if(len(titleElementList)>1):
            for i,title in enumerate(titleElementList):
                
                
                #Set atribute "text" of Card
                titleText:str = title.find_element(By.CLASS_NAME,"card-text-card-name").text
                card.title.append(titleText)
                
                
                
                #Set atribute "mana_cost" of Card
                try:
                    costText:str = ""
                    costElement:WebElement = title.find_element(By.CLASS_NAME, "card-text-mana-cost")
                    costsText:List[WebElement] = costElement.find_elements(By.TAG_NAME,"abbr")
                    
                    for j, cost in enumerate(costsText):
                        costText = costText+cost.text
                    
                    card.mana_cost.append(costText)
                except:
                    card.mana_cost.append("null")

                
                
                #Set atribute "type" of Card
                typeText:str = typeElementList[i].text
                card.type.append(typeText)
                
                
                
                #Set atribute "pasive" of Card
                try:
                    pasiveParragraphList:List[WebElement] = pasiveElementList[i].find_elements(By.TAG_NAME, "p")
                    pasiveText = ""
                    for k, parragraph in enumerate(pasiveParragraphList):
                            pasiveText = pasiveText+parragraph.text+"\n"
                except:
                    card.pasive.append("null")
                
                card.pasive.append(pasiveText)

                
                
                #Set atribute "pasive" of Card
                if(len(statsElementList)>1):
                    card.stats.append(statsElementList[i].text)
                else:
                    try:
                        card.stats.append(statsElementList[0].text)
                    except:
                        card.stats.append("null")
            card.doble = True
            # print("---------CARTA DOBLE------------")
            # print("Primera cara:")
            # print(card.title[1])
            # print(card.mana_cost[1])
            # print(card.type[1])
            # print(card.pasive[1])
            # print(card.stats[1])

            # print("Segunda cara:")
            # print(card.title[2])
            # print(card.mana_cost[2])
            # print(card.type[2])
            # print(card.pasive[2])
            # print(card.stats[2])
            print(card.doble)
        #Else if card have only one face
        else:

            #Set atribute "text" of Card
            try:
                titleText = titleElementList[0].find_element(By.CLASS_NAME,"card-text-card-name").text
                card.title[0] = titleText
            except:
                titleText = "null"
            

            #Set atribute "mana_cost" of Card
            costText:str = ""
            try:
                costElement:WebElement = titleElementList[0].find_element(By.CLASS_NAME, "card-text-mana-cost")
                costsText:List[WebElement] = costElement.find_elements(By.TAG_NAME,"abbr")
                
                for j, cost in enumerate(costsText):
                    costText = costText+cost.text
                
                card.mana_cost[0] = costText
            except:
                card.mana_cost[0] = "null"



            #Set atribute "type" of Card
            typeText = typeElementList[0].text
            card.type[0] = typeText



            #Set atribute "pasive" of Card
            try:
                pasiveParragraphList:List[WebElement] = pasiveElementList[0].find_elements(By.TAG_NAME, "p")
                pasiveText = ""
                for k, parragraph in enumerate(pasiveParragraphList):
                        pasiveText = pasiveText+parragraph.text+"\n"
                    
                card.pasive[0] = pasiveText
            except:
                card.pasive[0] = "null"


            #Set atribute "stats" of Card
            try:
                card.stats[0] = statsElementList[0].text
            except:
                card.stats[0] = "null"
                
            

            # print("---------CARTA SIMPLE------------")
            # print(card.title[0])
            # print(card.mana_cost[0])
            # print(card.type[0])
            # print(card.pasive[0])
            # print(card.stats[0])
            card.doble = False

        #cardList.append(card)
        if(not card.doble):
            DBController.insertCard(card)
        else:
            DBController.insertCard(card)

        driver.close()

    def getDeals(cardList):
        options = Options()
        options.headless = True  # Set to True for headless mode
        options.add_argument('--no-sandbox')  # Evita problemas con el sandboxing de Chrome

        
        driver = webdriver.Chrome(options=options)
        for card in cardList:
            
            print(card[0])
            title1:str = str(card[1])
            title1:str = title1.replace(" ", "-")
            
            driver.get("https://www.cardmarket.com/en/Magic/Cards/"+title1+"?sellerCountry=10&sellerType=1,2&language=1,4&minCondition=3")
            offerColumnList:List[WebElement] = driver.find_elements(By.CLASS_NAME, "row.g-0.article-row")

            for i, column in enumerate(offerColumnList):
                sellerPart:WebElement = column.find_element(By.CLASS_NAME, "col-sellerProductInfo.col")
                pricePart:WebElement = column.find_element(By.CLASS_NAME, "col-offer.col-auto")

                subSellerPart1:WebElement = sellerPart.find_element(By.CLASS_NAME, "row.g-0")
                
                #Pillar el seller
                subSellerPart2:WebElement = subSellerPart1.find_element(By.CLASS_NAME, "col-seller.col-12.col-lg-auto")
                subSellerPart3:WebElement = subSellerPart2.find_element(By.CLASS_NAME, "seller-info.d-flex.align-items-center")
                subSellerPart4:WebElement = subSellerPart3.find_element(By.CLASS_NAME, "seller-name.d-flex")
                #subSellerPart5:WebElement = subSellerPart4.find_element(By.CLASS_NAME, "seller-name.d-flex")

                sellerPartAtributes:List[WebElement] = subSellerPart4.find_elements(By.CLASS_NAME, "d-flex.has-content-centered.me-1")


                for j, part in enumerate(sellerPartAtributes):
                    if(j == 1):
                        seller:WebElement = part.find_element(By.TAG_NAME, "a").text
                        break
                    

                
                print(seller)
                if(seller == "Levodin" or seller == "Devian-Magic-Cards" or seller == "Magic-Industria-61" or seller == "Lallanuratcg" or seller == "inGenio" or seller == "MagicBarcelona" or seller == "PhyrexianMTG" or seller == "TesoroDragon"):
                    bcn = True
                else:
                    bcn = False

                print(bcn)
                subExpansionAndQualityPart:WebElement = subSellerPart1.find_element(By.CLASS_NAME, "col-product.col-12.col-lg")
                subExpansionAndQualityPart2:WebElement = subExpansionAndQualityPart.find_element(By.CLASS_NAME, "row.g-0")
                subExpansionAndQualityPart3:WebElement = subExpansionAndQualityPart2.find_element(By.CLASS_NAME, "product-attributes.col")
                subExpansionAndQualityPart4:List[WebElement] = subExpansionAndQualityPart3.find_elements(By.TAG_NAME, "A")

                for q, slot in enumerate(subExpansionAndQualityPart4):
                    if(q == 0):
                        expansion:str = slot.get_attribute("data-bs-original-title")
                        print(expansion)
                    if(q == 1):
                        quality:str = slot.get_attribute("data-bs-original-title")

                print("Expansion: "+expansion+", Quality: "+quality)
                print("pasa")

                #Pillar Cantidad y Precio   
                pricePart2:WebElement = pricePart.find_element(By.CLASS_NAME, "price-container.d-none.d-md-flex.justify-content-end")
                pricePart3:WebElement = pricePart2.find_element(By.CLASS_NAME, "d-flex.flex-column")
                pricePart4:WebElement = pricePart3.find_element(By.CLASS_NAME, "d-flex.align-items-center.justify-content-end")
                price:str = pricePart4.find_element(By.CLASS_NAME, "color-primary.small.text-end.text-nowrap.fw-bold").text
                priceFloat = float((price[0:(len(price)-2)]).replace(",", "."))
                print(price)
                print(priceFloat)

                quantityPart2:WebElement = pricePart.find_element(By.CLASS_NAME, "amount-container.d-none.d-md-flex.justify-content-end.me-3")
                quantity:WebElement = quantityPart2.find_element(By.CLASS_NAME, "item-count.small.text-end").text

                print(quantity)




            
            
            

            
        
    
    # Abre el archivo en modo lectura
    def insertImgFromFile(file:str):
        with open('./ModelFiles/CardNames.txt', 'r') as file:
            i:int = 1
    # Itera sobre cada línea del archivo
    #    for linea in file:
    #        DBController.insertImg(i, linea.strip())
    #        i = i+1
            
      #      print(linea.strip()) 
       #     getCard(linea.strip(), cardList)
             # 'strip()' elimina los saltos de línea al final de cada línea


    cardList = DBController.getCards()
    getDeals(cardList)
    # getCard("https://scryfall.com/card/khm/168/esika-god-of-the-tree-the-prismatic-bridge", cardList)

    # for i,card in enumerate(cardList):
    #     if(not card.doble):
    #         DBController.insertCard(card)
    #     else:
    #         DBController.insertCard(card)
    #getAllLinkCards("https://scryfall.com/search?as=grid&order=name&page=1&q=%28game%3Apaper%29+legal%3Acommander&unique=cards")
    #writeDocument("./ModelFiles/CardLinks.txt", getAllLinkCards("https://scryfall.com/search?as=grid&order=name&page=1&q=%28game%3Apaper%29+legal%3Acommander&unique=cards"))
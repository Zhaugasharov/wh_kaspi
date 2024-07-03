from whatsapp import WhatsApp
from kaspi import Kaspi
from datetime import datetime
import json
import logging
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():

    f = open("messages.json", "r", encoding="UTF-8")
    messages = json.load(f)
    orders_new = []
    orders_delivered = []
    current_date = datetime.now().date()
    start_of_day = int(time.mktime(time.strptime(time.strftime("%Y-%m-%d 00:00:01"), "%Y-%m-%d %H:%M:%S")) * 1000)
    #start_of_day = int(time.mktime(time.strptime(time.strftime("2024-06-28 00:00:01"), "%Y-%m-%d %H:%M:%S")) * 1000)
    end_of_day = int(time.mktime(time.strptime(time.strftime("%Y-%m-%d 23:59:59"), "%Y-%m-%d %H:%M:%S")) * 1000)
    #end_of_day = int(time.mktime(time.strptime(time.strftime("2024-07-01 23:59:59"), "%Y-%m-%d %H:%M:%S")) * 1000)

    kaspi = Kaspi()
    whatsapp = WhatsApp()
    whatsapp.init_webm()
    input("Обойдите защиту ватсапп и нажмите ENTER!")

    try:
        while True:
            check_date = datetime.now().date()
            kaspi_new_orders = kaspi.get_orders("NEW", "APPROVED_BY_BANK", start_of_day, end_of_day)

            if kaspi_new_orders.status_code != 200:
                logging.error("Kaspi error on kaspi_new_orders")
                logging.error(kaspi_new_orders)
                continue

            kaspi_new_orders = kaspi_new_orders.json()

            try:
                for order in kaspi_new_orders["data"]:

                    if order["id"] in orders_new:
                        continue

                    orders_new.append(order["id"])
                    message = messages["bought"]
                    goods = kaspi.get_info_about_good(order["id"]).json()
                    good = kaspi.join_goods_text(goods["data"])
                    message = kaspi.format_message(message, order, good, goods["data"])
                    msisdn = order["attributes"]["customer"]["cellPhone"]

                    found = whatsapp.search_contact("7" + str(msisdn))

                    if found is False:
                        whatsapp.back()
                        logging.warning("Not found: " + str(msisdn))
                    else:
                        whatsapp.send_message(message)
            except Exception as e:
                print("NEW ORDER PARSE ERROR")
                print(e)

            if not kaspi_new_orders["data"]:
                time.sleep(3)

            kaspi_delivered_orders = kaspi.get_orders("ARCHIVE", "COMPLETED", start_of_day, end_of_day)

            if kaspi_delivered_orders.status_code != 200:
                logging.error("Kaspi error on delivered")
                logging.error(kaspi_delivered_orders)
                continue

            kaspi_delivered_orders = kaspi_delivered_orders.json()
            try:
                for order in kaspi_delivered_orders["data"]:
                    if order["id"] in orders_delivered:
                        continue

                    goods = kaspi.get_info_about_good(order["id"]).json()
                    orders_delivered.append(order["id"])
                    message = messages["delivered"]
                    good = kaspi.join_goods_text(goods["data"])
                    message = kaspi.format_message(message, order, good, goods["data"])
                    msisdn = order["attributes"]["customer"]["cellPhone"]
                    print(message)
                    found = whatsapp.search_contact("7" + str(msisdn))

                    if found is False:
                        whatsapp.back()
                        logging.warning("Not found: " + str(msisdn))
                    else:
                        whatsapp.send_message(message)
            except Exception as e:
                print("DELIVERED ERROR")
                print(e)

            print("_________")
            if not kaspi_delivered_orders["data"]:
                time.sleep(3)

            if current_date != check_date:
                orders_new = []
                orders_delivered = []
                current_date = datetime.now().date()
                start_of_day = int(time.mktime(time.strptime(time.strftime("%Y-%m-%d 01:00:00"), "%Y-%m-%d %H:%M:%S")) * 1000)
                end_of_day = int(time.mktime(time.strptime(time.strftime("%Y-%m-%d 23:59:59"), "%Y-%m-%d %H:%M:%S")) * 1000)

    except Exception as err:
        logging.error("Something went wrong!")
        logging.error(err)

if __name__ == "__main__":
    main()
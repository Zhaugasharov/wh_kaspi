import logging

import requests
from datetime import datetime


class Kaspi:
    __url = "https://kaspi.kz/shop/api/v2/orders"
    __token = ""

    def set_token(self, token):
        self.__token = token

    def get_orders(self, state, status, start_at, end_at):
        query = {
            "page[number]": 0,
            "page[size]": 20,
            "filter[orders][status]": status,
            "filter[orders][creationDate][$ge]": start_at,
            "filter[orders][creationDate][$le]": end_at,
            "filter[orders][signatureRequired]": "false",
            "filter[orders][state]": state,
            "include[orders]": "user",
        }

        return requests.get(self.__url, params=query, headers={"X-Auth-Token": self.__token, "User-Agent": "Xcs",
                                                               "Content-Type": "application/vnd.api+json"},
                            verify=False)

    def get_info_about_good(self, order_id):
        url = "https://kaspi.kz/shop/api/v2/orders/" + str(order_id) + "/entries"
        return requests.get(url, headers={"X-Auth-Token": self.__token, "User-Agent": "Xcs",
                                          "Content-Type": "application/vnd.api+json"}, verify=False)

    def join_goods_text(self, goods):
        text_ru = ""
        text_kk = ""

        for good in goods:
            text_ru += good["attributes"]["offer"]["name"] + " " + str(good["attributes"]["quantity"]) + " шт.\n"
            text_kk += good["attributes"]["offer"]["name"] + " " + str(good["attributes"]["quantity"]) + " дана.\n"

        return {
            "text_ru": text_ru,
            "text_kk": text_kk
        }

    def format_message(self, message, order, good=None, goods=None):

        try:
            order_date = order["attributes"]["kaspiDelivery"]["courierTransmissionPlanningDate"]
            d = datetime.fromtimestamp(order_date / 1000.0)
            message = message.replace("DATE", str(d.date()))
        except Exception as err:
            logging.error(err)

        message = message.replace("ORDER_NUMBER", order["attributes"]["code"])

        if good is not None:

            link = ""

            for g in goods:
                link = "https://kaspi.kz/shop/review/productreview?orderCode=" + str(order["attributes"][
                    "code"]) + "&productCode=" + str(g["attributes"]["offer"]["code"]) + "&rating=5\n"

            message = message.replace("LINK", link)
            message = message.replace("PRODUCT_NAME_RU", good["text_ru"])
            message = message.replace("PRODUCT_NAME_KK", good["text_kk"])

        message = message.replace("NAME", order["attributes"]["customer"]["firstName"])

        return message



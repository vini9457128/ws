import asyncio
import websockets
import json
from pprint import pprint
from urllib import parse, parse
from ads.facebookAds import Facebook
from abc import ABC
import pymysql


class BaseHeart(ABC):
    def __init__(self, host="127.0.0.1",
                 user="root",
                 password="root",
                 port=3306,
                 database="panel",
                 queue="deloran.private.ltrck.com.br",
                 **kwargs):

        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.database = database
        self.queue = queue

        self._db, self._cursor = self._connect_mysql(
            host, user, password, port, database)

    def _connect_mysql(
            self, host="127.0.0.1", user="root", password="root", port=3306,
            database="panel"):
        db = pymysql.connect(
            host=host,
            user=user,
            password=password,
            port=port,
            database=database,
            cursorclass=pymysql.cursors.DictCursor
        )

        return db, db.cursor()

    def _close_db_connection(self):
        if self._db:
            self._db.close()

    def _execute_query(self, query, count=0):
        if count >= 5:
            return False

        try:
            self._cursor.execute(query)

            return True
        except Exception as error:
            print(f"ERROR: {error}")
            self._close_db_connection()

            # try re-connect mysql
            self._db, self._cursor = self._connect_mysql(
                self.host, self.user, self.password, self.port,
                self.database
            )

            self._execute_query(query, count + 1)


class Heart(BaseHeart):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def get_last_hour(self):
        async with websockets.connect("ws://q3.private.ltrck.com.br:8090/node") as ws:
            await ws.send('{"bind_account": 12589}')  # Conta Aprovasim
            # await ws.send('{"bind_account": 1}')  # Conta coringa

            while True:
                cmd = await ws.recv()

                for data in json.loads(cmd):
                    # print(data)
                    try:
                        if isinstance(data, list) and data[0] and data[1]:
                            self.process_by_type(type=data[0], data=data[1])
                    except Exception as error:
                        # print(data)
                        # print(error)
                        ...

    def get_token(self, ltm_type, account_id="12589"):
        ltm_type_names = {
            "FACEADS": "FaceBook Ads",
            "GADS": "Google Ads"
        }

        ltm_type_name = ltm_type_names.get(ltm_type)

        if not ltm_type_name:
            print(f"ERROR: cant find {ltm_type} into ltm_type_names")
            return None

        query = f"""
            SELECT dinCustomField
            FROM DataIntegration
            JOIN Integration ON dinIntegration = intId
            WHERE intName = "{ltm_type_name}"
            AND dinAccId = "{account_id}"
            AND dinStatus = "ACTIVE"
        """

        self._execute_query(query)

        result = self._cursor.fetchone()

        result_dict = json.loads(result["dinCustomField"])

        if not result:
            return None

        if ltm_type_name == "FaceBook Ads":
            id = result_dict["accounts"][0]["id"]
            access_token = result_dict["access_token"]

            # print(id)
            # access_token = result["dinCustomField"]["access_token"]
            # print({"id": id, "access_token": access_token}
            #   )
            return {"id": id, "access_token": access_token}

        # print(result.get("dinCustomField"))

        if ltm_type_name == "Google Ads":
            ...

        # print(result.get("dinCustomField"))
        return (result.get("dinCustomField"))

    def process_by_type(self, type, data):

        if type == "pageview":
            params = dict(parse.parse_qsl(parse.urlsplit(data['url']).query))

            # print(params)

            if params.get('ltk_fag'):

                # Aprovasim
                fb_aprovasim = Facebook(
                    'act_1407542209639031', 'EAAKxZBuKX3BoBADkRZBZCBD50cjpB7gZCCdJyGXYaqskzLYRLMHg3hJfohOzPXoBms3BjBbcsfpNZA0a4E2zuFz0EV9vnb3ySf7DjxhoaQ836RU52xgrwZBGUPTumR7ltTakx7tYhdKEFgRdXw0Dxwuq7VPH34Nki0b6PUvtGuOmYYVCeO5upT20K0N8UStoiUExhLQg8e9LZAWBMtsq63fvu5AMwCq4tpdtECGn5lCwaIhjRmAeN2e')

                # pprint(fb_aprovasim.adset_insights_last_minute(
                #     adset_id=params.get('ltk_fag')))
                # pprint(fb_aprovasim.ad_insights_last_minute(
                #     ad_id=params.get('ltk_fac')))
                # pprint(fb_aprovasim.campaign_insights_last_minute(
                #     campaign_id=params.get('ltk_fcm')))

                # TNM
                # fb_tnm = Facebook('act_1169556923743324', 'EAAKxZBuKX3BoBAA0MnyupYFEJkxlX9XYj22tXIpeBoSwlgOh6IQuxYg6FPXdh8QCuO5z09BTwPlZADonPtEkB2tAhmUvOEAREvByQBs8zknKQ6duu5tEF4TlB7aNhZA2ZBh9UBuvHBCgUEIwzTDF8vkjiJ2JV2qLfVwkrrelDEMhd4LtpFgUesxVti5IDB7jwuZAsK2fnHqR6BZAvP3pK9MwkZCeRQhZBN34sbyTh3hHZCT0dgseMpGBH')
                # print(fb.get_facebook_accounts())

                # pprint(fb_tnm.campaign_insights_last_minute(
                #     campaign_id=params.get('ltk_fcm')))

                # fb_coringa = Facebook("act_1175654669483341", "EAAKxZBuKX3BoBOwZAGuZB4apsSQISzoon8u38ZCGpJEycrn7oHlFbN11WOxsvuWre2zesuZBoOaZC71c6xnwLYErQ1GbIB1KL9aYaXHhyzAtpANqDgCiSt5uzuvXLRaB2YPr7rZAZCcDtGDIOLZBVn6ZAFsGs5dLiZChsVFQ7pTiGem3SGnNd8lb5H61rWD2gDd1MptUQU1OqosZC0KAnvvLqZBpvjX7wPpeWDKxczM6a57tu0PfmWrNZAJZC3G")

                # pprint(fb_coringa.campaign_insights_last_minute(
                #     campaign_id=params.get('ltk_fcm')))


if __name__ == "__main__":

    connection = Heart()

    connection.get_token(ltm_type="FACEADS")

    asyncio.get_event_loop().create_task(connection.get_last_hour())
    asyncio.get_event_loop().run_forever()

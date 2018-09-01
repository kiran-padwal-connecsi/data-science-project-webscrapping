import pandas as pd
import pymysql,pymysql.cursors
from sshtunnel import SSHTunnelForwarder

class MyModel:


    def __init__(self,URL=''):
        self.URL = URL
        # self.server = SSHTunnelForwarder(
        #     '46.28.109.89',
        #     ssh_username='kiran',
        #     ssh_password='vD2eV&^bKS(AB92G',
        #     ssh_pkey='C:/Users/Mika/.ssh/id_rsa',
        #     remote_bind_address=('127.0.0.1', 3306)
        # )
        # self.server.start()

        self.cnx = pymysql.connect(
            host='127.0.0.1',
            # port=self.server.local_bind_port,
            user='root',
            password='',
            db='crypto',
            use_unicode=True, charset="utf8"

        )


    def get_coin_details(self):

        table_name = "coin"
        try:
            with self.cnx.cursor() as cursor:
                # get all records
                sql = "SELECT *from " +table_name+"` "
                cursor.execute(sql)
                data = cursor.fetchall()
                #print(result)

            print("closing cnx")
            cursor.close()
            print("stopping server")
            # self.server.stop()
            return data

        except:
            print("i m in exception")
            # self.server.stop()

    def get_coin_id_by_symbol(self,symbol):
        print("symbol inside model = ", symbol)
        table_name = "coin"
        try:
            with self.cnx.cursor() as cursor:
                # get coin id
                sql = "SELECT `coin_id`  FROM `" +table_name+"` WHERE symbol = '" + symbol + "'"
                # print(sql)
                cursor.execute(sql)
                coin_id = cursor.fetchone()
                # print("inside model coin id =",coin_id)

            print("closing cnx")
            cursor.close()
            print("stopping server")
            # self.server.stop()
            return coin_id

        except:
            print("i m in exception No coin id found")
            # self.server.stop()

    def get_coin_id_by_coin_name(self,coin_name):
        table_name = "coin"
        try:
            with self.cnx.cursor() as cursor:
                # get coin id
                sql = "SELECT `coin_id`  FROM `" + table_name + "` WHERE coin_name = '" + coin_name + "'"
                # print(sql)
                cursor.execute(sql)
                coin_id = cursor.fetchone()
                # print("inside model coin id =",coin_id)

            print("closing cnx")
            cursor.close()
            print("stopping server")
            # self.server.stop()
            return coin_id

        except:
            print("i m in exception No coin id found")
            # self.server.stop()

    def insert_coin_details(self,data):
        table_name = "coin"
        try:

            with self.cnx.cursor() as cursor:
                     #sql = "INSERT INTO "+table_name+" (symbol, coin_name) SELECT * FROM (SELECT %s, %s) AS tmp WHERE NOT EXISTS ( SELECT symbol, coin_name FROM "+ table_name +" WHERE symbol = %s and coin_name = %s) LIMIT 1 "
                     sql = "INSERT IGNORE INTO `"+table_name+"` (`coin_name`, `symbol`) VALUES (%s, %s)"
                     #print(sql)
                     dataList = []
                     for item in data :
                        #print(item)
                        tdata =(item[1],item[0])
                        dataList.append(tdata)
                        #print(tdata)
                     # print(dataList)
                     cursor.executemany(sql, dataList)
                     self.cnx.commit()
            print("closing cnx")
            cursor.close()
            print("stopping server")
            # self.server.stop()
        except:
                print("i m in exception")
                # self.server.stop()

    def updateCoinDetails(self,data):
        table_name = "coin"
        try:

            with self.cnx.cursor() as cursor:

                     cursor.execute("UPDATE " + table_name + " SET `name` = %s, `norm_name` = %s, `domain` = %s WHERE `coin_id` = %s ", (data[0],data[1],data[2],data[3]))

                     self.cnx.commit()
            print("closing cnx")
            cursor.close()
            print("stopping server")
            # self.server.stop()
        except:
                print("i m in exception")
                # self.server.stop()


    def insert_coin_price_daily(self, data):
        table_name = "coin_price_daily_dup"
        try:
            with self.cnx.cursor() as cursor:
                    sql = "INSERT INTO `" + table_name + "` (`date`,`open`,`high`,`low`,`close`,`volume`,`market_capital`,`coin_id`, `source_id`) VALUES (%s, %s,%s,%s, %s,%s,%s, %s,%s)"
                    # print(sql)
                    dataList = []
                    for item in data:
                        #print("my item - ",item)
                        tdata = (item[0], item[1],item[2],item[3],item[4],item[5],item[6],item[7],item[8])
                        dataList.append(tdata)
                        # print(tdata)
                    # print(dataList)
                    cursor.executemany(sql, dataList)
                    self.cnx.commit()
            print("closing cnx")
            cursor.close()
            print("stopping server")
            # self.server.stop()

        except:
                print("i m in exception")
                # self.server.stop()

    def get_coin_price_daily_records_by_range(self,start,end):

        table_name = "coin_price_daily"
        coin_id = '1'
        try:
            with self.cnx.cursor() as cursor:
                # get coin_proce_daily
                print(" i m here inside table")
                print(start)
                print(end)
                sql = "SELECT `cpd`.`coin_id`, `coin_name`, count(`cpd`.`coin_id`) as `no_rows` " \
                      "FROM `coin_price_daily` as `cpd` JOIN `coin` as `c` ON `cpd`.`coin_id` = `c`.`coin_id` " \
                      "group by `cpd`.`coin_id` having count(`cpd`.`coin_id`) between "\
                      + str(start) + \
                      " and "\
                      + str(end)
                # sql = "SELECT coin_id, count(coin_id) as no_rows FROM "+ table_name + "group by coin_id having count(coin_id) between"+ start +" and "+ end
                # sql = "SELECT coin_id  FROM " + table_name + " WHERE coin_id = " + coin_id
                print(sql)
                # exit()
                cursor.execute(sql)
                results = cursor.fetchall()
            print("closing cnx")
            cursor.close()
            print("stopping server")
            # self.server.stop()
            return results
        except:
            print("i m in exception No coin id found")
            # self.server.stop()

    def del_records_coin_price_daily(self,coin_id):
        table_name = "coin_price_daily"
        # print(" i m inside delete method")
        try:
            with self.cnx.cursor() as cursor:
                sql = "DELETE FROM "+ table_name +" WHERE coin_id = "+ str(coin_id)
                print(sql)
                # exit()
                cursor.execute(sql)
                self.cnx.commit()
            print("closing cnx")
            cursor.close()
            print("stopping server")
            # self.server.stop()

        except:
            print("i m in exception")
            # self.server.stop()

    def insert_coin_price_minute(self, data):
        table_name = "coin_price_daily_supply"
        try:
            with self.cnx.cursor() as cursor:
                sql = "INSERT INTO `" + table_name + "` (`coin_id`,`available_supply`,`total_supply`, `max_supply`,`last_updated_new`) VALUES (%s,%s,%s,%s,%s)"
                print(sql)
                dataList = []
                for item in data:
                    # print("my item - ",item)
                    tdata = (item[0], item[1], item[2], item[3], item[4])
                    dataList.append(tdata)
                    print(tdata)
                # print(dataList)
                # exit()
                cursor.executemany(sql, dataList)
                self.cnx.commit()
            print("closing cnx")
            cursor.close()
            print("stopping server")
            # self.server.stop()

        except Exception as e:
            print(e)
            print("i m in exception")
            # self.server.stop()


    def insert_cindicator_Question_details(self, data):
        table_name = "cindicator"
        # print(data)
        # exit()
        try:
            with self.cnx.cursor() as cursor:
                sql = "INSERT INTO `" + table_name + "` (`question_type`,`signal_date`,`start_date`,`end_date`,`symbol`,`currency`,`settled_price`,`lower`, `upper`,`target`,`probability`,`notes`,`uid`,`email_from`,`email_date`) VALUES (%s, %s,%s,%s, %s,%s,%s, %s,%s,%s,%s,%s,%s,%s,%s)"
                # print(sql)
                dataList = []
                for item in data:
                    # print("my item - ",item)
                    tdata = (item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8],item[9],item[10],item[11],item[12],item[13],item[14])
                    dataList.append(tdata)
                    # print(tdata)
                # print(dataList)
                cursor.executemany(sql, dataList)
                self.cnx.commit()
            print("closing cnx")
            cursor.close()
            print("stopping server")
            # self.server.stop()

        except Exception as e:
            print(e)
            print("i m in exception")
            # self.server.stop()


    def insert_telegram_Signal_details(self, data):
        table_name = "telegram"
        try:
            with self.cnx.cursor() as cursor:
                sql = "INSERT IGNORE INTO `" + table_name + "` (`coin_id`,`source_id`,`symbol`,`target1`,`target2`,`target3`,`stop_loss`,`signal_date`, `signal_id`,`target4`,`currency`,`q_type`,`zone_type`,`zone`) VALUES (%s, %s,%s,%s, %s,%s,%s, %s,%s,%s,%s,%s,%s,%s)"
                # print(sql)
                dataList = []
                for item in data:
                    # print("my item - ",item)
                    tdata = (item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8],item[9],item[10],item[11],item[12],item[13])
                    dataList.append(tdata)
                    # print(tdata)
                # print(dataList)
                cursor.executemany(sql, dataList)
                self.cnx.commit()
            print("closing cnx")
            cursor.close()
            print("stopping server")
            # self.server.stop()

        except Exception as e:
            print(e)
            print("i m in exception")
            # self.server.stop()


    def insert_hackedCom_Signal_details(self, data):
        table_name = "hackedCom"
        try:
            with self.cnx.cursor() as cursor:
                sql = "INSERT IGNORE INTO `" + table_name + "` (`coin_id`,`source_id`,`symbol`,`target1`,`target2`,`target3`,`stop_loss`,`signal_date`, `signal_id`,`target4`,`currency`,`q_type`,`zone_type`,`zone`) VALUES (%s, %s,%s,%s, %s,%s,%s, %s,%s,%s,%s,%s,%s,%s)"
                # print(sql)
                dataList = []
                for item in data:
                    # print("my item - ",item)
                    tdata = (item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8],item[9],item[10],item[11],item[12],item[13])
                    dataList.append(tdata)
                    # print(tdata)
                # print(dataList)
                cursor.executemany(sql, dataList)
                self.cnx.commit()
            print("closing cnx")
            cursor.close()
            print("stopping server")
            # self.server.stop()

        except Exception as e:
            print(e)
            print("i m in exception")
            # self.server.stop()

######################################################### coinmarketcal ##############################
    def insertUpdate_coinmarketcal_categories(self,data):
        table_name = "coinmarketcal_categories"
        try:
            with self.cnx.cursor() as cursor:
                sql = "INSERT IGNORE INTO `" + table_name + "` (`cat_id`,`cat_name`) VALUES (%s,%s)"
                print(sql)

                print(data)
                # exit()

                cursor.executemany(sql,data)
                self.cnx.commit()
            print("closing cnx")
            cursor.close()
            print("stopping server")
            # self.server.stop()

        except Exception as e:
            print(e)
            print("i m in exception")
            # self.server.stop()


    def insertUpdate_coinmarketcal_coins(self,data):
        table_name = "coinmarketcal_coin"
        try:
            with self.cnx.cursor() as cursor:
                sql = "INSERT IGNORE INTO `" + table_name + "` (`coin_id`,`ID`,`name`,`symbol`) VALUES (%s,%s,%s,%s)"
                print(sql)

                # print(data)
                # exit()

                cursor.executemany(sql, data)
                self.cnx.commit()
            print("closing cnx")
            cursor.close()
            print("stopping server")
            # self.server.stop()

        except Exception as e:
            print(e)
            print("i m in exception")
            # self.server.stop()


    def get_coinmarketcal_coin_details(self):
        table_name = "coinmarketcal_coin"
        try:
            with self.cnx.cursor() as cursor:
                # get all records
                sql = "SELECT *from " + table_name + "` "
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)

            print("closing cnx")
            cursor.close()
            print("stopping server")
            # self.server.stop()
            return data

        except:
            print("i m in exception")
            # self.server.stop()

    def insertUpdate_coinmarketcal_events(self,data):
        table_name = "coinmarketcal_events"
        try:
            with self.cnx.cursor() as cursor:
                sql = "INSERT IGNORE INTO `" + table_name + "` (`event_id`,`title`,`date_event`,`created_date`,`description`,`proof`,`source`,`is_hot`,`vote_count`,`positive_vote_count`,`percentage`,`tip_symbol`,`tip_adress`,`can_occur_before`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                print(sql)
                # cursor.execute('SET CHARACTER SET utf8;')
                cursor.executemany(sql, data)
                self.cnx.commit()
            print("closing cnx")
            cursor.close()
            print("stopping server")
            # self.server.stop()

        except Exception as e:
            print(e)
            print("i m in exception")
            # self.server.stop()

    def insertUpdate_event_coin_ids(self,data):
        table_name = "coinmarketcal_events_coin"
        try:
            with self.cnx.cursor() as cursor:
                sql = "INSERT INTO `" + table_name + "` (`event_id`,`coin_id`,`coin_name`) VALUES (%s,%s,%s)"
                print(sql)
                cursor.executemany(sql, data)
                self.cnx.commit()
            print("closing cnx")
            cursor.close()
            print("stopping server")
            # self.server.stop()

        except Exception as e:
            print(e)
            print("i m in exception")
            # self.server.stop()

    def insertUpdate_event_cat_ids(self,data):
        table_name = "coinmarketcal_events_cat"
        try:
            with self.cnx.cursor() as cursor:
                sql = "INSERT INTO `" + table_name + "` (`event_id`,`cat_id`) VALUES (%s,%s)"
                print(sql)
                cursor.executemany(sql, data)
                self.cnx.commit()
            print("closing cnx")
            cursor.close()
            print("stopping server")
            # self.server.stop()

        except Exception as e:
            print(e)
            print("i m in exception")
            # self.server.stop()

    def del_all_events(self):
        table_events = "coinmarketcal_events"
        table_coinmarketcal_events_coin = "coinmarketcal_events_coin"
        table_coinmarketcal_events_cat = "coinmarketcal_events_cat"
        try:
            with self.cnx.cursor() as cursor:
                sql1 = "TRUNCATE TABLE " + table_events
                sql2 = "TRUNCATE TABLE " + table_coinmarketcal_events_coin
                sql3 = "TRUNCATE TABLE " + table_coinmarketcal_events_cat
                print(sql1)
                # exit()
                cursor.execute(sql1)
                cursor.execute(sql2)
                cursor.execute(sql3)
                self.cnx.commit()
            print("closing cnx")
            cursor.close()
            print("stopping server")
            # self.server.stop()

        except:
            print("i m in exception")
            # self.server.stop()



    ################################################# CRYPTO COMPARE #################################
    def insertUpdate_cryptoCompare_exchange_pairs(self,data):
        table_name = "cryptoCompare_exchange_pairs"
        try:
            with self.cnx.cursor() as cursor:
                sql = "INSERT INTO `" + table_name + "` (`exchange_name`,`symbol`,`currency`,`is_fiat_pair`) VALUES (%s,%s,%s,%s)"
                print(sql)
                cursor.executemany(sql, data)
                self.cnx.commit()
            print("closing cnx")
            cursor.close()
            print("stopping server")
            # self.server.stop()

        except Exception as e:
            print(e)
            print("i m in exception")
            # self.server.stop()

    def get_exchange_pair_data(self,is_fiat_pair):

        table_name = 'cryptoCompare_exchange_pairs'

        try:
            with self.cnx.cursor() as cursor:
                if is_fiat_pair == "True":
                    # print("i m in if")
                    # print(is_fiat_pair)
                    sql = "SELECT * FROM `"+table_name+"` WHERE is_fiat_pair = "+is_fiat_pair
                    print(sql)

                else:
                    sql = "SELECT * FROM " +table_name
                cursor.execute(sql)
                data = cursor.fetchall()

            print("closing cnx")
            cursor.close()
            print("stopping server")
            # self.server.stop()
            return data

        except:
            print("i m in exception")
            # self.server.stop()


    def get_priority_exchange_names(self,priority):
        # print(priority)
        # print(type(priority))
        # exit()
        table_name = 'cryptoCompare_prioroty_exchanges'
        print(table_name)
        try:
            with self.cnx.cursor() as cursor:
                print("i m in model")
                sql = "SELECT * FROM `" + table_name + "` WHERE priority = "+ str(priority)
                print(sql)
                # exit()
                cursor.execute(sql)
                data = cursor.fetchall()

            print("closing cnx")
            cursor.close()
            print("stopping server")
            # self.server.stop()
            return data

        except:
            print("i m in exception")
            # self.server.stop()



    def get_exchange_pair_data_by_exchange_name(self,is_fiat_pair,exchange_name):

        table_name = 'cryptoCompare_exchange_pairs'

        try:
            with self.cnx.cursor() as cursor:
                if is_fiat_pair == "True":
                    # print("i m in if")
                    # print(is_fiat_pair)
                    sql = "SELECT * FROM `"+table_name+"` WHERE is_fiat_pair = "+is_fiat_pair+ " and exchange_name = '"+exchange_name+"'"
                    print(sql)

                else:
                    sql = "SELECT * FROM " +table_name
                cursor.execute(sql)
                data = cursor.fetchall()

            print("closing cnx")
            cursor.close()
            print("stopping server")
            # self.server.stop()
            return data

        except:
            print("i m in exception")
            # self.server.stop()


    def get_exchange_pair_data_custom(self,is_fiat_pair,symbol,currency):

        table_name = 'cryptoCompare_exchange_pairs'

        try:
            with self.cnx.cursor() as cursor:
                if is_fiat_pair == "True":
                    # print("i m in if")
                    # print(is_fiat_pair)
                    sql = "SELECT * FROM `"+table_name+"` WHERE is_fiat_pair = "+is_fiat_pair+ " and symbol = '"+symbol+"'"+" and currency = '"+currency+"'"
                    print(sql)

                else:
                    sql = "SELECT * FROM " +table_name
                cursor.execute(sql)
                data = cursor.fetchall()

            print("closing cnx")
            cursor.close()
            print("stopping server")
            # self.server.stop()
            return data

        except:
            print("i m in exception")
            # self.server.stop()

    def get_symbol_from_cryptoCompare_coin_list(self):

        table_name = 'cryptoCompare_coin_list'

        try:
            with self.cnx.cursor() as cursor:
                #                 print('i m here')
                sql = "SELECT symbol FROM `" + table_name
                print(sql)
                cursor.execute(sql)
                data = cursor.fetchall()
                print("closing cnx")
                cursor.close()
                print("stopping server")
                # self.server.stop()
                return data

        except Exception as e:
            print(e)
            # self.server.stop()

    def insertUpdate_cryptoCompare_fiat_daily_data(self,data):
        table_name = "cryptoCompare_fiat_daily_data"
        # table_name = "cryptoCompare_fiat_daily_data"
        try:
            with self.cnx.cursor() as cursor:
                sql = "INSERT INTO `" + table_name + "` (`exchange_pair_id`,`date`,`open`,`high`,`low`,`close`,`volume_from`,`volume_to`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                print(sql)
                cursor.executemany(sql, data)
                self.cnx.commit()
            print("closing cnx")
            cursor.close()
            print("stopping server")
            # self.server.stop()

        except Exception as e:
            print(e)
            print("i m in exception")
            # self.server.stop()

    def insertUpdate_cryptoCompare_agg_daily_data(self,data):
        table_name = "cryptoCompare_agg_daily_data"
        try:
            with self.cnx.cursor() as cursor:
                sql = "INSERT INTO `" + table_name + "` (`sym`,`currency`,`date`,`open`,`high`,`low`,`close`,`volume_from`,`volume_to`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                print(sql)
                cursor.executemany(sql, data)
                self.cnx.commit()
            print("closing cnx")
            cursor.close()
            print("stopping server")
            # self.server.stop()

        except Exception as e:
            print(e)
            print("i m in exception")
            # self.server.stop()



    def insertUpdate_cryptoCompare_fiat_hourly_data_test(self,data):
        # table_name = "cryptoCompare_fiat_hourly_data"
        table_name = "cryptoCompare_fiat_hourly_test"
        try:
            with self.cnx.cursor() as cursor:
                sql = "INSERT INTO `" + table_name + "` (`exchange_pair_id`,`date`,`open`,`high`,`low`,`close`,`volume_from`,`volume_to`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                print(sql)
                cursor.executemany(sql, data)
                self.cnx.commit()
            print("closing cnx")
            cursor.close()
            print("stopping server")
            # self.server.stop()

        except Exception as e:
            print(e)
            print("i m in exception")
            # self.server.stop()

    def insertUpdate_cryptoCompare_fiat_hourly_data(self,data):
        # table_name = "cryptoCompare_fiat_hourly_data"
        table_name = "cryptoCompare_fiat_hourly_test"
        try:
            with self.cnx.cursor() as cursor:
                sql = "INSERT INTO `" + table_name + "` (`exchange_pair_id`,`date`,`open`,`high`,`low`,`close`,`volume_from`,`volume_to`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                print(sql)
                cursor.executemany(sql, data)
                self.cnx.commit()
            print("closing cnx")
            cursor.close()
            print("stopping server")
            # self.server.stop()

        except Exception as e:
            print(e)
            print("i m in exception")
            # self.server.stop()


    def insertUpdate_cryptoCompare_all_coin_list(self,data):
        table_name = "cryptoCompare_coin_list"
        try:
            with self.cnx.cursor() as cursor:
                sql = "INSERT IGNORE INTO `"+table_name+"` (`id`,`url`,`image_url`,`name`,`symbol`,`coin_name`,`full_name`,`algorithm`,`proof_type`,`fully_premined`,`total_coin_supply`,`premined_value`,`total_coins_free_float`,`sort_order`,`sponsored`,`is_trading`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                print(sql)
                cursor.executemany(sql, data)
                self.cnx.commit()
            print("closing cnx")
            cursor.close()
            print("stopping server")
            # self.server.stop()

        except Exception as e:
            print(e)
            print("i m in exception")
            # self.server.stop()

    def get_cryptoCompare_coin_list(self):
        table_name = "cryptoCompare_coin_list"
        try:
            with self.cnx.cursor() as cursor:
                # get all records
                sql = "SELECT *from " + table_name + "` "
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)

            print("closing cnx")
            cursor.close()
            print("stopping server")
            # self.server.stop()
            return data

        except:
            print("i m in exception")
            # self.server.stop()


    def get_fiat_symbols(self):
        table_name = "cryptoCompare_fiat_list"
        try:
            with self.cnx.cursor() as cursor:
                # get all records
                sql = "SELECT *from " + table_name + "` "
                cursor.execute(sql)
                data = cursor.fetchall()
                # print(result)

            print("closing cnx")
            cursor.close()
            print("stopping server")
            # self.server.stop()
            return data

        except:
            print("i m in exception")
            # self.server.stop()


    def update_cryptoCompare_fiat_list(self,data):
        table_name = "cryptoCompare_fiat_list"
        # print(data)
        # print(data[0])

        # exit()
        try:

                with self.cnx.cursor() as cursor:
                     # for item in data:
                         sql = "UPDATE " + table_name + " SET `currency_name` = %s, `exchange_rate` = %s WHERE `symbol` = %s"
                         print(sql)
                         for item in data:
                             print(item)
                             try:
                                cursor.execute(sql, (item[1],item[2],item[0]))
                                self.cnx.commit()
                             except Exception as e:
                                 print(e)

                print("closing cnx")
                cursor.close()
                print("stopping server")
            # self.server.stop()
        except:
                print("i m in exception")
                # self.server.stop()

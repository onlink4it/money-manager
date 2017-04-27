import MySQLdb
import datetime

### Connection To DB ###
def connect():
    config = {
      'user': 'amk6216',
      'passwd': 'OLPleaseN3verEnd',
      'host': '197.51.69.163',
      'db': 'radius',
    }
    cnx = MySQLdb.connect(**config)
    return cnx


### Get All Packages From DB ###
def get_all_packages():
    db = connect()
    sql = """
        SELECT
            srvname,srvid
        FROM
            rm_services
        """
    cursor = db.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    for x in results:
        count = get_users_by_package(x[1])
        if count > 0:
            print(x[0], " : ", count)


### Get How Many Active Users For Each Package ###
def get_users_by_package(srvid):
    db = connect()
    sql = """
        SELECT
            expiration,srvid
        FROM
            rm_users
        WHERE
            srvid =
        """ + str(srvid)
    cursor = db.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    count = 0
    for x in results:
        if x[0] > datetime.datetime.now():
            count += 1
        else:
            pass
    return count


### Get Active Users ###
def get_users():
    db = connect()
    sql = """
        SELECT
            username,expiration,srvid
        FROM
            rm_users
        """
    cursor = db.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    for x in results:
        if x[1] > datetime.datetime.now():
            calculate(x[2])
        else:
            pass

    print_details()
    return results


### Calculate Total Report ###
def calculate(srvid):
    global total_active
    global total_price
    global total_quota
    global total_speed
    results = get_packages(srvid)
    for x in results:
        active = 1
        price = x[1]
        quota = x[2]
        speed=  x[0]
    total_active += 1
    total_price += price
    total_quota += quota
    total_speed += speed


### Print Total Report ###
def print_details():
    print("Total Active = ", total_active, " Users")
    print("Total Price = ", total_price, " EGP")
    print("Total Speed = ", total_speed / 1024 / 1024, " Mbps")
    print("Total Quota = ", total_quota / 1024, " GB")


### Get Package Info ###
def get_packages(srvid):
    db = connect()
    sql = """
        SELECT
            downrate,unitprice,trafficunitcomb
        FROM
            rm_services
        WHERE
            srvid=""" + str(srvid)
    cursor = db.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    db.close()
    return results


while True:
    total_active = 0
    total_price = 0
    total_speed = 0
    total_quota = 0
    print("Hello To ON-Link Statics".center(50, '='))
    print("1- Get Packages")
    print("2- Get Users")
    print("3- Exit")
    option = input("\t \tPlease select an option:")
    if str(option) == '1':
        get_all_packages()
    elif str(option) == '2':
        get_users()
    elif str(option) == '3':
        break
    else:
        print(type(option), option)
        print("Please enter valid option")




from dbutils.steady_db import connect
import pymysql,sys
from dbutils.pooled_db import PooledDB
from pymysql import err
from util import ManageApi


def db_pool_link():
    #没有调试好！！！
    api = ManageApi()
    print("login:[{}]".format(api.login()))

    pool = PooledDB(pymysql, 
                    host="47.103.86.5",
                    db="bwpj_database",
                    user="bwpj_database",
                    password="SHSJPpYWj2CFAWLH",
                    port=3306,
                    charset='utf8',
                    cursorclass=pymysql.cursors.SSCursor
                    )

    conn = pool.connection()
    cs = conn.cursor()
    sql = "SELECT name,categorys,identifiers,is_used from qrcode_qrcode"
    try:
        cs.execute(sql)
        while True:
            result = cs.fetchone()
            if result:
                if(result[0] == ""):
                    pass
                a = api.postData(result[1],result[2],result[0],result[3])
                print("{}\tupload\t{}".format(result[0],a),flush=True)
            else:
                break
    except:
        pass
    cs.close()
    conn.close()

def db_link():
    api = ManageApi()
    print("login:[{}]".format(api.login()))
    connect = pymysql.connect(
        host="47.103.86.5",
        db="bwpj_database",
        user="bwpj_database",
        password="SHSJPpYWj2CFAWLH",
        port=3306,
        charset='utf8',
    )
    cur = connect.cursor()
    sql = "SELECT name,categorys,identifiers,is_used from qrcode_qrcode"
    try:
        cur.execute(sql)
        results = cur.fetchall()
        for result in results:
            a = api.postData(result[1],result[2],result[0],result[3])
            print("{}\tupload\t{}".format(result[0],a),flush=True)
    except err as e:
        print(e)
        
    pass

if(__name__ == "__main__"):
    db_link()
import json

from flask import Flask, redirect
from flask import render_template
from stellar_base.builder import Builder
from stellar_base.keypair import Keypair
import mysql.connector

"""
    # Find whether an account sent money
    http://horizon-testnet.stellar.org/accounts/GAFNKWN2GX7FCCSYLS36OUN2NIWJAU4UVZC44MVTQQX6HDAUZ2UUQL6I/transactions
"""

# connect to database
cn = mysql.connector.connect(user='root', password='123456789', database='db_stellarShop')
cursor = cn.cursor()

app = Flask(__name__)


def send_payment(amount, item, asset='XLM'):
    flag = False
    try:
        builder = Builder(secret=MEMBER_SEED)
        builder.append_payment_op(SITE_ADDR, amount, asset)
        builder.add_text_memo(item)
        builder.sign()
        s = builder.submit()
        print(s)
        flag = True
    except Exception as ex:
        print('Error in Payment')
        print(str(ex))
    finally:
        return flag


@app.route("/gen_address")
def gen_address():
    kp = Keypair.random()
    publickey = kp.address().decode()
    seed = kp.seed().decode()
    return json.dumps({'publickey': publickey, 'seed': seed})


@app.route("/thanks")
def thanks():
    return 'Thanks for your order'


@app.route("/pay", methods=['GET', 'POST'])
def pay():
    result = False
    item = 'Buyer - Jon Doe'

    amt = 10
    result = send_payment(amt, item)
    if result:
        return redirect("/thanks", code=302)
    else:
        return 'Invalid Transaction'


@app.route("/basket")
def basket():
    return render_template('basket.html')


@app.route("/checkout")
def checkout():
    return render_template('checkout.html')


@app.route("/")
def main():
    # k, s = gen_address()
    # print(k)
    # print(s)
    return render_template('home.html')


if __name__ == "__main__":

    user_shop = 'admin'
    pw_shop = 'admin'
    user_custom = 'custom1'
    pw_custom = 'custom1'
    
    cursor.execute("SELECT public_key, private_key FROM tbl_account WHERE user = '" + user_shop + "'" + " AND password = '" + pw_shop + "'")
    result_set = cursor.fetchall()
    SITE_ADDR, SITE_SEED = result_set[0][0:2]

    cursor.execute("SELECT public_key, private_key FROM tbl_account WHERE user = '" + user_custom + "'" + " AND password = '" + pw_custom + "'")
    result_set = cursor.fetchall()
    MEMBER_ADD, MEMBER_SEED = result_set[0][0:2]

    # print SITE_ADDR
    # print SITE_SEED
    # print MEMBER_ADD
    # print MEMBER_SEED
    # check shop account: https://horizon-testnet.stellar.org/accounts/GAFNKWN2GX7FCCSYLS36OUN2NIWJAU4UVZC44MVTQQX6HDAUZ2UUQL6I
    # SITE_ADDR = 'GAFNKWN2GX7FCCSYLS36OUN2NIWJAU4UVZC44MVTQQX6HDAUZ2UUQL6I'
    # SITE_SEED = 'SCC2V25EPMDLWUXNOJNLTBFXMWDHLLNJOY4DN5LWIEKFMYADNPW2OFXX'

    # MEMBER_ADD = 'GBYVSIXRDKJDHY5JGK6N37RFLZ2JDH3GDZPYOWXITQCWOCQ26VSRSXZF'
    # MEMBER_SEED = 'SBGUJJV6FSUL5S3AWH36XPYFIGGMAV3RQK7NSZWO7PTIS2ZCSPFVREGT'

    app.run(debug=True)

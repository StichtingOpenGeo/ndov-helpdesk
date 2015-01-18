from zmq.eventloop import ioloop
import protobix
import psycopg2

conn_string = "host='localhost' dbname='ndov-helpdesk' user='ndov-helpdesk'"

ioloop.install()

def zabbix_send():
    data = {
        'fr.ovapi.nl': {
            'ndovloket.aanmelding.verwerkt': 0,
            'ndovloket.aanmelding.ondertekend': 0,
            'ndovloket.aanmelding.fouten': 0,
            }
    }

    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()

    cursor.execute("""SELECT status, count(*) FROM signup_signupqueue WHERE status IN (1, 4, 5) GROUP BY status ORDER BY status;""")
    records = cursor.fetchall()

    if records[0][0] == '1':
        data['fr.ovapi.nl']['ndovloket.aanmelding.verwerkt'] = records[0][1]
        data['fr.ovapi.nl']['ndovloket.aanmelding.ondertekend'] = records[1][1]
        data['fr.ovapi.nl']['ndovloket.aanmelding.fouten'] = records[2][1]
    else:
        data['fr.ovapi.nl']['ndovloket.aanmelding.ondertekend'] = records[0][1]

    zbx_container = protobix.DataContainer("items", "localhost", 10051)
    zbx_container.add(data)

    ret = zbx_container.send(zbx_container)
    if not ret:
        print "Ooops. Something went wrong when sending data to Zabbix"
    else:
        print "Everything is OK"

myioloop = ioloop.IOLoop.instance()
myperiodiccallback = ioloop.PeriodicCallback(zabbix_send, 300000, myioloop)

myperiodiccallback.start()
myioloop.start()
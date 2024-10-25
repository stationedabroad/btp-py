import os
from flask import Flask
from cfenv import AppEnv
from hdbcli import dbapi


app = Flask(__name__)
env = AppEnv()

hana_service = 'hana'
hana = env.get_service(label=hana_service)

port = int(os.environ.get('PORT', 3000))

@app.route('/')
def server_reached():
    if hana is None:
        return "Can't connect to HANA service '{}' – check service name?".format(hana_service)
    
    
    conn = dbapi.connect(address=hana.credentials['host'],port=int(hana.credentials['port']), \
    user=hana.credentials['user'],password=hana.credentials['password'], \
    encrypt='true',sslTrustStore=hana.credentials['certificate'])
    
    cursor = conn.cursor()
    cursor.execute("select CURRENT_UTCTIMESTAMP from DUMMY")
    ro = cursor.fetchone()
    cursor.close()
    conn.close()

    return "Current time is: " + str(ro["CURRENT_UTCTIMESTAMP"])

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port)

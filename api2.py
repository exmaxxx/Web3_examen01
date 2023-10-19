# Call external libraries
import psycopg2
import locale
from flask import Flask, jsonify, abort, make_response, request

# Create default flask application
locale.setlocale(locale.LC_ALL, "es")
app = Flask(__name__)


# ================================================================
# D A T A A C C E S S C O D E
# ================================================================
# Function to execute data modification sentence
def execute(auxsql):
    data = None
    try:
        # Create data access object
        conex = psycopg2.connect(host='10.90.28.178',
                                 database='demo',
                                 user='instalador',
                                 password='utn12345')
        # Create local cursor to SQL executor
        cur = conex.cursor()
        # Execute SQL sentence
        cur.execute(auxsql)
        # Retrieve data if exists
        data = cur.fetchall()
        # close cursor
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conex is not None:
            conex.close()
    print('Close connection.')
    # Return data
    return data


# ================================================================
# A P I R E S T F U L S E R V I C E
# ================================================================
# -----------------------------------------------------
# Error support section
# -----------------------------------------------------
@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request....!'}), 400)


@app.errorhandler(401)
def unauthorized(error):
    return make_response(jsonify({'error': 'Unauthorized....!'}), 401)


@app.errorhandler(403)
def forbiden(error):
    return make_response(jsonify({'error': 'Forbidden....!'}), 403)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found....!'}), 404)


# Get Aircraft
@app.route('/aircraft', methods=['GET'])
def get_aircraft():
    resu = execute("select ad.aircraft_code, ad.model->'en', ad.range from aircrafts_data ad")
    if resu != None:
        salida = {"status_code": 200,
                  "status": "OK",
                  "data": []
                  }
    for cod, modelo, rango in resu:
        salida["data"].append({
            "code": cod,
            "model": modelo,
            "range": rango
        })
    else:
        abort(404)
    return jsonify({'data': salida}), 200

    # Get Aeropuertos
@app.route('/aircraft', methods=['GET'])
def get_aircraft():
        resu = execute("select ad.airport_code, ad.airport_name ->'en', ad.city ->'en', ad.coordinates, ad.timezone from airports_data ad")
        if resu != None:
                salida = {"status_code": 200,
                            "status": "OK",
                            "data": []
                          }
        for cod, modelo, rango in resu:
                salida["data"].append({
                    "code": code,
                    "Airport": airport,
                    "City": city,
                    "Cordenada": coordinates,
                    "Time": time
            })
        else:
            abort(404)
            return jsonify({'data': salida}), 200

    # Get Pasageros
@app.route('/aircraft', methods=['GET'])
def get_travelers():
        resu = execute("select ad.flight_no, ad.scheduled_departure, ad.scheduled_arrival, ad.departure_airport, ad.arrival_airport, g.passenger_id, g.passenger_name, c.fare_conditions, g.contact_data from flights ad inner join ticket_flights c on ad.flight_id = c.flight_id inner jointickets g on c.ticket_no = g.ticket_no")
        if resu != None:
            salida = {"status_code": 200,
                    "status": "OK",
                    "data": []
                    }
        for cod, modelo, rango in resu:
            salida["data"].append({
                "Vuelo": codi,
                "Aeropuerto Salida": departure,
                "Aeropuerto Llegada": arribal,
                "Hora Salida": time_departure,
                "Hora Llegada": time_arribal,
                "ID del Pasagero": id,
                "Nombre del pasagero": nombre,
                "Clase en la que viaja": clase,
                "Datos del pasagero": datos
            })
        else:
            abort(404)
        return jsonify({'data': salida}), 200

# -----------------------------------------------------
# Create thread app
# -----------------------------------------------------
if __name__ == '__main__':
    app.run(host='10.90.28.178', port=5001, debug=True)

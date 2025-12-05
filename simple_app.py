from flask import Flask, request, jsonify, render_template
import mysql.connector as connector
import uuid
from hashlib import sha256
import ecdsa
import datetime
import json
from flask_cors import CORS, cross_origin

# app.config['CORS_HEADERS'] = 'Content-Type'

# cors = CORS(app, resources={r"/*": {"origins": "http://localhost:port"}})

app = Flask(__name__)
# app.config['CORS_HEADERS'] = 'Content-Type'
private_key = ecdsa.SigningKey.from_string(bytes.fromhex("81e54fb13a011093019fc1b369dc178bf2debfdf06de6071a7656cb8ddab8465"), curve=ecdsa.SECP256k1)

conn = connector.connect(
    host='localhost',
    user='root',
    password='localhost',
    database='Students_Info'
)

mycursor = conn.cursor()

@app.route('/')
@cross_origin()
def index():
    return render_template('./index.html')

def authorization_transaction(session_id, account_id):
    if session_id == "":
        return -1
    sql = "SELECT id, session_token FROM Students_info.accounts WHERE id=%s AND session_token=%s;"
    val = (account_id, session_id)
    mycursor.execute(sql, val)
    result = mycursor.fetchall()
    if len(result) == 0:
        return -1
    return 0

def authenticate_login(val):
    sql = "SELECT id, password FROM Students_info.accounts WHERE id=%s AND password=%s;"
    val_tuple = (val['id'], val['password'])
    mycursor.execute(sql, val_tuple)
    result = mycursor.fetchone()
    if len(result) == 0:
        return False
    return result[0]

@app.route('/get_session_token/<account_id>', methods=['POST'])
@cross_origin()
def get_session_token(account_id):
    val = request.json
    account_id = authenticate_login(val)
    if account_id != False:
        sql = "SELECT session_token, public_key FROM Students_info.accounts WHERE id=%s;"
        val = (account_id,)
        mycursor.execute(sql, val)
        result = mycursor.fetchone()
        if len(result) == 0:
            return jsonify({"error": "wrong password but account id is present"}), 401
        return jsonify({"session_token": result[0], "id": account_id, "public_key": result[1]}), 201
    else:
        return jsonify({"error": "Unauthorized"}), 401


@app.route("/create_account", methods=['POST'])
@cross_origin()
def create_account():
    val = request.json
    id=str(uuid.uuid1())
    sql = "INSERT INTO Students_info.accounts (id, public_key, password, session_token, tokern_created_time) VALUES(%s, %s, %s, %s, %s);"
    session_token = sha256(str(uuid.uuid1()).encode(encoding="utf-8")).hexdigest()
    val_tuple = (id, val['public_key'], val['password'], session_token, datetime.datetime.now())
    mycursor.execute(sql, val_tuple)
    conn.commit()
    return jsonify({"message": "Account created successfully. Please login to create session token to continue further.", "account_id": id, "session_token": session_token, }), 201

@app.route('/all_students/<account_id>', methods=['GET'])
@cross_origin()
def get_all_students(account_id):
    session_id = request.headers.get('Authorization')
    if authorization_transaction(session_id, account_id) == -1:
        return jsonify({"error": "Unauthorized"}), 401
    sql = "SELECT id, name, course, joining_year, graduated_year FROM Students_info.students_info;"
    mycursor.execute(sql)
    students = mycursor.fetchall()
    return jsonify(students)

@app.route('/students_uploaded/<account_id>', methods=['GET'])
@cross_origin()
def get_students_uploaded(account_id):
    sql = "SELECT id, name, course, joining_year, graduated_year FROM Students_info.students_info where account_id=%s;"
    val = (account_id,)
    mycursor.execute(sql, val)
    students = mycursor.fetchall()
    return jsonify(students)

@app.route("/action_log/<account_id>", methods=['POST'])
@cross_origin()
def action_log(account_id):
    val = request.json
    header = request.headers.get('Authorization')
    if authorization_transaction(header, account_id) == -1:
        return jsonify({"error": "Unauthorized"}), 401
    sql = "INSERT INTO Students_info.action_logs (public_key, signature, message, action_type, verified, creater_id, transaction_id) VALUES(%s, %s, %s, %s, %s, %s, %s);"
    transaction_id = str(uuid.uuid1())
    val_tuple = (val['public_key'], val['signature'], json.dumps(val['message']), val['action_type'], False, account_id, transaction_id)
    mycursor.execute(sql, val_tuple)
    conn.commit()
    return jsonify({"message": "Action log added successfully"}), 201

@app.route("/unverified_action_log_list/<account_id>", methods=['GET'])
@cross_origin()
def get_unverified_action_logs(account_id):
    header = request.headers.get('Authorization')
    if authorization_transaction(header, account_id) == -1:
        return jsonify({"error": "Unauthorized"}), 401
    sql = "SELECT transaction_id, message FROM Students_info.action_logs WHERE verified=%s;"
    val = (0,)
    mycursor.execute(sql, val)
    result = mycursor.fetchall()
    return jsonify(result), 200

@app.route("/verify_action/<account_id>", methods=['POST'])
@cross_origin()
def verify_log_in_action_logs(account_id):
    req = request.json
    header = request.headers.get('Authorization')
    if authorization_transaction(header, account_id) == -1:
        return jsonify({"error": "Unauthorized"}), 401
    
    sql = "SELECT action_type, public_key, signature, message FROM Students_info.action_logs WHERE transaction_id=%s;"
    val = (req['transaction_id'],)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    if result is None:
        return jsonify({"error": "No action log found for verification"}), 404
    publick_key = ecdsa.VerifyingKey.from_string(bytes.fromhex(result[1]), curve=ecdsa.SECP256k1)
    print(bytes.fromhex(result[2]))
    print(json.dumps(json.loads(result[3])).encode('utf-8'))
    verify = publick_key.verify(bytes.fromhex(result[2]), json.dumps(json.loads(result[3])).encode('utf-8'))
    if verify:
        if result[0] == "add":
            data=json.loads(result[3])
            if data is None:
                return jsonify({"error": "No data found for update"}), 404
            sql = "INSERT INTO Students_info.students_info (id, account_id, Name, course, joining_year, graduated_year) VALUES(%s, %s, %s, %s, %s, %s);"
            val_tuple = (str(uuid.uuid1()), account_id, data['Name'], data['course'], data['joining_year'], data['graduated_year'])
            mycursor.execute(sql, val_tuple)
            conn.commit()
            
            sql = "UPDATE Students_info.action_logs SET verified=%s WHERE transaction_id=%s;"
            val_tuple = (True, req['transaction_id'])
            mycursor.execute(sql, val_tuple)
            conn.commit()
            return jsonify({"message": "Action verified and updated successfully"}), 201
        elif result[0] == "delete":
            data=json.loads(result[3])
            if data is None:
                return jsonify({"error": "No data found for update"}), 404
            sql = "DELETE FROM Students_info.students_info WHERE id=%s;"
            val_tuple = (data['id'],)
            mycursor.execute(sql, val_tuple)
            conn.commit()
            
            sql = "UPDATE Students_info.action_logs SET verified=%s WHERE transaction_id=%s;"
            val_tuple = (True, req['transaction_id'])
            mycursor.execute(sql, val_tuple)
            conn.commit()
            return jsonify({"message": "Action verified and deleted successfully"}), 201
        elif result[0] == "update":
            data=json.loads(result[3])
            if data is None:
                return jsonify({"error": "No data found for update"}), 404
            if data["id"] == "":
                return jsonify({"error": "Student id is required for update"}), 400
            sql = "UPDATE Students_info.students_info SET Name=%s, course=%s, joining_year=%s, graduated_year=%s WHERE id=%s;"
            val_tuple = (data['Name'], data['course'], data['joining_year'], data['graduated_year'], data['id'])
            mycursor.execute(sql, val_tuple)
            conn.commit()
            
            sql = "UPDATE Students_info.action_logs SET verified=%s WHERE transaction_id=%s;"
            val_tuple = (True, req['transaction_id'],)
            mycursor.execute(sql, val_tuple)
            conn.commit()
            return jsonify({"message": "Action verified and updated successfully"}), 201
        else:
            return jsonify({"error": "Invalid action type"}), 400
    else:
        return jsonify({"error": "Signature verification failed"}), 400

@app.route('/action_log_status/<transaction_id>', methods=['GET'])
@cross_origin()
def get_transaction_status(transaction_id):
    sql = "SELECT verified FROM Students_info.action_logs WHERE transaction_id=%s;"
    val = (transaction_id,)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    if result is None:
        return jsonify({"error": "Transaction not found"}), 404
    return jsonify({"status": result[0]}), 200

@app.route('/generate_signature', methods=['POST'])
@cross_origin()
def generate_signature():
    val = request.json
    message = val['message']
    byte_wise_json = json.dumps(json.loads(message)).encode('utf-8')
    private_key = ecdsa.SigningKey.from_string(bytes.fromhex(val['private_key']), curve=ecdsa.SECP256k1)
    signature = private_key.sign_deterministic(byte_wise_json)
    public_key = private_key.get_verifying_key()
    print(byte_wise_json)
    print(signature)
    print(signature.hex())
    print(public_key.verify(signature, byte_wise_json))
    return jsonify({"signature": signature.hex()}), 201

@app.route('/generate_keys', methods=['GET'])
@cross_origin()
def generate_keys():
    private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    public_key = private_key.get_verifying_key()
    return jsonify({
        "private_key": private_key.to_string().hex(),
        "public_key": public_key.to_string().hex()
    }), 200

if __name__ == '__main__':
    app.run(port=8080,debug=False)
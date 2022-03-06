from flask_session import Session
from flask import Flask, render_template, request, session
import time
import datetime



app = Flask(__name__) # Creating our Flask Instance


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

logs = []
logs_request = []



@app.route('/', methods=['GET'])
def index():
    """ Displays the index page accessible at '/' """
    method = request.method
    ip_address = request.remote_addr
    now = datetime.datetime.now()
    date_time = now.strftime("%d/%m/%Y %H:%M:%S")
    args = request.url
    image='/static/' + 'cartoon.jpg'
    # image_file = url_for('static', filename='cartoon.jpg')

    if session.get("logs") is None:
        session["logs"] = []

    if session.get("logs_request") is None:
        session["logs_request"] = []
    
    session["logs_request"].append(["IP Address: " + str(ip_address)+  " TimeStamp: " +str(date_time) +  " Method: "+str(method) + " " + str(args)])
    L = len(session["logs"])
    R = len(session["logs_request"])
    return render_template('index.html', image=image ,L=L, R=R , logs= session["logs"] , logs_for_request= session["logs_request"])



@app.route('/operation_result/', methods=['GET','POST'])
def operation_result():
    """Route where we send calculator form input"""

    error = None
    result = None
    
    
    method = request.method
    ip_address = request.remote_addr
    now = datetime.datetime.now()
    date_time = now.strftime("%d/%m/%Y %H:%M:%S")
    args = request.url
    image='/static/' + 'cartoon.jpg'

    if request.method == 'GET':
        # session["logs_request"].append("IP Address:" + str(ip_address) +  " TimeStamp: " +str(date_time) +  "Method: "+str(method) +"]")
        session["logs_request"].append(["IP Address: " + str(ip_address)+  " TimeStamp: " +str(date_time) +  " Method: "+str(method) + " " + str(args)])

        if session.get("logs") is None:
            session["logs"] = []

        if session.get("logs_request") is None:
            session["logs_request"] = []

        L = len(session["logs"])
        R = len(session["logs_request"])
        return render_template('index.html',image=image,logs= session["logs"],L=L, R=R ,logs_for_request= session["logs_request"])
    
    else:

        if len(session["logs"]) == 21:
            time.sleep(120)
            session["logs"] = []
            session["logs_request"] = []  




        if session.get("logs") is None:
            session["logs"] = []

        if session.get("logs_request") is None:
            session["logs_request"] = []




        # request.form looks for:
        # html tags with matching "name= "
        first_input = request.form['Input1']  
        second_input = request.form['Input2']
        operation = request.form['operation']

        try:
            input1 = float(first_input)
            input2 = float(second_input)

            # On default, the operation on webpage is addition
            if operation == "+":
                result = input1 + input2

            elif operation == "-":
                result = input1 - input2

            elif operation == "/":
                result = input1 / input2 

            elif operation == "*":
                result = input1 * input2

            else:
                operation = "%"
                result = input1 % input2

            session["logs"].append(str(first_input) + str(operation) + str(second_input) + " = " + str(result))
            session["logs_request"].append(["IP Address: " + str(ip_address)+  " TimeStamp: " +str(date_time) +  " Method: "+str(method) + " " + str(args)])
            
            # session["logs_request"].append("[IP Address: " + str(ip_address)+ "]"+  " [TimeStamp: " +str(date_time) + "]" +  " [Method: "+str(method) +"]")

            if len(session["logs"]) != 20:
                L = len(session["logs"])
                R = len(session["logs_request"])
                
                return render_template(
                'index.html',
                input1=input1,
                input2=input2,
                operation=operation,
                result=result,
                calculation_success=True,
                logs=session["logs"], L = L, R=R, logs_for_request = session["logs_request"],
                image=image
                )
            
            elif len(session["logs"]) == 20:
                session["logs"].append(" Wait for 2 minutes ")
                session["logs_request"].append(" Wait for 2 minutes")
                L = len(session["logs"])
                R = len(session["logs_request"])
                return render_template('index.html',image=image, L=L, R=R ,logs=session["logs"], logs_for_request = session["logs_request"] )
            
            else: 
                pass





            
        
            
        except ZeroDivisionError:
            return render_template(
                'index.html',
                input1=input1,
                input2=input2,
                operation=operation,
                result="Bad Input",
                calculation_success=False,
                error="You cannot divide by zero",
                logs=session["logs"],
                logs_for_request = session["logs_request"],
                image=image
            )
            
        except ValueError:
            return render_template(
                'index.html',
                input1=first_input,
                input2=second_input,
                operation=operation,
                result="Bad Input",
                calculation_success=False,
                error="Cannot perform numeric operations with provided input",
                logs=session["logs"],
                logs_for_request = session["logs_request"],
                image=image
            )

        

# @Flask_App.after_request
# def after_request(response):
#     timestamp = strftime('[%Y-%b-%d %H:%M]')
#     logger.error('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
#     return response

# print(response)

if __name__ == '__main__':

    app.run(host='127.0.0.1', port=8080, debug=True)



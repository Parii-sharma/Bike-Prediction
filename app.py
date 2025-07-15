from flask import Flask , render_template, request, url_for
import joblib
import csv
model = joblib.load('model.joblib')
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')
@app.route("/contact")
def contact():
    return render_template('contact.html')
# @app.route("/history")
# def history():
#     return render_template('history.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/project', methods = ["POST","GET"])
def predict():
    if request.method=='POST':
        brand_name=request.form['brand_name']
        owner = request.form['owner']
        age = request.form['age']
        power = request.form['power']
        kms_driven=request.form['kms_driven']
        # print("My Data >>>>>>>>>>>>>", brand_name,age,owner,power,kms_driven)

        brand_dict = {
    'TVS':1,
    'Royal Enfield':2,
    'Triumph':3,
    'Yamaha':4,
    'Honda':5,
    'Hero':6,
    'Bajaj':7,
    'Suzuki':8,
    'Benelli':9,
    'KTM':10,
    'Mahindra':11,
    'Kawasaki':12,
    'Ducati':13,
    'Hyosung':14,
    'Harley-Davidson':15,
    'Jawa':16,
    'BMW':17,
    'Indian':18,
    'Rajdoot':19,
    'LML':20,
    'Yezdi':21,
    'MV':22,
    'Ideal':23
              }
    
        brand_name=brand_dict[brand_name]
        print("My Data >>>>>>>>>>>>>", brand_name,age,owner,power,kms_driven)
        lst = [[brand_name,owner,age,power,kms_driven]]

        prediction=model.predict(lst)
        rounded_prediction = round(prediction[0], 2)
        print("prediction:-", prediction)
        # Record prediction in history.csv
        with open('history.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([rounded_prediction, owner, request.form['brand_name'], kms_driven, age, power])
        return render_template('project.html', prediction=rounded_prediction,
                            brand_name=request.form['brand_name'],
                            owner=owner,
                            age=age,
                            power=power,
                            kms_driven=kms_driven)

    return render_template('project.html',
        prediction=None,
        brand_name='',
        owner='',
        age='',
        power='',
        kms_driven=''
    )


#     brand_dict= dt2[brand_name]
#     data = [[brand_name,owner,age,power,kms_driven]]
    


@app.route('/history')
def history():
    historical_data = []
    try:
        with open('history.csv', 'r') as f:
            reader = csv.reader(f)
            historical_data = list(reader)
    except FileNotFoundError:
        pass
    return render_template('history.html', historical_data=historical_data)

if __name__ == "__main__":
    app.run(debug = True)
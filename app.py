from flask import *
from flask.templating import render_template
import pickle
import numpy as np

app = Flask(__name__)
model = pickle.load(open('Loan_Predict.pkl', 'rb'))

# Home Page
@app.route('/')
def about() :
    return render_template('/about.html')

@app.route('/submit',methods=['POST','GET'])
def submit():
    if request.method ==  'POST':
        gender = request.form['gender']
        married = request.form['married']
        dependents = request.form['dependents']
        education = request.form['education']
        employed = request.form['employed']
        ApplicantIncome = float(request.form['applicantIncome'])
        CoapplicantIncome = float(request.form['coapplicantIncome'])
        LoanAmount = float(request.form['loanAmount'])
        loanamountterm = float(request.form['loan_Amount_Term'])
        credit = request.form['credit']
        area = request.form['area']

        
        # totalincomelog
        totalincomelog = np.log(ApplicantIncome+CoapplicantIncome)
        print('Log of Total Income : ' + str(totalincomelog))

        # loanamountlog
        loanamountlog = np.log(LoanAmount)
        print('Log of Loan Amount : ' + str(loanamountlog))
        
        # loanamountterm
        print('Loan Amount Term: ' + str(loanamountterm))

        # credithistory
        if(credit == "No"):
            credit_hist = 0
        else:
            credit_hist = 1
        print('Credit History : ' + str(credit_hist))

        # gender
        if (gender == "Male"):
            gender_male = 1
            gender_none = 0
        elif (gender == "Female"):
            gender_male = 0
            gender_none = 0
        else:
            gender_male = 0
            gender_none = 1
        print('Gender Bytes : ' + str(gender_male) + ' '+ str(gender_none))

        # married
        if(married=="Yes"):
            married_yes = 1
        else:
            married_yes=0
        print('Married : ' + str(married_yes))

        # dependents
        if(dependents=='1'):
            dependents_1 = 1
            dependents_2 = 0
            dependents_3 = 0
            dependents_n = 0
        elif(dependents == '2'):
            dependents_1 = 0
            dependents_2 = 1
            dependents_3 = 0
            dependents_n = 0
        elif(dependents=="3+"):
            dependents_1 = 0
            dependents_2 = 0
            dependents_3 = 1
            dependents_n = 0
        elif(dependents=="None"):
            dependents_1 = 0
            dependents_2 = 0
            dependents_3 = 0
            dependents_n = 1
        else:
            dependents_1 = 0
            dependents_2 = 0
            dependents_3 = 0
            dependents_n = 0
        print('Dependent Bytes : ' + str(dependents_1) + ' '+ str(dependents_2)+' '+str(dependents_3) + ' '+ str(dependents_n))

        # education
        if (education=="Not Graduate"):
            not_graduate=1
        else:
            not_graduate=0
        print('Not Graduate : ' + str(not_graduate))

        # employed
        if (employed == "Yes"):
            employed_yes=1
            employed_none=0
        elif(employed == "No"):
            employed_yes=0
            employed_none=0
        else:
            employed_yes=0
            employed_none=1
        print('Employed Bytes : ' + str(employed_none) + ' '+ str(employed_yes))

        # property area
        if(area=="Semiurban"):
            semiurban=1
            urban=0
        elif(area=="Urban"):
            semiurban=0
            urban=1
        else:
            semiurban=0
            urban=0
        print('Property Area Bytes : ' + str(semiurban) + ' '+ str(urban))

        # Prediction using ML Model
        prediction = model.predict([[totalincomelog,loanamountlog,loanamountterm,credit_hist,gender_male,gender_none,married_yes,dependents_1,dependents_2,dependents_3,dependents_n,not_graduate,employed_none,employed_yes,semiurban,urban]])
        print('Prediction : ' + str(prediction[0]))
    

        if(prediction == 0):
            prediction = "No"
        else:
            prediction = "Yes"

        #return render_template("result.html", result = prediction)
        #return "Loan Sanctioned? " + prediction
        return redirect(url_for('result',Loan_Status=prediction))

@app.route('/result/<Loan_Status>')
def result(Loan_Status):
    return render_template('result.html',result=Loan_Status)


# Application Execution Starts from here
if __name__ == '__main__':
    app.run(debug=True,port=8000)
from flask import Flask, render_template, request
import pandas as pd
import pickle
import numpy as np

app = Flask(__name__)
model = pickle.load(open("linearRegModel.pkl", "rb"))
modelbike = pickle.load(open("BikelinearReg.pkl","rb"))
modellap = pickle.load(open("LaptopRanForpipe.pkl","rb"))


@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/selectedItems',methods=['GET'])
def selectedItems():
   if request.method == 'GET':
        if request.args['selectedItems'] == 'Car':
            return render_template('Carmodel.html')

   if request.method == 'GET':
       if request.args['selectedItems'] == 'Bike':
           return render_template('Bikemodel.html')

   if request.method == 'GET':
       if request.args['selectedItems'] == 'Laptop':
           return render_template('Laptopmodel.html')


@app.route('/predict', methods=['GET'])
def predict():
    if request.method == 'GET':
        CarName=request.args['CarName']
        CarCompany=request.args['CarCompany']
        CarPurchaseYear=int(request.args['CarPurchaseYear'])
        fuel_type=request.args['fuel_type']
        kms_driven=int(request.args['kms_driven'])

        prediction = model.predict(pd.DataFrame([[CarName,CarCompany,CarPurchaseYear,kms_driven,fuel_type]], columns=['name','company','year','kms_driven','fuel_type'] ))
        prediction = "{:.2f}".format(abs(prediction[0]))
        return render_template('CarPricePred.html',
                               prediction=prediction ,
                               CarName=CarName,
                               CarCompany=CarCompany,
                               CarPurchaseYear=CarPurchaseYear,
                               fuel_type=fuel_type,
                               kms_driven=kms_driven,
                               )

@app.route('/predictbike',methods=['GET'])
def predictbike():
    if request.method == 'GET':
        BikeName=request.args['BikeName']
        BikeCompany=request.args['BikeCompany']
        BikePurchaseCity=request.args['BikePurchaseCity']
        Owner=request.args['Owner']
        kms_driven=request.args['kms_driven']
        age=request.args['age']
        Power=request.args['Power']

        prediction = modelbike.predict(pd.DataFrame([[BikeName, BikePurchaseCity, kms_driven, Owner, age,Power,BikeCompany]],
                                                columns=['bike_name', 'city', 'kms_driven', 'owner', 'age','power','brand']))

        prediction = "{:.2f}".format(abs(prediction[0]))
        return render_template('BikePricePred.html',
                               prediction=prediction,
                               BikeName=BikeName,
                               BikeCompany=BikeCompany,
                               BikePurchaseCity=BikePurchaseCity,
                               Owner=Owner,
                               kms_driven=kms_driven,
                               age=age,
                               Power=Power,
                               )

@app.route('/predictlaptop',methods=['GET'])
def predictlaptop():
    if request.method == 'GET':
        Laptop=request.args['Laptop']
        LaptopType=request.args['LaptopType']
        Cpu_Brand=request.args["Cpu_Brand"]
        HDD=request.args['HDD']
        SDD=request.args['SDD']
        Gpubrand=request.args['Gpu brand']
        OS = request.args['OS']
        RAM = request.args['RAM']
        Weight = request.args['Weight']
        Touchscreen = request.args['Touchscreen']
        IPS = request.args['IPS']
        PPI = request.args['PPI']
        prediction = modellap.predict(pd.DataFrame([[Laptop, LaptopType, RAM, Weight, Touchscreen,IPS,PPI,Cpu_Brand,HDD,SDD,Gpubrand,OS]],
                                                columns=['Company', 'TypeName', 'Ram', 'Weight', 'Touchscreen','IPS','ppi','Cpu_Brand','HDD','SSD' ,'Gpu brand','os']))
        prediction = "{:.2f}".format(abs(prediction[0]))

        return render_template('laptopPricePred.html',
                               prediction=prediction,
                               Laptop=Laptop,
                               LaptopType=LaptopType,
                               RAM=RAM,
                               Cpu_Brand=Cpu_Brand,
                               Gpubrand=Gpubrand,
                               OS=OS,
                               )


if __name__ == '__main__':
    app.run()
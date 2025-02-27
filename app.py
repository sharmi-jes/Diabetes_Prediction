from flask import Flask,request,render_template
import os

from sklearn.preprocessing import LabelEncoder,StandardScaler
from Diabetetic.pipeline.train_pipeline import CustomData,TrainingPipeline
from Diabetetic.logging import logging

app=Flask(__name__)

@app.route("/")
def index():
    return render_template("home.html")



# gender,age,hypertension,heart_disease,smoking_history,bmi,HbA1c_level,blood_glucose_level
@app.route("/predict",methods=["GET","POST"])
def predict_datapoint():
    if request.method=="GET":
        return render_template("index.html")
    else:
        data=CustomData(
            gender=request.form.get("gender"),
            age=request.form.get("age"),
            hypertension=request.form.get("hypertension"),
            heart_disease=request.form.get("heart_disease"),
            smoking_history=request.form.get("smoking_history"),
            bmi=request.form.get("bmi"),
            HbA1c_level=request.form.get("HbA1c_level"),
            blood_glucose_level=request.form.get("blood_glucose_level"),

        )

        data_frame=data.input_data_as_dataframe()
        print(data_frame)
        
        logging.info("take the predict method from the training pipeline class") 
        training_pipeline=TrainingPipeline()
        results= training_pipeline.predict(data_frame)

        if results[0]==0:
             print("The person have no diabetic")
        else:
            print("The person have a diabetic")

        return render_template('index.html',results=results[0])
    

if __name__ == "__main__":
    app.run(debug=True)
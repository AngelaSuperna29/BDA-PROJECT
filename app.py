import streamlit as st
from pyspark.ml.regression import LinearRegressionModel
from pyspark.ml.feature import VectorAssembler
from pyspark.sql import SparkSession
from pyspark.sql.types import FloatType

# Initialize Spark Session
spark = SparkSession.builder.appName("RideShareDeployment").getOrCreate()

# Load the trained model
model_path = "/content/linear_regression_model"
model = LinearRegressionModel.load(model_path)

# Streamlit UI
st.title("Ride Price Prediction")

# User inputs
distance = st.number_input("Enter Distance (miles)", min_value=0.1, step=0.1)
surge_multiplier = st.number_input("Enter Surge Multiplier", min_value=1.0, step=0.1)

if st.button("Predict Price"):
    # Convert input to Spark DataFrame
    input_data = spark.createDataFrame([(distance, surge_multiplier)], ["distance", "surge_multiplier"])
    
    # Feature transformation
    assembler = VectorAssembler(inputCols=["distance", "surge_multiplier"], outputCol="features")
    input_transformed = assembler.transform(input_data)
    
    # Prediction
    prediction = model.transform(input_transformed).select("prediction").collect()[0][0]
    
    st.success(f"Estimated Ride Price: ${prediction:.2f}")

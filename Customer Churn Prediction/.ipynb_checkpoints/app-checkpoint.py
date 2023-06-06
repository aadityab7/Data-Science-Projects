from flask import Flask, render_template, request

app = Flask(__name__)

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle form submission
@app.route('/predict', methods=['POST'])
def predict():
    # Retrieve the form data
    age = int(request.form['age'])
    gender = request.form['gender']
    subscription_type = request.form['subscription_type']
    has_internet = request.form['has_internet']

    # Perform the prediction using your machine learning model
    # Replace the following lines with your own prediction code
    prediction = "Churn" if age > 30 else "Not churn"

    # Render the prediction result in a new template
    return render_template('result.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)

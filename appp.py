from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Create static folder if not exists
if not os.path.exists("static"):
    os.makedirs("static")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    soil = float(request.form['soil'])
    temp = float(request.form['temp'])
    humidity = float(request.form['humidity'])
    rainfall = float(request.form['rainfall'])

    # Smart irrigation logic
    if soil < 60 and rainfall < 2:
        result = "Irrigation Required"
        irrigation_value = 1
    else:
        result = "No Irrigation Needed"
        irrigation_value = 0

    # -------- BAR CHART --------
    parameters = ['Soil', 'Temperature', 'Humidity', 'Rainfall']
    values = [soil, temp, humidity, rainfall]

    plt.figure()
    plt.bar(parameters, values)
    plt.title("Environmental Parameters")
    plt.xlabel("Parameters")
    plt.ylabel("Values")
    plt.savefig("static/bar_chart.png")
    plt.close()

    # -------- PIE CHART --------
    labels = ['Irrigation Needed', 'No Irrigation']
    sizes = [irrigation_value, 1 - irrigation_value]

    plt.figure()
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.title("Irrigation Decision")
    plt.savefig("static/pie_chart.png")
    plt.close()

    return render_template('index.html',
                           prediction_text=result,
                           show_graph=True)

if __name__ == '__main__':
    app.run(debug=True)

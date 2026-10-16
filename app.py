from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "55d6448c269aa35f4305d6fb5339b356"

@app.route("/")
def home():
    return render_template("hiking.html")

@app.route("/check", methods=["POST"])
def check():
    location = request.form["location"]
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if data["cod"] != 200:
        return render_template("hiking.html", error="Location not found!")

    temp = round(data["main"]["temp"])
    wind = data["wind"]["speed"]
    humidity = data["main"]["humidity"]
    visibility = round(data.get("visibility", 0) / 1000, 1)
    description = data["weather"][0]["description"].capitalize()
    clouds = data["clouds"]["all"]
    icon = data["weather"][0]["icon"]

    # Hiking verdict logic
    score = 0
    reasons = []

    if 5 <= temp <= 22:
        score += 1
    else:
        reasons.append(f"Temperature is {temp}°C — not ideal for hiking")

    if wind < 30:
        score += 1
    else:
        reasons.append(f"Wind is {wind} m/s — too windy!")

    if humidity < 80:
        score += 1
    else:
        reasons.append(f"Humidity is {humidity}% — very muggy")

    if clouds < 70:
        score += 1
    else:
        reasons.append("Heavy cloud cover")

    if score == 4:
        verdict = "Perfect hiking day! 🥾"
        verdict_color = "#7fff7f"
    elif score >= 2:
        verdict = "Decent day — go for it! ⚠️"
        verdict_color = "#ffd700"
    else:
        verdict = "Stay home today! ❌"
        verdict_color = "#e94560"

    conditions = {
        "location": data["name"],
        "country": data["sys"]["country"],
        "temp": temp,
        "wind": wind,
        "humidity": humidity,
        "visibility": visibility,
        "description": description,
        "icon": icon,
        "verdict": verdict,
        "verdict_color": verdict_color,
        "reasons": reasons
    }

    return render_template("hiking.html", conditions=conditions)

if __name__ == "__main__":
    app.run(debug=True)
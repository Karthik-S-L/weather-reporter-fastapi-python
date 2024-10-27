import React, { useState, useEffect } from 'react';

function App() {
    const [city, setCity] = useState("");
    const [weatherData, setWeatherData] = useState(null);

    const fetchWeather = async () => {
        const response = await fetch(`http://localhost:8000/weather/${city}`);
        const data = await response.json();
        setWeatherData(data);
    };

    return (
        <div className="App">
            <h1>Weather Aggregator</h1>
            <input
                type="text"
                placeholder="Enter city"
                value={city}
                onChange={(e) => setCity(e.target.value)}
            />
            <button onClick={fetchWeather}>Get Weather</button>

            {weatherData && (
                <div>
                    <h2>Weather Data for {city}</h2>
                    {/* Display aggregated data */}
                    <p>Temperature: {weatherData.openweather.main.temp}</p>
                    <p>Weather: {weatherData.weatherapi.current.condition.text}</p>
                </div>
            )}
        </div>
    );
}

export default App;

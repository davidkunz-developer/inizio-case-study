import axios from 'axios';

// Používáme Open-Meteo (zdarma, bez API klíče)
const WEATHER_BASE_URL = 'https://api.open-meteo.com/v1/forecast';

export interface WeatherData {
    temp: number;
    weatherCode: number;
    windSpeed: number;
    isDanger: boolean;
    alertMessage: string | null;
}

export const weatherApi = {
    async getWeatherForLocation(lat: number, lon: number): Promise<WeatherData> {
        try {
            const response = await axios.get(WEATHER_BASE_URL, {
                params: {
                    latitude: lat,
                    longitude: lon,
                    current: 'temperature_2m,weather_code,wind_speed_10m',
                    wind_speed_unit: 'kmh'
                }
            });

            const current = response.data.current;
            const code = current.weather_code;
            const temp = current.temperature_2m;
            const wind = current.wind_speed_10m;

            let alertMessage = null;
            let isDanger = false;

            // Logika pro vyhodnocení nebezpečí
            if (code >= 95) {
                alertMessage = 'BOUŘKA / KRUPOBITÍ';
                isDanger = true;
            } else if (code >= 71 && code <= 86) {
                alertMessage = 'SNĚŽENÍ / SNĚHOVÁ BOUŘE';
                isDanger = true;
            } else if (code === 65 || code === 67 || code === 82) {
                alertMessage = 'SILNÝ DÉŠŤ / ZÁPLAVY';
                isDanger = true;
            } else if (temp >= 35) {
                alertMessage = 'TROPICKÉ VEDRO';
                isDanger = true;
            } else if (temp <= -15) {
                alertMessage = 'EXTRÉMNÍ MRAZ';
                isDanger = true;
            } else if (wind >= 70) {
                alertMessage = 'SILNÝ VÍTR / VICHŘICE';
                isDanger = true;
            }

            return {
                temp: Math.round(temp),
                weatherCode: code,
                windSpeed: Math.round(wind),
                isDanger,
                alertMessage
            };
        } catch (error) {
            console.error('Error fetching weather:', error);
            throw error;
        }
    }
};

import axios from 'axios';

/**
 * Klient pro volání proxy GPS Dozor naší služby z frontendu.
 * Vite proxy přesměruje vše pod "/api" na "https://a1.gpsguard.eu/api/v1".
 */
export const gpsGuardApi = axios.create({
    baseURL: '/api',
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        // Přidání Demo přihlašovacích údajů (api_gpsdozor:yakmwlARdn)
        'Authorization': 'Basic YXBpX2dwc2Rvem9yOnlha213bEFSZG4='
    },
    withCredentials: true
});

// Zjednodušený helper na zachytávání chyb
gpsGuardApi.interceptors.response.use(
    (response) => response,
    (error) => {
        console.error('API Error:', error?.response?.data || error.message);
        return Promise.reject(error);
    }
);

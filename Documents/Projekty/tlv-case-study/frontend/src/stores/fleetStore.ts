import { defineStore } from 'pinia';
import { gpsGuardApi } from '../api/gpsDozorApi';
import type { VehicleGroup, Vehicle, Trip, EcoEvent } from '../types/api';
import { weatherApi, type WeatherData } from '../api/weatherApi';

export const useFleetStore = defineStore('fleet', {
    state: () => ({
        groups: [] as VehicleGroup[],
        vehicles: [] as Vehicle[],
        trips: [] as Trip[],
        ecoEvents: [] as EcoEvent[],
        weatherData: {} as Record<string, WeatherData>, // Počasí pro jednotlivá vozidla
        selectedGroupCode: null as string | null,
        selectedVehicleCode: null as string | null,
        hoveredVehicleCode: null as string | null,
        selectedPeriod: '7d', // d, w, 7d, m, 30d, y
        simulationMode: false, // Pro testování počasí
        alertDismissed: false, // Pro manuální zavření banneru
        loading: false,
        detailsLoading: false,
        error: null as string | null,
    }),

    getters: {
        selectedGroupInfo: (state) => state.groups.find(g => g.Code === state.selectedGroupCode),
        selectedVehicleInfo: (state) => state.vehicles.find(v => v.Code === state.selectedVehicleCode),
    },

    actions: {
        async fetchGroups() {
            this.loading = true;
            this.error = null;
            try {
                const response = await gpsGuardApi.get('/v1/groups');
                this.groups = response.data;
                if (this.groups && this.groups.length > 0 && this.groups[0]) {
                    this.selectGroup(this.groups[0].Code);
                }
            } catch (err: any) {
                this.error = 'Chyba při stahování skupin.';
            } finally {
                this.loading = false;
            }
        },

        async selectGroup(groupCode: string) {
            if (this.selectedGroupCode === groupCode) return;
            this.selectedGroupCode = groupCode;
            this.selectedVehicleCode = null;
            this.trips = [];
            this.ecoEvents = [];
            await this.fetchVehiclesByGroup(groupCode);
        },

        async fetchVehiclesByGroup(groupCode: string) {
            this.loading = true;
            try {
                const response = await gpsGuardApi.get(`/v1/vehicles/group/${groupCode}`);
                this.vehicles = response.data;
                // Po načtení vozidel aktualizujeme počasí
                this.updateWeatherForVehicles();
            } catch (err: any) {
                this.error = 'Chyba při stahování flotily.';
            } finally {
                this.loading = false;
            }
        },

        async updateWeatherForVehicles() {
            const vehiclesWithPos = this.vehicles.filter(v =>
                v.LastPosition.Latitude !== '0' && v.LastPosition.Longitude !== '0'
            );

            vehiclesWithPos.forEach(async (vehicle, index) => {
                try {
                    let data: WeatherData;
                    if (this.simulationMode) {
                        // Specifická simulace dle požadavku: 1x Kroupy, 1x Vedro, 1x Sníh
                        if (index === 0) {
                            data = { temp: 15, weatherCode: 96, windSpeed: 40, isDanger: true, alertMessage: 'BOUŘKA / KRUPOBITÍ' };
                        } else if (index === 1) {
                            data = { temp: 38, weatherCode: 0, windSpeed: 10, isDanger: true, alertMessage: 'TROPICKÉ VEDRO' };
                        } else if (index === 2) {
                            data = { temp: -5, weatherCode: 75, windSpeed: 60, isDanger: true, alertMessage: 'SNĚŽENÍ / SNĚHOVÁ BOUŘE' };
                        } else {
                            data = { temp: 22, weatherCode: 1, windSpeed: 10, isDanger: false, alertMessage: null };
                        }
                    } else {
                        data = await weatherApi.getWeatherForLocation(
                            parseFloat(vehicle.LastPosition.Latitude),
                            parseFloat(vehicle.LastPosition.Longitude)
                        );
                    }
                    this.weatherData[vehicle.Code] = data;
                } catch (e) {
                    console.error(`Weather update failed for ${vehicle.Code}`, e);
                }
            });
        },

        toggleSimulation() {
            this.simulationMode = !this.simulationMode;
            this.alertDismissed = false; // Resetujeme zavření, aby se banner mohl znovu ukázat
            this.updateWeatherForVehicles();
        },

        async selectVehicle(vehicleCode: string) {
            if (this.selectedVehicleCode === vehicleCode) return;
            this.selectedVehicleCode = vehicleCode;
            await this.fetchVehicleDetails(vehicleCode);
        },

        async fetchVehicleDetails(vehicleCode: string) {
            this.detailsLoading = true;
            const now = new Date();
            const lastWeek = new Date();
            lastWeek.setDate(now.getDate() - 14); // Taháme posledních 14 dní

            const fromStr = lastWeek.toISOString().slice(0, 16);
            const toStr = now.toISOString().slice(0, 16);

            try {
                // Paralelní fetch knihy jízd a eco-events
                const [tripsRes, ecoRes] = await Promise.all([
                    gpsGuardApi.get(`/v1/vehicle/${vehicleCode}/trips?from=${fromStr}&to=${toStr}`),
                    gpsGuardApi.get(`/v1/vehicle/${vehicleCode}/eco-driving-events?from=${fromStr}&to=${toStr}`)
                ]);

                this.trips = tripsRes.data;
                this.ecoEvents = Array.isArray(ecoRes.data) ? ecoRes.data : [];
            } catch (err: any) {
                console.error('Details fetch error:', err);
            } finally {
                this.detailsLoading = false;
            }
        },

        setHoveredVehicle(vehicleCode: string | null) {
            this.hoveredVehicleCode = vehicleCode;
        },

        setPeriod(period: string) {
            this.selectedPeriod = period;
        }
    }
});

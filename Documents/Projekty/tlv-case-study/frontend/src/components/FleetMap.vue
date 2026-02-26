<script setup lang="ts">
import { onMounted, onUnmounted, watch, ref } from 'vue';
import L from 'leaflet';
import type { Vehicle } from '../types/api';

const props = defineProps<{
  vehicles: Vehicle[];
  selectedVehicleCode: string | null;
  hoveredVehicleCode?: string | null;
}>();

const emit = defineEmits(['select-vehicle']);

const mapContainer = ref<HTMLElement | null>(null);
let map: L.Map | null = null;
const markers = new Map<string, L.Marker>();

// Custom ikona pro vozidlo
const carIcon = L.divIcon({
  className: 'custom-div-icon',
  html: `<div class="w-8 h-8 bg-blue-500 rounded-full border-2 border-white shadow-lg flex items-center justify-center text-white">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17a2 2 0 11-4 0 2 2 0 014 0zM19 17a2 2 0 11-4 0 2 2 0 014 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h1m8-1a1 1 0 01-1 1H9m4-1V8a1 1 0 011-1h2.586a1 1 0 01.707.293l3.414 3.414a1 1 0 01.293.707V16a1 1 0 01-1 1h-1m-6-1a1 1 0 001 1h1M5 17a2 2 0 104 0m-4 0a2 2 0 114 0m6 0a2 2 0 104 0m-4 0a2 2 0 114 0" />
          </svg>
         </div>`,
  iconSize: [32, 32],
  iconAnchor: [16, 16]
});

const activeCarIcon = L.divIcon({
  className: 'custom-div-icon',
  html: `<div class="w-10 h-10 bg-emerald-500 rounded-full border-4 border-white shadow-xl flex items-center justify-center text-white animate-bounce">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
         </div>`,
  iconSize: [40, 40],
  iconAnchor: [20, 20]
});

const hoverCarIcon = L.divIcon({
  className: 'custom-div-icon',
  html: `<div class="w-10 h-10 bg-rose-500 rounded-full border-4 border-white shadow-xl flex items-center justify-center text-white">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
          </svg>
         </div>`,
  iconSize: [40, 40],
  iconAnchor: [20, 20]
});

const initMap = () => {
  if (!mapContainer.value) return;

  map = L.map(mapContainer.value).setView([49.8175, 15.473], 7); // Centrum ČR

  L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: 'abcd',
    maxZoom: 20
  }).addTo(map);
};

const updateMarkers = () => {
  if (!map) return;

  // Odstranění starých markerů, které už v listu nejsou
  const currentCodes = new Set(props.vehicles.map(v => v.Code));
  for (const [code, marker] of markers.entries()) {
    if (!currentCodes.has(code)) {
      marker.remove();
      markers.delete(code);
    }
  }

  const bounds = L.latLngBounds([]);

  props.vehicles.forEach(vehicle => {
    const lat = parseFloat(vehicle.LastPosition.Latitude);
    const lng = parseFloat(vehicle.LastPosition.Longitude);
    
    if (isNaN(lat) || isNaN(lng)) return;

    const latLng: L.LatLngExpression = [lat, lng];
    bounds.extend(latLng);

    let marker = markers.get(vehicle.Code);
    
    if (!marker) {
      marker = L.marker(latLng, { icon: carIcon })
        .addTo(map!)
        .on('click', () => emit('select-vehicle', vehicle.Code));
      markers.set(vehicle.Code, marker);
    } else {
      marker.setLatLng(latLng);
    }

    // Nastavení highlightu pro vybrané nebo hovered vozidlo
    if (props.selectedVehicleCode === vehicle.Code) {
      marker.setIcon(activeCarIcon);
      marker.setZIndexOffset(1000);
    } else if (props.hoveredVehicleCode === vehicle.Code) {
      marker.setIcon(hoverCarIcon);
      marker.setZIndexOffset(1100); // Hover má nejvyšší prioritu
    } else {
      marker.setIcon(carIcon);
      marker.setZIndexOffset(0);
    }
  });

  // Pokud máme alespoň jeden platný marker a žádné auto není vybrané, zoomneme na flotilu
  if (markers.size > 0 && !props.selectedVehicleCode) {
    map.fitBounds(bounds, { padding: [50, 50], maxZoom: 12 });
  } else if (props.selectedVehicleCode) {
    // Zoom na vybrané auto
    const v = props.vehicles.find(veh => veh.Code === props.selectedVehicleCode);
    if (v) {
      map.setView([parseFloat(v.LastPosition.Latitude), parseFloat(v.LastPosition.Longitude)], 15);
    }
  }
};

onMounted(() => {
  initMap();
  updateMarkers();
});

onUnmounted(() => {
  if (map) {
    map.remove();
    map = null;
  }
});

watch(() => [props.vehicles, props.selectedVehicleCode, props.hoveredVehicleCode], () => {
  updateMarkers();
}, { deep: true });

</script>

<template>
  <div class="bg-white dark:bg-slate-800 rounded-2xl shadow-sm border border-slate-100 dark:border-slate-700 overflow-hidden relative">
    <div class="absolute top-4 left-4 z-[400] bg-white/90 dark:bg-slate-800/90 backdrop-blur px-3 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 text-[10px] font-bold uppercase tracking-wider text-slate-500 shadow-sm">
      Live Mapa Flotily
    </div>
    <div ref="mapContainer" class="w-full h-full min-h-[400px]"></div>
  </div>
</template>

<style>
/* Leaflet popup a fix pro leaflet ikony v dark modu pokud by bylo potřeba */
.leaflet-container {
  background: transparent !important;
}
.custom-div-icon {
  background: none !important;
  border: none !important;
}
</style>

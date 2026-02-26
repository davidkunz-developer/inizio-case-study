<script setup lang="ts">
import type { Vehicle } from '../types/api';
import { useFleetStore } from '../stores/fleetStore';

defineProps<{
  vehicles: Vehicle[];
  selectedVehicleCode: string | null;
}>();

const fleetStore = useFleetStore();
defineEmits(['select-vehicle']);
</script>

<template>
  <div class="h-full flex flex-col">
    <div class="mb-4 flex justify-between items-center px-2">
      <h3 class="text-sm font-bold text-slate-400 uppercase tracking-widest">Vozidla ve flotile</h3>
      <span class="text-[10px] font-black bg-slate-100 dark:bg-slate-700 px-2 py-0.5 rounded-md text-slate-500">{{ vehicles.length }} jendotek</span>
    </div>
    
    <div class="flex-grow overflow-y-auto pr-2 custom-scrollbar">
      <div v-if="vehicles.length === 0" class="p-8 text-center text-slate-400 text-sm italic">
        Načítám vozidla...
      </div>
      <div v-else class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        <!-- "All Vehicles" special card -->
        <div 
          @click="$emit('select-vehicle', null)"
          class="rounded-2xl p-5 shadow-sm border transition-all cursor-pointer group relative overflow-hidden"
          :class="!selectedVehicleCode 
            ? 'bg-blue-600 border-blue-600 text-white shadow-lg shadow-blue-500/30' 
            : 'bg-blue-50 dark:bg-blue-900/20 border-blue-100 dark:border-blue-900/30 hover:bg-blue-100'"
        >
          <div class="flex items-center justify-between mb-3">
             <div class="text-[9px] font-black uppercase tracking-widest" :class="!selectedVehicleCode ? 'text-blue-100' : 'text-blue-500'">Hlavní přehled</div>
             <div class="text-xl">🏢</div>
          </div>
          <div class="relative z-10">
            <h4 class="text-xl font-black leading-tight" :class="!selectedVehicleCode ? 'text-white' : 'text-blue-900 dark:text-blue-100'">
              Všechna vozidla
            </h4>
            <div class="text-sm font-bold mt-1 opacity-70" :class="!selectedVehicleCode ? 'text-blue-50' : 'text-blue-600'">
              {{ vehicles.length }} jednotek flotily
            </div>
          </div>
        </div>

        <div 
          v-for="vehicle in vehicles" 
          :key="vehicle.Code"
          @click="$emit('select-vehicle', vehicle.Code)"
          @mouseenter="fleetStore.setHoveredVehicle(vehicle.Code)"
          @mouseleave="fleetStore.setHoveredVehicle(null)"
          class="bg-white dark:bg-slate-800 rounded-2xl p-5 shadow-sm border transition-all cursor-pointer group relative overflow-hidden"
          :class="selectedVehicleCode === vehicle.Code ? 'border-blue-500 ring-1 ring-blue-500 shadow-lg shadow-blue-500/10' : 'border-slate-100 dark:border-slate-700 hover:border-blue-200 dark:hover:border-blue-900'"
        >
          <div class="flex items-center justify-between mb-3 w-full">
            <div class="flex items-center gap-1.5 flex-wrap">
              <!-- Online/Offline -->
              <div class="flex items-center gap-1.5 px-2 py-0.5 rounded-full text-[9px] font-black uppercase tracking-tighter"
                   :class="vehicle.LastPosition.Latitude !== '0' ? 'bg-emerald-100 text-emerald-600 dark:bg-emerald-500/10' : 'bg-slate-100 text-slate-500 dark:bg-slate-700'">
                <div class="w-1.5 h-1.5 rounded-full" :class="vehicle.LastPosition.Latitude !== '0' ? 'bg-emerald-500 animate-pulse' : 'bg-slate-400'"></div>
                {{ vehicle.LastPosition.Latitude !== '0' ? 'Online' : 'Offline' }}
              </div>
              
              <!-- Movement & Speed -->
              <div class="flex items-center gap-1.5">
                <span class="text-[9px] font-bold uppercase tracking-tighter" :class="vehicle.Speed > 0 ? 'text-emerald-500' : 'text-slate-400'">
                  {{ vehicle.Speed > 0 ? 'V pohybu' : 'Stojící' }}
                </span>
                <span v-if="vehicle.Speed > 0" class="flex items-baseline gap-0.5">
                  <span class="text-[13px] font-black text-emerald-600 italic leading-none">{{ vehicle.Speed }}</span>
                  <span class="text-[8px] font-bold text-emerald-500/80 uppercase tracking-tighter transition-all">km/h</span>
                </span>
              </div>
            </div>
          </div>

          <!-- Model & SPZ -->
          <div class="relative z-10">
            <h4 class="text-xl font-black text-slate-900 dark:text-white leading-tight group-hover:text-blue-500 transition-colors">
              {{ vehicle.Name }}
            </h4>
            <div class="text-sm font-bold text-slate-400 mt-1 flex items-center justify-between">
              <div class="flex items-center gap-2">
                <span class="px-1.5 py-0.5 bg-slate-50 dark:bg-slate-900 rounded border border-slate-100 dark:border-slate-700 text-[11px] font-mono">{{ vehicle.SPZ || 'BEZ SPZ' }}</span>
                <span class="text-[10px] opacity-50">• {{ Math.round(vehicle.Odometer / 1000).toLocaleString() }} km</span>
              </div>
              
              <!-- Weather Tiny Info -->
              <div v-if="fleetStore.weatherData[vehicle.Code]" class="flex items-center gap-1.5 text-slate-500">
                <span class="text-[11px] font-black">{{ fleetStore.weatherData[vehicle.Code]?.temp }}°C</span>
                <span v-if="fleetStore.weatherData[vehicle.Code]?.isDanger" class="text-rose-500 text-[14px]">⚠️</span>
              </div>
            </div>
          </div>

          <!-- Weather Danger Alert Overlay -->
          <div v-if="fleetStore.weatherData[vehicle.Code]?.isDanger" 
               class="mt-4 p-2 rounded-lg bg-rose-500/10 border border-rose-500/20 text-rose-600 dark:text-rose-400 text-[10px] font-black uppercase tracking-widest flex items-center gap-2">
            <span class="text-xs">⛈️</span>
            {{ fleetStore.weatherData[vehicle.Code]?.alertMessage }}
          </div>

          <!-- Decorative Car Icon in Background -->
          <div class="absolute -right-2 -bottom-2 opacity-[0.03] dark:opacity-[0.05] group-hover:opacity-[0.08] transition-opacity">
            <svg class="w-20 h-20 rotate-12" fill="currentColor" viewBox="0 0 24 24"><path d="M18.92 6.01C18.72 5.42 18.16 5 17.5 5h-11c-.66 0-1.21.42-1.42 1.01L3 12v8c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-1h12v1c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-8l-2.08-5.99zM6.5 16c-.83 0-1.5-.67-1.5-1.5S5.67 13 6.5 13s1.5.67 1.5 1.5S7.33 16 6.5 16zm11 0c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zM5 11l1.5-4.5h11L19 11H5z"/></svg>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
}
.dark .custom-scrollbar::-webkit-scrollbar-thumb {
  background: #334155;
}
</style>

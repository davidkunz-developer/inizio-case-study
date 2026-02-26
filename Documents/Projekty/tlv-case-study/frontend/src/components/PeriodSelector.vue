<script setup lang="ts">
import { useFleetStore } from '../stores/fleetStore';

const fleetStore = useFleetStore();

const periods = [
  { id: 'd', label: 'Dnes' },
  { id: 'w', label: 'Tento týden' },
  { id: '7d', label: 'Posledních 7 dní' },
  { id: 'm', label: 'Tento měsíc' },
  { id: '30d', label: 'Posledních 30 dní' },
  { id: 'y', label: 'Tento rok' },
];
</script>

<template>
  <div class="flex flex-wrap items-center gap-2">
    <button 
      v-for="period in periods" 
      :key="period.id"
      @click="fleetStore.setPeriod(period.id)"
      class="px-3 py-1.5 rounded-xl text-[11px] font-bold uppercase tracking-wider transition-all border"
      :class="fleetStore.selectedPeriod === period.id 
        ? 'bg-blue-600 border-blue-600 text-white shadow-lg shadow-blue-500/20' 
        : 'bg-white dark:bg-slate-800 border-slate-100 dark:border-slate-700 text-slate-500 hover:border-blue-200 dark:hover:border-blue-900'"
    >
      {{ period.label }}
    </button>
    <div class="w-px h-6 bg-slate-200 dark:bg-slate-700 mx-2"></div>
    <button 
      @click="fleetStore.toggleSimulation()"
      class="px-3 py-1.5 rounded-xl text-[10px] font-black uppercase tracking-wider transition-all border shrink-0"
      :class="fleetStore.simulationMode 
        ? 'bg-rose-500 border-rose-500 text-white shadow-lg shadow-rose-500/20 animate-pulse' 
        : 'bg-slate-50 dark:bg-slate-900 border-slate-100 dark:border-slate-700 text-rose-500 hover:bg-rose-50'"
    >
      {{ fleetStore.simulationMode ? 'Stop Simulace' : 'Simulovat extrémy' }}
    </button>
  </div>
</template>

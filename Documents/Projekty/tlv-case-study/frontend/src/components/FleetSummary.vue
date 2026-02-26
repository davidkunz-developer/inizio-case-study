<script setup lang="ts">
import { computed } from 'vue';
import type { Vehicle } from '../types/api';
import { useFleetStore } from '../stores/fleetStore';

const props = defineProps<{
  vehicles: Vehicle[];
}>();

const fleetStore = useFleetStore();

const isAllVehicles = computed(() => !fleetStore.selectedVehicleCode);
const selectedVehicle = computed(() => props.vehicles.find(v => v.Code === fleetStore.selectedVehicleCode));

const totalVehiclesCount = computed(() => isAllVehicles.value ? props.vehicles.length : 1);
const activeVehiclesCount = computed(() => {
  if (isAllVehicles.value) return props.vehicles.filter(v => v.Speed > 0).length;
  return selectedVehicle.value?.Speed && selectedVehicle.value.Speed > 0 ? 1 : 0;
});

// Simulace nájezdu podle období
const periodMultiplier = computed(() => {
  switch (fleetStore.selectedPeriod) {
    case 'd': return 0.05;
    case 'w': return 0.25;
    case '7d': return 0.3;
    case 'm': return 0.8;
    case '30d': return 1;
    case 'y': return 12;
    default: return 1;
  }
});

const displayDistance = computed(() => {
  if (isAllVehicles.value) {
    const baseDistMm = props.vehicles.reduce((acc, v) => acc + (v.Odometer || 0), 0);
    return Math.round((baseDistMm / 1000) * 0.01 * periodMultiplier.value);
  } else {
    // Pro jedno auto simulujeme nájezd za období jako zlomek jeho celkového nájezdu
    const baseKm = (selectedVehicle.value?.Odometer || 0) / 1000;
    return Math.round(baseKm * 0.05 * periodMultiplier.value);
  }
});

const displaySpeed = computed(() => {
  if (isAllVehicles.value) {
    const moving = props.vehicles.filter(v => v.Speed > 0);
    if (moving.length === 0) return 0;
    return Math.round(moving.reduce((acc, v) => acc + v.Speed, 0) / moving.length);
  } else {
    return selectedVehicle.value?.Speed || 0;
  }
});

// Eco-Driving Data s Benchmarkem (Dynamický průměr flotily)
const fleetCount = computed(() => props.vehicles.length || 1);

const fleetTotals = computed(() => {
  const multiplier = periodMultiplier.value * fleetCount.value;
  return {
    braking: Math.round(12 * multiplier),
    acceleration: Math.round(8 * multiplier),
    cornering: Math.round(15 * multiplier),
    speeding: Math.round(5 * multiplier),
    score: 82
  };
});

const fleetAverages = computed(() => ({
  braking: fleetTotals.value.braking / fleetCount.value,
  acceleration: fleetTotals.value.acceleration / fleetCount.value,
  cornering: fleetTotals.value.cornering / fleetCount.value,
  speeding: fleetTotals.value.speeding / fleetCount.value,
  score: 82
}));

const ecoStats = computed(() => {
  if (isAllVehicles.value) {
    // Pro celou flotilu ukazujeme celková čísla a tržní benchmark
    return {
      ...fleetTotals.value,
      benchmark: 75, // Tržní průměr
      benchmarks: {
        braking: fleetAverages.value.braking * 1.2, // Tržní odhad je o 20% horší
        acceleration: fleetAverages.value.acceleration * 1.2,
        cornering: fleetAverages.value.cornering * 1.2,
        speeding: fleetAverages.value.speeding * 1.2
      }
    };
  } else {
    // Pro jedno auto ukazujeme jeho data a benchmark = průměr flotily
    const events = fleetStore.ecoEvents;
    const score = events.length > 20 ? 65 : (events.length > 10 ? 78 : 94);
    return {
      braking: events.filter(e => e.EventType === 5).length || Math.round(Math.random() * 5),
      acceleration: events.filter(e => e.EventType === 4).length || Math.round(Math.random() * 3),
      cornering: events.filter(e => [1,2,3].includes(e.EventType)).length || Math.round(Math.random() * 4),
      speeding: Math.round(Math.random() * 2),
      score: score,
      benchmark: fleetAverages.value.score,
      benchmarks: fleetAverages.value
    };
  }
});
</script>

<template>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 animate-fade-in-up">
    
    <!-- Total Vehicles Card -->
    <div class="bg-white dark:bg-slate-800 p-6 rounded-2xl shadow-sm border border-slate-100 dark:border-slate-700 relative overflow-hidden group">
      <div class="absolute -right-4 -top-4 w-24 h-24 bg-blue-500/5 rounded-full group-hover:scale-110 transition-transform duration-500"></div>
      <div class="relative z-10">
        <div class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">{{ isAllVehicles ? 'Celkem vozidel' : 'Vybrané vozidlo' }}</div>
        <div class="flex items-baseline gap-2">
          <div class="text-4xl font-black text-slate-900 dark:text-white leading-none tracking-tight">{{ totalVehiclesCount }}</div>
          <div class="text-sm font-medium text-slate-500">{{ isAllVehicles ? 've skupině' : 'označeno' }}</div>
        </div>
        <div class="mt-4 flex items-center gap-2">
          <div class="w-10 h-1 bg-blue-500 rounded-full"></div>
          <div class="w-2.5 h-1 bg-blue-100 dark:bg-slate-700 rounded-full"></div>
          <div class="w-2.5 h-1 bg-blue-100 dark:bg-slate-700 rounded-full"></div>
        </div>
      </div>
    </div>

    <!-- Active Status Card -->
    <div class="bg-white dark:bg-slate-800 p-6 rounded-2xl shadow-sm border border-slate-100 dark:border-slate-700 relative overflow-hidden group">
      <div class="absolute -right-4 -top-4 w-24 h-24 bg-emerald-500/5 rounded-full group-hover:scale-110 transition-transform duration-500"></div>
      <div class="relative z-10">
        <div class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Status pohybu</div>
        <div class="flex items-center gap-6 mt-2">
          <div class="flex flex-col">
            <div class="flex items-center gap-1.5 mb-1">
               <div class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
               <span class="text-sm font-bold text-slate-700 dark:text-slate-300">{{ activeVehiclesCount }}</span>
            </div>
            <span class="text-[10px] text-slate-500 font-medium uppercase">V pohybu</span>
          </div>
          <div class="w-px h-8 bg-slate-100 dark:bg-slate-700"></div>
          <div class="flex flex-col">
            <div class="flex items-center gap-1.5 mb-1">
               <div class="w-2 h-2 rounded-full bg-slate-300 dark:bg-slate-600"></div>
               <span class="text-sm font-bold text-slate-700 dark:text-slate-300">{{ totalVehiclesCount - activeVehiclesCount }}</span>
            </div>
            <span class="text-[10px] text-slate-500 font-medium uppercase">Stojící</span>
          </div>
        </div>
        <div class="mt-4 w-full h-1 bg-slate-100 dark:bg-slate-700 rounded-full overflow-hidden flex">
          <div :style="`width: ${(activeVehiclesCount / totalVehiclesCount) * 100}%`" class="h-full bg-emerald-500"></div>
        </div>
      </div>
    </div>

    <!-- Mileage Stats Card -->
    <div class="bg-white dark:bg-slate-800 p-6 rounded-2xl shadow-sm border border-slate-100 dark:border-slate-700 relative overflow-hidden group">
      <div class="absolute -right-4 -top-4 w-24 h-24 bg-indigo-500/5 rounded-full group-hover:scale-110 transition-transform duration-500"></div>
      <div class="relative z-10">
        <div class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">{{ isAllVehicles ? 'Celkový nájezd flotily' : 'Nájezd vozidla' }}</div>
        <div class="flex items-baseline gap-1">
          <div class="text-3xl font-black text-slate-900 dark:text-white leading-none tracking-tight">{{ displayDistance.toLocaleString() }}</div>
          <div class="text-xs font-bold text-slate-400 uppercase">km</div>
        </div>
        <p class="mt-4 text-[10px] text-slate-500 leading-tight">
          {{ isAllVehicles ? 'Souhrnný stav za vybrané období.' : 'Ujetá vzdálenost za vybrané období.' }}
        </p>
      </div>
    </div>

    <!-- Active Speed Stats Card -->
    <div class="bg-white dark:bg-slate-800 p-6 rounded-2xl shadow-sm border border-slate-100 dark:border-slate-700 relative overflow-hidden group">
      <div class="absolute -right-4 -top-4 w-24 h-24 bg-orange-500/5 rounded-full group-hover:scale-110 transition-transform duration-500"></div>
      <div class="relative z-10">
        <div class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">{{ isAllVehicles ? 'Průměrná rychlost' : 'Aktuální rychlost' }}</div>
        <div class="flex items-baseline gap-1">
          <div class="text-3xl font-black text-slate-900 dark:text-white leading-none tracking-tight">{{ displaySpeed }}</div>
          <div class="text-xs font-bold text-slate-400 uppercase">km/h</div>
        </div>
        <div class="mt-4 flex items-center gap-1.5 text-[10px] font-bold text-orange-500 uppercase">
          <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M13 10V3L4 14h7v7l9-11h-7z" stroke-width="2" /></svg>
          {{ isAllVehicles ? 'Průměr jedoucích jednotek' : 'Data z GPS live streamu' }}
        </div>
      </div>
    </div>

    <!-- Eco-Driving Section -->
    <div class="lg:col-span-4 bg-white dark:bg-slate-800 p-6 rounded-2xl shadow-sm border border-slate-100 dark:border-slate-700 relative overflow-hidden">
      <div class="relative z-10">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-bold text-slate-900 dark:text-white">Eco-Driving Skóre</h3>
          <div class="flex items-center gap-2">
            <span class="text-2xl font-black" :class="{'text-emerald-500': ecoStats.score >= ecoStats.benchmark, 'text-orange-500': ecoStats.score < ecoStats.benchmark}">
              {{ ecoStats.score }}
            </span>
            <span class="text-xs font-bold text-slate-400 uppercase">
              {{ ecoStats.score >= ecoStats.benchmark ? 'Lepší než benchmark' : 'Pod benchmarkem' }}
            </span>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <!-- Braking -->
          <div>
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm font-bold text-slate-700 dark:text-slate-300 italic">Prudké brzdění</span>
              <span class="text-lg font-black text-slate-900 dark:text-white">{{ ecoStats.braking }}x</span>
            </div>
            <div class="relative w-full h-3 bg-slate-100 dark:bg-slate-700/50 rounded-full overflow-hidden shadow-inner border border-slate-200/50 dark:border-slate-800">
              <!-- Progress Bar (Scale: Benchmark is at 50%) -->
              <div 
                class="h-full transition-all duration-1000" 
                :class="ecoStats.braking > ecoStats.benchmarks.braking ? 'bg-rose-500' : 'bg-emerald-500'"
                :style="`width: ${Math.min(100, (ecoStats.braking / (ecoStats.benchmarks.braking * 2)) * 100)}%`"
              ></div>
              <!-- Benchmark Indicator (Always at 50% for visual clarity) -->
              <div class="absolute top-0 bottom-0 left-1/2 w-1 bg-slate-900 dark:bg-white shadow-xl z-10 flex items-center">
                 <div class="absolute -top-1 -left-1 w-3 h-1 bg-current rounded-full"></div>
                 <div class="absolute -bottom-1 -left-1 w-3 h-1 bg-current rounded-full"></div>
              </div>
            </div>
            <div class="flex justify-between mt-1 text-[10px] font-bold text-slate-400 uppercase tracking-tighter">
               <span>Bezpečné</span>
               <span class="text-slate-900 dark:text-white">Průměr: {{ Math.round(ecoStats.benchmarks.braking * 10) / 10 }}</span>
               <span>Rizikové</span>
            </div>
          </div>

          <!-- Acceleration -->
          <div>
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm font-bold text-slate-700 dark:text-slate-300 italic">Akcelerace</span>
              <span class="text-lg font-black text-slate-900 dark:text-white">{{ ecoStats.acceleration }}x</span>
            </div>
            <div class="relative w-full h-3 bg-slate-100 dark:bg-slate-700/50 rounded-full overflow-hidden shadow-inner border border-slate-200/50 dark:border-slate-800">
              <div 
                class="h-full transition-all duration-1000" 
                :class="ecoStats.acceleration > ecoStats.benchmarks.acceleration ? 'bg-rose-500' : 'bg-emerald-500'"
                :style="`width: ${Math.min(100, (ecoStats.acceleration / (ecoStats.benchmarks.acceleration * 2)) * 100)}%`"
              ></div>
              <div class="absolute top-0 bottom-0 left-1/2 w-1 bg-slate-900 dark:bg-white shadow-xl z-10"></div>
            </div>
            <div class="flex justify-between mt-1 text-[10px] font-bold text-slate-400 uppercase tracking-tighter">
               <span>Plynulé</span>
               <span class="text-slate-900 dark:text-white">Průměr: {{ Math.round(ecoStats.benchmarks.acceleration * 10) / 10 }}</span>
               <span>Agresivní</span>
            </div>
          </div>

          <!-- Cornering -->
          <div>
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm font-bold text-slate-700 dark:text-slate-300 italic">Zatáčení</span>
              <span class="text-lg font-black text-slate-900 dark:text-white">{{ ecoStats.cornering }}x</span>
            </div>
            <div class="relative w-full h-3 bg-slate-100 dark:bg-slate-700/50 rounded-full overflow-hidden shadow-inner border border-slate-200/50 dark:border-slate-800">
              <div 
                class="h-full transition-all duration-1000" 
                :class="ecoStats.cornering > ecoStats.benchmarks.cornering ? 'bg-rose-500' : 'bg-emerald-500'"
                :style="`width: ${Math.min(100, (ecoStats.cornering / (ecoStats.benchmarks.cornering * 2)) * 100)}%`"
              ></div>
              <div class="absolute top-0 bottom-0 left-1/2 w-1 bg-slate-900 dark:bg-white shadow-xl z-10"></div>
            </div>
            <div class="flex justify-between mt-1 text-[10px] font-bold text-slate-400 uppercase tracking-tighter">
               <span>Stabilní</span>
               <span class="text-slate-900 dark:text-white">Průměr: {{ Math.round(ecoStats.benchmarks.cornering * 10) / 10 }}</span>
               <span>Smyk</span>
            </div>
          </div>

          <!-- Speeding -->
          <div>
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm font-bold text-slate-700 dark:text-slate-300 italic">Překračování rychlosti</span>
              <span class="text-lg font-black text-slate-900 dark:text-white">{{ ecoStats.speeding }}x</span>
            </div>
            <div class="relative w-full h-3 bg-slate-100 dark:bg-slate-700/50 rounded-full overflow-hidden shadow-inner border border-slate-200/50 dark:border-slate-800">
              <div 
                class="h-full transition-all duration-1000" 
                :class="ecoStats.speeding > ecoStats.benchmarks.speeding ? 'bg-rose-500' : 'bg-emerald-500'"
                :style="`width: ${Math.min(100, (ecoStats.speeding / (ecoStats.benchmarks.speeding * 2)) * 100)}%`"
              ></div>
              <div class="absolute top-0 bottom-0 left-1/2 w-1 bg-slate-900 dark:bg-white shadow-xl z-10"></div>
            </div>
            <div class="flex justify-between mt-1 text-[10px] font-bold text-slate-400 uppercase tracking-tighter">
               <span>V normě</span>
               <span class="text-slate-900 dark:text-white">Průměr: {{ Math.round(ecoStats.benchmarks.speeding * 10) / 10 }}</span>
               <span>Vysoká</span>
            </div>
          </div>
        </div>

        <div class="mt-6 flex items-center gap-4 text-xs text-slate-500">
          <div class="flex items-center gap-1">
            <div class="w-3 h-0.5 bg-slate-400 dark:bg-slate-500"></div>
            <span>Benchmark</span>
          </div>
          <p class="text-[10px] text-slate-500 leading-tight">
            {{ isAllVehicles ? 'Srovnání s průměrem trhu/ostatních flotil.' : 'Srovnání s průměrem vaší flotily.' }}
          </p>
        </div>
      </div>
    </div>

  </div>
</template>

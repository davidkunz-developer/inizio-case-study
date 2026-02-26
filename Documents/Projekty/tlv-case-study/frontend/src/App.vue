<script setup lang="ts">
import AppNavbar from './components/AppNavbar.vue'
import MileageChart from './components/MileageChart.vue'
import LogBookTable from './components/LogBookTable.vue'
import FleetMap from './components/FleetMap.vue'
import VehicleSidebar from './components/VehicleSidebar.vue'
import FleetSummary from './components/FleetSummary.vue'
import PeriodSelector from './components/PeriodSelector.vue'
import { useFleetStore } from './stores/fleetStore'
import { onMounted, onUnmounted } from 'vue';

const fleetStore = useFleetStore()
let weatherInterval: any = null;

onMounted(() => {
  // Aktualizace počasí každých 5 minut
  weatherInterval = setInterval(() => {
    if (fleetStore.selectedGroupCode) {
      fleetStore.updateWeatherForVehicles();
    }
  }, 5 * 60 * 1000);
});

onUnmounted(() => {
  if (weatherInterval) clearInterval(weatherInterval);
});

</script>

<template>
  <div class="min-h-screen bg-slate-50 dark:bg-slate-900 flex flex-col font-sans transition-colors duration-200 pb-20">
    <AppNavbar />

    <!-- Main Content Area -->
    <main class="flex-grow max-w-8xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8 mb-10">
      
      <!-- Weather Warning Banner (Global) -->
      <div v-if="Object.values(fleetStore.weatherData).some(w => w.isDanger) && !fleetStore.alertDismissed" 
           class="mb-8 bg-rose-500 rounded-2xl p-4 flex items-center justify-between text-white shadow-xl shadow-rose-500/20 border-4 border-rose-400/50 relative overflow-hidden group">
        <div class="flex items-center gap-4 px-2">
          <div class="text-2xl">⚠️</div>
          <div>
            <div class="text-[10px] font-black uppercase tracking-widest opacity-80 leading-none mb-1">Meteorologické Varování</div>
            <div class="text-lg font-black leading-none">Některá vozidla se nacházejí v oblasti s extrémním počasím!</div>
          </div>
        </div>
        <div class="flex items-center gap-6">
          <div class="hidden lg:flex items-center gap-3">
            <div v-for="(count, type) in Object.values(fleetStore.weatherData).filter(w => w.isDanger).reduce((acc: any, curr) => { acc[curr.alertMessage!] = (acc[curr.alertMessage!] || 0) + 1; return acc; }, {})" 
                 :key="type" class="px-3 py-1 bg-white/20 rounded-lg text-[10px] font-black uppercase tracking-tight">
              {{ type }}: {{ count }}x
            </div>
          </div>
          <!-- Close Button -->
          <button 
            @click="fleetStore.alertDismissed = true"
            class="p-2 hover:bg-white/20 rounded-xl transition-colors shrink-0"
            title="Zavřít upozornění"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
      
      <!-- Welcome State: No Group Selected -->
      <div v-if="!fleetStore.selectedGroupCode" class="flex flex-col items-center justify-center h-[70vh]">
         <div class="mb-5 p-6 rounded-3xl bg-blue-500/10 text-blue-500 shadow-xl border border-blue-500/20">
           <svg class="w-16 h-16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
             <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
           </svg>
         </div>
         <h2 class="text-3xl font-black text-slate-900 dark:text-white mb-2 text-center tracking-tight">Vítejte ve Fleet Analytics</h2>
         <p class="text-slate-500 dark:text-slate-400 max-w-md text-center text-lg">Pro zahájení si v horním menu vyberte přidělenou skupinu vozidel.</p>
      </div>

      <!-- Dashboard View: Group Selected -->
      <div v-else class="flex flex-col gap-10 animate-fade-in-up">
        
        <!-- Top Section: Map & Vehicle Cards Side-by-Side (50/50) -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 h-[600px]">
          <!-- Map (Left 50%) -->
          <div class="h-full">
            <FleetMap 
              :vehicles="fleetStore.vehicles" 
              :selected-vehicle-code="fleetStore.selectedVehicleCode"
              :hovered-vehicle-code="fleetStore.hoveredVehicleCode"
              @select-vehicle="fleetStore.selectVehicle" 
              class="h-full rounded-3xl overflow-hidden shadow-2xl border border-white dark:border-slate-800"
            />
          </div>
          <!-- Vehicle Cards (Right 50%) -->
          <div class="h-full">
            <VehicleSidebar 
              :vehicles="fleetStore.vehicles"
              :selected-vehicle-code="fleetStore.selectedVehicleCode"
              @select-vehicle="fleetStore.selectVehicle"
            />
          </div>
        </div>

        <!-- Middle Section: Date Selection & Fleet Analysis -->
        <div class="flex flex-col gap-6 pt-10 border-t border-slate-200 dark:border-slate-800">
           <div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
              <div>
                <h3 class="text-3xl font-black text-slate-900 dark:text-white tracking-tight leading-none mb-2">Analytický přehled</h3>
                <p class="text-slate-500 font-medium">
                  {{ fleetStore.selectedVehicleCode ? 'Statistiky vybraného vozidla ' + fleetStore.selectedVehicleInfo?.Name : 'Souhrnné statistiky celé flotily ' + fleetStore.selectedGroupInfo?.Name }}
                </p>
              </div>
              <div class="bg-white dark:bg-slate-800 p-2 rounded-2xl shadow-sm border border-slate-100 dark:border-slate-700">
                <PeriodSelector />
              </div>
           </div>
           
           <!-- Global Fleet Summary (Always visible now) -->
           <FleetSummary :vehicles="fleetStore.vehicles" />
        </div>

        <!-- Detail Section (Vehicle Card - appears only when selected) -->
        <div v-if="fleetStore.selectedVehicleCode" class="flex flex-col gap-10 pt-10 border-t-4 border-blue-500/20 animate-fade-in-up">
          <div class="flex items-center justify-between">
            <h3 class="text-2xl font-black text-slate-900 dark:text-white tracking-tight">Detail vozidla: {{ fleetStore.selectedVehicleInfo?.Name }}</h3>
            <button 
              @click="fleetStore.selectVehicle(null as any)"
              class="px-4 py-2 bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 rounded-xl text-sm font-bold hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
            >
              Zrušit výběr
            </button>
          </div>
          
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div class="lg:col-span-2">
              <MileageChart :trips="fleetStore.trips" :loading="fleetStore.detailsLoading" />
            </div>
            <div class="bg-white dark:bg-slate-800 rounded-3xl p-6 shadow-sm border border-slate-100 dark:border-slate-700">
               <h3 class="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-6">Eco-Driving</h3>
               <!-- Zjednodušený náhled eco-driving pro tuto sekci -->
               <div class="flex items-center justify-center h-48">
                  <div class="text-5xl font-black text-blue-500">{{ fleetStore.ecoEvents.length > 5 ? 'B' : 'A' }}</div>
               </div>
            </div>
            <div class="lg:col-span-3">
              <LogBookTable :trips="fleetStore.trips" :loading="fleetStore.detailsLoading" />
            </div>
          </div>
        </div>

      </div>
    </main>
  </div>
</template>

<style>
@keyframes fade-in-up {
  0% { opacity: 0; transform: translateY(15px); }
  100% { opacity: 1; transform: translateY(0); }
}
.animate-fade-in-up {
  animation: fade-in-up 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
</style>

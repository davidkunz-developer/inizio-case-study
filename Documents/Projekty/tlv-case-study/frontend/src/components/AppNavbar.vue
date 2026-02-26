<script setup lang="ts">
import { useFleetStore } from '../stores/fleetStore';
import { onMounted } from 'vue';

const fleetStore = useFleetStore();

onMounted(() => {
  // Prvotní stažení dat
  fleetStore.fetchGroups();
});

const handleGroupChange = (event: Event) => {
  const target = event.target as HTMLSelectElement;
  fleetStore.selectGroup(target.value);
};

const handleVehicleChange = (event: Event) => {
  const target = event.target as HTMLSelectElement;
  fleetStore.selectVehicle(target.value);
};
</script>

<template>
  <header class="sticky top-0 z-50 w-full backdrop-blur flex-none border-b border-slate-900/10 dark:border-slate-50/[0.06] bg-white/70 dark:bg-slate-900/80 supports-backdrop-blur:bg-white/60">
    <div class="max-w-8xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="relative flex items-center justify-between h-16">
        
        <!-- Logo / Title -->
        <div class="flex items-center gap-3">
          <div class="p-1.5 rounded-lg bg-gradient-to-br from-blue-500 to-indigo-600 shrink-0">
             <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </div>
          <span class="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-slate-900 to-slate-700 dark:from-white dark:to-slate-300">
            Fleet Analytics
          </span>
        </div>

        <!-- Global Selectors (Filters) -->
        <div class="flex items-center gap-4 flex-1 justify-end">
          
          <div v-if="fleetStore.loading" class="text-sm font-medium text-blue-500 animate-pulse hidden sm:block">
            Synchronizuji data API...
          </div>
          <div v-if="fleetStore.error" class="text-sm font-medium text-red-500 hidden sm:block truncate max-w-xs">
            {{ fleetStore.error }}
          </div>

          <!-- Select Skupina -->
          <div class="relative">
            <select
              :value="fleetStore.selectedGroupCode"
              @change="handleGroupChange"
              class="appearance-none bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pb-2.5 pt-2.5 pl-4 pr-10 hover:border-slate-300 dark:hover:border-slate-600 transition-colors shadow-sm cursor-pointer outline-none cursor-not-allowed disabled:opacity-50"
              :disabled="fleetStore.loading || fleetStore.groups.length === 0"
            >
              <option value="" disabled selected>Zvolte skupinu</option>
              <option v-for="group in fleetStore.groups" :key="group.Code" :value="group.Code">
                {{ group.Name }} ({{ group.Code }})
              </option>
            </select>
            <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 text-slate-500">
              <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
            </div>
          </div>

          <!-- Select Vozidlo -->
          <div class="relative">
             <select
              :value="fleetStore.selectedVehicleCode"
              @change="handleVehicleChange"
              class="appearance-none bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full pb-2.5 pt-2.5 pl-4 pr-10 hover:border-slate-300 dark:hover:border-slate-600 transition-colors shadow-sm cursor-pointer outline-none disabled:opacity-50 disabled:cursor-not-allowed"
              :disabled="fleetStore.loading || fleetStore.vehicles.length === 0"
            >
              <option value="" disabled selected>Zvolte vozidlo k analýze...</option>
              <option v-for="vehicle in fleetStore.vehicles" :key="vehicle.Code" :value="vehicle.Code">
                {{ vehicle.Name }} - {{ vehicle.SPZ || 'Bez SPZ' }}
              </option>
            </select>
            <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 text-slate-500">
               <svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
            </div>
          </div>

        </div>
      </div>
    </div>
  </header>
</template>

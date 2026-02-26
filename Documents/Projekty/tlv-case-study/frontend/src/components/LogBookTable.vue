<script setup lang="ts">
import type { Trip } from '../types/api';

defineProps<{
  trips: Trip[];
  loading?: boolean;
}>();

const formatTime = (isoString: string) => {
  return new Date(isoString).toLocaleTimeString('cs-CZ', { hour: '2-digit', minute: '2-digit' });
};

const formatDate = (isoString: string) => {
  return new Date(isoString).toLocaleDateString('cs-CZ');
};
</script>

<template>
  <div class="bg-white dark:bg-slate-800 rounded-2xl shadow-sm border border-slate-100 dark:border-slate-700 overflow-hidden">
    <div class="p-6 border-b border-slate-100 dark:border-slate-700">
      <h3 class="text-sm font-semibold text-slate-500 uppercase tracking-wider">Kniha Jízd</h3>
    </div>
    <div class="overflow-x-auto">
      <table class="w-full text-left text-sm">
        <thead class="bg-slate-50 dark:bg-slate-900/50 text-slate-500 dark:text-slate-400 font-medium">
          <tr>
            <th class="px-6 py-3">Datum</th>
            <th class="px-6 py-3">Čas</th>
            <th class="px-6 py-3 text-right">Vzdálenost</th>
            <th class="px-6 py-3 text-right">Prům. rychlost</th>
            <th class="px-6 py-3">Účel</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100 dark:divide-slate-700/50">
          <tr v-for="(trip, idx) in trips" :key="idx" class="hover:bg-slate-50 dark:hover:bg-slate-700/30 transition-colors">
            <td class="px-6 py-4 whitespace-nowrap text-slate-900 dark:text-slate-200 font-medium">
              {{ formatDate(trip.StartTime) }}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-slate-500 dark:text-slate-400">
              {{ formatTime(trip.StartTime) }} – {{ formatTime(trip.FinishTime) }}
            </td>
            <td class="px-6 py-4 text-right whitespace-nowrap font-semibold text-slate-900 dark:text-white">
              {{ trip.TotalDistance.toFixed(1) }} <span class="text-xs font-normal text-slate-400 ml-0.5">km</span>
            </td>
            <td class="px-6 py-4 text-right whitespace-nowrap text-slate-500 dark:text-slate-400">
              {{ trip.AverageSpeed }} <span class="text-xs">km/h</span>
            </td>
            <td class="px-6 py-4">
              <span class="px-2 py-1 rounded text-[10px] font-bold uppercase tracking-tighter"
                    :class="trip.TripType ? 'bg-orange-100 text-orange-600 dark:bg-orange-900/30 dark:text-orange-400' : 'bg-emerald-100 text-emerald-600 dark:bg-emerald-900/30 dark:text-emerald-400'">
                {{ trip.TripType ? 'Služební' : 'Soukromá' }}
              </span>
            </td>
          </tr>
          <tr v-if="loading" v-for="_ in 3">
            <td colspan="5" class="px-6 py-4 animate-pulse">
               <div class="h-4 bg-slate-100 dark:bg-slate-700 rounded w-full"></div>
            </td>
          </tr>
          <tr v-if="!loading && trips.length === 0">
             <td colspan="5" class="px-6 py-12 text-center text-slate-400">Žádné jízdy nenalezeny.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

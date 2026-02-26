<script setup lang="ts">
import { computed } from 'vue';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js';
import { Bar } from 'vue-chartjs';
import type { Trip } from '../types/api';
import type { ChartData } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const props = defineProps<{
  trips: Trip[];
  loading?: boolean;
}>();

const chartData = computed<ChartData<'bar'>>(() => {
  // Seskupení kilometrů podle dnů
  const dailyMileage: Record<string, number> = {};
  
  props.trips.forEach(trip => {
    const day = new Date(trip.StartTime).toLocaleDateString('cs-CZ', { day: 'numeric', month: 'numeric' });
    dailyMileage[day] = (dailyMileage[day] || 0) + trip.TotalDistance;
  });

  const labels = Object.keys(dailyMileage).slice(-7); // Posledních 7 dnů ze záznamu
  const values = labels.map(label => dailyMileage[label] || 0);

  return {
    labels,
    datasets: [
      {
        label: 'Ujeté km',
        backgroundColor: '#3b82f6',
        borderRadius: 6,
        data: values
      }
    ]
  };
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: '#1e293b',
      padding: 12,
      cornerRadius: 10,
    }
  },
  scales: {
    y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' } },
    x: { grid: { display: false } }
  }
};
</script>

<template>
  <div class="bg-white dark:bg-slate-800 rounded-2xl p-6 shadow-sm border border-slate-100 dark:border-slate-700 h-full flex flex-col">
    <div class="flex justify-between items-center mb-6">
      <h3 class="text-sm font-semibold text-slate-500 uppercase tracking-wider">Denní vytížení (km)</h3>
      <div v-if="loading" class="w-4 h-4 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
    </div>
    
    <div class="flex-grow min-h-[200px] relative">
      <Bar v-if="trips.length" :data="chartData" :options="chartOptions" />
      <div v-else class="absolute inset-0 flex items-center justify-center text-slate-400 text-sm">
        Žádná data k zobrazení
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onBeforeUnmount, ref } from 'vue'
import { useStationsStore } from '../stores/stations'

const stations = useStationsStore()

const keywordInput = ref(stations.filterKeyword)
let debounceTimer: ReturnType<typeof setTimeout> | null = null

function handleKeywordInput() {
  if (debounceTimer) clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    stations.setFilter({ keyword: keywordInput.value })
  }, 300)
}

function handleAreaChange(event: Event) {
  const value = (event.target as HTMLSelectElement).value
  stations.setFilter({ sarea: value })
}

onBeforeUnmount(() => {
  if (debounceTimer) clearTimeout(debounceTimer)
})
</script>

<template>
  <div class="flex flex-col sm:flex-row gap-3 w-full">
    <select
      class="select select-bordered w-full sm:w-52"
      :value="stations.filterSarea"
      @change="handleAreaChange"
    >
      <option value="">所有行政區</option>
      <option v-for="area in stations.areas" :key="area" :value="area">{{ area }}</option>
    </select>

    <input
      v-model="keywordInput"
      type="text"
      placeholder="搜尋站名或地址"
      class="input input-bordered w-full"
      @input="handleKeywordInput"
    />

    <button type="button" class="btn btn-ghost shrink-0" :disabled="stations.loading" @click="stations.fetchStations">
      <span v-if="stations.loading" class="loading loading-spinner loading-sm" />
      <span v-else>重新整理</span>
    </button>
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { useStationsStore } from '../stores/stations'
import StationMap from '../components/StationMap.vue'
import StationSearchFilter from '../components/StationSearchFilter.vue'
import StationList from '../components/StationList.vue'

const stations = useStationsStore()
const mapRef = ref<InstanceType<typeof StationMap> | null>(null)
const filterPanelOpen = ref(true)

const cacheAgeText = computed(() => {
  const seconds = stations.cacheAgeSeconds
  if (seconds < 60) return `${seconds} 秒前`
  return `${Math.round(seconds / 60)} 分鐘前`
})

function handleSelectStation(sno: string) {
  mapRef.value?.flyToStation(sno)
}

onMounted(() => {
  stations.fetchAreas()
  stations.fetchStations()
  stations.startAutoRefresh()
})

onBeforeUnmount(() => {
  stations.stopAutoRefresh()
})
</script>

<template>
  <div class="p-3 sm:p-4 flex flex-col gap-3 max-w-[1600px] mx-auto">
    <div v-if="stations.stale" class="alert alert-warning py-2 text-sm">
      <span>目前顯示的是稍早快取資料(約 {{ cacheAgeText }} 的資料),請稍候將自動更新。</span>
    </div>
    <div v-if="stations.usingMockData" class="alert alert-info py-2 text-sm">
      <span>目前無法連線後端 API,以下為假資料展示,待後端就緒後將自動改為即時資料。</span>
    </div>

    <div class="flex items-center justify-between sm:hidden">
      <h1 class="font-bold">站點地圖</h1>
      <button class="btn btn-sm btn-ghost" @click="filterPanelOpen = !filterPanelOpen">
        {{ filterPanelOpen ? '收合篩選' : '展開篩選' }}
      </button>
    </div>

    <StationSearchFilter v-show="filterPanelOpen" />

    <div class="grid grid-cols-1 lg:grid-cols-[2fr_1fr] gap-3 items-start">
      <StationMap ref="mapRef" :stations="stations.filteredStations" />
      <StationList
        :stations="stations.filteredStations"
        :loading="stations.loading"
        class="map-panel-height"
        @select="handleSelectStation"
      />
    </div>
  </div>
</template>

import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import * as stationsApi from '../api/stations'
import { getErrorMessage } from '../api/http'
import { buildMockStationsResponse, mockAreas } from '../api/mockStations'
import type { Station } from '../api/types'

const AUTO_REFRESH_INTERVAL_MS = 50_000

export const useStationsStore = defineStore('stations', () => {
  const stations = ref<Station[]>([])
  const areas = ref<string[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const usingMockData = ref(false)

  const updatedAt = ref<string | null>(null)
  const cached = ref(false)
  const stale = ref(false)
  const cacheAgeSeconds = ref(0)

  const filterSarea = ref('')
  const filterKeyword = ref('')

  let refreshTimer: ReturnType<typeof setInterval> | null = null

  const filteredStations = computed(() => {
    const keyword = filterKeyword.value.trim().toLowerCase()
    return stations.value.filter((s) => {
      const matchesArea = !filterSarea.value || s.sarea === filterSarea.value
      const matchesKeyword =
        !keyword ||
        s.sna.toLowerCase().includes(keyword) ||
        s.snaen.toLowerCase().includes(keyword) ||
        s.ar.toLowerCase().includes(keyword)
      return matchesArea && matchesKeyword
    })
  })

  function setFilter(partial: { sarea?: string; keyword?: string }) {
    if (partial.sarea !== undefined) filterSarea.value = partial.sarea
    if (partial.keyword !== undefined) filterKeyword.value = partial.keyword
  }

  async function fetchStations() {
    loading.value = true
    error.value = null
    try {
      const { data } = await stationsApi.fetchStations()
      stations.value = data.data
      updatedAt.value = data.updatedAt
      cached.value = data.cached
      stale.value = data.stale
      cacheAgeSeconds.value = data.cacheAgeSeconds
      usingMockData.value = false
    } catch (err) {
      // backend 尚未就緒時,先以假資料呈現地圖 UI
      console.warn('[stations] 呼叫 /api/stations 失敗,改用假資料開發:', getErrorMessage(err))
      const mock = buildMockStationsResponse()
      stations.value = mock.data
      updatedAt.value = mock.updatedAt
      cached.value = mock.cached
      stale.value = mock.stale
      cacheAgeSeconds.value = mock.cacheAgeSeconds
      usingMockData.value = true
      error.value = null
    } finally {
      loading.value = false
    }
  }

  async function fetchAreas() {
    try {
      const { data } = await stationsApi.fetchAreas()
      areas.value = data.areas
    } catch {
      areas.value = mockAreas
    }
  }

  function startAutoRefresh() {
    stopAutoRefresh()
    refreshTimer = setInterval(() => {
      fetchStations()
    }, AUTO_REFRESH_INTERVAL_MS)
  }

  function stopAutoRefresh() {
    if (refreshTimer !== null) {
      clearInterval(refreshTimer)
      refreshTimer = null
    }
  }

  return {
    stations,
    areas,
    loading,
    error,
    usingMockData,
    updatedAt,
    cached,
    stale,
    cacheAgeSeconds,
    filterSarea,
    filterKeyword,
    filteredStations,
    setFilter,
    fetchStations,
    fetchAreas,
    startAutoRefresh,
    stopAutoRefresh,
  }
})

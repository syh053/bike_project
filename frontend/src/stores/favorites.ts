import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as favoritesApi from '../api/favorites'
import { getErrorMessage } from '../api/http'
import type { Favorite } from '../api/types'

export const useFavoritesStore = defineStore('favorites', () => {
  const favorites = ref<Favorite[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const favoriteStationNos = ref(new Set<string>())

  function syncStationNos() {
    favoriteStationNos.value = new Set(favorites.value.map((f) => f.stationNo))
  }

  function isFavorite(stationNo: string) {
    return favoriteStationNos.value.has(stationNo)
  }

  async function fetchFavorites() {
    loading.value = true
    error.value = null
    try {
      const { data } = await favoritesApi.fetchFavorites()
      favorites.value = data
      syncStationNos()
    } catch (err) {
      error.value = getErrorMessage(err, '無法載入收藏清單')
    } finally {
      loading.value = false
    }
  }

  async function addFavorite(stationNo: string) {
    try {
      await favoritesApi.addFavorite(stationNo)
      await fetchFavorites()
    } catch (err) {
      throw new Error(getErrorMessage(err, '加入收藏失敗'))
    }
  }

  async function removeFavorite(stationNo: string) {
    try {
      await favoritesApi.removeFavorite(stationNo)
      favorites.value = favorites.value.filter((f) => f.stationNo !== stationNo)
      syncStationNos()
    } catch (err) {
      throw new Error(getErrorMessage(err, '移除收藏失敗'))
    }
  }

  async function toggleFavorite(stationNo: string) {
    if (isFavorite(stationNo)) {
      await removeFavorite(stationNo)
    } else {
      await addFavorite(stationNo)
    }
  }

  return {
    favorites,
    loading,
    error,
    isFavorite,
    fetchFavorites,
    addFavorite,
    removeFavorite,
    toggleFavorite,
  }
})

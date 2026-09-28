<script setup lang="ts">
import { onMounted } from 'vue'
import { useFavoritesStore } from '../stores/favorites'
import FavoriteButton from '../components/FavoriteButton.vue'

const favorites = useFavoritesStore()

onMounted(() => {
  favorites.fetchFavorites()
})
</script>

<template>
  <div class="p-4 max-w-3xl mx-auto flex flex-col gap-3">
    <h1 class="text-xl font-bold">我的收藏</h1>

    <div v-if="favorites.error" class="alert alert-error text-sm">
      <span>{{ favorites.error }}</span>
    </div>

    <div v-if="favorites.loading" class="flex flex-col gap-2">
      <div v-for="i in 4" :key="i" class="skeleton h-20 w-full" />
    </div>

    <div v-else-if="favorites.favorites.length === 0" class="text-center opacity-60 py-12">
      尚未收藏任何站點,快去地圖頁挑幾個常用站點吧!
    </div>

    <div
      v-for="fav in favorites.favorites"
      :key="fav.stationNo"
      class="card card-compact bg-base-100 shadow-sm"
    >
      <div class="card-body flex-row items-center justify-between gap-2">
        <div v-if="fav.station" class="min-w-0">
          <p class="font-semibold truncate">{{ fav.station.sna }}</p>
          <p class="text-xs opacity-60 truncate">{{ fav.station.sarea }} · {{ fav.station.ar }}</p>
          <div class="flex gap-2 mt-1">
            <span class="badge badge-success badge-sm">可借 {{ fav.station.availableRent }}</span>
            <span class="badge badge-info badge-sm">可還 {{ fav.station.availableReturn }}</span>
          </div>
        </div>
        <div v-else class="min-w-0 opacity-60">
          <p class="font-semibold">站點 {{ fav.stationNo }}</p>
          <p class="text-xs">此站點資料目前無法取得(可能已下架)</p>
        </div>
        <FavoriteButton :station-no="fav.stationNo" size="sm" />
      </div>
    </div>
  </div>
</template>

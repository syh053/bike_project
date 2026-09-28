<script setup lang="ts">
import { watch } from 'vue'
import NavBar from './components/NavBar.vue'
import { useAuthStore } from './stores/auth'
import { useFavoritesStore } from './stores/favorites'

const auth = useAuthStore()
const favorites = useFavoritesStore()

// 登入狀態改變時同步收藏清單,讓地圖/列表上的收藏星號在全站保持一致
watch(
  () => auth.isAuthenticated,
  (isAuthenticated) => {
    if (isAuthenticated) {
      favorites.fetchFavorites()
    } else {
      favorites.favorites = []
    }
  },
  { immediate: true },
)
</script>

<template>
  <div class="min-h-screen bg-base-200 flex flex-col">
    <NavBar />
    <main class="flex-1">
      <router-view />
    </main>
  </div>
</template>

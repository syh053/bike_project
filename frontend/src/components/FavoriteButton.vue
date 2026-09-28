<script setup lang="ts">
import { computed, ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useFavoritesStore } from '../stores/favorites'

const props = defineProps<{
  stationNo: string
  size?: 'xs' | 'sm' | 'md'
}>()

const auth = useAuthStore()
const favorites = useFavoritesStore()

const pending = ref(false)
const isFavorite = computed(() => favorites.isFavorite(props.stationNo))
const btnSize = computed(() => `btn-${props.size ?? 'sm'}`)

async function handleClick() {
  if (pending.value) return
  pending.value = true
  try {
    await favorites.toggleFavorite(props.stationNo)
  } catch {
    // 錯誤已存放在 favorites.error,由呼叫端 UI 決定是否顯示
  } finally {
    pending.value = false
  }
}
</script>

<template>
  <button
    v-if="auth.isAuthenticated"
    type="button"
    class="btn btn-circle"
    :class="[btnSize, isFavorite ? 'btn-warning' : 'btn-outline']"
    :disabled="pending"
    :aria-label="isFavorite ? '取消收藏' : '加入收藏'"
    @click="handleClick"
  >
    <span v-if="pending" class="loading loading-spinner loading-xs" />
    <span v-else>{{ isFavorite ? '★' : '☆' }}</span>
  </button>
</template>

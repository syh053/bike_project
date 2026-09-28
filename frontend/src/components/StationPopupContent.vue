<script setup lang="ts">
import { computed } from 'vue'
import type { Station } from '../api/types'
import FavoriteButton from './FavoriteButton.vue'

const props = defineProps<{ station: Station }>()

const updateTimeText = computed(() => {
  const date = new Date(props.station.updateTime)
  return Number.isNaN(date.getTime())
    ? props.station.updateTime
    : date.toLocaleString('zh-TW', { hour12: false })
})
</script>

<template>
  <div class="min-w-[220px] flex flex-col gap-1.5 text-sm">
    <div class="flex items-start justify-between gap-2">
      <h3 class="font-bold text-base leading-tight">{{ station.sna }}</h3>
      <FavoriteButton :station-no="station.sno" size="xs" />
    </div>

    <p class="opacity-70">{{ station.ar }}</p>

    <div class="flex gap-2">
      <span class="badge badge-success gap-1">可借 {{ station.availableRent }}</span>
      <span class="badge badge-info gap-1">可還 {{ station.availableReturn }}</span>
    </div>

    <div v-if="!station.active" class="badge badge-error badge-sm">站點暫停服務</div>

    <p class="text-xs opacity-50">更新時間:{{ updateTimeText }}</p>
  </div>
</template>

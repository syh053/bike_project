<script setup lang="ts">
import type { Station } from '../api/types'
import FavoriteButton from './FavoriteButton.vue'

defineProps<{
  stations: Station[]
  loading: boolean
}>()

const emit = defineEmits<{ select: [sno: string] }>()
</script>

<template>
  <div class="flex flex-col gap-2 overflow-y-auto">
    <div v-if="loading" class="flex flex-col gap-2">
      <div v-for="i in 6" :key="i" class="skeleton h-16 w-full" />
    </div>

    <div v-else-if="stations.length === 0" class="text-center opacity-60 py-8">找不到符合條件的站點</div>

    <button
      v-for="station in stations"
      :key="station.sno"
      type="button"
      class="text-left card card-compact bg-base-100 shadow-sm hover:shadow-md transition-shadow"
      @click="emit('select', station.sno)"
    >
      <div class="card-body flex-row items-center justify-between gap-2">
        <div class="min-w-0">
          <p class="font-semibold truncate">{{ station.sna }}</p>
          <p class="text-xs opacity-60 truncate">{{ station.sarea }} · {{ station.ar }}</p>
          <div class="flex gap-2 mt-1">
            <span class="badge badge-success badge-sm">可借 {{ station.availableRent }}</span>
            <span class="badge badge-info badge-sm">可還 {{ station.availableReturn }}</span>
            <span v-if="!station.active" class="badge badge-error badge-sm">暫停服務</span>
          </div>
        </div>
        <FavoriteButton :station-no="station.sno" size="sm" @click.stop />
      </div>
    </button>
  </div>
</template>

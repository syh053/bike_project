<script setup lang="ts">
import { createApp, onBeforeUnmount, onMounted, ref, watch, type App as VueApp } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import 'leaflet.markercluster'
import 'leaflet.markercluster/dist/MarkerCluster.css'
import 'leaflet.markercluster/dist/MarkerCluster.Default.css'
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png'
import markerIcon from 'leaflet/dist/images/marker-icon.png'
import markerShadow from 'leaflet/dist/images/marker-shadow.png'
import { pinia } from '../pinia'
import type { Station } from '../api/types'
import StationPopupContent from './StationPopupContent.vue'

// Leaflet 預設 icon 在打包後路徑會失效,改成手動指定 bundler 產生的 asset URL
delete (L.Icon.Default.prototype as unknown as { _getIconUrl?: unknown })._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
})

const props = defineProps<{ stations: Station[] }>()

const mapContainer = ref<HTMLDivElement | null>(null)
let map: L.Map | null = null
let clusterGroup: L.MarkerClusterGroup | null = null
let activePopup: { marker: L.Marker; app: VueApp } | null = null
const markerBySno = new Map<string, L.Marker>()

function closeActivePopup() {
  if (!activePopup) return
  activePopup.app.unmount()
  activePopup = null
}

// Leaflet 的 popup autoClose 會在開新 popup 時,對「上一個」marker 觸發 popupclose,
// 若各 marker 的 popupclose 都無條件 unmount 共用變數,會誤刪剛掛載好的新 popup 內容。
// 因此改成只有在 popupclose 事件來源仍是目前 activePopup 記錄的 marker 時才 unmount。
function openPopupFor(marker: L.Marker, station: Station) {
  closeActivePopup()
  const container = document.createElement('div')
  const app = createApp(StationPopupContent, { station })
  app.use(pinia)
  app.mount(container)
  marker.bindPopup(container, { closeButton: true, minWidth: 220 })
  marker.openPopup()
  activePopup = { marker, app }
}

function createMarker(station: Station): L.Marker {
  const marker = L.marker([station.lat, station.lng])
  marker.on('click', () => openPopupFor(marker, station))
  marker.on('popupclose', () => {
    if (activePopup?.marker === marker) {
      closeActivePopup()
    }
  })
  return marker
}

function renderMarkers(stations: Station[]) {
  if (!clusterGroup) return
  clusterGroup.clearLayers()
  markerBySno.clear()
  for (const station of stations) {
    const marker = createMarker(station)
    markerBySno.set(station.sno, marker)
    clusterGroup.addLayer(marker)
  }
}

function flyToStation(sno: string) {
  const station = props.stations.find((s) => s.sno === sno)
  const marker = markerBySno.get(sno)
  if (!clusterGroup || !station || !marker) return
  // marker 可能目前被群聚圖示蓋住,zoomToShowLayer 會自動縮放/展開群聚,
  // 待 marker 真正加入地圖後才呼叫 callback 開啟 popup,避免對隱藏的 marker 開 popup 失敗
  clusterGroup.zoomToShowLayer(marker, () => openPopupFor(marker, station))
}

defineExpose({ flyToStation })

onMounted(() => {
  if (!mapContainer.value) return

  const defaultLat = Number(import.meta.env.VITE_MAP_DEFAULT_LAT)
  const defaultLng = Number(import.meta.env.VITE_MAP_DEFAULT_LNG)
  const defaultZoom = Number(import.meta.env.VITE_MAP_DEFAULT_ZOOM)

  map = L.map(mapContainer.value).setView([defaultLat, defaultLng], defaultZoom)

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  }).addTo(map)

  clusterGroup = L.markerClusterGroup({
    maxClusterRadius: 60,
    iconCreateFunction: (cluster) => {
      const count = cluster.getChildCount()
      return L.divIcon({
        html: `<div class="marker-cluster-custom" style="width:40px;height:40px;">${count}</div>`,
        className: '',
        iconSize: L.point(40, 40),
      })
    },
  })
  map.addLayer(clusterGroup)

  renderMarkers(props.stations)
})

watch(
  () => props.stations,
  (next) => renderMarkers(next),
)

onBeforeUnmount(() => {
  closeActivePopup()
  map?.remove()
  map = null
  clusterGroup = null
})
</script>

<template>
  <div ref="mapContainer" class="map-panel-height w-full rounded-lg overflow-hidden" />
</template>

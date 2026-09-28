import { http } from './http'
import type { Favorite } from './types'

export function fetchFavorites() {
  return http.get<Favorite[]>('/favorites')
}

export function addFavorite(stationNo: string) {
  return http.post<{ stationNo: string; createdAt: string }>('/favorites', { stationNo })
}

export function removeFavorite(stationNo: string) {
  return http.delete<void>(`/favorites/${stationNo}`)
}

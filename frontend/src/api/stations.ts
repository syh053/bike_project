import { http } from './http'
import type { AreasResponse, Station, StationsResponse } from './types'

export interface FetchStationsParams {
  sarea?: string
  keyword?: string
  active_only?: boolean
}

export function fetchStations(params: FetchStationsParams = {}) {
  return http.get<StationsResponse>('/stations', { params })
}

export function fetchStationBySno(sno: string) {
  return http.get<Station>(`/stations/${sno}`)
}

export function fetchAreas() {
  return http.get<AreasResponse>('/stations/areas')
}

export interface User {
  id: number
  email: string
  displayName: string
}

export interface Station {
  sno: string
  sna: string
  snaen: string
  sarea: string
  sareaen: string
  ar: string
  aren: string
  lat: number
  lng: number
  totalQuantity: number
  availableRent: number
  availableReturn: number
  yb2Quantity: number
  eybQuantity: number
  active: boolean
  updateTime: string
}

export interface StationsResponse {
  updatedAt: string
  cached: boolean
  stale: boolean
  cacheAgeSeconds: number
  total: number
  data: Station[]
}

export interface AreasResponse {
  areas: string[]
}

export interface Favorite {
  stationNo: string
  createdAt: string
  station: Station | null
}

export interface ApiError {
  detail: string
}

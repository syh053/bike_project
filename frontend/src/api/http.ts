import axios from 'axios'
import type { ApiError } from './types'

export const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  withCredentials: true,
})

export function getErrorMessage(error: unknown, fallback = '發生未知錯誤,請稍後再試'): string {
  if (axios.isAxiosError<ApiError>(error)) {
    return error.response?.data?.detail ?? fallback
  }
  return fallback
}

export default http

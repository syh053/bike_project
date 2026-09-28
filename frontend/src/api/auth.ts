import { http } from './http'
import type { User } from './types'

export interface LoginPayload {
  email: string
  password: string
}

export interface RegisterPayload {
  email: string
  password: string
  displayName: string
}

export function login(payload: LoginPayload) {
  return http.post<User>('/auth/login', payload)
}

export function register(payload: RegisterPayload) {
  return http.post<User>('/auth/register', payload)
}

export function logout() {
  return http.post<void>('/auth/logout')
}

export function fetchMe() {
  return http.get<User>('/auth/me')
}

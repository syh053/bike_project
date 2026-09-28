import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import * as authApi from '../api/auth'
import { getErrorMessage } from '../api/http'
import type { User } from '../api/types'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const loading = ref(false)
  const initialized = ref(false)

  const isAuthenticated = computed(() => user.value !== null)

  async function fetchMe() {
    loading.value = true
    try {
      const { data } = await authApi.fetchMe()
      user.value = data
    } catch {
      user.value = null
    } finally {
      loading.value = false
      initialized.value = true
    }
  }

  async function login(email: string, password: string) {
    loading.value = true
    try {
      const { data } = await authApi.login({ email, password })
      user.value = data
    } catch (error) {
      throw new Error(getErrorMessage(error, '帳號或密碼錯誤'))
    } finally {
      loading.value = false
    }
  }

  async function register(email: string, password: string, displayName: string) {
    loading.value = true
    try {
      await authApi.register({ email, password, displayName })
    } catch (error) {
      loading.value = false
      throw new Error(getErrorMessage(error, '註冊失敗'))
    }
    // register 端點不會設定 session cookie(只有 login 會),註冊成功後需再呼叫一次 login 才是真正登入
    try {
      await login(email, password)
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    try {
      await authApi.logout()
    } finally {
      user.value = null
    }
  }

  return { user, loading, initialized, isAuthenticated, fetchMe, login, register, logout }
})

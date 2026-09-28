<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()

async function handleLogout() {
  await auth.logout()
  router.push({ name: 'login' })
}
</script>

<template>
  <div class="navbar bg-base-100 shadow-md px-4">
    <div class="flex-1">
      <router-link to="/" class="btn btn-ghost text-lg">新北 YouBike 即時資訊</router-link>
    </div>
    <div class="flex-none gap-2">
      <template v-if="auth.isAuthenticated">
        <router-link to="/favorites" class="btn btn-ghost">我的收藏</router-link>
        <span class="hidden sm:inline text-sm opacity-70">{{ auth.user?.displayName }}</span>
        <button class="btn btn-outline btn-sm" @click="handleLogout">登出</button>
      </template>
      <template v-else>
        <router-link to="/login" class="btn btn-ghost">登入</router-link>
        <router-link to="/register" class="btn btn-primary btn-sm">註冊</router-link>
      </template>
    </div>
  </div>
</template>

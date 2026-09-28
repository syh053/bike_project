<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

const email = ref('')
const password = ref('')
const errorMessage = ref('')
const submitting = ref(false)

async function handleSubmit() {
  errorMessage.value = ''
  submitting.value = true
  try {
    await auth.login(email.value, password.value)
    const redirect = (route.query.redirect as string) || '/'
    router.push(redirect)
  } catch (err) {
    errorMessage.value = err instanceof Error ? err.message : '登入失敗'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="flex justify-center items-center py-12 px-4">
    <div class="card w-full max-w-sm bg-base-100 shadow-xl">
      <div class="card-body">
        <h1 class="card-title">登入</h1>

        <div v-if="errorMessage" class="alert alert-error text-sm">
          <span>{{ errorMessage }}</span>
        </div>

        <form class="flex flex-col gap-3" @submit.prevent="handleSubmit">
          <label class="form-control">
            <span class="label-text mb-1">Email</span>
            <input v-model="email" type="email" required class="input input-bordered w-full" />
          </label>

          <label class="form-control">
            <span class="label-text mb-1">密碼</span>
            <input v-model="password" type="password" required class="input input-bordered w-full" />
          </label>

          <button type="submit" class="btn btn-primary mt-2" :class="{ loading: submitting }" :disabled="submitting">
            登入
          </button>
        </form>

        <p class="text-sm mt-2">
          還沒有帳號?
          <router-link to="/register" class="link link-primary">前往註冊</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

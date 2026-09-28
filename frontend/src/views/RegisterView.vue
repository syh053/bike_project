<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()

const email = ref('')
const password = ref('')
const displayName = ref('')
const errorMessage = ref('')
const submitting = ref(false)

async function handleSubmit() {
  errorMessage.value = ''
  submitting.value = true
  try {
    await auth.register(email.value, password.value, displayName.value)
    router.push('/')
  } catch (err) {
    errorMessage.value = err instanceof Error ? err.message : '註冊失敗'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="flex justify-center items-center py-12 px-4">
    <div class="card w-full max-w-sm bg-base-100 shadow-xl">
      <div class="card-body">
        <h1 class="card-title">註冊</h1>

        <div v-if="errorMessage" class="alert alert-error text-sm">
          <span>{{ errorMessage }}</span>
        </div>

        <form class="flex flex-col gap-3" @submit.prevent="handleSubmit">
          <label class="form-control">
            <span class="label-text mb-1">暱稱</span>
            <input v-model="displayName" type="text" required class="input input-bordered w-full" />
          </label>

          <label class="form-control">
            <span class="label-text mb-1">Email</span>
            <input v-model="email" type="email" required class="input input-bordered w-full" />
          </label>

          <label class="form-control">
            <span class="label-text mb-1">密碼</span>
            <input v-model="password" type="password" required minlength="8" class="input input-bordered w-full" />
          </label>

          <button type="submit" class="btn btn-primary mt-2" :class="{ loading: submitting }" :disabled="submitting">
            註冊
          </button>
        </form>

        <p class="text-sm mt-2">
          已經有帳號了?
          <router-link to="/login" class="link link-primary">前往登入</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

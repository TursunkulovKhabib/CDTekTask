<template>
  <div class="login-page">
    <div class="login-card">
      <div class="logo"></div>
      <h1>Школьная система</h1>
      <p class="subtitle">Войдите в свой кабинет</p>

      <form @submit.prevent="handleLogin">
        <div class="field">
          <label for="username">Логин</label>
          <input
            id="username"
            v-model="username"
            type="text"
            placeholder="Введите логин"
            autocomplete="username"
            required
          />
        </div>

        <div class="field">
          <label for="password">Пароль</label>
          <input
            id="password"
            v-model="password"
            type="password"
            placeholder="Введите пароль"
            autocomplete="current-password"
            required
          />
        </div>

        <p v-if="error" class="error">{{ error }}</p>

        <button type="submit" :disabled="loading">
          <span v-if="loading" class="spinner"></span>
          {{ loading ? 'Вход...' : 'Войти' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const username = ref<string>('')
const password = ref<string>('')
const error = ref<string>('')
const loading = ref<boolean>(false)

async function handleLogin(): Promise<void> {
  error.value = ''
  loading.value = true
  try {
    await auth.login(username.value, password.value)
    if (!auth.hasReportAccess) {
      error.value = 'Нет доступа к отчётам. Обратитесь к администратору.'
      auth.logout()
      return
    }
    await router.push({ name: 'Reports' })
  } catch {
    error.value = 'Неверный логин или пароль'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
}

.login-card {
  background: rgba(255, 255, 255, 0.07);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  padding: 2.75rem 2.5rem;
  border-radius: 20px;
  width: 100%;
  max-width: 420px;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4);
}

.logo {
  font-size: 2.5rem;
  text-align: center;
  margin-bottom: 0.75rem;
}

h1 {
  font-size: 1.6rem;
  font-weight: 700;
  color: #ffffff;
  text-align: center;
  margin-bottom: 0.25rem;
}

.subtitle {
  color: rgba(255, 255, 255, 0.5);
  text-align: center;
  margin-bottom: 2rem;
  font-size: 0.9rem;
}

.field {
  margin-bottom: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

label {
  font-size: 0.85rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.7);
}

input {
  padding: 0.7rem 1rem;
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 10px;
  font-size: 1rem;
  background: rgba(255, 255, 255, 0.08);
  color: #ffffff;
  transition: all 0.2s;
  outline: none;
}

input::placeholder { color: rgba(255, 255, 255, 0.3); }

input:focus {
  border-color: #818cf8;
  background: rgba(129, 140, 248, 0.1);
  box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.2);
}

button {
  width: 100%;
  padding: 0.8rem;
  background: linear-gradient(135deg, #6366f1, #818cf8);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  margin-top: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  letter-spacing: 0.02em;
}

button:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 8px 25px rgba(99, 102, 241, 0.45);
}

button:active:not(:disabled) { transform: translateY(0); }
button:disabled { opacity: 0.6; cursor: not-allowed; }

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  flex-shrink: 0;
}

@keyframes spin { to { transform: rotate(360deg); } }

.error {
  color: #fca5a5;
  font-size: 0.875rem;
  margin-bottom: 0.75rem;
  padding: 0.6rem 0.85rem;
  background: rgba(239, 68, 68, 0.15);
  border-radius: 8px;
  border: 1px solid rgba(239, 68, 68, 0.3);
}
</style>
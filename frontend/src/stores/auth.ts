import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api/axios'
import type { LoginResponse, UserRole } from '@/types'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('access_token'))
  const role = ref<UserRole | null>(localStorage.getItem('role') as UserRole | null)
  const fullName = ref<string | null>(localStorage.getItem('full_name'))
  const hasReportAccess = ref<boolean>(
    localStorage.getItem('has_report_access') === 'true'
  )

  const isAuthenticated = computed<boolean>(() => !!token.value)

  async function login(username: string, password: string): Promise<void> {
    const { data } = await api.post<LoginResponse>('/token/', { username, password })

    token.value = data.access
    role.value = data.role
    fullName.value = data.full_name
    hasReportAccess.value = data.has_report_access

    localStorage.setItem('access_token', data.access)
    localStorage.setItem('role', data.role)
    localStorage.setItem('full_name', data.full_name)
    localStorage.setItem('has_report_access', String(data.has_report_access))
  }

  function logout(): void {
    token.value = null
    role.value = null
    fullName.value = null
    hasReportAccess.value = false
    localStorage.clear()
  }

  return { token, role, fullName, hasReportAccess, isAuthenticated, login, logout }
})
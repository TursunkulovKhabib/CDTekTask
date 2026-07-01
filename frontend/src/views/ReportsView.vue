<template>
  <div class="reports-page">
    <header class="page-header">
      <div class="header-left">
        <span class="logo"></span>
        <div>
          <h1>Отчёты</h1>
          <p class="welcome">{{ auth.fullName }} · {{ roleLabel }}</p>
        </div>
      </div>
      <button class="logout-btn" @click="handleLogout">Выйти</button>
    </header>

    <div class="tabs">
      <button
        v-if="auth.role === 'director' || auth.role === 'teacher'"
        :class="['tab', { active: activeTab === 'student' }]"
        @click="activeTab = 'student'"
      >По студенту</button>

      <button
        v-if="auth.role === 'director' || auth.role === 'teacher'"
        :class="['tab', { active: activeTab === 'group' }]"
        @click="activeTab = 'group'"
      >По группе (RAW SQL)</button>

      <button
        v-if="auth.role === 'student'"
        :class="['tab', { active: activeTab === 'student' }]"
        @click="activeTab = 'student'"
      >Мои оценки</button>
    </div>

    <section v-if="activeTab === 'student'" class="report-section">
      <div class="controls">
        <label>ID студента:</label>
        <input v-model.number="studentId" type="number" :min="1" placeholder="1" />
        <button class="action-btn" @click="loadStudentReport" :disabled="loadingStudent">
          {{ loadingStudent ? 'Загрузка...' : 'Показать' }}
        </button>
      </div>
      <p v-if="studentError" class="error">{{ studentError }}</p>
      <ReportTable :rows="studentRows" :columns="studentColumns" />
    </section>

    <section v-else class="report-section">
      <div class="controls">
        <label>ID группы:</label>
        <input v-model.number="groupId" type="number" :min="1" placeholder="1" />
        <button class="action-btn" @click="loadGroupReport" :disabled="loadingGroup">
          {{ loadingGroup ? 'Загрузка...' : 'Показать' }}
        </button>
      </div>
      <p v-if="groupError" class="error">{{ groupError }}</p>
      <ReportTable :rows="groupRows" :columns="groupColumns" />
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import ReportTable from '@/components/ReportTable.vue'
import api from '@/api/axios'
import type { TableColumn } from '@/types'

const router = useRouter()
const auth = useAuthStore()

type TabType = 'student' | 'group'
const activeTab = ref<TabType>('student')

const studentId = ref<number>(1)
const studentRows = ref<Record<string, unknown>[]>([])
const loadingStudent = ref<boolean>(false)
const studentError = ref<string>('')

const studentColumns: TableColumn[] = [
  { key: 'student__user__last_name', label: 'Фамилия' },
  { key: 'student__user__first_name', label: 'Имя' },
  { key: 'student__group__name', label: 'Группа' },
  { key: 'subject__name', label: 'Предмет' },
  { key: 'avg_grade', label: 'Средний балл' },
]

async function loadStudentReport(): Promise<void> {
  studentError.value = ''
  loadingStudent.value = true
  try {
    const { data } = await api.get<Record<string, unknown>[]>(
      `/reports/student/${studentId.value}/`
    )
    studentRows.value = data
  } catch (e: unknown) {
    const err = e as { response?: { data?: { error?: string } } }
    studentError.value = err.response?.data?.error ?? 'Ошибка загрузки'
    studentRows.value = []
  } finally {
    loadingStudent.value = false
  }
}

const groupId = ref<number>(1)
const groupRows = ref<Record<string, unknown>[]>([])
const loadingGroup = ref<boolean>(false)
const groupError = ref<string>('')

const groupColumns: TableColumn[] = [
  { key: 'group_name', label: 'Группа' },
  { key: 'subject_name', label: 'Предмет' },
  { key: 'avg_grade', label: 'Средний балл' },
]

async function loadGroupReport(): Promise<void> {
  groupError.value = ''
  loadingGroup.value = true
  try {
    const { data } = await api.get<Record<string, unknown>[]>(
      `/reports/group/${groupId.value}/`
    )
    groupRows.value = data
  } catch (e: unknown) {
    const err = e as { response?: { data?: { error?: string } } }
    groupError.value = err.response?.data?.error ?? 'Ошибка загрузки'
    groupRows.value = []
  } finally {
    loadingGroup.value = false
  }
}

const roleLabel = computed<string>(() => {
  const labels: Record<string, string> = {
    director: 'Директор',
    teacher: 'Учитель',
    student: 'Студент',
  }
  return labels[auth.role ?? ''] ?? ''
})

function handleLogout(): void {
  auth.logout()
  void router.push({ name: 'Login' })
}

onMounted(() => {
  if (auth.role === 'student' && auth.studentId) {
    studentId.value = auth.studentId
    void loadStudentReport()
  }
})

</script>

<style scoped>
.reports-page {
  max-width: 980px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 16px;
  padding: 1rem 1.5rem;
  backdrop-filter: blur(10px);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logo { font-size: 1.75rem; }

h1 {
  font-size: 1.4rem;
  font-weight: 700;
  color: #ffffff;
  margin: 0;
}

.welcome {
  color: rgba(255,255,255,0.5);
  font-size: 0.85rem;
  margin-top: 0.1rem;
}

.logout-btn {
  padding: 0.5rem 1.25rem;
  background: rgba(239, 68, 68, 0.15);
  color: #fca5a5;
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.logout-btn:hover {
  background: rgba(239, 68, 68, 0.25);
  color: #fff;
}

.tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid rgba(255,255,255,0.1);
  padding-bottom: 0;
}

.tab {
  padding: 0.65rem 1.25rem;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 0.95rem;
  color: rgba(255,255,255,0.45);
  border-bottom: 2px solid transparent;
  margin-bottom: -1px;
  transition: all 0.2s;
  border-radius: 6px 6px 0 0;
}

.tab:hover { color: rgba(255,255,255,0.75); }

.tab.active {
  color: #818cf8;
  border-bottom-color: #818cf8;
  font-weight: 600;
}

.report-section {
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 16px;
  padding: 1.75rem;
  backdrop-filter: blur(10px);
}

.controls {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.controls label {
  font-weight: 500;
  color: rgba(255,255,255,0.7);
  font-size: 0.9rem;
}

.controls input {
  padding: 0.5rem 0.75rem;
  border: 1px solid rgba(255,255,255,0.15);
  border-radius: 8px;
  width: 100px;
  font-size: 1rem;
  background: rgba(255,255,255,0.08);
  color: #fff;
  outline: none;
  transition: all 0.2s;
}

.controls input:focus {
  border-color: #818cf8;
  box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.2);
}

.action-btn {
  padding: 0.5rem 1.25rem;
  background: linear-gradient(135deg, #6366f1, #818cf8);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.action-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
}

.action-btn:disabled { opacity: 0.5; cursor: not-allowed; }

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
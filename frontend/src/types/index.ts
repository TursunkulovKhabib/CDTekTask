export type UserRole = 'director' | 'teacher' | 'student'

export interface LoginResponse {
  access: string
  refresh: string
  role: UserRole
  full_name: string
  has_report_access: boolean
}

export interface StudentReportRow {
  student__user__last_name: string
  student__user__first_name: string
  student__group__name: string
  subject__name: string
  avg_grade: number
}

export interface GroupReportRow {
  group_name: string
  subject_name: string
  avg_grade: number
}

export interface TableColumn {
  key: string
  label: string
}

declare module 'vue-router' {
  interface RouteMeta {
    guestOnly?: boolean
    requiresAuth?: boolean
    requiresReport?: boolean
  }
}
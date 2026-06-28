<template>
  <div class="table-wrap">
    <table v-if="rows.length">
      <thead>
        <tr>
          <th v-for="col in columns" :key="col.key">{{ col.label }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, i) in rows" :key="i">
          <td v-for="col in columns" :key="col.key">
            {{ formatCell(row[col.key], col.key) }}
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else class="empty">Нет данных — введите ID и нажмите «Показать»</p>
  </div>
</template>

<script setup lang="ts">
import type { TableColumn } from '@/types'

interface Props {
  rows: Record<string, unknown>[]
  columns: TableColumn[]
}

defineProps<Props>()

function formatCell(value: unknown, key: string): string {
  if (key === 'avg_grade' && value != null) {
    return Number(value).toFixed(2)
  }
  return value != null ? String(value) : '—'
}
</script>

<style scoped>
.table-wrap { overflow-x: auto; }

table { width: 100%; border-collapse: collapse; font-size: 0.9rem; }

th {
  background: rgba(129, 140, 248, 0.12);
  padding: 0.75rem 1rem;
  text-align: left;
  font-weight: 600;
  color: #a5b4fc;
  border-bottom: 1px solid rgba(255,255,255,0.08);
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

td {
  padding: 0.7rem 1rem;
  border-bottom: 1px solid rgba(255,255,255,0.06);
  color: rgba(255,255,255,0.85);
}

tr:last-child td { border-bottom: none; }
tr:hover td { background: rgba(255,255,255,0.04); }

.empty {
  text-align: center;
  padding: 3rem;
  color: rgba(255,255,255,0.3);
  font-size: 0.9rem;
}
</style>
<template>
  <div class="diaries-page">
    <div class="page-header">
      <h1>Our Diary</h1>
      <p>Stories from the heart</p>
    </div>

    <!-- Filter Section -->
    <div class="filter-section">
      <div class="search-box">
        <el-icon><Search /></el-icon>
        <input v-model="filterForm.tags" placeholder="Search by tags..." @keyup.enter="loadDiaries" />
      </div>

      <div class="category-filters">
        <button class="filter-btn" :class="{ active: !filterForm.category }" @click="setCategory('')">All</button>
        <button v-for="cat in categories" :key="cat" class="filter-btn"
          :class="{ active: filterForm.category === cat }" @click="setCategory(cat)">
          {{ cat }}
        </button>
      </div>
    </div>

    <!-- Diary List -->
    <div class="diaries-container" v-loading="loading">
      <div class="diaries-list" v-if="diaries.length > 0">
        <div v-for="diary in diaries" :key="diary.id" class="diary-card" @click="openDiary(diary)">
          <div class="diary-left">
            <div class="date-block">
              <span class="day">{{ getDayFromDate(diary.created_at) }}</span>
              <span class="month">{{ getMonthFromDate(diary.created_at) }}</span>
              <span class="year">{{ getYearFromDate(diary.created_at) }}</span>
            </div>
          </div>
          <div class="diary-right">
            <div class="diary-header-row">
              <h3>{{ diary.title }}</h3>
              <span class="mood" v-if="diary.mood">{{ diary.mood }}</span>
            </div>
            <p class="diary-excerpt">{{ diary.content }}</p>
            <div class="diary-footer">
              <div class="tags" v-if="diary.tags?.length">
                <span v-for="tag in diary.tags.slice(0, 3)" :key="tag" class="tag">{{ tag }}</span>
              </div>
              <span class="category-label" v-if="diary.category">{{ diary.category }}</span>
            </div>
          </div>
        </div>
      </div>

      <div v-else-if="!loading" class="empty-state">
        <el-icon><Document /></el-icon>
        <p>No diary entries found. Try adjusting your filters.</p>
      </div>

      <!-- Pagination -->
      <div class="pagination-container" v-if="diaries.length > 0">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.per_page"
          :total="pagination.total"
          :page-sizes="[10, 20]"
          layout="prev, pager, next"
          @current-change="loadDiaries"
        />
      </div>
    </div>

    <!-- Diary Detail Dialog -->
    <el-dialog v-model="showDetail" :title="currentDiary?.title" width="680px" destroy-on-close class="diary-dialog">
      <div class="diary-detail" v-if="currentDiary">
        <div class="detail-header">
          <span class="detail-mood" v-if="currentDiary.mood">{{ currentDiary.mood }}</span>
          <span class="detail-date">{{ formatDate(currentDiary.created_at) }}</span>
          <span class="detail-category" v-if="currentDiary.category">{{ currentDiary.category }}</span>
        </div>
        <div class="detail-content">{{ currentDiary.content }}</div>
        <div class="detail-tags" v-if="currentDiary.tags?.length">
          <span v-for="tag in currentDiary.tags" :key="tag" class="tag">{{ tag }}</span>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { diaryApi } from '@/api/diary'
import dayjs from 'dayjs'
import { Search, Document } from '@element-plus/icons-vue'

const diaries = ref([])
const categories = ref([])
const loading = ref(false)
const showDetail = ref(false)
const currentDiary = ref(null)

const filterForm = reactive({ category: '', tags: '' })
const pagination = reactive({ page: 1, per_page: 10, total: 0 })

const loadDiaries = async () => {
  loading.value = true
  try {
    const params = { page: pagination.page, per_page: pagination.per_page }
    if (filterForm.category) params.category = filterForm.category
    if (filterForm.tags) params.tags = filterForm.tags
    const data = await diaryApi.getDiaries(params)
    diaries.value = data.diaries || []
    pagination.total = data.total || 0
  } catch (e) {
    console.error('Failed to load diaries:', e)
  } finally {
    loading.value = false
  }
}

const loadCategories = async () => {
  try { categories.value = (await diaryApi.getCategories()).categories || [] } catch {}
}

const setCategory = (cat) => {
  filterForm.category = cat
  pagination.page = 1
  loadDiaries()
}

const openDiary = (diary) => {
  currentDiary.value = diary
  showDetail.value = true
}

const formatDate = (d) => dayjs(d).format('MMMM D, YYYY · HH:mm')
const getDayFromDate = (d) => dayjs(d).format('DD')
const getMonthFromDate = (d) => dayjs(d).format('MMM')
const getYearFromDate = (d) => dayjs(d).format('YYYY')

onMounted(() => { loadDiaries(); loadCategories() })
</script>

<style lang="scss" scoped>
@import '@/assets/styles/variables.scss';

.diaries-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem;
}

.page-header {
  text-align: center;
  margin-bottom: 3rem;

  h1 {
    font-size: 2.5rem;
    color: var(--primary-color);
    margin-bottom: 0.5rem;
    font-family: 'Georgia', serif;
  }

  p { color: var(--text-secondary); }
}

.filter-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.search-box {
  position: relative;
  width: 100%;
  max-width: 400px;

  .el-icon {
    position: absolute; left: 1rem; top: 50%;
    transform: translateY(-50%); color: var(--text-secondary);
  }

  input {
    width: 100%;
    padding: 0.8rem 1rem 0.8rem 2.5rem;
    border: 1px solid rgba(0,0,0,0.1);
    border-radius: 50px;
    background: white;
    font-size: 1rem;
    transition: all 0.3s ease;

    &:focus {
      outline: none;
      border-color: var(--primary-color);
      box-shadow: 0 0 0 3px rgba(232, 166, 177, 0.2);
    }
  }
}

.category-filters {
  display: flex; flex-wrap: wrap; gap: 0.8rem; justify-content: center;

  .filter-btn {
    padding: 0.5rem 1.2rem; border-radius: 20px; background: white;
    color: var(--text-secondary); font-size: 0.9rem;
    transition: all 0.3s ease; border: 1px solid transparent;

    &:hover { color: var(--primary-color); background: var(--bg-color); }
    &.active { background: var(--primary-color); color: white; box-shadow: var(--shadow-sm); }
  }
}

.diaries-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.diary-card {
  display: flex;
  gap: 1.5rem;
  background: white;
  border-radius: var(--radius-md);
  padding: 1.5rem;
  box-shadow: var(--shadow-sm);
  cursor: pointer;
  transition: all 0.4s ease;
  border-left: 4px solid transparent;

  &:hover {
    transform: translateX(4px);
    box-shadow: var(--shadow-md);
    border-left-color: var(--primary-color);
  }
}

.diary-left {
  flex-shrink: 0;
}

.date-block {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 60px;
  padding: 12px 8px;
  background: var(--bg-color);
  border-radius: 12px;

  .day {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--primary-color);
    line-height: 1.2;
  }

  .month {
    font-size: 0.8rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    font-weight: 600;
  }

  .year {
    font-size: 0.7rem;
    color: #ccc;
  }
}

.diary-right {
  flex: 1;
  min-width: 0;
}

.diary-header-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.5rem;

  h3 {
    margin: 0;
    font-size: 1.1rem;
    color: var(--text-primary);
    font-weight: 600;
  }
}

.mood {
  font-size: 1.2rem;
  flex-shrink: 0;
}

.diary-excerpt {
  color: var(--text-secondary);
  font-size: 0.95rem;
  line-height: 1.7;
  margin: 0 0 1rem;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.diary-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tags {
  display: flex; gap: 6px; flex-wrap: wrap;
}

.tag {
  padding: 3px 10px;
  border-radius: 10px;
  background: var(--bg-color);
  color: var(--primary-color);
  font-size: 0.8rem;
  font-weight: 500;
}

.category-label {
  font-size: 0.8rem;
  color: var(--text-secondary);
  background: #f5f5f5;
  padding: 3px 10px;
  border-radius: 10px;
}

.empty-state {
  text-align: center; padding: 4rem; color: var(--text-secondary);

  .el-icon { font-size: 3rem; margin-bottom: 1rem; color: var(--primary-color); }
}

.pagination-container {
  display: flex; justify-content: center; margin-top: 3rem;
}

:deep(.el-pagination) {
  --el-pagination-hover-color: var(--primary-color);
  --el-pagination-button-bg-color: transparent;
}

/* Detail Dialog */
.diary-detail {
  .detail-header {
    display: flex; align-items: center; gap: 12px;
    margin-bottom: 1.5rem; padding-bottom: 1rem;
    border-bottom: 1px solid #f0f0f0;
  }

  .detail-mood { font-size: 1.5rem; }
  .detail-date { color: var(--text-secondary); font-size: 0.9rem; }
  .detail-category {
    color: var(--primary-color); font-size: 0.85rem; font-weight: 500;
    background: var(--bg-color); padding: 3px 10px; border-radius: 10px;
  }

  .detail-content {
    color: var(--text-primary); font-size: 1rem; line-height: 2;
    white-space: pre-wrap; margin-bottom: 1.5rem;
  }

  .detail-tags {
    display: flex; gap: 6px; flex-wrap: wrap;
    padding-top: 1rem; border-top: 1px solid #f0f0f0;
  }
}

@media (max-width: 600px) {
  .diary-card { flex-direction: column; gap: 1rem; }
  .date-block { flex-direction: row; gap: 6px; width: auto; padding: 8px 16px; }
}
</style>
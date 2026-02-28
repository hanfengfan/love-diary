<template>
  <div class="admin-diaries">
    <div class="page-actions">
      <el-button type="primary" class="action-btn" @click="openCreateDialog">
        <el-icon><Plus /></el-icon>
        新建日记
      </el-button>
    </div>

    <!-- Filters -->
    <div class="filter-bar">
      <el-select v-model="filterForm.category" placeholder="所有分类" clearable @change="loadDiaries">
        <el-option v-for="cat in categories" :key="cat" :label="cat" :value="cat" />
      </el-select>
      <el-select v-model="filterForm.mood" placeholder="所有心情" clearable @change="loadDiaries">
        <el-option v-for="m in moods" :key="m" :label="m" :value="m" />
      </el-select>
      <el-input v-model="filterForm.tags" placeholder="按标签搜索..." clearable style="width: 200px" @keyup.enter="loadDiaries" />
      <el-button @click="resetFilter">重置</el-button>
    </div>

    <!-- Diary List -->
    <div class="diary-list" v-loading="loading">
      <div v-for="diary in diaries" :key="diary.id" class="diary-card">
        <div class="diary-header">
          <div class="diary-title-row">
            <div class="mood-badge" v-if="diary.mood">{{ diary.mood }}</div>
            <h3>{{ diary.title }}</h3>
          </div>
          <div class="diary-actions">
            <el-button type="primary" size="small" text @click="editDiary(diary)">
              <el-icon><Edit /></el-icon> 编辑
            </el-button>
            <el-button type="danger" size="small" text @click="deleteDiary(diary)">
              <el-icon><Delete /></el-icon> 删除
            </el-button>
          </div>
        </div>
        <p class="diary-content">{{ diary.content }}</p>
        <div class="diary-footer">
          <div class="tags">
            <el-tag v-for="tag in diary.tags" :key="tag" size="small" effect="plain" class="tag-item">{{ tag }}</el-tag>
          </div>
          <div class="meta-info">
            <el-tag size="small" type="info">{{ diary.category }}</el-tag>
            <span class="date">{{ formatDate(diary.created_at) }}</span>
          </div>
        </div>
      </div>
    </div>

    <div v-if="!loading && diaries.length === 0" class="empty-state">
      <el-icon><Document /></el-icon>
      <p>暂无日记</p>
    </div>

    <div class="pagination-bar" v-if="pagination.total > 0">
      <el-pagination v-model:current-page="pagination.page" v-model:page-size="pagination.per_page"
        :total="pagination.total" :page-sizes="[10, 20, 50]"
        layout="total, sizes, prev, pager, next" @size-change="loadDiaries" @current-change="loadDiaries" />
    </div>

    <!-- Create/Edit Dialog -->
    <el-dialog v-model="showDialog" :title="isEdit ? '编辑日记' : '新建日记'" width="640px" destroy-on-close>
      <el-form :model="diaryForm" label-width="80px" label-position="top">
        <el-form-item label="标题" required>
          <el-input v-model="diaryForm.title" placeholder="请输入日记标题" maxlength="100" show-word-limit />
        </el-form-item>
        <el-form-item label="内容" required>
          <el-input v-model="diaryForm.content" type="textarea" :rows="8" placeholder="记录你们的故事..." />
        </el-form-item>
        <div class="form-row">
          <el-form-item label="分类" style="flex: 1">
            <el-select v-model="diaryForm.category" placeholder="选择分类" style="width: 100%">
              <el-option label="日常" value="日常" />
              <el-option label="约会" value="约会" />
              <el-option label="节日" value="节日" />
              <el-option label="旅行" value="旅行" />
              <el-option label="纪念日" value="纪念日" />
              <el-option label="其他" value="其他" />
            </el-select>
          </el-form-item>
          <el-form-item label="心情" style="flex: 1">
            <el-select v-model="diaryForm.mood" placeholder="今天的心情" clearable style="width: 100%">
              <el-option label="😊 开心" value="😊 开心" />
              <el-option label="🥰 幸福" value="🥰 幸福" />
              <el-option label="😌 平静" value="😌 平静" />
              <el-option label="🤔 思考" value="🤔 思考" />
              <el-option label="😢 难过" value="😢 难过" />
              <el-option label="😤 生气" value="😤 生气" />
              <el-option label="🥳 兴奋" value="🥳 兴奋" />
            </el-select>
          </el-form-item>
        </div>
        <el-form-item label="标签">
          <el-input v-model="diaryForm.tags" placeholder="多个标签用逗号分隔，如：散步,公园" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="handleSave">
          {{ isEdit ? '保存修改' : '发布日记' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { diaryApi } from '@/api/diary'
import dayjs from 'dayjs'

const diaries = ref([])
const categories = ref([])
const moods = ref([])
const loading = ref(false)
const saving = ref(false)
const showDialog = ref(false)
const isEdit = ref(false)

const filterForm = reactive({ category: '', mood: '', tags: '' })
const pagination = reactive({ page: 1, per_page: 10, total: 0 })
const diaryForm = reactive({ id: null, title: '', content: '', category: '日常', tags: '', mood: '' })

const loadDiaries = async () => {
  loading.value = true
  try {
    const data = await diaryApi.getDiaries({ page: pagination.page, per_page: pagination.per_page, ...filterForm })
    diaries.value = data.diaries || []
    pagination.total = data.total || 0
  } catch { ElMessage.error('加载日记失败') }
  finally { loading.value = false }
}

const loadCategories = async () => {
  try { categories.value = (await diaryApi.getCategories()).categories || [] } catch {}
}

const loadMoods = async () => {
  try { moods.value = (await diaryApi.getMoods()).moods || [] } catch {}
}

const resetFilter = () => {
  Object.assign(filterForm, { category: '', mood: '', tags: '' })
  pagination.page = 1
  loadDiaries()
}

const openCreateDialog = () => {
  isEdit.value = false
  Object.assign(diaryForm, { id: null, title: '', content: '', category: '日常', tags: '', mood: '' })
  showDialog.value = true
}

const editDiary = (d) => {
  isEdit.value = true
  Object.assign(diaryForm, {
    id: d.id, title: d.title, content: d.content,
    category: d.category, tags: d.tags ? d.tags.join(', ') : '', mood: d.mood || ''
  })
  showDialog.value = true
}

const handleSave = async () => {
  if (!diaryForm.title.trim()) { ElMessage.error('请输入标题'); return }
  if (!diaryForm.content.trim()) { ElMessage.error('请输入内容'); return }
  saving.value = true
  try {
    const tags = diaryForm.tags ? diaryForm.tags.split(',').map(t => t.trim()).filter(Boolean) : []
    const payload = { title: diaryForm.title, content: diaryForm.content, category: diaryForm.category, tags, mood: diaryForm.mood || null }
    if (isEdit.value) {
      await diaryApi.updateDiary(diaryForm.id, payload)
      ElMessage.success('日记更新成功')
    } else {
      await diaryApi.createDiary(payload)
      ElMessage.success('日记发布成功')
    }
    showDialog.value = false
    loadDiaries()
  } catch { ElMessage.error('保存失败') }
  finally { saving.value = false }
}

const deleteDiary = async (d) => {
  try {
    await ElMessageBox.confirm(`确定删除日记"${d.title}"吗？`, '确认', { type: 'warning' })
    await diaryApi.deleteDiary(d.id)
    ElMessage.success('删除成功')
    loadDiaries()
  } catch (e) { if (e !== 'cancel') ElMessage.error('删除失败') }
}

const formatDate = (d) => dayjs(d).format('YYYY-MM-DD HH:mm')

onMounted(() => { loadDiaries(); loadCategories(); loadMoods() })
</script>

<style scoped>
.page-actions { display: flex; justify-content: flex-end; margin-bottom: 20px; }
.action-btn { border-radius: 10px; padding: 10px 20px; font-weight: 500; }

.filter-bar {
  display: flex; gap: 12px; margin-bottom: 24px; align-items: center;
  padding: 16px 20px; background: white; border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}

.diary-list { display: flex; flex-direction: column; gap: 16px; }

.diary-card {
  background: white; border-radius: 14px; padding: 20px 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05); transition: all 0.3s ease;
  border-left: 4px solid transparent;
}
.diary-card:hover {
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
  border-left-color: #d45d79;
}

.diary-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px; }
.diary-title-row { display: flex; align-items: center; gap: 10px; }
.diary-title-row h3 { margin: 0; font-size: 1.1rem; color: #333; }

.mood-badge {
  font-size: 1.2rem; background: #fff5f7; padding: 4px 8px; border-radius: 8px;
}

.diary-content {
  color: #666; font-size: 0.95rem; line-height: 1.7; margin: 0 0 16px;
  display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden;
}

.diary-footer { display: flex; justify-content: space-between; align-items: center; }
.tags { display: flex; gap: 6px; flex-wrap: wrap; }
.tag-item { border-radius: 6px; }
.meta-info { display: flex; align-items: center; gap: 10px; }
.date { font-size: 0.8rem; color: #bbb; }

.form-row { display: flex; gap: 16px; }

.empty-state {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  height: 300px; color: #ccc; background: white; border-radius: 14px;
}
.empty-state .el-icon { font-size: 48px; margin-bottom: 12px; }

.pagination-bar { display: flex; justify-content: center; margin-top: 24px; }
</style>
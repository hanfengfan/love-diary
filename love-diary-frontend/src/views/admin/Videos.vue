<template>
  <div class="admin-videos">
    <div class="page-actions">
      <el-button type="primary" class="action-btn" @click="showUploadDialog = true">
        <el-icon><Upload /></el-icon>
        上传视频
      </el-button>
    </div>

    <!-- Filters -->
    <div class="filter-bar">
      <el-select v-model="filterForm.category" placeholder="所有分类" clearable @change="loadVideos">
        <el-option v-for="cat in categories" :key="cat" :label="cat" :value="cat" />
      </el-select>
      <el-input v-model="filterForm.tags" placeholder="按标签搜索..." clearable style="width: 200px" @keyup.enter="loadVideos" />
      <el-button @click="resetFilter">重置</el-button>
    </div>

    <!-- Video List -->
    <div class="video-grid" v-loading="loading">
      <div v-for="video in videos" :key="video.id" class="video-card">
        <div class="video-thumb">
          <img v-if="video.thumbnail" :src="`/uploads/${video.thumbnail}`" :alt="video.title" />
          <div v-else class="thumb-placeholder">
            <el-icon><VideoPlay /></el-icon>
          </div>
          <span v-if="video.duration" class="duration-badge">{{ formatDuration(video.duration) }}</span>
          <div class="card-actions">
            <el-button type="primary" size="small" circle @click="editVideo(video)"><el-icon><Edit /></el-icon></el-button>
            <el-button type="danger" size="small" circle @click="deleteVideo(video)"><el-icon><Delete /></el-icon></el-button>
          </div>
        </div>
        <div class="video-info">
          <h4>{{ video.title }}</h4>
          <p class="desc">{{ video.description || '暂无描述' }}</p>
          <div class="meta">
            <el-tag size="small" type="info">{{ video.category }}</el-tag>
            <span class="date">{{ formatDate(video.created_at) }}</span>
          </div>
        </div>
      </div>
    </div>

    <div v-if="!loading && videos.length === 0" class="empty-state">
      <el-icon><VideoPlay /></el-icon>
      <p>暂无视频</p>
    </div>

    <div class="pagination-bar" v-if="pagination.total > 0">
      <el-pagination v-model:current-page="pagination.page" v-model:page-size="pagination.per_page"
        :total="pagination.total" :page-sizes="[12, 24, 48]"
        layout="total, sizes, prev, pager, next" @size-change="loadVideos" @current-change="loadVideos" />
    </div>

    <!-- Upload Dialog -->
    <el-dialog v-model="showUploadDialog" title="上传视频" width="520px" destroy-on-close>
      <el-form :model="uploadForm" label-width="80px">
        <el-form-item label="视频文件" required>
          <el-upload class="video-uploader" :show-file-list="false" :before-upload="beforeUpload" action="">
            <div v-if="uploadForm.file" class="file-selected">
              <el-icon><VideoPlay /></el-icon>
              <span>{{ uploadForm.file.name }}</span>
            </div>
            <div v-else class="upload-trigger">
              <el-icon><Upload /></el-icon>
              <span>点击选择视频文件</span>
            </div>
          </el-upload>
        </el-form-item>
        <el-form-item label="标题" required>
          <el-input v-model="uploadForm.title" placeholder="请输入视频标题" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="uploadForm.description" type="textarea" :rows="3" placeholder="请输入视频描述" />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="uploadForm.category" placeholder="选择分类">
            <el-option label="日常" value="日常" />
            <el-option label="约会" value="约会" />
            <el-option label="节日" value="节日" />
            <el-option label="旅行" value="旅行" />
            <el-option label="其他" value="其他" />
          </el-select>
        </el-form-item>
        <el-form-item label="标签">
          <el-input v-model="uploadForm.tags" placeholder="多个标签用逗号分隔" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showUploadDialog = false">取消</el-button>
        <el-button type="primary" :loading="uploading" @click="handleUpload">上传</el-button>
      </template>
    </el-dialog>

    <!-- Edit Dialog -->
    <el-dialog v-model="showEditDialog" title="编辑视频" width="520px" destroy-on-close>
      <el-form :model="editForm" label-width="80px">
        <el-form-item label="标题" required>
          <el-input v-model="editForm.title" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="editForm.description" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="editForm.category">
            <el-option label="日常" value="日常" />
            <el-option label="约会" value="约会" />
            <el-option label="节日" value="节日" />
            <el-option label="旅行" value="旅行" />
            <el-option label="其他" value="其他" />
          </el-select>
        </el-form-item>
        <el-form-item label="标签">
          <el-input v-model="editForm.tags" placeholder="多个标签用逗号分隔" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { videoApi } from '@/api/video'
import dayjs from 'dayjs'

const videos = ref([])
const categories = ref([])
const loading = ref(false)
const uploading = ref(false)
const saving = ref(false)
const showUploadDialog = ref(false)
const showEditDialog = ref(false)

const filterForm = reactive({ category: '', tags: '' })
const pagination = reactive({ page: 1, per_page: 12, total: 0 })
const uploadForm = reactive({ file: null, title: '', description: '', category: '日常', tags: '' })
const editForm = reactive({ id: null, title: '', description: '', category: '', tags: '' })

const loadVideos = async () => {
  loading.value = true
  try {
    const params = { page: pagination.page, per_page: pagination.per_page, ...filterForm }
    const data = await videoApi.getVideos(params)
    videos.value = data.videos || []
    pagination.total = data.total || 0
  } catch (e) {
    ElMessage.error('加载视频失败')
  } finally {
    loading.value = false
  }
}

const loadCategories = async () => {
  try {
    const data = await videoApi.getCategories()
    categories.value = data.categories || []
  } catch {}
}

const resetFilter = () => {
  Object.assign(filterForm, { category: '', tags: '' })
  pagination.page = 1
  loadVideos()
}

const beforeUpload = (file) => {
  const isVideo = file.type.startsWith('video/')
  if (!isVideo) { ElMessage.error('只能上传视频文件!'); return false }
  if (file.size / 1024 / 1024 > 100) { ElMessage.error('视频大小不能超过100MB!'); return false }
  uploadForm.file = file
  return false
}

const handleUpload = async () => {
  if (!uploadForm.file) { ElMessage.error('请选择视频文件'); return }
  if (!uploadForm.title.trim()) { ElMessage.error('请输入视频标题'); return }
  uploading.value = true
  try {
    const fd = new FormData()
    fd.append('video', uploadForm.file)
    fd.append('title', uploadForm.title)
    fd.append('description', uploadForm.description)
    fd.append('category', uploadForm.category)
    fd.append('tags', uploadForm.tags)
    await videoApi.uploadVideo(fd)
    ElMessage.success('上传成功')
    showUploadDialog.value = false
    Object.assign(uploadForm, { file: null, title: '', description: '', category: '日常', tags: '' })
    loadVideos()
  } catch { ElMessage.error('上传失败') }
  finally { uploading.value = false }
}

const editVideo = (v) => {
  Object.assign(editForm, { id: v.id, title: v.title, description: v.description || '', category: v.category, tags: v.tags ? v.tags.join(', ') : '' })
  showEditDialog.value = true
}

const handleSave = async () => {
  if (!editForm.title.trim()) { ElMessage.error('请输入标题'); return }
  saving.value = true
  try {
    const tags = editForm.tags ? editForm.tags.split(',').map(t => t.trim()).filter(Boolean) : []
    await videoApi.updateVideo(editForm.id, { title: editForm.title, description: editForm.description, category: editForm.category, tags })
    ElMessage.success('保存成功')
    showEditDialog.value = false
    loadVideos()
  } catch { ElMessage.error('保存失败') }
  finally { saving.value = false }
}

const deleteVideo = async (v) => {
  try {
    await ElMessageBox.confirm(`确定删除视频"${v.title}"吗？`, '确认', { type: 'warning' })
    await videoApi.deleteVideo(v.id)
    ElMessage.success('删除成功')
    loadVideos()
  } catch (e) { if (e !== 'cancel') ElMessage.error('删除失败') }
}

const formatDate = (d) => dayjs(d).format('YYYY-MM-DD HH:mm')
const formatDuration = (s) => {
  const m = Math.floor(s / 60)
  const sec = s % 60
  return `${m}:${sec.toString().padStart(2, '0')}`
}

onMounted(() => { loadVideos(); loadCategories() })
</script>

<style scoped>
.page-actions { display: flex; justify-content: flex-end; margin-bottom: 20px; }
.action-btn { border-radius: 10px; padding: 10px 20px; font-weight: 500; }

.filter-bar {
  display: flex; gap: 12px; margin-bottom: 24px; align-items: center;
  padding: 16px 20px; background: white; border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}

.video-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px; min-height: 200px;
}

.video-card {
  background: white; border-radius: 14px; overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  transition: all 0.3s ease;
}
.video-card:hover { transform: translateY(-4px); box-shadow: 0 8px 24px rgba(0,0,0,0.1); }

.video-thumb {
  position: relative; aspect-ratio: 16/9; overflow: hidden; background: #1a1a2e;
}
.video-thumb img { width: 100%; height: 100%; object-fit: cover; }

.thumb-placeholder {
  width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;
  color: rgba(255,255,255,0.3); font-size: 3rem;
}

.duration-badge {
  position: absolute; bottom: 8px; right: 8px; background: rgba(0,0,0,0.75);
  color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem;
}

.card-actions {
  position: absolute; top: 8px; right: 8px; display: flex; gap: 4px;
  opacity: 0; transition: opacity 0.3s;
}
.video-card:hover .card-actions { opacity: 1; }

.video-info { padding: 16px; }
.video-info h4 { margin: 0 0 6px; font-size: 1rem; color: #333; }
.video-info .desc {
  font-size: 0.85rem; color: #888; margin: 0 0 10px; line-height: 1.4;
  display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
}
.meta { display: flex; justify-content: space-between; align-items: center; }
.date { font-size: 0.8rem; color: #bbb; }

.empty-state {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  height: 300px; color: #ccc; background: white; border-radius: 14px;
}
.empty-state .el-icon { font-size: 48px; margin-bottom: 12px; }

.pagination-bar { display: flex; justify-content: center; margin-top: 24px; }

.video-uploader { width: 100%; }
.upload-trigger, .file-selected {
  width: 100%; padding: 24px; border: 2px dashed #ddd; border-radius: 10px;
  display: flex; flex-direction: column; align-items: center; gap: 8px;
  color: #999; cursor: pointer; transition: all 0.3s;
}
.upload-trigger:hover { border-color: #d45d79; color: #d45d79; }
.file-selected { border-color: #67c23a; color: #67c23a; }
</style>
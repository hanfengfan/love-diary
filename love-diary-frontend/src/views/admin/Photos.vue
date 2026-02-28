<template>
  <div class="admin-photos">
    <div class="page-actions">
      <el-button type="primary" class="action-btn" @click="showUploadDialog = true">
        <el-icon><Upload /></el-icon>
        上传照片
      </el-button>
    </div>

    <!-- Filters -->
    <div class="filter-bar">
      <el-select v-model="filterForm.category" placeholder="所有分类" clearable @change="loadPhotos">
        <el-option v-for="cat in categories" :key="cat" :label="cat" :value="cat" />
      </el-select>
      <el-input v-model="filterForm.tags" placeholder="按标签搜索..." clearable style="width: 200px" @keyup.enter="loadPhotos" />
      <el-button @click="resetFilter">重置</el-button>
    </div>

    <!-- Photo Grid -->
    <div class="photos-grid" v-loading="loading">
      <div v-for="photo in photos" :key="photo.id" class="photo-card">
        <div class="photo-container">
          <img :src="`/uploads/${photo.filepath}`" :alt="photo.title" />
          <div class="card-actions">
            <el-button type="primary" size="small" circle @click="viewPhoto(photo)"><el-icon><View /></el-icon></el-button>
            <el-button type="warning" size="small" circle @click="editPhoto(photo)"><el-icon><Edit /></el-icon></el-button>
            <el-button type="danger" size="small" circle @click="deletePhoto(photo)"><el-icon><Delete /></el-icon></el-button>
          </div>
        </div>
        <div class="photo-info">
          <h4>{{ photo.title }}</h4>
          <p class="desc">{{ photo.description || '暂无描述' }}</p>
          <div class="meta">
            <el-tag size="small" type="info">{{ photo.category }}</el-tag>
            <span class="date">{{ formatDate(photo.created_at) }}</span>
          </div>
        </div>
      </div>
    </div>

    <div v-if="!loading && photos.length === 0" class="empty-state">
      <el-icon><Picture /></el-icon>
      <p>暂无照片</p>
    </div>

    <div class="pagination-bar" v-if="pagination.total > 0">
      <el-pagination v-model:current-page="pagination.page" v-model:page-size="pagination.per_page"
        :total="pagination.total" :page-sizes="[12, 24, 48]"
        layout="total, sizes, prev, pager, next" @size-change="loadPhotos" @current-change="loadPhotos" />
    </div>

    <!-- Upload Dialog -->
    <el-dialog v-model="showUploadDialog" title="上传照片" width="520px" destroy-on-close>
      <el-form :model="uploadForm" label-width="80px">
        <el-form-item label="照片文件" required>
          <el-upload class="photo-uploader" :show-file-list="false" :before-upload="beforeUpload" action="">
            <img v-if="uploadForm.imageUrl" :src="uploadForm.imageUrl" class="uploaded-preview" />
            <div v-else class="upload-trigger">
              <el-icon><Plus /></el-icon>
              <span>点击选择照片</span>
            </div>
          </el-upload>
        </el-form-item>
        <el-form-item label="标题" required>
          <el-input v-model="uploadForm.title" placeholder="请输入照片标题" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="uploadForm.description" type="textarea" :rows="3" placeholder="请输入照片描述" />
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
    <el-dialog v-model="showEditDialog" title="编辑照片" width="520px" destroy-on-close>
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

    <!-- Image Viewer -->
    <el-image-viewer v-if="showImageViewer" :url-list="imageUrls" :initial-index="currentImageIndex"
      @close="showImageViewer = false" />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { photoApi } from '@/api/photo'
import dayjs from 'dayjs'

const photos = ref([])
const categories = ref([])
const loading = ref(false)
const uploading = ref(false)
const saving = ref(false)
const showUploadDialog = ref(false)
const showEditDialog = ref(false)
const showImageViewer = ref(false)
const imageUrls = ref([])
const currentImageIndex = ref(0)

const filterForm = reactive({ category: '', tags: '' })
const pagination = reactive({ page: 1, per_page: 12, total: 0 })
const uploadForm = reactive({ imageUrl: '', file: null, title: '', description: '', category: '日常', tags: '' })
const editForm = reactive({ id: null, title: '', description: '', category: '', tags: '' })

onMounted(() => { loadPhotos(); loadCategories() })

const loadPhotos = async () => {
  loading.value = true
  try {
    const params = { page: pagination.page, per_page: pagination.per_page }
    if (filterForm.category) params.category = filterForm.category
    if (filterForm.tags) params.tags = filterForm.tags
    const data = await photoApi.getPhotos(params)
    photos.value = data.photos || []
    pagination.total = data.total || 0
  } catch { ElMessage.error('加载照片失败') }
  finally { loading.value = false }
}

const loadCategories = async () => {
  try { categories.value = (await photoApi.getCategories()).categories || [] } catch {}
}

const resetFilter = () => {
  Object.assign(filterForm, { category: '', tags: '' })
  pagination.page = 1
  loadPhotos()
}

const beforeUpload = (file) => {
  if (!file.type.startsWith('image/')) { ElMessage.error('只能上传图片文件!'); return false }
  if (file.size / 1024 / 1024 > 10) { ElMessage.error('图片不能超过 10MB!'); return false }
  uploadForm.file = file
  uploadForm.imageUrl = URL.createObjectURL(file)
  return false
}

const handleUpload = async () => {
  if (!uploadForm.file) { ElMessage.error('请选择照片文件'); return }
  if (!uploadForm.title.trim()) { ElMessage.error('请输入照片标题'); return }
  uploading.value = true
  try {
    const fd = new FormData()
    fd.append('photo', uploadForm.file)
    fd.append('title', uploadForm.title)
    fd.append('description', uploadForm.description)
    fd.append('category', uploadForm.category)
    fd.append('tags', uploadForm.tags)
    await photoApi.uploadPhoto(fd)
    ElMessage.success('上传成功')
    showUploadDialog.value = false
    Object.assign(uploadForm, { imageUrl: '', file: null, title: '', description: '', category: '日常', tags: '' })
    loadPhotos()
  } catch { ElMessage.error('上传失败') }
  finally { uploading.value = false }
}

const editPhoto = (p) => {
  Object.assign(editForm, { id: p.id, title: p.title, description: p.description || '', category: p.category, tags: p.tags ? p.tags.join(', ') : '' })
  showEditDialog.value = true
}

const handleSave = async () => {
  if (!editForm.title.trim()) { ElMessage.error('请输入标题'); return }
  saving.value = true
  try {
    const tags = editForm.tags ? editForm.tags.split(',').map(t => t.trim()).filter(Boolean) : []
    await photoApi.updatePhoto(editForm.id, { title: editForm.title, description: editForm.description, category: editForm.category, tags })
    ElMessage.success('保存成功')
    showEditDialog.value = false
    loadPhotos()
  } catch { ElMessage.error('保存失败') }
  finally { saving.value = false }
}

const deletePhoto = async (p) => {
  try {
    await ElMessageBox.confirm(`确定删除照片"${p.title}"吗？`, '确认', { type: 'warning' })
    await photoApi.deletePhoto(p.id)
    ElMessage.success('删除成功')
    loadPhotos()
  } catch (e) { if (e !== 'cancel') ElMessage.error('删除失败') }
}

const viewPhoto = (p) => {
  imageUrls.value = [`/uploads/${p.filepath}`]
  currentImageIndex.value = 0
  showImageViewer.value = true
}

const formatDate = (d) => dayjs(d).format('YYYY-MM-DD HH:mm')
</script>

<style scoped>
.page-actions { display: flex; justify-content: flex-end; margin-bottom: 20px; }
.action-btn { border-radius: 10px; padding: 10px 20px; font-weight: 500; }

.filter-bar {
  display: flex; gap: 12px; margin-bottom: 24px; align-items: center;
  padding: 16px 20px; background: white; border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}

.photos-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 20px; min-height: 200px;
}

.photo-card {
  background: white; border-radius: 14px; overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06); transition: all 0.3s ease;
}
.photo-card:hover { transform: translateY(-4px); box-shadow: 0 8px 24px rgba(0,0,0,0.1); }

.photo-container { position: relative; aspect-ratio: 1; overflow: hidden; }
.photo-container img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.4s ease; }
.photo-card:hover .photo-container img { transform: scale(1.05); }

.card-actions {
  position: absolute; top: 8px; right: 8px; display: flex; gap: 4px;
  opacity: 0; transition: opacity 0.3s ease;
}
.photo-card:hover .card-actions { opacity: 1; }

.photo-info { padding: 16px; }
.photo-info h4 { margin: 0 0 6px; font-size: 1rem; color: #333; }
.desc {
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

.photo-uploader { width: 100%; }
.upload-trigger {
  width: 100%; height: 200px; border: 2px dashed #ddd; border-radius: 10px;
  display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px;
  color: #999; cursor: pointer; transition: all 0.3s;
}
.upload-trigger:hover { border-color: #d45d79; color: #d45d79; }
.upload-trigger .el-icon { font-size: 28px; }

.uploaded-preview {
  width: 100%; height: 200px; object-fit: cover; border-radius: 10px;
}
</style>
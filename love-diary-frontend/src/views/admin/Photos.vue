<template>
  <div class="admin-photos">
    <div class="page-header">
      <div class="header-left">
        <h2>照片管理</h2>
      </div>
      <div class="header-right">
        <el-button type="primary" @click="showUploadDialog = true">
          <el-icon><Upload /></el-icon>
          上传照片
        </el-button>
      </div>
    </div>

    <!-- 筛选器 -->
    <el-card class="filter-card">
      <el-form :model="filterForm" inline>
        <el-form-item label="分类">
          <el-select v-model="filterForm.category" placeholder="选择分类" clearable>
            <el-option
              v-for="category in categories"
              :key="category"
              :label="category"
              :value="category"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="标签">
          <el-input
            v-model="filterForm.tags"
            placeholder="输入标签"
            clearable
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadPhotos">搜索</el-button>
          <el-button @click="resetFilter">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 照片列表 -->
    <el-card class="photos-card">
      <div class="photos-grid">
        <div
          v-for="photo in photos"
          :key="photo.id"
          class="photo-card"
        >
          <div class="photo-container">
            <img :src="`/uploads/${photo.filepath}`" :alt="photo.title" />
            <div class="photo-actions">
              <el-button
                type="primary"
                size="small"
                circle
                @click="viewPhoto(photo)"
              >
                <el-icon><View /></el-icon>
              </el-button>
              <el-button
                type="warning"
                size="small"
                circle
                @click="editPhoto(photo)"
              >
                <el-icon><Edit /></el-icon>
              </el-button>
              <el-button
                type="danger"
                size="small"
                circle
                @click="deletePhoto(photo)"
              >
                <el-icon><Delete /></el-icon>
              </el-button>
            </div>
          </div>
          <div class="photo-info">
            <h4>{{ photo.title }}</h4>
            <p class="photo-description">{{ photo.description || '暂无描述' }}</p>
            <div class="photo-meta">
              <el-tag size="small">{{ photo.category }}</el-tag>
              <span class="photo-date">{{ formatDate(photo.created_at) }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.per_page"
          :total="pagination.total"
          :page-sizes="[12, 24, 48]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="loadPhotos"
          @current-change="loadPhotos"
        />
      </div>

      <div v-if="loading" class="loading">
        <el-icon class="is-loading"><Loading /></el-icon>
        <span>加载中...</span>
      </div>

      <div v-if="!loading && photos.length === 0" class="empty-state">
        <el-icon><Picture /></el-icon>
        <p>暂无照片</p>
      </div>
    </el-card>

    <!-- 上传对话框 -->
    <el-dialog v-model="showUploadDialog" title="上传照片" width="500px">
      <el-form :model="uploadForm" label-width="80px">
        <el-form-item label="照片文件" required>
          <el-upload
            class="photo-uploader"
            :show-file-list="false"
            :before-upload="beforeUpload"
            :on-success="handleUploadSuccess"
            action=""
          >
            <img v-if="uploadForm.imageUrl" :src="uploadForm.imageUrl" class="uploaded-image" />
            <el-icon v-else class="photo-uploader-icon"><Plus /></el-icon>
          </el-upload>
        </el-form-item>
        <el-form-item label="标题" required>
          <el-input v-model="uploadForm.title" placeholder="请输入照片标题" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            v-model="uploadForm.description"
            type="textarea"
            placeholder="请输入照片描述"
            :rows="3"
          />
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
          <el-input
            v-model="uploadForm.tags"
            placeholder="请输入标签，用逗号分隔"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="showUploadDialog = false">取消</el-button>
        <el-button type="primary" :loading="uploading" @click="handleUpload">
          上传
        </el-button>
      </template>
    </el-dialog>

    <!-- 编辑对话框 -->
    <el-dialog v-model="showEditDialog" title="编辑照片" width="500px">
      <el-form :model="editForm" label-width="80px">
        <el-form-item label="标题" required>
          <el-input v-model="editForm.title" placeholder="请输入照片标题" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            v-model="editForm.description"
            type="textarea"
            placeholder="请输入照片描述"
            :rows="3"
          />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="editForm.category" placeholder="选择分类">
            <el-option label="日常" value="日常" />
            <el-option label="约会" value="约会" />
            <el-option label="节日" value="节日" />
            <el-option label="旅行" value="旅行" />
            <el-option label="其他" value="其他" />
          </el-select>
        </el-form-item>
        <el-form-item label="标签">
          <el-input
            v-model="editForm.tags"
            placeholder="请输入标签，用逗号分隔"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="handleSave">
          保存
        </el-button>
      </template>
    </el-dialog>

    <!-- 照片查看器 -->
    <el-image-viewer
      v-if="showImageViewer"
      :url-list="imageUrls"
      :initial-index="currentImageIndex"
      @close="showImageViewer = false"
    />
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

const filterForm = reactive({
  category: '',
  tags: ''
})

const pagination = reactive({
  page: 1,
  per_page: 12,
  total: 0
})

const uploadForm = reactive({
  imageUrl: '',
  file: null,
  title: '',
  description: '',
  category: '日常',
  tags: ''
})

const editForm = reactive({
  id: null,
  title: '',
  description: '',
  category: '',
  tags: ''
})

onMounted(() => {
  loadPhotos()
  loadCategories()
})

const loadPhotos = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      per_page: pagination.per_page,
      ...filterForm
    }

    if (filterForm.category) {
      params.category = filterForm.category
    }

    if (filterForm.tags) {
      params.tags = filterForm.tags
    }

    const data = await photoApi.getPhotos(params)
    photos.value = data.photos || []
    pagination.total = data.total || 0
  } catch (error) {
    ElMessage.error('加载照片失败')
    console.error('加载照片失败:', error)
  } finally {
    loading.value = false
  }
}

const loadCategories = async () => {
  try {
    const data = await photoApi.getCategories()
    categories.value = data.categories || []
  } catch (error) {
    console.error('加载分类失败:', error)
  }
}

const resetFilter = () => {
  Object.assign(filterForm, {
    category: '',
    tags: ''
  })
  pagination.page = 1
  loadPhotos()
}

const beforeUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt10M = file.size / 1024 / 1024 < 10

  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }

  if (!isLt10M) {
    ElMessage.error('图片大小不能超过 10MB!')
    return false
  }

  uploadForm.file = file
  uploadForm.imageUrl = URL.createObjectURL(file)
  return false // 阻止自动上传
}

const handleUploadSuccess = () => {
  ElMessage.success('上传成功')
  showUploadDialog.value = false
  resetUploadForm()
  loadPhotos()
}

const handleUpload = async () => {
  if (!uploadForm.file) {
    ElMessage.error('请选择照片文件')
    return
  }

  if (!uploadForm.title.trim()) {
    ElMessage.error('请输入照片标题')
    return
  }

  uploading.value = true
  try {
    const formData = new FormData()
    formData.append('photo', uploadForm.file)
    formData.append('title', uploadForm.title)
    formData.append('description', uploadForm.description)
    formData.append('category', uploadForm.category)
    formData.append('tags', uploadForm.tags)

    await photoApi.uploadPhoto(formData)
    ElMessage.success('照片上传成功')
    showUploadDialog.value = false
    resetUploadForm()
    loadPhotos()
  } catch (error) {
    ElMessage.error('照片上传失败')
    console.error('照片上传失败:', error)
  } finally {
    uploading.value = false
  }
}

const resetUploadForm = () => {
  Object.assign(uploadForm, {
    imageUrl: '',
    file: null,
    title: '',
    description: '',
    category: '日常',
    tags: ''
  })
}

const editPhoto = (photo) => {
  Object.assign(editForm, {
    id: photo.id,
    title: photo.title,
    description: photo.description || '',
    category: photo.category,
    tags: photo.tags ? photo.tags.join(', ') : ''
  })
  showEditDialog.value = true
}

const handleSave = async () => {
  if (!editForm.title.trim()) {
    ElMessage.error('请输入照片标题')
    return
  }

  saving.value = true
  try {
    const tags = editForm.tags
      ? editForm.tags.split(',').map(tag => tag.trim()).filter(tag => tag)
      : []

    await photoApi.updatePhoto(editForm.id, {
      title: editForm.title,
      description: editForm.description,
      category: editForm.category,
      tags: tags
    })

    ElMessage.success('照片信息更新成功')
    showEditDialog.value = false
    loadPhotos()
  } catch (error) {
    ElMessage.error('照片信息更新失败')
    console.error('照片信息更新失败:', error)
  } finally {
    saving.value = false
  }
}

const deletePhoto = async (photo) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除照片"${photo.title}"吗？`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )

    await photoApi.deletePhoto(photo.id)
    ElMessage.success('照片删除成功')
    loadPhotos()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('照片删除失败')
      console.error('照片删除失败:', error)
    }
  }
}

const viewPhoto = (photo) => {
  imageUrls.value = [`/uploads/${photo.filepath}`]
  currentImageIndex.value = 0
  showImageViewer.value = true
}

const formatDate = (date) => {
  return dayjs(date).format('YYYY-MM-DD HH:mm')
}
</script>

<style scoped>
.admin-photos {
  padding: 0;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-left h2 {
  margin: 0;
  color: #333;
}

.filter-card {
  margin-bottom: 20px;
}

.photos-card {
  min-height: 600px;
}

.photos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.photo-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.photo-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.photo-container {
  position: relative;
  aspect-ratio: 1;
  overflow: hidden;
}

.photo-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.photo-actions {
  position: absolute;
  top: 8px;
  right: 8px;
  display: flex;
  gap: 4px;
  opacity: 0;
  transition: opacity 0.3s;
}

.photo-container:hover .photo-actions {
  opacity: 1;
}

.photo-info {
  padding: 16px;
}

.photo-info h4 {
  margin: 0 0 8px 0;
  font-size: 16px;
  color: #333;
}

.photo-description {
  margin: 0 0 12px 0;
  font-size: 14px;
  color: #666;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.photo-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.photo-date {
  font-size: 12px;
  color: #999;
}

.pagination {
  display: flex;
  justify-content: center;
  padding: 20px 0;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: #999;
}

.loading .el-icon {
  font-size: 24px;
  margin-bottom: 8px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: #999;
}

.empty-state .el-icon {
  font-size: 48px;
  margin-bottom: 8px;
}

.photo-uploader {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  width: 100%;
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.photo-uploader:hover {
  border-color: #409eff;
}

.photo-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}

.uploaded-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>
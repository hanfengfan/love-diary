<template>
  <div class="photos-page">
    <div class="page-header">
      <h1>Our Gallery</h1>
      <p>Snapshots of our love</p>
    </div>

    <!-- Filter Section -->
    <div class="filter-section">
      <div class="search-box">
        <el-icon><Search /></el-icon>
        <input 
          v-model="filterForm.tags" 
          placeholder="Search by tags..." 
          @keyup.enter="loadPhotos"
        />
      </div>
      
      <div class="category-filters">
        <button 
          class="filter-btn" 
          :class="{ active: !filterForm.category }"
          @click="setCategory('')"
        >
          All
        </button>
        <button 
          v-for="cat in categories" 
          :key="cat"
          class="filter-btn"
          :class="{ active: filterForm.category === cat }"
          @click="setCategory(cat)"
        >
          {{ cat }}
        </button>
      </div>
    </div>

    <!-- Photos Grid -->
    <div class="photos-container" v-loading="loading">
      <div class="masonry-grid" v-if="photos.length > 0">
        <div 
          v-for="photo in photos" 
          :key="photo.id" 
          class="photo-item"
          @click="viewPhoto(photo)"
        >
          <img :src="`/uploads/${photo.filepath}`" :alt="photo.title" loading="lazy" />
          <div class="photo-overlay">
            <div class="photo-content">
              <h3>{{ photo.title }}</h3>
              <div class="photo-meta">
                <span class="date">{{ formatDate(photo.created_at) }}</span>
                <span class="category" v-if="photo.category">{{ photo.category }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else-if="!loading" class="empty-state">
        <el-icon><Picture /></el-icon>
        <p>No photos found. Try adjusting your filters.</p>
      </div>

      <!-- Pagination -->
      <div class="pagination-container" v-if="photos.length > 0">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.per_page"
          :total="pagination.total"
          :page-sizes="[12, 24, 48]"
          layout="prev, pager, next"
          @current-change="loadPhotos"
        />
      </div>
    </div>

    <!-- Image Viewer -->
    <el-image-viewer
      v-if="showImageViewer"
      :url-list="imageUrls"
      :initial-index="currentImageIndex"
      @close="showImageViewer = false"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch, onUnmounted } from 'vue'
import { photoApi } from '@/api/photo'
import dayjs from 'dayjs'
import { Search, Picture } from '@element-plus/icons-vue'

const photos = ref([])
const categories = ref([])
const loading = ref(false)
const showImageViewer = ref(false)
const imageUrls = ref([])
const currentImageIndex = ref(0)

const filterForm = reactive({
  category: '',
  tags: ''
})

const pagination = reactive({
  page: 1,
  per_page: 24,
  total: 0
})

const loadPhotos = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      per_page: pagination.per_page,
      ...filterForm
    }
    const data = await photoApi.getPhotos(params)
    photos.value = data.photos || []
    pagination.total = data.total || 0
    
    imageUrls.value = photos.value.map(photo => `/uploads/${photo.filepath}`)
  } catch (error) {
    console.error('Failed to load photos:', error)
  } finally {
    loading.value = false
  }
}

const loadCategories = async () => {
  try {
    const data = await photoApi.getCategories()
    categories.value = data.categories || []
  } catch (error) {
    console.error('Failed to load categories:', error)
  }
}

const setCategory = (cat) => {
  filterForm.category = cat
  pagination.page = 1
  loadPhotos()
}

const viewPhoto = (photo) => {
  const index = photos.value.findIndex(p => p.id === photo.id)
  currentImageIndex.value = index
  showImageViewer.value = true
}

const formatDate = (date) => dayjs(date).format('MMM D, YYYY')

let debounceTimer = null
watch(() => filterForm.tags, () => {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    pagination.page = 1
    loadPhotos()
  }, 300)
})

onUnmounted(() => {
  clearTimeout(debounceTimer)
})

onMounted(() => {
  loadPhotos()
  loadCategories()
})
</script>

<style lang="scss" scoped>
@import '@/assets/styles/variables.scss';

.photos-page {
  max-width: 1400px;
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
  
  p {
    color: var(--text-secondary);
  }
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
    position: absolute;
    left: 1rem;
    top: 50%;
    transform: translateY(-50%);
    color: var(--text-secondary);
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
  display: flex;
  flex-wrap: wrap;
  gap: 0.8rem;
  justify-content: center;
  
  .filter-btn {
    padding: 0.5rem 1.2rem;
    border-radius: 20px;
    background: white;
    color: var(--text-secondary);
    font-size: 0.9rem;
    transition: all 0.3s ease;
    border: 1px solid transparent;
    
    &:hover {
      color: var(--primary-color);
      background: var(--bg-color);
    }
    
    &.active {
      background: var(--primary-color);
      color: white;
      box-shadow: var(--shadow-sm);
    }
  }
}

.masonry-grid {
  column-count: 4;
  column-gap: 1.5rem;
  
  @media (max-width: 1200px) {
    column-count: 3;
  }
  
  @media (max-width: 900px) {
    column-count: 2;
  }
  
  @media (max-width: 600px) {
    column-count: 1;
  }
}

.photo-item {
  break-inside: avoid;
  margin-bottom: 1.5rem;
  border-radius: var(--radius-md);
  overflow: hidden;
  position: relative;
  cursor: pointer;
  transform: translateZ(0); // Fix for webkit rendering
  
  img {
    width: 100%;
    display: block;
    transition: transform 0.5s ease;
  }
  
  .photo-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(to top, rgba(0,0,0,0.7), transparent);
    opacity: 0;
    transition: opacity 0.3s ease;
    display: flex;
    align-items: flex-end;
    padding: 1.5rem;
  }
  
  &:hover {
    img {
      transform: scale(1.05);
    }
    
    .photo-overlay {
      opacity: 1;
    }
  }
}

.photo-content {
  color: white;
  width: 100%;
  transform: translateY(10px);
  transition: transform 0.3s ease;
  
  .photo-item:hover & {
    transform: translateY(0);
  }
  
  h3 {
    font-size: 1.1rem;
    margin-bottom: 0.5rem;
    font-weight: 600;
  }
}

.photo-meta {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
  opacity: 0.9;
}

.empty-state {
  text-align: center;
  padding: 4rem;
  color: var(--text-secondary);
  
  .el-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    color: var(--primary-color);
  }
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 3rem;
}

:deep(.el-pagination) {
  --el-pagination-hover-color: var(--primary-color);
  --el-pagination-button-bg-color: transparent;
}
</style>
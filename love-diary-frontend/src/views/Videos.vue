<template>
  <div class="videos-page">
    <div class="page-header">
      <h1>Our Videos</h1>
      <p>Moments captured in motion</p>
    </div>

    <!-- Filter Section -->
    <div class="filter-section">
      <div class="search-box">
        <el-icon><Search /></el-icon>
        <input v-model="filterForm.tags" placeholder="Search by tags..." @keyup.enter="loadVideos" />
      </div>

      <div class="category-filters">
        <button class="filter-btn" :class="{ active: !filterForm.category }" @click="setCategory('')">All</button>
        <button v-for="cat in categories" :key="cat" class="filter-btn"
          :class="{ active: filterForm.category === cat }" @click="setCategory(cat)">
          {{ cat }}
        </button>
      </div>
    </div>

    <!-- Videos Grid -->
    <div class="videos-container" v-loading="loading">
      <div class="videos-grid" v-if="videos.length > 0">
        <div v-for="video in videos" :key="video.id" class="video-card" @click="playVideo(video)">
          <div class="video-thumb">
            <img v-if="video.thumbnail" :src="`/uploads/${video.thumbnail}`" :alt="video.title" loading="lazy" />
            <div v-else class="thumb-placeholder">
              <el-icon><VideoPlay /></el-icon>
            </div>
            <div class="play-overlay">
              <div class="play-btn">
                <el-icon><VideoPlay /></el-icon>
              </div>
            </div>
            <span v-if="video.duration" class="duration">{{ formatDuration(video.duration) }}</span>
          </div>
          <div class="video-info">
            <h3>{{ video.title }}</h3>
            <p class="description" v-if="video.description">{{ video.description }}</p>
            <div class="video-meta">
              <span class="date">{{ formatDate(video.created_at) }}</span>
              <span class="category" v-if="video.category">{{ video.category }}</span>
            </div>
          </div>
        </div>
      </div>

      <div v-else-if="!loading" class="empty-state">
        <el-icon><VideoPlay /></el-icon>
        <p>No videos found. Try adjusting your filters.</p>
      </div>

      <!-- Pagination -->
      <div class="pagination-container" v-if="videos.length > 0">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.per_page"
          :total="pagination.total"
          :page-sizes="[12, 24]"
          layout="prev, pager, next"
          @current-change="loadVideos"
        />
      </div>
    </div>

    <!-- Video Player Dialog -->
    <el-dialog v-model="showPlayer" :title="currentVideo?.title" width="800px" destroy-on-close class="video-dialog">
      <div class="video-player" v-if="currentVideo">
        <video controls autoplay :src="`/uploads/${currentVideo.filepath}`" style="width: 100%; border-radius: 12px;"></video>
        <div class="player-info">
          <p class="player-desc" v-if="currentVideo.description">{{ currentVideo.description }}</p>
          <div class="player-tags" v-if="currentVideo.tags?.length">
            <span v-for="tag in currentVideo.tags" :key="tag" class="tag">{{ tag }}</span>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { videoApi } from '@/api/video'
import dayjs from 'dayjs'
import { Search, VideoPlay } from '@element-plus/icons-vue'

const videos = ref([])
const categories = ref([])
const loading = ref(false)
const showPlayer = ref(false)
const currentVideo = ref(null)

const filterForm = reactive({ category: '', tags: '' })
const pagination = reactive({ page: 1, per_page: 12, total: 0 })

const loadVideos = async () => {
  loading.value = true
  try {
    const params = { page: pagination.page, per_page: pagination.per_page }
    if (filterForm.category) params.category = filterForm.category
    if (filterForm.tags) params.tags = filterForm.tags
    const data = await videoApi.getVideos(params)
    videos.value = data.videos || []
    pagination.total = data.total || 0
  } catch (e) {
    console.error('Failed to load videos:', e)
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

const setCategory = (cat) => {
  filterForm.category = cat
  pagination.page = 1
  loadVideos()
}

const playVideo = (video) => {
  currentVideo.value = video
  showPlayer.value = true
}

const formatDate = (d) => dayjs(d).format('MMM D, YYYY')
const formatDuration = (s) => {
  const m = Math.floor(s / 60)
  const sec = s % 60
  return `${m}:${sec.toString().padStart(2, '0')}`
}

onMounted(() => { loadVideos(); loadCategories() })
</script>

<style lang="scss" scoped>
@import '@/assets/styles/variables.scss';

.videos-page {
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

.videos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.5rem;

  @media (max-width: 600px) {
    grid-template-columns: 1fr;
  }
}

.video-card {
  border-radius: var(--radius-md);
  overflow: hidden;
  background: white;
  box-shadow: var(--shadow-sm);
  cursor: pointer;
  transition: all 0.4s ease;

  &:hover {
    transform: translateY(-6px);
    box-shadow: var(--shadow-md);

    .play-overlay {
      opacity: 1;
    }

    .video-thumb img {
      transform: scale(1.05);
    }
  }
}

.video-thumb {
  position: relative;
  aspect-ratio: 16/9;
  overflow: hidden;
  background: #1a1225;

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.5s ease;
  }
}

.thumb-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: rgba(255,255,255,0.2);
  font-size: 3rem;
}

.play-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.play-btn {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: rgba(255,255,255,0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary-color);
  font-size: 1.5rem;
  transition: transform 0.3s ease;
  box-shadow: 0 4px 20px rgba(0,0,0,0.2);

  &:hover {
    transform: scale(1.1);
  }
}

.duration {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: rgba(0,0,0,0.75);
  color: white;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
}

.video-info {
  padding: 1.2rem;

  h3 {
    font-size: 1.05rem;
    color: var(--text-primary);
    margin: 0 0 0.5rem;
    font-weight: 600;
  }
}

.description {
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin: 0 0 0.8rem;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.video-meta {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;

  .date { color: #999; }
  .category {
    color: var(--primary-color);
    font-weight: 500;
  }
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

/* Video Player Dialog */
.player-info {
  padding: 1rem 0;
}

.player-desc {
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0 0 0.8rem;
}

.player-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.tag {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  background: var(--bg-color);
  color: var(--primary-color);
  font-size: 0.85rem;
}
</style>
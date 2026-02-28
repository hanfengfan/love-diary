<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-content">
        <h1 class="title">Our Love Story</h1>
        <p class="subtitle">Recording every beautiful moment with you</p>
        <div class="days-counter">
          <div class="counter-item">
            <span class="number">{{ daysTogether }}</span>
            <span class="label">Days Together</span>
          </div>
        </div>
        <div class="scroll-indicator">
          <span>Scroll to explore</span>
          <el-icon class="bounce"><ArrowDown /></el-icon>
        </div>
      </div>
      <div class="hero-background"></div>
    </section>

    <div class="container">
      <!-- Stats Overview -->
      <section class="stats-section">
        <div class="stat-card" v-for="(value, key) in displayStats" :key="key">
          <div class="stat-icon">
            <el-icon v-if="key === 'photos'"><Picture /></el-icon>
            <el-icon v-else-if="key === 'videos'"><VideoPlay /></el-icon>
            <el-icon v-else><Document /></el-icon>
          </div>
          <div class="stat-info">
            <span class="stat-value">{{ value }}</span>
            <span class="stat-label">{{ key.charAt(0).toUpperCase() + key.slice(1) }}</span>
          </div>
        </div>
      </section>

      <!-- Recent Memories -->
      <section class="recent-section">
        <div class="section-header">
          <h2>Recent Memories</h2>
          <router-link to="/timeline" class="view-all">View Timeline <el-icon><ArrowRight /></el-icon></router-link>
        </div>
        
        <div class="memories-grid">
          <!-- Latest Photos -->
          <div class="memory-group">
            <h3>Latest Photos</h3>
            <div class="photo-grid">
              <div v-for="photo in latestPhotos" :key="photo.id" class="photo-card" @click="viewPhoto(photo)">
                <img :src="`/uploads/${photo.filepath}`" :alt="photo.title" loading="lazy" />
                <div class="overlay">
                  <span>{{ photo.title }}</span>
                </div>
              </div>
              <div v-if="latestPhotos.length === 0" class="empty-placeholder">No photos yet</div>
            </div>
          </div>

          <!-- Latest Diaries -->
          <div class="memory-group">
            <h3>Latest Diaries</h3>
            <div class="diary-list">
              <div v-for="diary in latestDiaries" :key="diary.id" class="diary-card" @click="viewDiary(diary)">
                <div class="diary-date">
                  <span class="day">{{ formatDateDay(diary.created_at) }}</span>
                  <span class="month">{{ formatDateMonth(diary.created_at) }}</span>
                </div>
                <div class="diary-content">
                  <h4>{{ diary.title }}</h4>
                  <p>{{ truncateText(diary.content, 60) }}</p>
                </div>
              </div>
              <div v-if="latestDiaries.length === 0" class="empty-placeholder">No diaries yet</div>
            </div>
          </div>
        </div>
      </section>
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
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { photoApi } from '@/api/photo'
import { videoApi } from '@/api/video'
import { diaryApi } from '@/api/diary'
import dayjs from 'dayjs'
import { Picture, VideoPlay, Document, ArrowDown, ArrowRight } from '@element-plus/icons-vue'

const router = useRouter()

// State
const stats = ref({ totalPhotos: 0, totalVideos: 0, totalDiaries: 0 })
const latestPhotos = ref([])
const latestVideos = ref([])
const latestDiaries = ref([])
const showImageViewer = ref(false)
const imageUrls = ref([])
const currentImageIndex = ref(0)

// 恋爱开始日期 — 可通过 localStorage 配置, 默认 2023-01-01
const startDate = dayjs(localStorage.getItem('love_start_date') || '2023-01-01')
const daysTogether = computed(() => {
  return dayjs().diff(startDate, 'day')
})

const displayStats = computed(() => ({
  photos: stats.value.totalPhotos,
  videos: stats.value.totalVideos,
  diaries: stats.value.totalDiaries
}))

// Methods
const loadData = async () => {
  try {
    const [photosData, videosData, diariesData] = await Promise.all([
      photoApi.getPhotos({ per_page: 4 }),
      videoApi.getVideos({ per_page: 0 }), // Just for stats
      diaryApi.getDiaries({ per_page: 3 })
    ])

    latestPhotos.value = photosData.photos || []
    stats.value.totalPhotos = photosData.total || 0

    stats.value.totalVideos = videosData.total || 0
    
    latestDiaries.value = diariesData.diaries || []
    stats.value.totalDiaries = diariesData.total || 0
  } catch (error) {
    console.error('Failed to load data:', error)
  }
}

const viewPhoto = (photo) => {
  imageUrls.value = [`/uploads/${photo.filepath}`]
  currentImageIndex.value = 0
  showImageViewer.value = true
}

const viewDiary = (diary) => {
  router.push(`/diaries?id=${diary.id}`)
}

const formatDateDay = (date) => dayjs(date).format('DD')
const formatDateMonth = (date) => dayjs(date).format('MMM')
const truncateText = (text, length) => {
  if (!text) return ''
  return text.length > length ? text.substring(0, length) + '...' : text
}

onMounted(() => {
  loadData()
})
</script>

<style lang="scss" scoped>
@import '@/assets/styles/variables.scss';

.home-page {
  padding-bottom: 4rem;
}

.hero-section {
  height: 90vh;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  color: white;
  overflow: hidden;
  margin-top: -80px; // Counteract main layout padding for full screen effect

  .hero-background {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 99%, #fecfef 100%);
    z-index: -1;
    
    &::after {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.2); /* Increased opacity for better contrast */
    }
  }

  .hero-content {
    z-index: 1;
    animation: fadeIn 1s ease-out;
  }

  .title {
    font-size: 4rem;
    font-weight: 700;
    margin-bottom: 1rem;
    text-shadow: 0 2px 15px rgba(0,0,0,0.2); /* Stronger shadow */
    font-family: 'Georgia', serif;
    color: white;
  }

  .subtitle {
    font-size: 1.5rem;
    opacity: 1; /* Full opacity */
    margin-bottom: 3rem;
    color: white;
    text-shadow: 0 1px 4px rgba(0,0,0,0.3);
  }

  .days-counter {
    display: inline-block;
    background: rgba(255, 255, 255, 0.25);
    backdrop-filter: blur(10px);
    padding: 2rem 4rem;
    border-radius: var(--radius-lg);
    border: 1px solid rgba(255, 255, 255, 0.4);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    
    .number {
      display: block;
      font-size: 5rem;
      font-weight: 800;
      line-height: 1;
      color: white;
      text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    .label {
      font-size: 1.2rem;
      text-transform: uppercase;
      letter-spacing: 2px;
      color: rgba(255, 255, 255, 0.95);
      font-weight: 600;
    }
  }

  .scroll-indicator {
    position: absolute;
    bottom: 2rem;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    opacity: 0.9;
    font-size: 0.9rem;
    color: white;
    text-shadow: 0 1px 2px rgba(0,0,0,0.2);

    .bounce {
      animation: bounce 2s infinite;
    }
  }
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.stats-section {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  margin-top: -3rem;
  position: relative;
  z-index: 10;
  margin-bottom: 4rem;

  .stat-card {
    @include glass;
    background: white;
    padding: 2rem;
    border-radius: var(--radius-md);
    display: flex;
    align-items: center;
    gap: 1.5rem;
    transition: transform 0.3s ease;

    &:hover {
      transform: translateY(-5px);
    }

    .stat-icon {
      width: 60px;
      height: 60px;
      border-radius: 50%;
      background: var(--secondary-color);
      color: var(--primary-color);
      @include flex-center;
      font-size: 1.8rem;
    }

    .stat-info {
      display: flex;
      flex-direction: column;
      
      .stat-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
      }
      
      .stat-label {
        color: var(--text-secondary);
        font-size: 0.9rem;
      }
    }
  }
}

.recent-section {
  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-bottom: 2rem;

    h2 {
      font-size: 2rem;
      color: var(--text-primary);
    }

    .view-all {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      color: var(--primary-color);
      font-weight: 500;
      
      &:hover {
        text-decoration: underline;
      }
    }
  }
}

.memories-grid {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 3rem;
}

.memory-group {
  h3 {
    font-size: 1.2rem;
    color: var(--text-secondary);
    margin-bottom: 1.5rem;
    font-weight: 500;
  }
}

.photo-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;

  .photo-card {
    aspect-ratio: 1;
    border-radius: var(--radius-md);
    overflow: hidden;
    position: relative;
    cursor: pointer;
    box-shadow: var(--shadow-sm);

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.5s ease;
    }

    .overlay {
      position: absolute;
      inset: 0;
      background: rgba(0, 0, 0, 0.3);
      display: flex;
      align-items: flex-end;
      padding: 1.5rem;
      opacity: 0;
      transition: opacity 0.3s ease;
      
      span {
        color: white;
        font-weight: 500;
        transform: translateY(10px);
        transition: transform 0.3s ease;
      }
    }

    &:hover {
      img {
        transform: scale(1.1);
      }
      
      .overlay {
        opacity: 1;
        
        span {
          transform: translateY(0);
        }
      }
    }
  }
}

.diary-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;

  .diary-card {
    background: white;
    padding: 1.5rem;
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-sm);
    display: flex;
    gap: 1.5rem;
    cursor: pointer;
    transition: all 0.3s ease;
    border: 1px solid transparent;

    &:hover {
      border-color: var(--secondary-color);
      transform: translateX(5px);
    }

    .diary-date {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 0.5rem 1rem;
      background: var(--bg-color);
      border-radius: var(--radius-sm);
      color: var(--primary-color);
      min-width: 70px;

      .day {
        font-size: 1.5rem;
        font-weight: 700;
        line-height: 1;
      }
      
      .month {
        font-size: 0.8rem;
        text-transform: uppercase;
      }
    }

    .diary-content {
      flex: 1;
      
      h4 {
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
        color: var(--text-primary);
      }
      
      p {
        font-size: 0.9rem;
        color: var(--text-secondary);
        line-height: 1.5;
      }
    }
  }
}

.empty-placeholder {
  padding: 2rem;
  text-align: center;
  color: var(--text-secondary);
  background: rgba(255, 255, 255, 0.5);
  border-radius: var(--radius-md);
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-10px); }
  60% { transform: translateY(-5px); }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 768px) {
  .stats-section {
    grid-template-columns: 1fr;
    margin-top: 2rem;
  }

  .memories-grid {
    grid-template-columns: 1fr;
  }
  
  .hero-section .title {
    font-size: 2.5rem;
  }
}
</style>
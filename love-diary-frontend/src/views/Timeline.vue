<template>
  <div class="timeline-page">
    <div class="page-header">
      <h1>Our Journey</h1>
      <p>Every step we took together</p>
    </div>

    <div class="timeline-container" v-if="timelineItems.length > 0">
      <div class="timeline-line"></div>
      
      <div 
        v-for="(item, index) in timelineItems" 
        :key="`${item.type}-${item.id}`"
        class="timeline-item"
        :class="{ 'left': index % 2 === 0, 'right': index % 2 !== 0 }"
      >
        <div class="timeline-dot"></div>
        <div class="timeline-date">{{ formatDateTime(item.created_at) }}</div>
        
        <div class="timeline-content" @click="viewItem(item)">
          <div class="content-type">
            <el-icon v-if="item.type === 'photo'"><Picture /></el-icon>
            <el-icon v-else-if="item.type === 'video'"><VideoPlay /></el-icon>
            <el-icon v-else><Document /></el-icon>
            <span>{{ item.type.charAt(0).toUpperCase() + item.type.slice(1) }}</span>
          </div>
          
          <h3>{{ item.title }}</h3>
          
          <div class="media-preview" v-if="item.type === 'photo'">
            <img :src="`/uploads/${item.filepath}`" :alt="item.title" loading="lazy" />
          </div>
          <div class="media-preview video" v-else-if="item.type === 'video'">
            <img v-if="item.thumbnail" :src="`/uploads/${item.thumbnail}`" :alt="item.title" />
            <div v-else class="video-placeholder">
              <el-icon><VideoPlay /></el-icon>
            </div>
          </div>
          <div class="text-preview" v-else>
            <p>{{ truncateText(item.content, 100) }}</p>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="empty-state">
      <el-icon><Clock /></el-icon>
      <p>No memories recorded yet. Start your journey!</p>
    </div>

    <div class="loading-trigger" v-if="hasMore" ref="loadingTrigger">
      <el-icon class="is-loading"><Loading /></el-icon>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { timelineApi } from '@/api/search'
import dayjs from 'dayjs'
import { Picture, VideoPlay, Document, Clock, Loading } from '@element-plus/icons-vue'

const router = useRouter()
const timelineItems = ref([])
const page = ref(1)
const hasMore = ref(true)
const loading = ref(false)

const loadData = async () => {
  if (loading.value || !hasMore.value) return
  
  loading.value = true
  try {
    const data = await timelineApi.getTimeline({ 
      page: page.value, 
      per_page: 10 
    })
    
    if (data.timeline && data.timeline.length > 0) {
      timelineItems.value.push(...data.timeline)
      page.value++
    } else {
      hasMore.value = false
    }
  } catch (error) {
    console.error('Failed to load timeline:', error)
  } finally {
    loading.value = false
  }
}

const viewItem = (item) => {
  if (item.type === 'photo') {
    // Ideally open a lightbox, but for now redirect or just show
    // We can emit an event or use a store to open global lightbox
    // For simplicity, let's assume we want to go to the detail page if it existed,
    // or just do nothing for now as photos are usually viewed in gallery.
    // Let's just log for now or maybe implement a simple view later.
    console.log('View photo', item)
  } else if (item.type === 'video') {
    router.push(`/videos?id=${item.id}`)
  } else if (item.type === 'diary') {
    router.push(`/diaries?id=${item.id}`)
  }
}

const formatDateTime = (date) => {
  return dayjs(date).format('MMM D, YYYY HH:mm')
}

const truncateText = (text, length) => {
  if (!text) return ''
  return text.length > length ? text.substring(0, length) + '...' : text
}

onMounted(() => {
  loadData()
  // Infinite scroll could be implemented here with IntersectionObserver on loadingTrigger
})
</script>

<style lang="scss" scoped>
@import '@/assets/styles/variables.scss';

.timeline-page {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem;
  min-height: 80vh;
}

.page-header {
  text-align: center;
  margin-bottom: 4rem;
  
  h1 {
    font-size: 2.5rem;
    color: var(--primary-color);
    margin-bottom: 0.5rem;
    font-family: 'Georgia', serif;
  }
  
  p {
    color: var(--text-secondary);
    font-size: 1.1rem;
  }
}

.timeline-container {
  position: relative;
  padding: 2rem 0;
}

.timeline-line {
  position: absolute;
  left: 50%;
  top: 0;
  bottom: 0;
  width: 2px;
  background: linear-gradient(to bottom, transparent, var(--primary-color), transparent);
  transform: translateX(-50%);
}

.timeline-item {
  position: relative;
  margin-bottom: 4rem;
  width: 50%;
  padding: 0 3rem;
  box-sizing: border-box;
  
  &.left {
    left: 0;
    text-align: right;
    
    .timeline-date {
      right: -140px;
      text-align: left;
    }
    
    .timeline-content {
      margin-left: auto;
    }
  }
  
  &.right {
    left: 50%;
    text-align: left;
    
    .timeline-date {
      left: -140px;
      text-align: right;
    }
    
    .timeline-dot {
      left: -6px;
    }
  }
}

.timeline-dot {
  position: absolute;
  top: 20px;
  width: 12px;
  height: 12px;
  background: var(--primary-color);
  border-radius: 50%;
  box-shadow: 0 0 0 4px rgba(232, 166, 177, 0.3);
  z-index: 2;
  
  .left & {
    right: -6px;
  }
}

.timeline-date {
  position: absolute;
  top: 18px;
  width: 120px;
  color: var(--text-secondary);
  font-size: 0.9rem;
  font-weight: 500;
}

.timeline-content {
  @include glass;
  background: white;
  padding: 1.5rem;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: var(--shadow-md);
  }
}

.content-type {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.8rem;
  font-size: 0.8rem;
  color: var(--primary-color);
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  
  .left & {
    justify-content: flex-end;
  }
}

h3 {
  margin-bottom: 1rem;
  font-size: 1.2rem;
  color: var(--text-primary);
}

.media-preview {
  width: 100%;
  border-radius: var(--radius-sm);
  overflow: hidden;
  margin-top: 1rem;
  
  img {
    width: 100%;
    height: auto;
    display: block;
    transition: transform 0.5s ease;
  }
  
  &:hover img {
    transform: scale(1.05);
  }
}

.video-placeholder {
  background: #f0f0f0;
  height: 150px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  font-size: 2rem;
}

.text-preview {
  color: var(--text-secondary);
  font-size: 0.95rem;
  line-height: 1.6;
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

.loading-trigger {
  text-align: center;
  padding: 2rem;
  color: var(--primary-color);
}

@media (max-width: 768px) {
  .timeline-line {
    left: 20px;
  }
  
  .timeline-item {
    width: 100%;
    padding-left: 50px;
    padding-right: 0;
    margin-bottom: 3rem;
    
    &.left, &.right {
      left: 0;
      text-align: left;
      
      .timeline-date {
        position: relative;
        top: 0;
        left: 0;
        right: auto;
        margin-bottom: 0.5rem;
        text-align: left;
      }
      
      .timeline-content {
        margin-left: 0;
      }
      
      .content-type {
        justify-content: flex-start;
      }
    }
    
    .timeline-dot {
      left: 14px;
      right: auto;
    }
  }
}
</style>
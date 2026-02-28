<template>
  <div class="search-page">
    <div class="page-header">
      <h1>Search</h1>
      <p>Find your cherished memories</p>
    </div>

    <!-- Search Input -->
    <div class="search-section">
      <div class="search-input-wrapper">
        <el-icon class="search-icon"><Search /></el-icon>
        <input
          v-model="keyword"
          placeholder="Search photos, videos, diaries..."
          @keyup.enter="doSearch"
          ref="searchInput"
          autofocus
        />
        <button class="search-submit" @click="doSearch" :disabled="!keyword.trim()">
          Search
        </button>
      </div>
    </div>

    <!-- Results -->
    <div class="results-container" v-loading="loading">
      <template v-if="hasSearched">
        <!-- Results Summary -->
        <div class="results-summary" v-if="totalResults > 0">
          <span>Found <strong>{{ totalResults }}</strong> results for "<em>{{ lastKeyword }}</em>"</span>
        </div>

        <!-- Photos Results -->
        <div class="result-section" v-if="results.photos?.length">
          <h2>
            <el-icon><Picture /></el-icon>
            Photos <span class="count">({{ results.photos.length }})</span>
          </h2>
          <div class="photos-grid">
            <div v-for="photo in results.photos" :key="'photo-' + photo.id" class="photo-item" @click="viewPhoto(photo)">
              <img :src="`/uploads/${photo.filepath}`" :alt="photo.title" loading="lazy" />
              <div class="photo-overlay">
                <h4>{{ photo.title }}</h4>
                <span>{{ formatDate(photo.created_at) }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Videos Results -->
        <div class="result-section" v-if="results.videos?.length">
          <h2>
            <el-icon><VideoPlay /></el-icon>
            Videos <span class="count">({{ results.videos.length }})</span>
          </h2>
          <div class="videos-grid">
            <div v-for="video in results.videos" :key="'video-' + video.id" class="video-item">
              <div class="video-thumb">
                <img v-if="video.thumbnail" :src="`/uploads/${video.thumbnail}`" :alt="video.title" />
                <div v-else class="thumb-placeholder"><el-icon><VideoPlay /></el-icon></div>
                <span v-if="video.duration" class="duration">{{ formatDuration(video.duration) }}</span>
              </div>
              <div class="video-info">
                <h4>{{ video.title }}</h4>
                <span class="date">{{ formatDate(video.created_at) }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Diaries Results -->
        <div class="result-section" v-if="results.diaries?.length">
          <h2>
            <el-icon><Document /></el-icon>
            Diaries <span class="count">({{ results.diaries.length }})</span>
          </h2>
          <div class="diaries-list">
            <div v-for="diary in results.diaries" :key="'diary-' + diary.id" class="diary-item"
              @click="openDiary(diary)">
              <div class="diary-head">
                <span class="mood" v-if="diary.mood">{{ diary.mood }}</span>
                <h4>{{ diary.title }}</h4>
              </div>
              <p class="excerpt">{{ diary.content }}</p>
              <span class="date">{{ formatDate(diary.created_at) }}</span>
            </div>
          </div>
        </div>

        <!-- No Results -->
        <div v-if="totalResults === 0" class="no-results">
          <el-icon><Search /></el-icon>
          <p>No results found for "<em>{{ lastKeyword }}</em>"</p>
          <span>Try using different keywords</span>
        </div>
      </template>

      <!-- Initial State -->
      <div v-else class="initial-state">
        <div class="initial-icon">🔍</div>
        <p>Enter a keyword to search through all your memories</p>
      </div>
    </div>

    <!-- Image Viewer -->
    <el-image-viewer v-if="showImageViewer" :url-list="imageUrls" :initial-index="0"
      @close="showImageViewer = false" />

    <!-- Diary Detail -->
    <el-dialog v-model="showDiaryDetail" :title="currentDiary?.title" width="680px" destroy-on-close>
      <div class="diary-detail" v-if="currentDiary">
        <div class="detail-meta">
          <span v-if="currentDiary.mood">{{ currentDiary.mood }}</span>
          <span class="date">{{ formatDate(currentDiary.created_at) }}</span>
        </div>
        <div class="detail-content">{{ currentDiary.content }}</div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { searchApi } from '@/api/search'
import dayjs from 'dayjs'
import { Search, Picture, VideoPlay, Document } from '@element-plus/icons-vue'

const keyword = ref('')
const lastKeyword = ref('')
const loading = ref(false)
const hasSearched = ref(false)
const results = ref({})
const showImageViewer = ref(false)
const imageUrls = ref([])
const showDiaryDetail = ref(false)
const currentDiary = ref(null)

const totalResults = computed(() => {
  return (results.value.photos?.length || 0) +
    (results.value.videos?.length || 0) +
    (results.value.diaries?.length || 0)
})

const doSearch = async () => {
  if (!keyword.value.trim()) return
  loading.value = true
  hasSearched.value = true
  lastKeyword.value = keyword.value.trim()
  try {
    results.value = await searchApi.search({ keyword: lastKeyword.value })
  } catch (e) {
    console.error('Search failed:', e)
    results.value = {}
  } finally {
    loading.value = false
  }
}

const viewPhoto = (photo) => {
  imageUrls.value = [`/uploads/${photo.filepath}`]
  showImageViewer.value = true
}

const openDiary = (diary) => {
  currentDiary.value = diary
  showDiaryDetail.value = true
}

const formatDate = (d) => dayjs(d).format('MMM D, YYYY')
const formatDuration = (s) => {
  const m = Math.floor(s / 60)
  const sec = s % 60
  return `${m}:${sec.toString().padStart(2, '0')}`
}
</script>

<style lang="scss" scoped>
@import '@/assets/styles/variables.scss';

.search-page {
  max-width: 1100px;
  margin: 0 auto;
  padding: 2rem;
}

.page-header {
  text-align: center;
  margin-bottom: 2rem;

  h1 {
    font-size: 2.5rem;
    color: var(--primary-color);
    font-family: 'Georgia', serif;
    margin-bottom: 0.5rem;
  }
  p { color: var(--text-secondary); }
}

.search-section {
  display: flex;
  justify-content: center;
  margin-bottom: 3rem;
}

.search-input-wrapper {
  display: flex;
  align-items: center;
  width: 100%;
  max-width: 600px;
  background: white;
  border-radius: 50px;
  box-shadow: var(--shadow-md);
  padding: 6px;
  position: relative;
  transition: box-shadow 0.3s ease;

  &:focus-within {
    box-shadow: 0 4px 20px rgba(212, 93, 121, 0.2);
  }

  .search-icon {
    position: absolute;
    left: 20px;
    color: #ccc;
    font-size: 1.1rem;
  }

  input {
    flex: 1;
    border: none;
    outline: none;
    padding: 0.9rem 1rem 0.9rem 3rem;
    font-size: 1rem;
    background: transparent;
    color: var(--text-primary);

    &::placeholder { color: #ccc; }
  }

  .search-submit {
    padding: 0.7rem 1.5rem;
    background: var(--primary-color);
    color: white;
    border-radius: 50px;
    font-size: 0.95rem;
    font-weight: 500;
    transition: all 0.3s ease;
    cursor: pointer;

    &:hover:not(:disabled) {
      background: var(--accent-color);
    }

    &:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
  }
}

.results-summary {
  margin-bottom: 2rem;
  color: var(--text-secondary);
  font-size: 0.95rem;

  strong { color: var(--text-primary); }
  em { color: var(--primary-color); font-style: normal; }
}

.result-section {
  margin-bottom: 3rem;

  h2 {
    display: flex; align-items: center; gap: 8px;
    font-size: 1.3rem; color: var(--text-primary);
    margin-bottom: 1.5rem;
    padding-bottom: 0.8rem;
    border-bottom: 2px solid var(--bg-color);

    .el-icon { color: var(--primary-color); }
    .count { color: #ccc; font-weight: 400; font-size: 1rem; }
  }
}

/* Photos Grid */
.photos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 1rem;
}

.photo-item {
  border-radius: 12px;
  overflow: hidden;
  position: relative;
  cursor: pointer;
  aspect-ratio: 1;

  img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.4s ease; }

  .photo-overlay {
    position: absolute; inset: 0;
    background: linear-gradient(to top, rgba(0,0,0,0.7), transparent 60%);
    display: flex; flex-direction: column; justify-content: flex-end;
    padding: 1rem; opacity: 0; transition: opacity 0.3s ease;
    color: white;

    h4 { margin: 0 0 4px; font-size: 0.9rem; }
    span { font-size: 0.75rem; opacity: 0.8; }
  }

  &:hover {
    img { transform: scale(1.08); }
    .photo-overlay { opacity: 1; }
  }
}

/* Videos Grid */
.videos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 1rem;
}

.video-item {
  background: white; border-radius: 12px; overflow: hidden;
  box-shadow: var(--shadow-sm); transition: all 0.3s ease;

  &:hover { transform: translateY(-4px); box-shadow: var(--shadow-md); }
}

.video-thumb {
  aspect-ratio: 16/9; position: relative; overflow: hidden; background: #1a1225;

  img { width: 100%; height: 100%; object-fit: cover; }
}

.thumb-placeholder {
  width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;
  color: rgba(255,255,255,0.2); font-size: 2.5rem;
}

.duration {
  position: absolute; bottom: 6px; right: 6px;
  background: rgba(0,0,0,0.75); color: white;
  padding: 2px 6px; border-radius: 4px; font-size: 0.75rem;
}

.video-info {
  padding: 12px;
  h4 { margin: 0 0 4px; font-size: 0.95rem; color: var(--text-primary); }
  .date { font-size: 0.8rem; color: #999; }
}

/* Diary List */
.diaries-list { display: flex; flex-direction: column; gap: 0.8rem; }

.diary-item {
  background: white; border-radius: 12px; padding: 1.2rem 1.5rem;
  box-shadow: var(--shadow-sm); cursor: pointer; transition: all 0.3s ease;
  border-left: 3px solid transparent;

  &:hover { border-left-color: var(--primary-color); transform: translateX(4px); }
}

.diary-head {
  display: flex; align-items: center; gap: 8px; margin-bottom: 6px;
  .mood { font-size: 1.1rem; }
  h4 { margin: 0; font-size: 1rem; color: var(--text-primary); }
}

.excerpt {
  color: var(--text-secondary); font-size: 0.9rem; line-height: 1.5;
  margin: 0 0 8px;
  display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
}

.date { font-size: 0.8rem; color: #bbb; }

/* Empty & Initial States */
.no-results, .initial-state {
  text-align: center; padding: 4rem 2rem; color: var(--text-secondary);

  .el-icon { font-size: 3rem; margin-bottom: 1rem; color: var(--primary-color); }
  p { font-size: 1.05rem; margin-bottom: 0.5rem; }
  em { color: var(--primary-color); font-style: normal; }
  span { font-size: 0.9rem; color: #ccc; }
}

.initial-state {
  .initial-icon { font-size: 3rem; margin-bottom: 1rem; }
}

/* Diary Detail */
.diary-detail {
  .detail-meta {
    display: flex; gap: 10px; align-items: center; margin-bottom: 1.5rem;
    padding-bottom: 1rem; border-bottom: 1px solid #f0f0f0;
    .date { color: var(--text-secondary); font-size: 0.9rem; }
  }
  .detail-content {
    color: var(--text-primary); line-height: 2; white-space: pre-wrap;
  }
}
</style>
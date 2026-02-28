<template>
  <div class="admin-statistics">
    <!-- Summary Cards -->
    <div class="stats-grid" v-loading="loading">
      <div class="stat-card photos-card">
        <div class="stat-icon">📷</div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.basic_stats?.total_photos || 0 }}</span>
          <span class="stat-label">照片总数</span>
        </div>
        <div class="stat-trend" v-if="stats.recent_stats">
          <span class="trend-value">+{{ stats.recent_stats.last_7_days?.photos || 0 }}</span>
          <span class="trend-period">近7天</span>
        </div>
      </div>

      <div class="stat-card videos-card">
        <div class="stat-icon">🎬</div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.basic_stats?.total_videos || 0 }}</span>
          <span class="stat-label">视频总数</span>
        </div>
        <div class="stat-trend" v-if="stats.recent_stats">
          <span class="trend-value">+{{ stats.recent_stats.last_7_days?.videos || 0 }}</span>
          <span class="trend-period">近7天</span>
        </div>
      </div>

      <div class="stat-card diaries-card">
        <div class="stat-icon">📝</div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.basic_stats?.total_diaries || 0 }}</span>
          <span class="stat-label">日记总数</span>
        </div>
        <div class="stat-trend" v-if="stats.recent_stats">
          <span class="trend-value">+{{ stats.recent_stats.last_7_days?.diaries || 0 }}</span>
          <span class="trend-period">近7天</span>
        </div>
      </div>

      <div class="stat-card total-card">
        <div class="stat-icon">💝</div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.basic_stats?.total_storage || 0 }}</span>
          <span class="stat-label">记录总数</span>
        </div>
        <div class="stat-trend" v-if="stats.recent_stats">
          <span class="trend-value">+{{ (stats.recent_stats.last_30_days?.photos || 0) + (stats.recent_stats.last_30_days?.videos || 0) + (stats.recent_stats.last_30_days?.diaries || 0) }}</span>
          <span class="trend-period">近30天</span>
        </div>
      </div>
    </div>

    <!-- Content Sections -->
    <div class="content-grid">
      <!-- Category Distribution -->
      <div class="stat-section">
        <h3>📊 分类分布</h3>
        <div class="distribution-panel">
          <div class="distrib-group" v-if="stats.category_stats?.photos?.length">
            <h4>照片分类</h4>
            <div v-for="item in stats.category_stats.photos" :key="item.category" class="distrib-item">
              <span class="distrib-label">{{ item.category }}</span>
              <div class="distrib-bar-track">
                <div class="distrib-bar photos" :style="{ width: getPercentage(item.count, stats.basic_stats?.total_photos) + '%' }"></div>
              </div>
              <span class="distrib-count">{{ item.count }}</span>
            </div>
          </div>

          <div class="distrib-group" v-if="stats.category_stats?.videos?.length">
            <h4>视频分类</h4>
            <div v-for="item in stats.category_stats.videos" :key="item.category" class="distrib-item">
              <span class="distrib-label">{{ item.category }}</span>
              <div class="distrib-bar-track">
                <div class="distrib-bar videos" :style="{ width: getPercentage(item.count, stats.basic_stats?.total_videos) + '%' }"></div>
              </div>
              <span class="distrib-count">{{ item.count }}</span>
            </div>
          </div>

          <div class="distrib-group" v-if="stats.category_stats?.diaries?.length">
            <h4>日记分类</h4>
            <div v-for="item in stats.category_stats.diaries" :key="item.category" class="distrib-item">
              <span class="distrib-label">{{ item.category }}</span>
              <div class="distrib-bar-track">
                <div class="distrib-bar diaries" :style="{ width: getPercentage(item.count, stats.basic_stats?.total_diaries) + '%' }"></div>
              </div>
              <span class="distrib-count">{{ item.count }}</span>
            </div>
          </div>

          <div v-if="!stats.category_stats?.photos?.length && !stats.category_stats?.videos?.length && !stats.category_stats?.diaries?.length" class="no-data">
            暂无分类数据
          </div>
        </div>
      </div>

      <!-- Mood Distribution -->
      <div class="stat-section">
        <h3>😊 心情统计</h3>
        <div class="mood-panel">
          <div v-if="stats.mood_stats?.length" class="mood-grid">
            <div v-for="item in stats.mood_stats" :key="item.mood" class="mood-item">
              <div class="mood-emoji">{{ item.mood }}</div>
              <div class="mood-count">{{ item.count }} 次</div>
            </div>
          </div>
          <div v-else class="no-data">暂无心情数据</div>
        </div>
      </div>

      <!-- Recent Activity (30 days) -->
      <div class="stat-section full-width">
        <h3>📅 近30天活跃度</h3>
        <div class="activity-panel" v-loading="timelineLoading">
          <div class="activity-heatmap">
            <div v-for="(data, date) in timelineStats" :key="date" class="heat-day"
              :class="getHeatLevel(data.total)"
              :title="`${date}: ${data.total} 条记录`"
            >
            </div>
          </div>
          <div class="heat-legend">
            <span>少</span>
            <div class="heat-day level-0"></div>
            <div class="heat-day level-1"></div>
            <div class="heat-day level-2"></div>
            <div class="heat-day level-3"></div>
            <span>多</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { statisticsApi } from '@/api/search'

const stats = ref({})
const timelineStats = ref({})
const loading = ref(false)
const timelineLoading = ref(false)

const loadStats = async () => {
  loading.value = true
  try {
    stats.value = await statisticsApi.getStatistics()
  } catch {
    ElMessage.error('加载统计数据失败')
  } finally {
    loading.value = false
  }
}

const loadTimeline = async () => {
  timelineLoading.value = true
  try {
    const data = await statisticsApi.getTimelineStatistics({ days: 30 })
    timelineStats.value = data.timeline || {}
  } catch {
    console.error('加载时间线统计失败')
  } finally {
    timelineLoading.value = false
  }
}

const getPercentage = (count, total) => {
  if (!total) return 0
  return Math.round((count / total) * 100)
}

const getHeatLevel = (total) => {
  if (!total || total === 0) return 'level-0'
  if (total <= 1) return 'level-1'
  if (total <= 3) return 'level-2'
  return 'level-3'
}

onMounted(() => {
  loadStats()
  loadTimeline()
})
</script>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
  margin-bottom: 28px;
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.08);
}

.stat-card::after {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 100px;
  height: 100%;
  opacity: 0.05;
  border-radius: 50% 0 0 50%;
}

.photos-card::after { background: linear-gradient(135deg, #d45d79, #ea90a6); }
.videos-card::after { background: linear-gradient(135deg, #409eff, #79bbff); }
.diaries-card::after { background: linear-gradient(135deg, #67c23a, #95d475); }
.total-card::after { background: linear-gradient(135deg, #e6a23c, #f0c78a); }

.stat-icon {
  font-size: 2.2rem;
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 14px;
  flex-shrink: 0;
}

.photos-card .stat-icon { background: rgba(212, 93, 121, 0.1); }
.videos-card .stat-icon { background: rgba(64, 158, 255, 0.1); }
.diaries-card .stat-icon { background: rgba(103, 194, 58, 0.1); }
.total-card .stat-icon { background: rgba(230, 162, 60, 0.1); }

.stat-info {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.stat-value {
  font-size: 1.8rem;
  font-weight: 700;
  color: #333;
  line-height: 1.2;
}

.stat-label {
  font-size: 0.85rem;
  color: #999;
  margin-top: 2px;
}

.stat-trend {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.trend-value {
  font-size: 0.9rem;
  font-weight: 600;
  color: #67c23a;
}

.trend-period {
  font-size: 0.75rem;
  color: #ccc;
}

/* Content Sections */
.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.stat-section {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.stat-section.full-width {
  grid-column: 1 / -1;
}

.stat-section h3 {
  margin: 0 0 20px;
  font-size: 1.05rem;
  color: #333;
}

/* Distribution Bars */
.distrib-group { margin-bottom: 20px; }
.distrib-group:last-child { margin-bottom: 0; }
.distrib-group h4 { margin: 0 0 10px; font-size: 0.9rem; color: #666; }

.distrib-item {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.distrib-label {
  width: 60px;
  text-align: right;
  font-size: 0.85rem;
  color: #666;
  flex-shrink: 0;
}

.distrib-bar-track {
  flex: 1;
  height: 8px;
  background: #f5f5f5;
  border-radius: 4px;
  overflow: hidden;
}

.distrib-bar {
  height: 100%;
  border-radius: 4px;
  transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
  min-width: 4px;
}

.distrib-bar.photos { background: linear-gradient(135deg, #d45d79, #ea90a6); }
.distrib-bar.videos { background: linear-gradient(135deg, #409eff, #79bbff); }
.distrib-bar.diaries { background: linear-gradient(135deg, #67c23a, #95d475); }

.distrib-count {
  width: 32px;
  font-size: 0.85rem;
  font-weight: 600;
  color: #333;
}

/* Mood Panel */
.mood-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.mood-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px 20px;
  background: #fafafa;
  border-radius: 12px;
  transition: all 0.3s ease;
  min-width: 80px;
}

.mood-item:hover {
  background: #fff5f7;
  transform: translateY(-2px);
}

.mood-emoji {
  font-size: 1.6rem;
  margin-bottom: 6px;
}

.mood-count {
  font-size: 0.85rem;
  color: #666;
  font-weight: 500;
}

/* Heatmap */
.activity-heatmap {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-bottom: 12px;
}

.heat-day {
  width: 18px;
  height: 18px;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.heat-day:hover {
  transform: scale(1.3);
}

.level-0 { background: #f0f0f0; }
.level-1 { background: rgba(212, 93, 121, 0.25); }
.level-2 { background: rgba(212, 93, 121, 0.55); }
.level-3 { background: rgba(212, 93, 121, 0.85); }

.heat-legend {
  display: flex;
  align-items: center;
  gap: 4px;
  justify-content: flex-end;
  font-size: 0.75rem;
  color: #999;
}

.heat-legend .heat-day {
  width: 14px;
  height: 14px;
}

.no-data {
  text-align: center;
  padding: 40px;
  color: #ccc;
  font-size: 0.95rem;
}

@media (max-width: 768px) {
  .content-grid {
    grid-template-columns: 1fr;
  }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
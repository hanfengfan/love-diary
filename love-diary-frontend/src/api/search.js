import request from './request'

export const searchApi = {
  // 搜索内容
  search(params) {
    return request.get('/search', { params })
  },
}

export const timelineApi = {
  // 获取时间线数据
  getTimeline(params) {
    return request.get('/timeline', { params })
  },

  // 获取日历数据
  getCalendarData(params) {
    return request.get('/timeline/calendar', { params })
  },
}

export const statisticsApi = {
  // 获取统计数据
  getStatistics() {
    return request.get('/statistics')
  },

  // 获取时间线统计数据
  getTimelineStatistics(params) {
    return request.get('/statistics/timeline', { params })
  },
}
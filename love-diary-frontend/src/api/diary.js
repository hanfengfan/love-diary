import request from './request'

export const diaryApi = {
  // 获取日记列表
  getDiaries(params) {
    return request.get('/diaries', { params })
  },

  // 创建日记
  createDiary(data) {
    return request.post('/diaries', data)
  },

  // 获取日记详情
  getDiary(id) {
    return request.get(`/diaries/${id}`)
  },

  // 更新日记
  updateDiary(id, data) {
    return request.put(`/diaries/${id}`, data)
  },

  // 删除日记
  deleteDiary(id) {
    return request.delete(`/diaries/${id}`)
  },

  // 获取分类
  getCategories() {
    return request.get('/diaries/categories')
  },

  // 获取标签
  getTags() {
    return request.get('/diaries/tags')
  },

  // 获取心情类型
  getMoods() {
    return request.get('/diaries/moods')
  },
}
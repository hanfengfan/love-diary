import request from './request'

export const videoApi = {
  // 获取视频列表
  getVideos(params) {
    return request.get('/videos', { params })
  },

  // 上传视频
  uploadVideo(formData) {
    return request.post('/videos', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },

  // 获取视频详情
  getVideo(id) {
    return request.get(`/videos/${id}`)
  },

  // 更新视频信息
  updateVideo(id, data) {
    return request.put(`/videos/${id}`, data)
  },

  // 删除视频
  deleteVideo(id) {
    return request.delete(`/videos/${id}`)
  },

  // 获取分类
  getCategories() {
    return request.get('/videos/categories')
  },

  // 获取标签
  getTags() {
    return request.get('/videos/tags')
  },
}
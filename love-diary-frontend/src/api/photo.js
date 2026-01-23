import request from './request'

export const photoApi = {
  // 获取照片列表
  getPhotos(params) {
    return request.get('/photos', { params })
  },

  // 上传照片
  uploadPhoto(formData) {
    return request.post('/photos', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },

  // 获取照片详情
  getPhoto(id) {
    return request.get(`/photos/${id}`)
  },

  // 更新照片信息
  updatePhoto(id, data) {
    return request.put(`/photos/${id}`, data)
  },

  // 删除照片
  deletePhoto(id) {
    return request.delete(`/photos/${id}`)
  },

  // 获取分类
  getCategories() {
    return request.get('/photos/categories')
  },

  // 获取标签
  getTags() {
    return request.get('/photos/tags')
  },
}
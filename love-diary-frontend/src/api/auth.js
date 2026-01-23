import request from './request'

export const authApi = {
  // 登录
  login(data) {
    return request.post('/auth/login', data)
  },

  // 登出
  logout() {
    return request.post('/auth/logout')
  },

  // 检查登录状态
  checkLogin() {
    return request.get('/auth/check')
  },

  // 修改密码
  changePassword(data) {
    return request.post('/auth/change-password', data)
  },
}
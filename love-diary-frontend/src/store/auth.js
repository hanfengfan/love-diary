import { defineStore } from 'pinia'
import { authApi } from '@/api/auth'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    isLoggedIn: false,
  }),

  actions: {
    async checkLogin() {
      try {
        const data = await authApi.checkLogin()
        this.isLoggedIn = data.logged_in
        this.user = data.user
      } catch (error) {
        this.isLoggedIn = false
        this.user = null
      }
    },

    async login(credentials) {
      try {
        const data = await authApi.login(credentials)
        this.isLoggedIn = true
        this.user = data.user
        return data
      } catch (error) {
        throw error
      }
    },

    async logout() {
      try {
        await authApi.logout()
        this.isLoggedIn = false
        this.user = null
      } catch (error) {
        // 即使API调用失败，也要清除本地状态
        this.isLoggedIn = false
        this.user = null
      }
    },

    async changePassword(passwordData) {
      try {
        return await authApi.changePassword(passwordData)
      } catch (error) {
        throw error
      }
    },
  },
})
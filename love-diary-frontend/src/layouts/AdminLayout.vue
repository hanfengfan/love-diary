<template>
  <div class="admin-layout">
    <el-container>
      <!-- 侧边栏 -->
      <el-aside width="200px" class="sidebar">
        <div class="logo">
          <router-link to="/admin/photos" class="logo-link">
            <el-icon><Management /></el-icon>
            <span>管理后台</span>
          </router-link>
        </div>

        <el-menu
          :default-active="activeIndex"
          class="sidebar-menu"
          @select="handleMenuSelect"
        >
          <el-menu-item index="/admin/photos">
            <el-icon><Picture /></el-icon>
            <span>照片管理</span>
          </el-menu-item>
          <el-menu-item index="/admin/videos">
            <el-icon><VideoPlay /></el-icon>
            <span>视频管理</span>
          </el-menu-item>
          <el-menu-item index="/admin/diaries">
            <el-icon><Document /></el-icon>
            <span>日记管理</span>
          </el-menu-item>
          <el-menu-item index="/admin/statistics">
            <el-icon><DataAnalysis /></el-icon>
            <span>数据统计</span>
          </el-menu-item>
        </el-menu>

        <div class="sidebar-footer">
          <el-button text @click="goToHome">
            <el-icon><House /></el-icon>
            返回首页
          </el-button>
        </div>
      </el-aside>

      <!-- 主要内容区域 -->
      <el-container>
        <!-- 头部 -->
        <el-header class="header">
          <div class="header-content">
            <div class="page-title">
              <h2>{{ pageTitle }}</h2>
            </div>

            <div class="header-actions">
              <el-dropdown @command="handleCommand">
                <span class="user-info">
                  <el-icon><User /></el-icon>
                  {{ authStore.user?.username }}
                  <el-icon class="el-icon--right"><arrow-down /></el-icon>
                </span>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="changePassword">
                      <el-icon><Key /></el-icon>
                      修改密码
                    </el-dropdown-item>
                    <el-dropdown-item divided command="logout">
                      <el-icon><SwitchButton /></el-icon>
                      退出登录
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </div>
        </el-header>

        <!-- 内容区域 -->
        <el-main class="main-content">
          <router-view />
        </el-main>
      </el-container>
    </el-container>

    <!-- 修改密码对话框 -->
    <el-dialog v-model="passwordDialogVisible" title="修改密码" width="400px">
      <el-form :model="passwordForm" :rules="passwordRules" ref="passwordFormRef">
        <el-form-item label="旧密码" prop="oldPassword">
          <el-input
            v-model="passwordForm.oldPassword"
            type="password"
            show-password
            placeholder="请输入旧密码"
          />
        </el-form-item>
        <el-form-item label="新密码" prop="newPassword">
          <el-input
            v-model="passwordForm.newPassword"
            type="password"
            show-password
            placeholder="请输入新密码"
          />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            v-model="passwordForm.confirmPassword"
            type="password"
            show-password
            placeholder="请确认新密码"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="passwordDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="passwordLoading" @click="handleChangePassword">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useAuthStore } from '@/store/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const passwordDialogVisible = ref(false)
const passwordLoading = ref(false)
const passwordFormRef = ref()

const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const passwordRules = {
  oldPassword: [
    { required: true, message: '请输入旧密码', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== passwordForm.newPassword) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

const activeIndex = computed(() => {
  return route.path
})

const pageTitle = computed(() => {
  return route.meta.title || '管理后台'
})

const handleMenuSelect = (index) => {
  if (index !== route.path) {
    router.push(index)
  }
}

const handleCommand = (command) => {
  switch (command) {
    case 'changePassword':
      openPasswordDialog()
      break
    case 'logout':
      handleLogout()
      break
  }
}

const openPasswordDialog = () => {
  passwordDialogVisible.value = true
  Object.assign(passwordForm, {
    oldPassword: '',
    newPassword: '',
    confirmPassword: ''
  })
}

const handleChangePassword = async () => {
  if (!passwordFormRef.value) return

  try {
    await passwordFormRef.value.validate()
    passwordLoading.value = true

    await authStore.changePassword({
      old_password: passwordForm.oldPassword,
      new_password: passwordForm.newPassword
    })

    ElMessage.success('密码修改成功')
    passwordDialogVisible.value = false
  } catch (error) {
    console.error('修改密码失败:', error)
  } finally {
    passwordLoading.value = false
  }
}

const handleLogout = async () => {
  try {
    await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })

    await authStore.logout()
    router.push('/')
  } catch (error) {
    // 用户取消操作
  }
}

const goToHome = () => {
  router.push('/')
}
</script>

<style scoped>
.admin-layout {
  min-height: 100vh;
}

.sidebar {
  background: #001529;
  overflow: hidden;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.1);
}

.logo-link {
  display: flex;
  align-items: center;
  gap: 8px;
  color: white;
  text-decoration: none;
  font-size: 16px;
  font-weight: 600;
}

.sidebar-menu {
  border-right: none;
  background: #001529;
}

.sidebar-menu :deep(.el-menu-item) {
  color: rgba(255, 255, 255, 0.65);
}

.sidebar-menu :deep(.el-menu-item:hover) {
  background: #1890ff !important;
  color: white;
}

.sidebar-menu :deep(.el-menu-item.is-active) {
  background: #1890ff !important;
  color: white;
}

.sidebar-footer {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 16px;
  text-align: center;
  background: #001529;
}

.header {
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  padding: 0 20px;
}

.page-title h2 {
  margin: 0;
  color: #333;
}

.header-actions {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #606266;
  font-size: 14px;
  cursor: pointer;
}

.main-content {
  background: #f5f5f5;
  padding: 20px;
}

:deep(.el-aside) {
  position: relative;
}

:deep(.el-header) {
  height: 60px;
  padding: 0;
}
</style>
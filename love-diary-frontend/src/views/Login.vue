<template>
  <div class="login-page">
    <div class="login-background"></div>
    
    <div class="login-card">
      <div class="login-header">
        <div class="logo">💖</div>
        <h2>Welcome Back</h2>
        <p>Sign in to manage your love diary</p>
      </div>

      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        class="login-form"
        @submit.prevent="handleLogin"
      >
        <el-form-item prop="username">
          <div class="input-group">
            <el-icon><User /></el-icon>
            <input 
              v-model="loginForm.username" 
              type="text" 
              placeholder="Username"
              autocomplete="username"
            />
          </div>
        </el-form-item>

        <el-form-item prop="password">
          <div class="input-group">
            <el-icon><Lock /></el-icon>
            <input 
              v-model="loginForm.password" 
              type="password" 
              placeholder="Password"
              autocomplete="current-password"
            />
          </div>
        </el-form-item>

        <button 
          type="submit" 
          class="login-btn" 
          :disabled="loading"
        >
          <span v-if="!loading">Sign In</span>
          <el-icon v-else class="is-loading"><Loading /></el-icon>
        </button>
      </el-form>

      <div class="login-footer">
        <router-link to="/" class="back-link">
          <el-icon><ArrowLeft /></el-icon> Back to Home
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/store/auth'
import { User, Lock, Loading, ArrowLeft } from '@element-plus/icons-vue'

const router = useRouter()
const authStore = useAuthStore()

const loginFormRef = ref()
const loading = ref(false)

const loginForm = reactive({
  username: '',
  password: ''
})

const loginRules = {
  username: [
    { required: true, message: 'Please enter username', trigger: 'blur' }
  ],
  password: [
    { required: true, message: 'Please enter password', trigger: 'blur' },
    { min: 6, message: 'Password must be at least 6 characters', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!loginFormRef.value) return

  try {
    await loginFormRef.value.validate()
    loading.value = true

    await authStore.login(loginForm)
    ElMessage.success('Welcome back!')
    router.push('/admin/photos')
  } catch (error) {
    console.error('Login failed:', error)
    ElMessage.error('Invalid username or password')
  } finally {
    loading.value = false
  }
}
</script>

<style lang="scss" scoped>
@import '@/assets/styles/variables.scss';

.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.login-background {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 99%, #fecfef 100%);
  z-index: -1;
  
  &::before {
    content: '';
    position: absolute;
    width: 150%;
    height: 150%;
    background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, transparent 60%);
    top: -25%;
    left: -25%;
    animation: float 10s infinite ease-in-out;
  }
}

.login-card {
  @include glass;
  background: rgba(255, 255, 255, 0.8);
  padding: 3rem;
  border-radius: var(--radius-lg);
  width: 100%;
  max-width: 420px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  animation: slideUp 0.5s ease-out;
}

.login-header {
  text-align: center;
  margin-bottom: 2.5rem;
  
  .logo {
    font-size: 3rem;
    margin-bottom: 1rem;
    animation: pulse 2s infinite;
  }
  
  h2 {
    color: var(--text-primary);
    font-size: 1.8rem;
    margin-bottom: 0.5rem;
  }
  
  p {
    color: var(--text-secondary);
  }
}

.input-group {
  position: relative;
  
  .el-icon {
    position: absolute;
    left: 1rem;
    top: 50%;
    transform: translateY(-50%);
    color: var(--text-secondary);
    font-size: 1.2rem;
  }
  
  input {
    width: 100%;
    padding: 1rem 1rem 1rem 3rem;
    border: 1px solid rgba(0,0,0,0.15); /* Darker border */
    border-radius: var(--radius-sm);
    font-size: 1rem;
    color: var(--text-primary); /* Ensure text is dark */
    background: rgba(255, 255, 255, 0.95); /* More opaque */
    transition: all 0.3s ease;
    
    &::placeholder {
      color: var(--text-secondary); /* Darker placeholder */
      opacity: 0.7;
    }
    
    &:focus {
      outline: none;
      border-color: var(--accent-color); /* Darker focus color */
      box-shadow: 0 0 0 3px rgba(168, 63, 88, 0.2);
    }
  }
}

.login-btn {
  width: 100%;
  padding: 1rem;
  background: var(--primary-color);
  color: white;
  border-radius: var(--radius-sm);
  font-size: 1rem;
  font-weight: 600;
  margin-top: 1rem;
  transition: all 0.3s ease;
  display: flex;
  justify-content: center;
  align-items: center;
  
  &:hover:not(:disabled) {
    background: var(--accent-color);
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }
  
  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }
}

.login-footer {
  margin-top: 2rem;
  text-align: center;
  
  .back-link {
    color: var(--text-secondary);
    font-size: 0.9rem;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    
    &:hover {
      color: var(--primary-color);
    }
  }
}

@keyframes float {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(50px, 50px); }
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}
</style>
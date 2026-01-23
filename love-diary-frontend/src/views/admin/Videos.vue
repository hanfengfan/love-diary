<template>
  <div class="admin-videos">
    <div class="page-header">
      <h2>视频管理</h2>
      <el-button type="primary">
        <el-icon><Upload /></el-icon>
        上传视频
      </el-button>
    </div>

    <el-card>
      <div class="empty-state">
        <el-icon><VideoPlay /></el-icon>
        <p>视频管理功能开发中...</p>
      </div>
    </el-card>
  </div>
</template>

<script setup>
// 视频管理页面占位符
</script>

<style scoped>
.admin-videos {
  padding: 0;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  color: #333;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  color: #999;
}

.empty-state .el-icon {
  font-size: 48px;
  margin-bottom: 8px;
}
</style>
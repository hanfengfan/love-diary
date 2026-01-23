<template>
  <div class="videos">
    <div class="page-header">
      <h2>视频</h2>
    </div>

    <el-card>
      <div class="empty-state">
        <el-icon><VideoPlay /></el-icon>
        <p>视频功能开发中...</p>
      </div>
    </el-card>
  </div>
</template>

<script setup>
// 视频页面占位符
</script>

<style scoped>
.videos {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
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
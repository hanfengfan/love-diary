<template>
  <div class="admin-statistics">
    <div class="page-header">
      <h2>数据统计</h2>
    </div>

    <el-card>
      <div class="empty-state">
        <el-icon><DataAnalysis /></el-icon>
        <p>数据统计功能开发中...</p>
      </div>
    </el-card>
  </div>
</template>

<script setup>
// 数据统计页面占位符
</script>

<style scoped>
.admin-statistics {
  padding: 0;
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
<script setup lang="ts">
import { ref } from 'vue'

const inputText = ref('')

const generateResponse = () => {
  console.log('Generating response for:', inputText.value)
}
</script>

<template>
  <div class="chat-input">
    <div class="chat-input-content">
      <div class="input-generate-container">
        <el-input
          v-model="inputText"
          type="textarea"
          :rows="1"
          placeholder="请输入你的回复内容（非必填），如：谢谢鉴赏"
          resize="none"
          class="custom-input"
        />
        <el-button @click="generateResponse" class="generate-btn">
          <el-icon><Promotion /></el-icon>
          生成意图
        </el-button>
      </div>
      
      <div class="smart-reply-container">
        <el-button 
          type="primary" 
          size="large" 
          class="smart-reply-btn"
          :style="{ backgroundColor: '#2563eb', borderColor: '#2563eb' }"
        >
          <el-icon><Magic /></el-icon>
          智能回复
        </el-button>
      </div>
      
      <div class="controls-container">
        <div class="selectors">
          <el-select placeholder="请选择助手" class="selector">
            <el-option label="助手 1" value="1" />
            <el-option label="助手 2" value="2" />
          </el-select>
          <el-select placeholder="请选择风格" class="selector">
            <el-option label="正式" value="formal" />
            <el-option label="随意" value="casual" />
            <el-option label="幽默" value="humorous" />
          </el-select>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.chat-input {
  background-color: #fff;
  border-top: 1px solid #e5e7eb;
}

.chat-input-content {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px 40px;
}

.input-generate-container {
  display: flex;
  gap: 16px;
  align-items: stretch;
  border: 1px solid #dcdfe6;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  background-color: #fff;
}

.custom-input {
  flex: 1;
}

.custom-input :deep(.el-textarea__inner) {
  border-radius: 8px;
  padding: 12px;
  font-size: 14px;
  background-color: #f9fafb;
  border-color: #e5e7eb;
  height: 100%;
}

.custom-input :deep(.el-textarea__inner:focus) {
  background-color: #fff;
  border-color: #409eff;
}

.generate-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 10px 20px;
  font-size: 14px;
  border-radius: 6px;
  min-width: 120px;
  height: auto;
  align-self: center;
}

.controls-container {
  display: flex;
  gap: 16px;
  justify-content: flex-start;
  align-items: center;
  margin-bottom: 16px;
}

.selectors {
  display: flex;
  gap: 12px;
}

.selector {
  width: 160px;
}

.selector :deep(.el-input__wrapper) {
  border-radius: 6px;
}

.smart-reply-container {
  display: flex;
  justify-content: center;
  margin-bottom: 16px;
}

.smart-reply-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 28px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 8px;
  transition: all 0.3s ease;
  width: 100%;
  max-width: 400px;
  justify-content: center;
  box-shadow: 0 2px 4px rgba(37, 99, 235, 0.1);
}

.smart-reply-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(37, 99, 235, 0.2);
  background-color: #1d4ed8 !important;
  border-color: #1d4ed8 !important;
}

.smart-reply-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(37, 99, 235, 0.1);
}

.smart-reply-btn .el-icon {
  font-size: 20px;
}
</style>
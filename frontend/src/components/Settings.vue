<script setup lang="ts">
import { ref, reactive, watch, onMounted } from 'vue'
import type { FormInstance } from 'element-plus'

const formData = reactive({
  // AI Settings
  model: '',
  apiKey: '',
  // Personal Information
  name: '',
  age: '',
  gender: '',
  occupation: '',
  otherInfo: ''
})

const modelOptions = [
  { label: 'GPT-3.5', value: 'gpt-3.5-turbo' },
  { label: 'GPT-4', value: 'gpt-4' }
]

const genderOptions = [
  { label: '男', value: 'male' },
  { label: '女', value: 'female' },
  { label: '其他', value: 'other' }
]

// 加载设置
const loadSettings = async () => {
  try {
    const response = await fetch('/api/setting/load')
    const data = await response.json()
    
    // 更新表单数据
    Object.assign(formData, data)
  } catch (error) {
    console.error('Failed to load settings:', error)
  }
}

// 保存设置
const saveSettings = async () => {
  try {
    const response = await fetch('/api/setting/save', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(formData)
    })
    
    if (!response.ok) {
      throw new Error('Failed to save settings')
    }
  } catch (error) {
    console.error('Failed to save settings:', error)
  }
}

// 监听表单数据变化
watch(formData, () => {
  saveSettings()
}, { deep: true })

// 组件挂载时加载设置
onMounted(() => {
  loadSettings()
})

const handleSubmit = async () => {
  // TODO: Implement save settings logic
  console.log('Settings saved:', formData)
}
</script>

<template>
  <div class="settings">
    <el-form :model="formData" label-width="80px">
      <!-- AI Settings Card -->
      <el-card class="settings-card">
        <template #header>
          <div class="card-header">
            <span>AI 设置</span>
          </div>
        </template>
        
        <el-form-item label="模型选择">
          <el-select v-model="formData.model" placeholder="请选择AI模型">
            <el-option
              v-for="option in modelOptions"
              :key="option.value"
              :label="option.label"
              :value="option.value"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="API Key">
          <el-input
            v-model="formData.apiKey"
            type="password"
            placeholder="请输入API Key"
            show-password
          />
        </el-form-item>
      </el-card>

      <!-- Personal Information Card -->
      <el-card class="settings-card">
        <template #header>
          <div class="card-header">
            <span>个人信息</span>
          </div>
        </template>

        <el-form-item label="姓名">
          <el-input v-model="formData.name" placeholder="请输入姓名" />
        </el-form-item>

        <el-form-item label="年龄">
          <el-input-number v-model="formData.age" :min="0" :max="150" placeholder="请输入年龄" />
        </el-form-item>

        <el-form-item label="性别">
          <el-select v-model="formData.gender" placeholder="请选择性别">
            <el-option
              v-for="option in genderOptions"
              :key="option.value"
              :label="option.label"
              :value="option.value"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="职业">
          <el-input v-model="formData.occupation" placeholder="请输入职业" />
        </el-form-item>

        <el-form-item label="其他信息">
          <el-input
            v-model="formData.otherInfo"
            type="textarea"
            rows="3"
            placeholder="请输入其他信息"
          />
        </el-form-item>
      </el-card>
    </el-form>
  </div>
</template>

<style scoped>
.settings {
  padding: 20px;
}

.settings-card {
  margin-bottom: 20px;
}

.card-header {
  font-weight: bold;
}

.form-actions {
  margin-top: 20px;
  text-align: center;
}
</style>

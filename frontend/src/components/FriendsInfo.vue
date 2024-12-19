<script setup lang="ts">
// FriendsInfo component
import { ref, reactive, watch, onMounted, nextTick, defineExpose } from 'vue'
import type { FormInstance } from 'element-plus'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const formRef = ref<FormInstance>()
const isLoading = ref(false)
const form = reactive({
  name: '',
  age: '',
  relationship: '',
  gender: '',
  occupation: '',
  additionalInfo: '',
  contextSize: 5,
  wechatNickname: ''
})

const relationshipOptions = [
  { label: '上级', value: '上级' },
  { label: '朋友', value: '朋友' },
  { label: '同事', value: '同事' },
  { label: '老公', value: '老公' },
  { label: '老婆', value: '老婆' },
  { label: '闺蜜', value: '闺蜜' },
  { label: '爸爸', value: '爸爸' },
  { label: '妈妈', value: '妈妈' },
  { label: '亲人', value: '亲人' },
  { label: '陌生人', value: '陌生人' },
]

// 加载好友信息
const loadFriendInfo = async () => {
  console.log('Loading friend info...')
  isLoading.value = true
  try {
    const response = await axios.get(`/api/friend/load`)
    console.log('Friend info loaded:', response.data)
    await nextTick()  // 等待 DOM 更新
    Object.assign(form, response.data)
  } catch (error: any) {
    if (error.response?.status !== 404) {  // 忽略404错误，因为新用户没有保存过数据是正常的
      console.error('Failed to load friend info:', error)
      ElMessage.error('加载好友信息失败')
    }
  } finally {
    await nextTick()  // 等待 DOM 更新
    console.log('Loading complete, isLoading set to false')
    isLoading.value = false
  }
}

// 保存好友信息
const saveFriendInfo = async () => {
  if (!form.wechatNickname) return
  console.log('Saving friend info, isLoading:', isLoading.value)
  try {
    await axios.post('/api/friend/save', form)
  } catch (error: any) {
    console.error('Failed to save friend info:', error)
    ElMessage.error('保存好友信息失败')
  }
}

// 监听表单数据变化自动保存
watch(form, (newVal, oldVal) => {
  console.log('Watch triggered, isLoading:', isLoading.value)
  console.log('New value:', newVal)
  console.log('Old value:', oldVal)
  if (!isLoading.value) {
    saveFriendInfo()
  } else {
    console.log('Save skipped due to loading state')
  }
}, { deep: true })

// 组件挂载时自动加载数据
onMounted(() => {
  loadFriendInfo()
})

// 暴露方法给父组件
defineExpose({
  loadFriendInfo
})
</script>

<template>
  <div class="friends-info">
    <el-form
      ref="formRef"
      :model="form"
      label-position="right"
      label-width="90px"
    >
      <!-- 基本信息卡片 -->
      <el-card class="info-card">
        <template #header>
          <div class="card-header">
            <span>基本信息</span>
          </div>
        </template>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="微信昵称">
              <el-input v-model="form.wechatNickname" readonly placeholder="微信昵称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="年龄">
              <el-input-number v-model="form.age"  size="mini" :min="1" :max="150" placeholder="请输入年龄" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="姓名">
              <el-input v-model="form.name" placeholder="请输入姓名" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="关系">
              <el-select v-model="form.relationship" allow-create filterable placeholder="请选择关系" style="width: 100%">
                <el-option
                  v-for="item in relationshipOptions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="性别">
              <el-radio-group v-model="form.gender">
                <el-radio label="male">男</el-radio>
                <el-radio label="female">女</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="职业">
              <el-input v-model="form.occupation" placeholder="请输入职业" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="其他信息">
          <el-input
            v-model="form.additionalInfo"
            type="textarea"
            rows="3"
            placeholder="请输入其他相关信息"
          />
        </el-form-item>
      </el-card>

      <!-- 对话设置卡片 -->
      <el-card class="info-card">
        <template #header>
          <div class="card-header">
            <span>对话设置</span>
          </div>
        </template>

        <el-form-item label="上下文数量">
          <el-input-number
            v-model="form.contextSize"
            :min="1"
            :max="20"
            placeholder="请输入上下文数量"
          >
            <template #description>
              <span class="context-description">设置每次对话时参考的历史消息数量（1-20条）</span>
            </template>
          </el-input-number>
        </el-form-item>
      </el-card>
    </el-form>
  </div>
</template>

<style scoped>
.friends-info {
  padding: 20px;
  max-width: 1000px;
  margin: 0 auto;
}

.info-card {
  margin-bottom: 20px;
  border-radius: 8px;
}

.info-card :deep(.el-card__header) {
  padding: 15px 20px;
  border-bottom: 1px solid var(--el-border-color-light);
}

.card-header {
  font-size: 16px;
  font-weight: bold;
  color: var(--el-text-color-primary);
}

.context-description {
  font-size: 12px;
  color: var(--el-text-color-secondary);
  margin-top: 4px;
}

:deep(.el-input-number .el-input__wrapper) {
  width: 100%;
}
</style>

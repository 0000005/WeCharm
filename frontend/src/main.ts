import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import * as ElementPlusIcons from '@element-plus/icons-vue'
import 'element-plus/dist/index.css'
import './style.css'
import App from './App.vue'
import { ref } from 'vue'
import type { ReplyCardMo } from './model/ReplyMo'

const app = createApp(App)

// 创建全局的会话信息列表
const globalSessionList = ref<ReplyCardMo[]>([])

// 将会话信息列表提供给所有组件
app.provide('sessionList', globalSessionList)

// Register all icons globally
for (const [key, component] of Object.entries(ElementPlusIcons)) {
  app.component(key, component)
}

app.use(ElementPlus)
app.mount('#app')
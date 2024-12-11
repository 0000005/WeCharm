import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import * as ElementPlusIcons from '@element-plus/icons-vue'
import 'element-plus/dist/index.css'
import './style.css'
import App from './App.vue'

const app = createApp(App)

// Register all icons globally
for (const [key, component] of Object.entries(ElementPlusIcons)) {
  app.component(key, component)
}

app.use(ElementPlus)
app.mount('#app')
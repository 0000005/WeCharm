<script setup lang="ts">
import TabMenu from './components/TabMenu.vue'
</script>

<template>
  <div class="app-container">
    <div class="main-container">
      <TabMenu />
      <div class="copyright">
        <span> 本软件开源免费，欢迎 <a href="https://github.com/" target="_blank">Star</a></span>
      </div>
    </div>
  </div>
</template>

<style>
.app-container {
  max-width: 1000px;
  margin: 0 auto;
  display: flex;
  align-items: flex-start;
  justify-content: center;
}

.main-container {
  display: flex;
  flex-direction: column;
  flex:1;
  width: 100%;
  min-height: 640px;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.copyright {
  text-align: center;
  padding: 20px 0;
  color: #666;
  font-size: 14px;
  border-top: 1px solid #eee;
  margin-top: auto;
}

.copyright a {
  color: #1890ff;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
}

.copyright a:hover {
  color: #40a9ff;
  text-decoration: underline;
}
</style>
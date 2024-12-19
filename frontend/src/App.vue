<script setup lang="ts">
import TabMenu from './components/TabMenu.vue'
</script>

<template>
  <div class="app-container">
    <div class="main-container">
      <TabMenu />
    </div>
    <div class="copyright">
      <span> 本软件开源免费，欢迎 <a href="https://github.com/" target="_blank">Star</a></span>
    </div>
  </div>
</template>

<style>
.app-container {
  min-height: 100vh;
  max-width: 1000px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  padding-bottom: 60px;
}

.main-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  min-height: calc(100vh - 60px);
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  margin-bottom: 60px;
}

.copyright {
  text-align: center;
  padding: 20px 0;
  color: #666;
  font-size: 14px;
  border-top: 1px solid #eee;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  width: 100%;
  background-color: #fff;
  z-index: 100;
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
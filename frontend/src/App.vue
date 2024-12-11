<script setup lang="ts">
import TabMenu from './components/TabMenu.vue'
</script>

<template>
  <div class="app-container">
    <div class="chat-card">
      <TabMenu />
    </div>
  </div>
</template>

<style>
.app-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 40px 20px;
  min-height: 100vh;
  display: flex;
  align-items: flex-start;
  justify-content: center;
}

.chat-card {
  width: 100%;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.chat-content {
  display: flex;
  flex-direction: column;
}
</style>
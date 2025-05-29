<!-- src/components/ResultTabs.vue -->
<template>
  <div class="result-tabs">
    <div class="tab-buttons">
      <button v-for="tab in tabs" :key="tab" :class="{ active: tab === selectedTab }" @click="$emit('update:tab', tab)">
        {{ tab }}
      </button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    selectedTab: String,
    tabs: Array
  }
}
</script>

<style scoped>
.tab-buttons {
  display: flex;
  flex-wrap: wrap;
  margin-bottom: 1em;
}
button {
  margin: 0.5em;
  padding: 0.5em 1em;
}
.active {
  background-color: #1976d2;
  color: white;
}
</style>

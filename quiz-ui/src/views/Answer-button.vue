<template>
  <button class="answer-button" :style="{ backgroundColor: color }" @click="$emit('click')">
    {{ text }}
  </button>
</template>

<script setup>
const props = defineProps({
  text: String,
  color: String
});
</script>

<style scoped>
.answer-button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  color: white;
  font-size: 16px;
  cursor: pointer;
  text-align: center;
  min-width: 10vh;
  max-width: 20vw;
  word-wrap: break-word;
}
</style>

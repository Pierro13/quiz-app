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
  max-width: 100%; /* Allow the button to expand to fill the container */
  word-wrap: break-word;
  box-sizing: border-box; /* Ensure padding and border are included in the element's total width and height */
}
</style>

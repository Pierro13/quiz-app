<template>
    <button :style="{ backgroundColor: color }" class="color-button">
      {{ text }}
    </button>
  </template>
  
  <script setup>
  const props = defineProps({
    text: {
      type: String,
      required: true
    },
    color: {
      type: String,
      required: true
    }
  });
  </script>
  
  <style scoped>
  .color-button {
    color: black;
    font-size: 18px;
    font-weight: bold;
    border: none;
    padding: 20px;
    cursor: pointer;
    margin: 10px;
    width: 15vw;
  }
  </style>
  
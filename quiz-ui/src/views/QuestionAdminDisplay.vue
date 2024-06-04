<template>
  <div>
    <h2>Question Details</h2>
    <div v-if="question">
      <h3>{{ question.title }}</h3>
      <p>{{ question.text }}</p>
      <img :src="question.image" alt="Question image" v-if="question.image" />
    </div>
    <div v-else>
      <p>Select a question to display</p>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  question: Object
});
</script>

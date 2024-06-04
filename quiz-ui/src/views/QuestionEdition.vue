<template>
  <div>
    <h2>Edit Question</h2>
    <div v-if="localQuestion">
      <input v-model="localQuestion.title" placeholder="Title" />
      <textarea v-model="localQuestion.text" placeholder="Text"></textarea>
      <input v-model="localQuestion.image" placeholder="Image URL" />
      <button @click="saveQuestion">Save</button>
      <button @click="$emit('save')">Cancel</button>
    </div>
    <div v-else>
      <p>Loading question...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const localQuestion = ref(null);

const fetchQuestion = async (id) => {
  try {
    const response = await axios.get(`http://127.0.0.1:5000/questions/${id}`);
    localQuestion.value = response.data;
  } catch (error) {
    console.error('Failed to fetch question:', error);
  }
};

onMounted(() => {
  const questionId = route.params.id;
  fetchQuestion(questionId);
});

const saveQuestion = async () => {
  try {
    await axios.put(`http://127.0.0.1:5000/questions/${localQuestion.value.id}`, localQuestion.value);
    alert('Question saved successfully');
    // Redirigez vers la liste des questions ou émettez un événement
  } catch (error) {
    console.error('Failed to save question:', error);
  }
};
</script>

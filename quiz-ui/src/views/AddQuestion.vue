<template>
  <div>
    <h2>Add New Question</h2>
    <form @submit.prevent="submitForm">
      <div>
        <label for="title">Title:</label>
        <input type="text" id="title" v-model="newQuestion.title" required>
      </div>
      <div>
        <label for="text">Text:</label>
        <textarea id="text" v-model="newQuestion.text" required></textarea>
      </div>
      <div>
        <label for="code">Code:</label>
        <textarea id="code" v-model="newQuestion.code"></textarea>
      </div>
      <div>
        <label for="image">Image URL:</label>
        <input type="text" id="image" v-model="newQuestion.image">
      </div>
      <div>
        <label for="position">Position:</label>
        <input type="number" id="position" v-model="newQuestion.position" required @input="validatePosition">
        <p v-if="positionError" class="error">{{ positionError }}</p>
      </div>
      <button type="submit" :disabled="!!positionError">Add Question</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const newQuestion = ref({
  title: '',
  text: '',
  code: '',
  image: '',
  position: null
});

const positionError = ref('');
const emit = defineEmits(['question-added']);

const validatePosition = () => {
  if (newQuestion.value.position < 1) {
    positionError.value = 'Position must be a positive number.';
  } else {
    positionError.value = '';
  }
};

const submitForm = async () => {
  try {
    const response = await axios.post('http://127.0.0.1:5000/questions', newQuestion.value);
    if (response.status === 201) {
      alert('Question added successfully!');
      emit('question-added');
      newQuestion.value = {
        title: '',
        text: '',
        code: '',
        image: '',
        position: null
      };
      positionError.value = '';
    }
  } catch (error) {
    if (error.response && error.response.status === 400) {
      positionError.value = 'Position is already taken. Please choose a different one.';
    } else {
      console.error('Failed to add question:', error);
    }
  }
};
</script>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.error {
  color: red;
}
</style>

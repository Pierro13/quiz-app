<template>
  <div>
    <h2>Add New Question</h2>
    <form @submit.prevent="submitForm" class="form-question">
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
      <div>
        <h3>Answers:</h3>
        <div v-for="(answer, index) in newQuestion.possibleAnswers" :key="index">
          <input type="text" v-model="answer.text" placeholder="Answer text" required>
          <input type="checkbox" v-model="answer.isCorrect"> Correct
        </div>
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
  position: null,
  possibleAnswers: [
    { text: '', isCorrect: false },
    { text: '', isCorrect: false },
    { text: '', isCorrect: false },
    { text: '', isCorrect: false }
  ]
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
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('No authentication token found');
    }
    if(newQuestion.value.image){
      newQuestion.value.image += '?t=' + new Date().getTime();
    }
    const response = await axios.post('http://127.0.0.1:5000/questions', newQuestion.value, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    if (response.status === 200) {
      alert('Question added successfully!');
      emit('question-added');
      resetForm();
    }
  } catch (error) {
    handleFormError(error);
  }
};

const resetForm = () => {
  newQuestion.value = {
    title: '',
    text: '',
    code: '',
    image: '',
    position: null,
    possibleAnswers: [
      { text: '', isCorrect: false },
      { text: '', isCorrect: false },
      { text: '', isCorrect: false },
      { text: '', isCorrect: false }
    ]
  };
  positionError.value = '';
};

const handleFormError = (error) => {
  if (error.response && error.response.status === 400) {
    positionError.value = 'Position is already taken. Please choose a different one.';
  } else if (error.response && error.response.status === 401) {
    alert('Unauthorized: Please login to add a question.');
  } else {
    console.error('Failed to add question:', error);
  }
};
</script>

<style scoped>
h2{
  text-align: center;
}
.form-question {
  border: 1px solid black;
  border-radius: 25px;
  display: flex;
}

.error {
  color: red;
}
</style>

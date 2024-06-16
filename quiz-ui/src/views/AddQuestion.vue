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
        <div class="code-editor">
          <textarea id="code" v-model="newQuestion.code" @input="highlightCode" class="code-input"></textarea>
          <pre v-html="highlightedCode" class="hljs code-output"></pre>
        </div>
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
import { ref, watch, onMounted } from 'vue';
import axios from 'axios';
import hljs from 'highlight.js';
import 'highlight.js/styles/github.css'; // Choisissez un style approprié

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
const highlightedCode = ref('');
const emit = defineEmits(['question-added']);

const validatePosition = () => {
  if (newQuestion.value.position < 1) {
    positionError.value = 'Position must be a positive number.';
  } else {
    positionError.value = '';
  }
};

const highlightCode = () => {
  if (newQuestion.value.code) {
    highlightedCode.value = hljs.highlightAuto(newQuestion.value.code).value;
  } else {
    highlightedCode.value = '';
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
  highlightedCode.value = '';
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

watch(() => newQuestion.value.code, highlightCode);

onMounted(() => {
  highlightCode();
});
</script>

<style scoped>
h2 {
  text-align: center;
}
.form-question {
  border: 1px solid black;
  border-radius: 25px;
  padding: 20px;
}
.code-editor {
  display: flex;
  position: relative;
}
.code-input {
  width: 50%;
  height: 150px;
  font-family: monospace;
  font-size: 14px;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 10px;
  resize: none;
}
.code-output {
  width: 50%;
  height: 150px;
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 10px;
  overflow: auto;
  white-space: pre-wrap; /* Permet l'habillage du texte */
  word-wrap: break-word; /* Permet l'habillage du texte */
}
.error {
  color: red;
}
</style>

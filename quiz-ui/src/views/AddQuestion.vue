<template>
  <div class="container">
    <h2 class="title">Ajouter une nouvelle question</h2>
    <form @submit.prevent="submitForm" class="form-container">
      <div class="form-group">
        <label for="title">Titre:</label>
        <input type="text" id="title" v-model="newQuestion.title" class="input" required>
      </div>
      <div class="form-group">
        <label for="text">Question:</label>
        <textarea id="text" v-model="newQuestion.text" class="textarea" required></textarea>
      </div>
      <div class="form-group">
        <label for="code">Code:</label>
        <div class="code-editor">
          <textarea id="code" v-model="newQuestion.code" @input="highlightCode" class="code-input"></textarea>
          <pre v-html="highlightedCode" class="hljs code-output"></pre>
        </div>
      </div>
      <div class="form-group">
        <label for="image">URL de l'image(Optionnel):</label>
        <input type="text" id="image" v-model="newQuestion.image" class="input">
      </div>
      <div class="form-group">
        <label for="position">Position:</label>
        <input type="number" id="position" v-model="newQuestion.position" class="input" required @input="validatePosition">
        <p v-if="positionError" class="error">{{ positionError }}</p>
      </div>
      <div class="form-group">
        <label>Réponses:</label>
        <div v-for="(answer, index) in newQuestion.possibleAnswers" :key="index" class="answer-container">
          <input type="text" v-model="answer.text" class="input" placeholder="Texte de réponse" required>
          <input type="checkbox" v-model="answer.isCorrect"> Correct
        </div>
      </div>
      <div class="button-container">
        <button type="submit" class="button save-button" :disabled="!!positionError">Ajouter la question</button>
      </div>
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
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.title {
  text-align: center;
  color: #333;
  margin-bottom: 20px;
}

.form-container {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
}

.input, .textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
}

.textarea {
  height: 100px;
  resize: vertical;
}

.answer-container {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.answer-container .input {
  flex: 1;
  margin-right: 10px;
}

.code-editor {
  display: flex;
  flex-direction: column;
}

.code-input {
  width: 100%;
  height: 150px;
  font-family: monospace;
  font-size: 14px;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 10px;
  resize: none;
}

.code-output {
  width: 100%;
  height: 150px;
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 10px;
  overflow: auto;
  white-space: pre-wrap; /* Permet l'habillage du texte */
  word-wrap: break-word; /* Permet l'habillage du texte */
}

.button-container {
  display: flex;
  justify-content: space-between;
}

.button {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}

.save-button {
  background-color: #4CAF50;
  color: white;
}

.cancel-button {
  background-color: #f44336;
  color: white;
}

.button:hover {
  opacity: 0.9;
}
</style>


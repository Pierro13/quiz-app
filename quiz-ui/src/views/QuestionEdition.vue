<template>
  <div class="container">
    <h2 class="title">Modifier la question</h2>
    <div v-if="localQuestion" class="form-container">
      <div class="form-group">
        <label for="title">Titre:</label>
        <input v-model="localQuestion.title" class="input" id="title" placeholder="Title" />
      </div>
      <div class="form-group">
        <label for="text">Question:</label>
        <textarea v-model="localQuestion.text" class="textarea" id="text" placeholder="Text"></textarea>
      </div>
      <div class="form-group">
        <label for="image">URL de l'image:</label>
        <input v-model="localQuestion.image" class="input" id="image" placeholder="Image URL" />
      </div>
      <div class="form-group">
        <label for="position">Position:</label>
        <input v-model="localQuestion.position" class="input" id="position" type="number" placeholder="Position" />
      </div>
      <div class="form-group">
        <label>Réponses:</label>
        <div v-for="(answer, index) in localQuestion.possibleAnswers" :key="index" class="answer-container">
          <input v-model="answer.text" class="input" placeholder="Answer text" />
          <input type="radio" :value="index" v-model="correctAnswerIndex"> Correcte
        </div>
      </div>
      <div class="form-group code-editor">
        <label for="code">Code:</label>
        <div class="code-editor">
          <textarea v-model="localQuestion.code" id="code" class="code-input" @input="highlightCode" placeholder="Code"></textarea>
          <pre v-html="highlightedCode" class="hljs code-output"></pre>
        </div>
      </div>
      <div class="button-container">
        <button @click="saveQuestion" class="button save-button">Enregistrer</button>
        <button @click="cancelQuestion" class="button cancel-button">Annuler</button>
      </div>
    </div>
    <div v-else>
      <p>Chargement de la question...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import hljs from 'highlight.js';
import 'highlight.js/styles/github.css';

const route = useRoute();
const router = useRouter();
const localQuestion = ref(null);
const highlightedCode = ref('');
const correctAnswerIndex = ref(null);

const fetchQuestion = async (id) => {
  try {
    const response = await axios.get(`http://127.0.0.1:5000/questions/${id}`);
    localQuestion.value = response.data;
    correctAnswerIndex.value = localQuestion.value.possibleAnswers.findIndex(answer => answer.isCorrect);
    highlightCode();
  } catch (error) {
    console.error('Failed to fetch question:', error);
  }
};

watch(correctAnswerIndex, (newIndex) => {
  if (localQuestion.value) {
    localQuestion.value.possibleAnswers.forEach((answer, index) => {
      answer.isCorrect = index === newIndex;
    });
  }
});

const highlightCode = () => {
  if (localQuestion.value?.code) {
    highlightedCode.value = hljs.highlightAuto(localQuestion.value.code).value;
  } else {
    highlightedCode.value = '';
  }
};

const saveQuestion = async () => {
  try {
    await axios.put(`http://127.0.0.1:5000/questions/${localQuestion.value.id}`, localQuestion.value);
    alert('Question enregistrée avec succès');
    router.push('/admin');
  } catch (error) {
    console.error('Failed to save question:', error);
  }
};

const cancelQuestion = () => {
  router.push('/admin');
};

onMounted(() => {
  const questionId = route.params.id;
  fetchQuestion(questionId);
});

watch(
  () => localQuestion.value?.code,
  () => {
    highlightCode();
  }
);
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
  padding-right: 4vw;
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
  white-space: pre-wrap;
  word-wrap: break-word;
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




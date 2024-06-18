<template>
  <div class="admin-container">
    <div v-if="!isTokenValid" class="login-container">
      <h2>Login</h2>
      <div class="input-container">
        <input type="password" v-model="password" placeholder="Password" class="admin-input">
        <button @click="login" class="admin-login-button">Login</button>
      </div>
    </div>
    <div v-else class="panel-container">
      <div class="container">
        <div class="buttons-container">
          <button @click="displayNewQuestionForm" class="add-question-button">Ajouter une question</button>
          <button @click="logout" class="logout-button">Déconnexion</button>
        </div>
      </div>
      <AddQuestion v-if="showAddQuestion" @question-added="fetchQuestions"/>
      <QuestionsList :questions="questions" @question-deleted="fetchQuestions"/>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import axios from 'axios';
import AddQuestion from './AddQuestion.vue';
import QuestionsList from './QuestionsList.vue';
import ParticipationStorageService from '@/services/ParticipationStorageService';

const password = ref('');
const token = ref(localStorage.getItem('token') || '');
const questions = ref([]);
const showAddQuestion = ref(false);
const isTokenValid = ref(false);

const checkToken = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/check-token-validity', { headers: { 'Authorization': `Bearer ${token.value}` } });
    console.log(response.data);
    isTokenValid.value = response.data.valid;
    if(isTokenValid.value){
      await fetchQuestions();
    }
  } catch (error) {
    console.error('Failed to check token:', error);
    if (error.response && error.response.status === 401) {
      ParticipationStorageService.clearAuthToken();
      isTokenValid.value = false;
    }
  }
};

const displayNewQuestionForm = () => {
  showAddQuestion.value = !showAddQuestion.value;
};

const logout = () => {
  ParticipationStorageService.clearAuthToken();
  window.location.href = '/';
};

const fetchQuestions = async () => {
  if (!isTokenValid.value) return;
  try {
    const response = await axios.get('http://127.0.0.1:5000/questions/all');
    console.log("Questions : ", response.data);
    questions.value = response.data;
  } catch (error) {
    console.error('Failed to fetch questions:', error);
  }
};

const login = async () => {
  try {
    const response = await axios.post('http://127.0.0.1:5000/login', { password: password.value });
    token.value = response.data.token;
    ParticipationStorageService.saveAuthToken(token.value);
    await checkToken();  // Vérifier la validité du token après connexion
  } catch (error) {
    console.error('Failed to login:', error);
  }
};

if (token.value) {
  checkToken();  // Vérifier la validité du token si présent lors de l'initialisation
}

onMounted(checkToken);
</script>

<style scoped>
  h1 {
    text-align: center;
  }

  .admin-container {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .login-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 30%;
    height: 17vh;
    border-radius: 10px;
    background-color: rgb(172, 236, 161);
  }

  .admin-input {
    border: none;
    border-top-left-radius: 5px;
    border-bottom-left-radius: 5px;
    padding: 10px;
  }

  .admin-input:focus {
    outline: none;
    border: 0.5px solid rgb(0, 128, 0);
  }

  .admin-login-button {
    border: none;
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
    padding: 10px;
    background-color: rgb(0, 128, 0);
    color: white;
    cursor: pointer;
  }

  .admin-login-button:hover {
    background-color: #006400;
  }

  .logout-button {
    border: none;
    background-color: rgb(172, 236, 161);
    color: black;
    padding: 10px 20px;
    font-size: 18px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  .logout-button:hover {
    background-color: #006400;
  }

  .add-question-button {
    border: none;
    background-color: rgb(172, 236, 161);
    color: black;
    padding: 10px 20px;
    font-size: 18px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  .add-question-button:hover {
    background-color: #006400;
  }

  .buttons-container {
    width: 100%;
    display: flex;
    justify-content: space-around;
    margin-bottom: 2vh;
  }
</style>

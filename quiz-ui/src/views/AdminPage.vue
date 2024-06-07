<template>
  <div class="admin-container">
    <h1>Admin Panel</h1>
    <div v-if="!token" class="login-container">
      <h2>Login</h2>
      <div class="input-container">
        <input type="password" v-model="password" placeholder="Password" class="admin-input">
        <button @click="login" class="admin-login-button">Login</button>
      </div>
      
    </div>
    <div v-else class="panel-container">
      <div class="container">
        <div class="buttons-container">
          <button @click="displayNewQuestionForm" class="add-question-button">Add Question</button>
          <button @click="logout" class="logout-button">Logout</button>
        </div>
      </div>
      <AddQuestion v-if="showAddQuestion" @question-added="fetchQuestions"/>
      <QuestionsList :questions="questions" @question-deleted="fetchQuestions"/>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import AddQuestion from './AddQuestion.vue';
import QuestionsList from './QuestionsList.vue';

const password = ref('');
const token = ref(localStorage.getItem('token') || '');
const questions = ref([]);
const showAddQuestion = ref(false);

const displayNewQuestionForm = () => {
  showAddQuestion.value = true;
};

const fetchQuestions = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/questions/all');
    console.log(response.data);  // Ajoutez ce log
    questions.value = response.data;
  } catch (error) {
    console.error('Failed to fetch questions:', error);
  }
};

const login = async () => {
  try {
    const response = await axios.post('http://127.0.0.1:5000/login', { password: password.value });
    token.value = response.data.token;
    localStorage.setItem('token', token.value);
    await fetchQuestions();
  } catch (error) {
    console.error('Failed to login:', error);
  }
};

if (token.value) {
  fetchQuestions();
}
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
    background-color: rgb(0, 100, 0);
  }


  .logout-button {
    border: 1px solid black;
    border-radius: 30px;
    background-color: rgb(172, 236, 161);
    color: black;
    padding: 10px 20px;
    font-size: 18px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  .logout-button:hover {
    background-color: rgb(0, 100, 0); /* Change background color to yellow when hovering over the button */
  }

  .add-question-button{
    border: 1px solid black;
    border-radius: 30px;
    background-color: rgb(172, 236, 161);
    color: black;
    padding: 10px 20px;
    font-size: 18px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  .add-question-button:hover{
    background-color: rgb(0, 100, 0);
  }
</style>
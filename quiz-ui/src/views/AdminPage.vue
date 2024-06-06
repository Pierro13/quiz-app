<template>
  <div>
    <h1>Admin Panel</h1>
    <div v-if="!token">
      <h2>Login</h2>
      <input type="password" v-model="password" placeholder="Password">
      <button @click="login">Login</button>
    </div>
    <div v-else>
      <AddQuestion @question-added="fetchQuestions"/>
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
</style>

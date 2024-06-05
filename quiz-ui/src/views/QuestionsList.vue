<template>
  <div>
    <h2>Questions List</h2>
    <ul>
      <li v-for="question in questions" :key="question.id">
        <div>
          <h3>{{ question.title }}</h3>
          <p>{{ question.text }}</p>
          <ul>
            <li v-for="answer in sortedQuestions.answers" :key="answer.id">
              {{ answer.text }} ({{ answer.is_correct ? 'Correct' : 'Incorrect' }})
            </li>
          </ul>
        </div>
        <button @click="editQuestion(question.id)">Edit</button>
        <button @click="deleteQuestion(question.id)">Delete</button>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
import axios from 'axios';
import { defineProps, defineEmits, computed } from 'vue';

const props = defineProps({
  questions: Array
});

const sortedQuestions = computed(() => {
  return [...props.questions].sort((a, b) => a.position - b.position);
});

const emit = defineEmits(['question-deleted']);

const router = useRouter();

const editQuestion = (id) => {
  router.push({ name: 'edit-question', params: { id } });
};

const deleteQuestion = async (id) => {
  try {
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('No authentication token found');
    }

    await axios.delete(`http://127.0.0.1:5000/questions/${id}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    emit('question-deleted'); // Émettre l'événement après la suppression
  } catch (error) {
    if (error.response && error.response.status === 401) {
      alert('Unauthorized: Please login to delete a question.');
    } else {
      console.error('Failed to delete question:', error);
    }
  }
};
</script>

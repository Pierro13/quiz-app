<template>
  <div>
    <div class="container">
      <h2>Liste des questions</h2>
      <div class="cards-container">
        <div v-for="question in sortedQuestions" :key="question.id" class="card">
          <div class="container-img-card">
            <div class="img-card">
              <img v-if="question.image" :src="`http://127.0.0.1:5000/${question.image}`" width="200px" height="50px" alt="Question image">
            </div>
          </div>
          <h3>{{ question.title }}</h3>
          <p><span class="bold">Question :</span>{{ question.text }}</p>
          <p class="bold">Réponses</p>
          <div class="answers">
            <p v-for="answer in question.possibleAnswers" :key="answer.id">-> {{ answer.text }} ({{ answer.isCorrect ? 'Correct' : 'Incorrect' }})</p>
          </div>
          <button @click="editQuestion(question.id)">Modifier</button>
          <button @click="deleteQuestion(question.id)">Supprimer</button>
        </div>
      </div>
    </div>
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

<style scoped>
h2 {
  text-align: center;
}

.container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.cards-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
  justify-items: center;
  width: 100%;
  padding: 20px;
}

.card {
  background-color: #ACECA1;
  border-radius: 25px;
  padding: 1vh 1vw;
  word-wrap: break-word;
  max-width: 200px;
}

.container-img-card {
  display: flex;
  justify-content: center;
}

.img-card {
  border: 1px solid green;
  justify-content: center;
}

.answers p {
  line-height: 1;
}

.card h3 {
  text-align: center;
}

.bold {
  font-weight: bold;
  padding-right: 0.5vw;
}
</style>

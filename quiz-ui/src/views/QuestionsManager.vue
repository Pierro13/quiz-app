<template>
  <div class="questions-manager">
    <h1>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestions }}</h1>
    <QuestionDisplay 
      v-if="currentQuestion" 
      :currentQuestion="currentQuestion" 
      :isLastQuestion="isLastQuestion"
      :score="score"
      @click-on-answer="answerClickedHandler"
      @next-question="loadNextQuestion"
    />
    <p v-else>Loading question...</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import QuestionDisplay from './QuestionDisplay.vue';
import ParticipationStorageService from '@/services/ParticipationStorageService';

const currentQuestion = ref(null);
const currentQuestionPosition = ref(1);
const totalNumberOfQuestions = ref(0);
const score = ref(0);
const playerName = ref(ParticipationStorageService.getPlayerName() || 'Anonymous');

const isLastQuestion = computed(() => {
  return currentQuestionPosition.value === totalNumberOfQuestions.value;
});

const loadQuestionByPosition = async (position) => {
  try {
    const response = await axios.get(`http://127.0.0.1:5000/questions?position=${position}`);
    console.log('Loaded question:', response.data);
    currentQuestion.value = response.data;
  } catch (error) {
    console.error('Failed to load question:', error);
  }
};

const loadNextQuestion = async () => {
  if (currentQuestionPosition.value < totalNumberOfQuestions.value) {
    currentQuestionPosition.value++;
    await loadQuestionByPosition(currentQuestionPosition.value);
  } else {
    await endQuiz();
  }
};

const answerClickedHandler = async (index) => {
  const answerId = currentQuestion.value.answers[index].id;
  try {
    const response = await axios.post('http://127.0.0.1:5000/submit-answer', { answer_id: answerId });
    const result = response.data;
    if (result.correct) {
      score.value += result.score;
    }
  } catch (error) {
    console.error('Failed to submit answer:', error);
  }
  await loadNextQuestion();
};

const endQuiz = async () => {
  console.log('Quiz Ended');
  try {
    const payload = { username: playerName.value, score: score.value };
    console.log('Payload:', payload);  // Ajoutez ce log
    const response = await axios.post('http://127.0.0.1:5000/add-user', payload);
    console.log('Response:', response);  // Ajoutez ce log
    if (response.status !== 201) throw new Error('Network response was not ok');
    const result = response.data;
    console.log('Quiz end result:', result);
  } catch (error) {
    console.error('Failed to end quiz:', error);
  }
};

onMounted(async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/quiz-info');
    totalNumberOfQuestions.value = response.data.total;

    await loadQuestionByPosition(currentQuestionPosition.value);
  } catch (error) {
    console.error('Failed to initialize quiz:', error);
  }
});
</script>

<style scoped>
.questions-manager {
  padding: 20px;
}
</style>

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
    const response = await fetch(`http://127.0.0.1:5000/questions?position=${position}`);
    if (!response.ok) throw new Error('Network response was not ok');
    const question = await response.json();
    currentQuestion.value = question;
    console.log('Loaded question:', question);
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
    const response = await fetch('http://127.0.0.1:5000/submit-answer', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ answer_id: answerId }),
    });
    const result = await response.json();
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
    const response = await fetch('http://127.0.0.1:5000/add-user', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username: playerName.value, score: score.value }), // Envoyer le score réel ici
    });
    if (!response.ok) throw new Error('Network response was not ok');
    const result = await response.json();
    console.log('Quiz end result:', result);
  } catch (error) {
    console.error('Failed to end quiz:', error);
  }
};

onMounted(async () => {
  try {
    const response = await fetch('http://127.0.0.1:5000/quiz-info');
    if (!response.ok) throw new Error('Network response was not ok');
    const data = await response.json();
    totalNumberOfQuestions.value = data.size;
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

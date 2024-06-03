<template>
    <div class="questions-manager">
      <h3>Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestions }}</h3>
      <QuestionDisplay 
        v-if="currentQuestion" 
        :currentQuestion="currentQuestion" 
        :isLastQuestion="isLastQuestion"
        @click-on-answer="answerClickedHandler"
        @next-question="loadNextQuestion"
      />
      <p v-else>Loading question...</p>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted } from 'vue';
  import QuestionDisplay from './QuestionDisplay.vue';
  
  const currentQuestion = ref(null);
  const currentQuestionPosition = ref(1);
  const totalNumberOfQuestions = ref(0);
  
  const isLastQuestion = computed(() => {
    return currentQuestionPosition.value === totalNumberOfQuestions.value;
  });
  
  const loadQuestionByPosition = async (position) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/questions?position=${position}`);
      if (!response.ok) throw new Error('Network response was not ok');
      const question = await response.json();
      currentQuestion.value = question;
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
    console.log(`Answer clicked: ${index}`);
    await loadNextQuestion();
  };
  
  const endQuiz = async () => {
    console.log('Quiz Ended');
    try {
      const response = await fetch('http://127.0.0.1:5000/quiz/end', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ score: 8 })  // Vous pouvez calculer et envoyer le score réel ici
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
      totalNumberOfQuestions.value = data.total;
  
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
  
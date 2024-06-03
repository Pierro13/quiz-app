<template>
    <h3>Question {{ currentQuestion.id }}</h3>
    <div class="container">
      <div class="left-part">
        <h3>Score : 78</h3>
      </div>
      <div class="middle-part">
        <div class="question-container">
        <p>{{ currentQuestion.text }}</p>
        <!-- <img v-if="currentQuestion.image" :src="currentQuestion.image" alt="Question image" /> -->
        <img src="@/assets/template.png" alt="Question image" width="1000px"/>
      </div>
      <div class="answers-container">
        <div class="answers" v-for="(answer, index) in currentQuestion.answers" :key="index">
            <AnswerButton :text="answer.text" :color="colors[index % colors.length]" @click="selectAnswer(index)"/>
        </div>
      </div>
      </div>
      <div class="right-part">
        <h3>Temps : 0:10</h3>
      </div>
    </div>
    <div class="next-button" v-if="!isLastQuestion">
      <button @click="nextQuestion">Next</button>
    </div>
  </template>
  
  <script setup>
  import AnswerButton from '@/views/Answer-button.vue';
  
  const props = defineProps({
    currentQuestion: Object,
    isLastQuestion: Boolean
  });
  const emit = defineEmits(['click-on-answer', 'next-question']);
  
  const selectAnswer = (index) => {
    emit('click-on-answer', index);
  };
  
  const nextQuestion = () => {
    emit('next-question');
  };

  const colors = ['#EF476F', '#1B9AAA', '#06D6A0', '#FFC43D'];
  </script>
  
  <style scoped>
    .container {
        display: flex;
        justify-content: center;
        border: 1px solid green;
    }

    .left-part {
        border: 1px solid blue;
        width: 10%;
        display: flex;
        justify-content: center;
    }

    .middle-part {
        border: 1px solid black;
        width: 80%;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .answers-container {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
    }

    .right-part {
        border: 1px solid red;
        width: 10%;
        display: flex;
        justify-content: center;
    }

    .question-container {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
  </style>
  
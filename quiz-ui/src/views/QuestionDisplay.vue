<template>
  <div class="container">
    <div class="left-part">
      <h3>Score : {{ score }}</h3>
    </div>
    <div class="middle-part">
      <div class="question-container">
        <h2>{{ currentQuestion.title }}</h2>
        <p>{{ currentQuestion.text }}</p>
        <pre v-if="currentQuestion.code" v-html="highlightedCode" class="hljs display-code"></pre>
        <img v-if="currentQuestion.image" :src="`http://127.0.0.1:5000/${currentQuestion.image}`" alt="Question image" />
      </div>
      <div class="answers-container">
        <div class="answers" v-for="(answer, index) in currentQuestion.possibleAnswers" :key="index">
          <AnswerButton ref="answerButtons" :text="answer.text" :color="colors[index % colors.length]" :disabled="isAnswerSubmitted" @click="selectAnswer(index)" />
        </div>
      </div>
    </div>
    <div class="right-part">
      <h3>Temps : 0:10</h3>
    </div>
    <div class="next-button" v-if="!isLastQuestion">
      <button @click="nextQuestion">Next</button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, nextTick } from 'vue';
import hljs from 'highlight.js';
import 'highlight.js/styles/github.css';

import AnswerButton from '@/views/Answer-button.vue';

const props = defineProps({
  currentQuestion: Object,
  isLastQuestion: Boolean,
  score: Number,
});
const emit = defineEmits(['click-on-answer', 'next-question']);

const highlightedCode = ref('');
const isAnswerSubmitted = ref(false);

const selectAnswer = (index) => {
  if (index < 0 || index >= props.currentQuestion.possibleAnswers.length) {
    console.error("Invalid answer index:", index);
    return;
  }
  if (!isAnswerSubmitted.value) {
    console.log("Selected answer index:", index);
    emit('click-on-answer', index);
    isAnswerSubmitted.value = true;
  } else {
    console.warn("Answer already submitted for this question.");
  }
};

const nextQuestion = () => {
  console.log("Next question button clicked.");
  isAnswerSubmitted.value = false;
  emit('next-question');
};

const colors = ['#EF476F', '#1B9AAA', '#06D6A0', '#FFC43D'];

const highlightCode = () => {
  if (props.currentQuestion.code) {
    highlightedCode.value = hljs.highlightAuto(props.currentQuestion.code).value;
  } else {
    highlightedCode.value = '';
  }
  console.log("Highlighting code for question:", props.currentQuestion);
};

watch(() => props.currentQuestion, (newQuestion, oldQuestion) => {
  console.log("Current question changed from:", oldQuestion, "to:", newQuestion);
  highlightCode();
  isAnswerSubmitted.value = false;
  nextTick(() => adjustButtonSizes());
});

onMounted(() => {
  highlightCode();
  nextTick(() => adjustButtonSizes());
});

const adjustButtonSizes = () => {
  nextTick(() => {
    const buttons = document.querySelectorAll('.answer-button');
    let maxWidth = 0;
    let maxHeight = 0;

    // Calculer la taille maximale des boutons
    buttons.forEach(button => {
      button.style.width = 'auto';
      button.style.height = 'auto';
      const rect = button.getBoundingClientRect();
      if (rect.width > maxWidth) {
        maxWidth = rect.width;
      }
      if (rect.height > maxHeight) {
        maxHeight = rect.height;
      }
    });

    // Appliquer la taille maximale à tous les boutons
    buttons.forEach(button => {
      button.style.width = `${maxWidth}px`;
      button.style.height = `${maxHeight}px`;
    });
  });
};
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
  align-items: center;
}

.middle-part {
  border: 1px solid black;
  width: 80%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.display-code {
  width: 100%;
  padding: 10px;
  background-color: #ddd;
  overflow: auto;
  border-radius: 5px;
  font-family: 'Fira Code', monospace;
  word-wrap: break-word;
}

.answers-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-gap: 10px;
}

.answers {
  display: flex;
  justify-content: center;
  align-items: center;
}

.right-part {
  border: 1px solid red;
  width: 10%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.question-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.next-button {
  margin-top: 20px;
}
</style>

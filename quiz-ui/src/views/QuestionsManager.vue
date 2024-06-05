<script setup>
import { ref, onMounted } from 'vue';
import quizApiService from "@/services/QuizApiService";
import QuestionDisplay from '@/views/QuestionDisplay.vue';
import ParticipationStorageService from '@/services/ParticipationStorageService';

const currentQuestion = ref(null);
const score = ref(0);
const questions = ref([]);
let questionIndex = 0;

const loadNextQuestion = async () => {
    if (questionIndex < questions.value.length) {
        currentQuestion.value = questions.value[questionIndex];
        questionIndex++;
    } else {
        currentQuestion.value = null; // No more questions
        await endQuiz();
    }
};

const answerClickedHandler = async (index) => {
    if (!currentQuestion.value || !currentQuestion.value.possibleAnswers || index >= currentQuestion.value.possibleAnswers.length) {
        console.error("Invalid answer index:", index);
        return;
    }

    const answerId = currentQuestion.value.possibleAnswers[index].id;
    currentQuestion.value.selectedAnswer = index + 1; // Store the selected answer index
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
    const playerName = ParticipationStorageService.getPlayerName() || "Anonymous";
    if (playerName) {
        const participation = {
            playerName: playerName,
            answers: questions.value.map(q => q.selectedAnswer),
        };
        try {
            const response = await fetch('http://127.0.0.1:5000/participations', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(participation),
            });
            const result = await response.json();
            console.log("Participation enregistrée:", result);
        } catch (error) {
            console.error('Failed to save participation:', error);
        }
    }
};

onMounted(async () => {
    try {
        const response = await quizApiService.getQuizQuestions();
        questions.value = response;
        await loadNextQuestion();
    } catch (error) {
        console.error("Erreur lors de la récupération des questions:", error);
    }
});
</script>

<template>
  <div v-if="currentQuestion" class="container">
    <QuestionDisplay
      :currentQuestion="currentQuestion"
      :isLastQuestion="questionIndex >= questions.length"
      :score="score"
      @click-on-answer="answerClickedHandler"
      @next-question="loadNextQuestion"
    />
  </div>
  <div v-else class="container">
    <p>Quiz terminé ! Votre score est de : {{ score }}</p>
  </div>
</template>

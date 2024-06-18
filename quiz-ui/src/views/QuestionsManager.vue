<script setup>
import { ref, onMounted } from 'vue';
import quizApiService from "@/services/QuizApiService";
import QuestionDisplay from '@/views/QuestionDisplay.vue';
import ParticipationStorageService from '@/services/ParticipationStorageService';

const currentQuestion = ref(null);
const score = ref(0);
const questions = ref([]);
let questionIndex = 0;
let isSubmitting = ref(false);

const loadNextQuestion = () => {
    if (questionIndex < questions.value.length) {
        currentQuestion.value = questions.value[questionIndex];
        console.log("Loaded question:", questionIndex, currentQuestion.value);
        questionIndex++;
        isSubmitting.value = false;
    } else {
        currentQuestion.value = null; // No more questions
        console.log("No more questions. Ending quiz.");
        endQuiz();
    }
};

const answerClickedHandler = async (index) => {
    if (isSubmitting.value) {
        console.warn("Answer already submitted for this question.");
        return;
    }
    isSubmitting.value = true;

    if (!currentQuestion.value || !currentQuestion.value.possibleAnswers || index >= currentQuestion.value.possibleAnswers.length) {
        console.error("Invalid answer index:", index);
        isSubmitting.value = false;
        return;
    }

    const answerId = currentQuestion.value.possibleAnswers[index].id;
    currentQuestion.value.selectedAnswer = index + 1; // Store the selected answer index
    console.log("Submitting answer with ID:", answerId);
    try {
        const response = await fetch('http://127.0.0.1:5000/submit-answer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ answer_id: answerId }),
        });
        const result = await response.json();
        console.log("Answer submitted. Result:", result);
        if (result.correct) {
            score.value += result.score;
        }
        loadNextQuestion();
    } catch (error) {
        console.error('Failed to submit answer:', error);
        isSubmitting.value = false; // Allow resubmission if there's an error
    }
};

const endQuiz = async () => {
    const playerName = ParticipationStorageService.getPlayerName() || "Anonymous";
    if (playerName) {
        const participation = {
            playerName: playerName,
            answers: questions.value.map(q => q.selectedAnswer || null),
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
        console.log("Questions loaded:", questions.value);
        loadNextQuestion();
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
  <div v-else class="container-end">
    <h1>Quiz terminé !</h1>
    <h1>Votre score est de : {{ score }}</h1>
    <a href="/scores" class="scores-link-end">
        Afficher les scores
    </a>
  </div>
</template>

<style scoped>
    .container-end{
        margin-top: 10vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .scores-link-end{
        border: 1px solid black;
        border-radius: 5px;
        background-color: #ACECA1;
        margin-bottom: 1vh;
        padding: 1vh 1vh;
        text-decoration: none;
        color: inherit;
    }

    .scores-link-end:hover{
        background-color: #01a201;
    }

</style>
